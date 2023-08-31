from fuzzywuzzy import fuzz
import ast
import re


def transform_NER_output(s):
    
    
    ''' For cleaning NER output i.e. transsforming from dict to NER format'''
    # Convert the string to a dictionary
    s = s.strip('"')
    s = "{" + s + "}"
    data = ast.literal_eval(s)
    
    # Filter out NULL values and transform the dictionary to the desired format
    #transformed_data = [f"{value}: {key.upper()}" for key, values in data.items() for value in values if value != 'NULL']
    transformed_data = [f"{value}: {key.upper()}" for key, values in data.items() for value in values if value not in ['NULL', 'Null', 'null', ""]]
    
    # Join the transformed data with commas
    return ',    '.join(transformed_data)




def transform_faulty_NER_output(stringA):
    
    stringA = stringA.strip('"')
    
    
    # Split the string by comma, but not the ones inside square brackets
    parts = re.split(r', (?![^\[]*\])', stringA)
    
    
    result_dict = {}
    for part in parts:
        
        # Check if the part contains the delimiter
        if ": " in part:
            #part = "Competitor: extracted entities if any"
            key, value = part.split(": ", 1)
            print("key: ", key)
            print("value: ", value)
            
            # Check if the value contains a list
            if '[' and ']' in value:
                result_dict[key] = value
            else:
                value = "[" + value + "]"
                result_dict[key] = value
    
    # Remove key-value pairs where the value contains the word 'entities'
    result_dict = {k: v for k, v in result_dict.items() if 'entities' not in v}

    
    # Convert string representation of lists into actual lists
    for key, value in result_dict.items():
        if value.startswith("[") and value.endswith("]") or value.endswith("] "):
            value = value.strip("[] ").split(", ")
            result_dict[key] = [v.strip() for v in value]

    transformed_data = [f"{value}: {key.upper()}" for key, values in result_dict.items() for value in values if value not in ['NULL', 'Null', 'null', ""]]
    
    # Join the transformed data with commas
    return ',    '.join(transformed_data)





def StyleColourEntities(entities_cleaned):
    # Split the string by commas
    entities_list = entities_cleaned.split(', ')
    
    # Dictionary of colors for each category
    color_dict = {
        "PERSON": "#D1E8E2",
        "EMAIL": "#D5E8D4",
        "PHONE": "#E1D5E7",
        "PRODUCT": "#D5E8EB",
        "COMPETITOR": "#F5D5D4" 
    }
    
    # Function to style entities based on category
    def style_entity(entity):
        for category, color in color_dict.items():
            if category in entity:
                entity = entity.replace(category, f'<span style="background-color: {color};">{category}</span>')
        return entity
    
    # Apply the styling function to each entity
    styled_entities = [style_entity(entity) for entity in entities_list]

    # Join the entities with extra space and wrap in markdown
    styled_text = ', &nbsp;&nbsp;'.join(styled_entities)  # joining with double space
    
    return styled_text








