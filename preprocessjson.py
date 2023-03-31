import json
import argparse

from typing import Union, Any

parser = argparse.ArgumentParser()
parser.add_argument("--input")
parser.add_argument("--output")

args = parser.parse_args()
SCHEMA_PATH = args.input
OUTPUT_PATH = args.output


def remove_null_types(schema: Union[dict, list]) -> Any:
    """Recursively remove all instances of items containing 'type':['null'] from `anyOf`."""
    if isinstance(schema, dict):
        # Check if it has "type" key and its value is ["null"]
        if "type" in schema and schema["type"] == ["null"]:
            # If it does, remove the entry
            return None
        # If it doesn't, recursively call this function on all its values
        return {k: remove_null_types(v) for k, v in schema.items()}
    if isinstance(schema, list):
        # Recursively call this function on all items in the list
        return [remove_null_types(item) for item in schema if remove_null_types(item) is not None]
    # Return the schema as-is if it's not a dict or list
    return schema


# Example usage
with open(SCHEMA_PATH, "r") as f:
    schema = json.load(f)

new_schema = remove_null_types(schema)

with open(OUTPUT_PATH, "w") as f:
    json.dump(new_schema, f, indent=2)
