from transformers import AutoTokenizer, AutoModel
import torch

model_name = 'emilyalsentzer/Bio_ClinicalBERT'

class SchemaTokensEmbedder():

    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)

    def get_embedding(self, text):
        inputs = self.tokenizer(text, return_tensors='pt', truncation=True, max_length=512)
        with torch.no_grad():
            outputs = self.model(**inputs)
        # Use the [CLS] token embedding
        embedding = outputs.last_hidden_state[:, 0, :]
        return embedding.squeeze().numpy()
