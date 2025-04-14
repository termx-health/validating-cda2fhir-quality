import xml.etree.ElementTree as ET
from datetime import datetime
import json
import os
import glob

class CdaTokenizer():
    def __init__(self):
        self.concept_maps = {}
        self._load_concept_maps()

    def _load_concept_maps(self):
        concept_maps_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'concept_maps')
        concept_map_files = glob.glob(os.path.join(concept_maps_dir, '*.json'))
        
        for file_path in concept_map_files:
            with open(file_path, 'r') as f:
                concept_map = json.load(f)
                source_uri = concept_map.get('sourceUri')
                
                code_mappings = {}
                for group in concept_map.get('group', []):
                    for i, element in enumerate(group.get('element', [])):
                        source_code = element.get('code')
                        if source_code and element.get('target'):
                            code_mappings[source_code] = f"{concept_map['id']}-{i}"
                
                if source_uri and code_mappings:
                    self.concept_maps[source_uri] = code_mappings

    def get_tokens(self, file_path) -> tuple[str, str]:
        tree = ET.parse(file_path)
        root = tree.getroot()
        schema_content = []
        values_content = []

        def recurse(node):
            # Append tag name to schema content
            node_tag = node.tag.replace(f'{{urn:hl7-org:v3}}', '')
            schema_content.append(node_tag)
            
            # Handle code system mappings first
            code = node.attrib.get('code')
            code_system = node.attrib.get('codeSystem')
            
            if code and code_system and code_system in self.concept_maps:
                if code in self.concept_maps[code_system]:
                    mapped_value = self.concept_maps[code_system][code]
                    values_content.append(mapped_value)
                    return
            
            # Handle remaining attributes
            for attr_name, attr_value in node.attrib.items():
                if attr_name in ['codeSystemName', 'classCode', 'moodCode', 'typeCode']: 
                    continue

                if attr_name in ['type']: 
                    schema_content.append(attr_value)
                    continue

                schema_content.append(attr_name)

                # Handle dates and other values
                if node_tag in ['birthTime', 'effectiveTime']:
                    values_content.append(str(datetime.strptime(attr_value.strip(), '%Y%m%d')))   
                else:
                    values_content.append(attr_value)

            # Handle text and children
            if node.text and node.text.strip():
                values_content.append(node.text.strip())
            for child in node:
                recurse(child)
            if node.tail and node.tail.strip():
                schema_content.append(node.tail.strip())

        recurse(root)
        schema_content = [word.strip().lower() for word in schema_content if not (word.strip() in ['classCode', 'moodCode', 'determinerCode', 'urn:hl7-org:v3', f'{{http://www.w3.org/2001/XMLSchema-instance}}schemaLocation', 'value'] or '.xsd' in word)]
        values_content = [word.strip().lower() for word in values_content if not (word.strip() in ['PSN', 'INSTANCE'] or '.xsd' in word)]
        return ' '.join(schema_content), ' '.join(values_content)
