"""
Sandbox
"""

from mcp_project.utils.generic_utils import export2json, load_json
from mcp_project.ecuc_creator.ecuc_configurator import ECUCConfiguratorV2

def main():
    configurator = ECUCConfiguratorV2()
    
    # Do not change parameters in this test
    input_definitionPath = "Com/ComGeneral"
    input_shortNameDict = {"ComGeneral": "ComGeneral"}
    
    # Create container without parameters
    configurator.create_container(input_definitionPath, input_shortNameDict)
    
    # Validate generated data
    validation_data = load_json("tests/container_without_parameters.json")
    
    export2json("_out/comgeneral.json", configurator.get_data())

if __name__ == "__main__":
    main()
