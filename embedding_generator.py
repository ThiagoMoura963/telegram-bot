from sentence_transformers import SentenceTransformer
import torch
from config import HF_API_KEY

class EmbeddingGenerator:
    def __init__(self, model_name: str = 'sentence-transformers/multi-qa-MiniLM-L6-cos-v1'):
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print(f'Dispositivo detectado: {self.device}')
        print(f'Carregando o modelo de embedding "{model_name}" no dispositivo: {self.device}')
        
        self.model = SentenceTransformer(model_name, device=self.device, token=HF_API_KEY)
        print('Modelo carregado com sucesso.')

    def generate_embeddings(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []
            
        print(f'Gerando embeddings para {len(texts)} textos no dispositivo: {self.device}...')

        embeddings = self.model.encode(
            texts,
            convert_to_tensor=True,
            show_progress_bar=True
        )

        return embeddings.cpu().tolist()