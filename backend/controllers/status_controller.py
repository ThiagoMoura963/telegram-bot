#type: ignore

from fastapi import APIRouter, Request
from backend.infra.database import PostgresManager
from datetime import datetime
import os

router = APIRouter(prefix='/api/v1/status', tags=['Status'])

@router.get('')
def get_status():
    updated_at = datetime.now().isoformat()
    postgres_manager = PostgresManager()

    with postgres_manager as cursor:
        cursor.execute('SHOW server_version;')
        database_version_result = cursor.fetchone()
        database_version_value = database_version_result[0]

        cursor.execute('SHOW max_connections;')
        database_max_connections_result = cursor.fetchone()
        database_max_connections_value = database_max_connections_result[0]

        database_name = postgres_manager.conn.info.dbname
        cursor.execute(
            'SELECT count(*) FROM pg_stat_activity WHERE datname = %s',
            (database_name,)
        )
        database_opened_connections_result = cursor.fetchone()
        database_opened_connections_value = database_opened_connections_result[0]

    return {
        'updated_at': updated_at,
        'dependencies': {
            'database': {
                'version': database_version_value,
                'max_connections': int(database_max_connections_value),
                'opened_connections': int(database_opened_connections_value),
                'db_name': database_name
            }
        }
    }