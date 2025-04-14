import json
from datetime import datetime
import os
import glob

class FhirTokenizer():
    def __init__(self):
        self.concept_maps = {}
        self.implied_systems = {
            'gender': 'http://hl7.org/fhir/ValueSet/administrative-gender',
            # Add more implied system mappings as needed
        }
        self._load_concept_maps()

    def _load_concept_maps(self):
        concept_maps_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'concept_maps')
        concept_map_files = glob.glob(os.path.join(concept_maps_dir, '*.json'))
        
        for file_path in concept_map_files:
            with open(file_path, 'r') as f:
                concept_map = json.load(f)
                target_uri = concept_map.get('targetUri')
                
                code_mappings = {}
                for group in concept_map.get('group', []):
                    for i, element in enumerate(group.get('element', [])):
                        if element.get('target'):
                            target_code = element['target'][0].get('code')
                            code_mappings[target_code] = f"{concept_map['id']}-{i}"
                
                if target_uri and code_mappings:
                    self.concept_maps[target_uri] = code_mappings
    
    def get_tokens(self, file_path) -> tuple[str, str]:
        with open(file_path, 'r') as f:
            data = json.load(f)

        schema_content = []
        values_content = []

        def recurse(obj):
            if isinstance(obj, dict):
                # Check for explicit coding entries
                if 'coding' in obj and isinstance(obj['coding'], list):
                    for coding in obj['coding']:
                        if 'system' in coding and 'code' in coding:
                            system = coding.get('system')
                            code = coding.get('code')
                            if system in self.concept_maps and code in self.concept_maps[system]:
                                mapped_value = self.concept_maps[system][code]
                                values_content.append(mapped_value)
                                return

                for key, value in obj.items():                    
                    # Append key
                    schema_content.append(str(key))

                    if key in self.implied_systems and isinstance(value, str):
                        system = self.implied_systems[key]
                        if system in self.concept_maps and value in self.concept_maps[system]:
                            mapped_value = self.concept_maps[system][value]
                            values_content.append(mapped_value)
                            continue

                    # Regular processing
                    if str(key) == 'resourceType':
                        schema_content.append(value.strip())
                    elif str(key) in ['birthDate', 'effectiveDateTime']:
                        values_content.append(str(datetime.strptime(value.strip(), '%Y-%m-%d')))
                    else:
                        recurse(value)
                        
            elif isinstance(obj, list):
                for item in obj:
                    recurse(item)
            else:
                if isinstance(obj, str) and obj.strip():
                    values_content.append(obj.strip())
                elif isinstance(obj, (int, float)):
                    values_content.append(str(obj))

        recurse(data)
        schema_content = [word.strip().lower() for word in schema_content if word not in ['resourceType', 'value', 'resource']]
        values_content = [word.strip().lower() for word in values_content]
        return ' '.join(schema_content), ' '.join(values_content)
