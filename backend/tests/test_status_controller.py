# from unittest.mock import MagicMock, patch


# def test_get_status(client):
#     target = 'backend.controllers.status_controller.PostgresManager'

#     with patch(target) as mock_postgres:
#         mock_cursor = MagicMock()
#         mock_cursor.fetchone.side_effect = [
#             ('16.12',),
#             ('100',),
#             (1,),
#         ]

#         mock_instance = MagicMock()
#         mock_instance.__enter__ = MagicMock(return_value=mock_cursor)
#         mock_instance.__exit__ = MagicMock(return_value=False)
#         mock_instance.conn.info.dbname = 'local_db'
#         mock_postgres.return_value = mock_instance

#         response = client.get('/api/v1/status')

#         assert response.status_code == 200

#         data = response.json()
#         assert data['dependencies']['database']['version'] == '16.12'
#         assert data['dependencies']['database']['max_connections'] == 100
#         assert data['dependencies']['database']['opened_connections'] == 1
