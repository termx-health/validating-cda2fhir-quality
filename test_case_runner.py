import os
from similarity_evaluator import evaluate_similarity
from tabulate import tabulate

TEST_CASE_FOLDER = 'test_cases'

def process_test_case(test_case, debug = False):
    print(f"Processing test case: {test_case}")
        
    # Construct file paths for this test case
    cda_path = os.path.join(TEST_CASE_FOLDER, test_case, 'cda.xml')
    fhir_path = os.path.join(TEST_CASE_FOLDER, test_case, 'fhir.json')
    
    if not (os.path.exists(cda_path) and os.path.exists(fhir_path)):
        print(f"Skipping {test_case} - missing required files")
        return
        
    # Evaluate similarity between CDA XML and FHIR JSON documents
    return evaluate_similarity(cda_path, fhir_path, debug)

def run_all():
    test_cases = [d for d in os.listdir(TEST_CASE_FOLDER) if os.path.isdir(os.path.join(TEST_CASE_FOLDER, d))]
    results = []

    for test_case in test_cases:
        schema_semantic_similarity, value_tokens_similarity, value_entry_count_similarity = process_test_case(test_case)

        results.append([
            test_case,
            f'{(schema_semantic_similarity * 100):.1f} %',
            f'{(value_tokens_similarity * 100):.1f} %',
            f'{(value_entry_count_similarity * 100):.1f} %'
        ])

    headers = ['Test Case', 'Schema Similarity', 'Value Similarity', 'Length Similarity']
    print("\nTest Results Summary:")
    print(tabulate(results, headers=headers, tablefmt='grid'))

def run_case(test_case, debug = False):
    schema_semantic_similarity, value_tokens_similarity, value_entry_count_similarity = process_test_case(test_case, debug)

    print("\nTest Case Results:")
    print(f"Schema Similarity: {(schema_semantic_similarity * 100):.1f} %")
    print(f"Value Similarity: {(value_tokens_similarity * 100):.1f} %")
    print(f"Length Similarity: {(value_entry_count_similarity * 100):.1f} %")

run_all()
#run_case('case_2_1', debug = True)
