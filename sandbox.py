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
    # configurator.create_container(input_definitionPath, input_shortNameDict)
    
    # Create container with parameters
    parameters = {
        "ComIPduDirection" : "RECEIVE",
        "ComIPduSignalProcessing" : "IMMEDIATE",
    }
    configurator.create_container_with_parameter(input_definitionPath, input_shortNameDict, parameters)
    
    export2json("_out/comgeneral.json", configurator.get_data())

if __name__ == "__main__":
    main()
