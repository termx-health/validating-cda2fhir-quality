from scipy.spatial import distance

from document_tokenizers.cda_tokenizer import CdaTokenizer
from document_tokenizers.fhir_tokenizer import FhirTokenizer
from token_embedders.value_tokens_embedder import ValueTokensEmbedder
from token_embedders.schema_tokens_embedder import SchemaTokensEmbedder 

# Initialize tokenizers and embedders
cda_tokenizer = CdaTokenizer()
fhir_tokenizer = FhirTokenizer()
schema_tokens_embedder = SchemaTokensEmbedder()
value_tokens_embedder = ValueTokensEmbedder()

# Get all test case directories
def evaluate_similarity(cda_path, fhir_path, debug = False):

    # Preprocess CDA input document and FHIR output document
    cda_schema_tokens, cda_value_tokens = cda_tokenizer.get_tokens(cda_path)
    fhir_schema_tokens, fhir_value_tokens = fhir_tokenizer.get_tokens(fhir_path)

    common_schema_tokens = set(cda_schema_tokens.split()).intersection(set(fhir_schema_tokens.split()))
    cda_schema_tokens = ' '.join([token for token in cda_schema_tokens.split() if token not in common_schema_tokens])
    fhir_schema_tokens = ' '.join([token for token in fhir_schema_tokens.split() if token not in common_schema_tokens])

    if debug:
        print('-----------------------------------')
        print("CDA Schema Tokens: ", cda_schema_tokens)
        print("FHIR Schema Tokens: ", fhir_schema_tokens)
        print('-----------------------------------')
        print("CDA Value Tokens: ", cda_value_tokens)
        print("FHIR Value Tokens: ", fhir_value_tokens)

    # Get schema token embeddings and calculate similarity measures
    cda_schema_embedding = schema_tokens_embedder.get_embedding(cda_schema_tokens)
    fhir_schema_embedding = schema_tokens_embedder.get_embedding(fhir_schema_tokens)
    
    schema_semantic_similarity = 1 - distance.cosine(cda_schema_embedding, fhir_schema_embedding)

    # Get value token embeddings and calculate similarity measures
    values_embeddings = value_tokens_embedder.get_embeddings([cda_value_tokens, fhir_value_tokens])
    cda_value_tokens_embedding = values_embeddings[0]
    fhir_value_tokens_embedding = values_embeddings[1]

    value_tokens_similarity = 1 - distance.cosine(cda_value_tokens_embedding, fhir_value_tokens_embedding)
    value_entry_count_similarity = ((len(fhir_value_tokens.split(' ')) / len(cda_value_tokens.split(' '))))

    return schema_semantic_similarity, value_tokens_similarity, value_entry_count_similarity
