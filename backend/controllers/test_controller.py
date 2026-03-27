from fastapi import APIRouter
import concurrent.futures
from backend.infra.database import PostgresManager

router = APIRouter(prefix="/api/v1/test", tags=["Debug/Stress"])

# CRITICAL: A lista precisa estar FORA da função (Escopo Global)
# Enquanto o servidor estiver ligado, o Python não ousará tocar no que estiver aqui.
pool_de_vazamento_global = []

@router.get("/flood")
async def trigger_flood():
    num_requisicoes = 20 # Volte para um número maior para ver o efeito
    
    def query_vazando(id_teste):
        try:
            manager = PostgresManager()
            # CHAMADA MANUAL: Sem o 'with', o Python não sabe quando fechar
            cursor = manager.__enter__() 
            
            cursor.execute("SELECT 1")
            
            # Guardamos na lista GLOBAL. 
            # Sem o 'with', o __exit__ nunca é disparado.
            # Sem o Garbage Collector (devido à lista global), o __del__ nunca é disparado.
            pool_de_vazamento_global.append(manager) 
            return True
        except Exception as e:
            print(f"Erro: {e}")
            return False

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_requisicoes) as executor:
        list(executor.map(query_vazando, range(num_requisicoes)))
    
    return {
        "status": "Inundação concluída!", 
        "total_na_ram": len(pool_de_vazamento_global)
    }

@router.get("/limpar-vazamento")
async def limpar():
    """Rota de pânico para fechar tudo manualmente"""
    contagem = len(pool_de_vazamento_global)
    while pool_de_vazamento_global:
        manager = pool_de_vazamento_global.pop()
        try:
            # Forçamos o fechamento que o Python não fez
            manager.__exit__(None, None, None)
        except:
            pass
    return {"message": f"Limpeza concluída. {contagem} conexões fechadas."}