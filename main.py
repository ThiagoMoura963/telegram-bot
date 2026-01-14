import argparse
import sys
import telegram_view
from services.ingestion_service import IngestionService

def main():
    parser = argparse.ArgumentParser(
        description='Bot de IA (Gemini) e Processador de Documentos RAG.'
    )
    
    parser.add_argument(
        '--process-pdf',
        type=str,
        help='Caminho para o arquivo PDF que será processado e salvo no banco.',
        metavar='CAMINHO_ARQUIVO'
    )

    args = parser.parse_args()

    if args.process_pdf:
        try:
            print(f'Iniciando processamento do documento: {args.process_pdf}')
            
            service = IngestionService()
            total_chunks = service.process_pdf(args.process_pdf)
            
            print(f'✅ Sucesso! {total_chunks} chunks e vetores armazenados no banco.')
            
        except Exception as e:
            print(f'Erro crítico no processamento: {e}')
            sys.exit(1)
            
    else:
        try:
            print('Iniciando Bot do Telegram...')
            telegram_view.run()
        except KeyboardInterrupt:
            print('\nBot encerrado pelo usuário.')
            sys.exit(0)
        except Exception as e:
            print(f'Falha ao iniciar o Bot: {e}')
            sys.exit(1)

if __name__ == '__main__':
    main()