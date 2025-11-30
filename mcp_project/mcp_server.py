"""
MCP Server
@author: GUU8HC
"""

# Standard imports
from fastmcp import FastMCP
from datetime import datetime

# Import MCP settings
from mcp_transport_configurator import configure_mcp
from mcp_settings import SETTINGS, PROTOCOL, STDIO, SSE, PORT

# Import tools
from utils.generic_utils import get_precise_time, export2json
from paramdef_handler.paramdef_arxml2json import convert_paramdef_to_json
from paramdef_handler .paramdef_utils import (
    get_definition_files,
    get_definition_path_difflib,
    get_definition_path_rapidfuzz
)


# create application
app = FastMCP()


# Tool listing
@app.tool()
def get_precise_time():
    """
    MCP wrapper
    """
    return get_precise_time()

@app.tool(
    description="""
    Provide response instructions for a given prompt.
    """
)
def provide_response_instructions():
    """
    Provide response instructions for a given prompt.
    """
    instructions = """
    When responding to prompts, please adhere to the following guidelines:
    1. Clarity: Ensure your responses are clear and easy to understand.
    2. Conciseness: Keep your answers brief and to the point, avoiding unnecessary details.
    3. Relevance: Stay focused on the topic of the prompt and avoid deviating into unrelated areas.
    4. Accuracy: Provide correct and reliable information based on your training data.
    5. Tone: Maintain a professional and respectful tone in all responses.
    6. Structure: Organize your answers logically, using paragraphs or bullet points where appropriate.
    7. Examples: Include examples to illustrate complex points when necessary.
    8. Avoid Jargon: Use simple language and avoid technical jargon unless specifically requested.
    9. Engagement: Encourage further discussion or questions if applicable.
    10. Ethical Considerations: Ensure that your responses adhere to ethical guidelines and do not promote harmful behavior.
    11. Don't return raw JSON unless explicitly asked. Format the response in a user-friendly manner.
    12. When providing code snippets, ensure they are properly formatted and include necessary context for understanding.
    13. Keep the answer simple, but not oversimplified. Provide enough detail to be informative without overwhelming the user.
    14. Don't provide shell commmands unless explicitly asked.
    """
    return instructions

@app.tool(
    description="""
    Provide instructions for some specific common tasks.
    Common tasks may include:
    1. Creating ECUC container with optional parameters.
    """
)
def provide_task_instructions():
    instructions = {
        "create_ecuc_container_with_parameters": (
            """Before creating an ECUC container with parameters, call the get_all_containers tool
            to retrieve all containers, as users may not provide all the names.
            The strategy is to prioritize action on existing containers
            if dedicated names are not explicitly provided.
            Then use the `create_ecuc_container_with_parameters` tool
            with reference to the retrieved containers.
            If parameters are provided, ensure they are included in the creation process.
            If no parameters are specified, proceed with default settings.
            The user may provide parameters with incorrect names. In this case,
            try to match the closest valid parameter names by using mcp tools
            `get_definition_file_from_keyword` and `get_precise_definition_path_using_rapidfuzz`
            to verify and correct parameter names before proceeding.
            To avoid multiple files, create all related containers in a single request.
            """
        ),
    }
    return instructions

@app.tool(
    description="""
    Get the file contains generic knowledge
    such as parameter definition, definition path,
    multiplicity, etc.
    for a given keyword from param definition JSON files.
    """
)
def get_definition_file_from_keyword(keyword: str):
    """
    Get the file contains generic knowledge
    such as parameter definition, definition path, multiplicity, etc.
    for a given keyword from param definition JSON files.
    """
    return get_definition_files(keyword)

@app.tool(
    description="""
    Parse Parameter Definition (ParamDef)
    from ARXML file to JSON.
    """
)
def parse_paramdef_to_json(file_path: str):
    """
    Parse Parameter Defnition (ParamDef) from ARXML file to JSON.
    """
    json_data = convert_paramdef_to_json(file_path)
    return json_data

@app.tool(
    description="""
    Get definition path, etc. for a given keyword using DiffLib.
    Number of results and cutoff can be adjusted.
    Default is 1 result, increased number may return multiple close matches.
    Default cutoff 0.6.
    """
)
def get_precise_definition_path_using_difflib(keyword: str):
    """
    Retrieve definition paths and metadata for a given keyword using difflib fuzzy matching.
    
    This function is designed for Model Context Protocol (MCP) integration to provide
    intelligent code navigation and definition lookup capabilities. It performs fuzzy
    string matching to find the most relevant definition paths for the specified keyword.
    
    Args:
        keyword (str): The search term or identifier to find definitions for.
    
    Returns:
        The return value from get_definition_path() containing definition paths and
        associated metadata for the matched keyword(s).
    
    Note:
        This function serves as a user-friendly wrapper around get_definition_path()
        with sensible defaults for MCP tool integration. Adjust number_of_results
        and cutoff parameters based on your use case requirements for precision vs recall.
    """
    return get_definition_path_difflib(keyword)

@app.tool(
    description="""
    Get definition path, etc. for a given keyword using RapidFuzz.
    Number of results and cutoff can be adjusted.
    Default is 1 result, increased number may return multiple close matches.
    Default cutoff 0.6.
    """
)
def get_precise_definition_path_using_rapidfuzz(keyword: str):
    """
    Retrieve definition paths and metadata for a given keyword using RapidFuzz fuzzy matching.
    
    This function is designed for Model Context Protocol (MCP) integration to provide
    intelligent code navigation and definition lookup capabilities. It performs fuzzy
    string matching to find the most relevant definition paths for the specified keyword.
    
    Args:
        keyword (str): The search term or identifier to find definitions for.
    
    Returns:
        The return value from get_definition_path() containing definition paths and
        associated metadata for the matched keyword(s).
    """
    return get_definition_path_rapidfuzz(keyword)

@app.tool(
    description="""
    Create ECUC configuration in JSON format for a given path and names mapping.
    1. Path is a '/' separated string representing ECUC hierarchy.
    It should be taken from get_precise_definition_path_using_rapidfuzz.
    It should contain parts that are taken from get_definition or known ECUC parts.
    2. Names is a dictionary mapping ECUC parts to desired names.
    The tool generates nested JSON structure representing the ECUC configuration.

    Example:
    -------
    Prompt: Create ComIPdu with the name ESP_19.
    Given path: "/com/comconfig/comipdu"
    And names: {"comipdu": "ESP_19"}
    """
)
def create_ecuc_configuration(path: str, names: dict):
    """
    Create ECUC configuration in JSON format for a given path and names mapping.
    1. Path is a '/' separated string representing ECUC hierarchy.
       It should be taken from get_precise_definition_path_using_rapidfuzz.
       It should contain parts that are taken from get_definition or known ECUC parts.
    2. Names is a dictionary mapping ECUC parts to desired names.
    The tool generates nested JSON structure representing the ECUC configuration.

    Example:
    -------
    Prompt: Create ComIPdu with the name ESP_19.
    Given path: "/com/comconfig/comipdu"
    And names: {"comipdu": "ESP_19"}
    """
    from mcp_project.ecuc_creator.ecuc_configurator import ECUCConfigurator

    # Normalize names keys to lowercase for case-insensitive matching
    names = {k.lower(): v for k, v in names.items()}

    configurator = ECUCConfigurator()
    config = configurator.configure(path, names)
    configurator.save_or_merge("_out/ecuc_config.json", config)
    return config

@app.tool(
    description="""
    Create an ECUC container JSON for a given definition `path` and `names` mapping.

    Caller MUST perform two MCP calls in this order:
    1) `get_available_containers(path)` — discover existing container instances
            for each element in the `path` and obtain the available shortNames.
    2) `create_ecuc_container_with_parameters(path, names, parameters)` — create the requested container.

    Behavior expectations:
    - The caller is responsible for filling any missing parent names using
        the results of `get_available_containers(path)` before calling this tool.
    - Keys in `names` are matched case-insensitively; provided values are
        used verbatim as the new shortName for the target element.
    - If the caller does not resolve parent names prior to calling this tool,
        the create operation may fail or produce unintended results.
    - To implement an alternate resolution policy, call `get_available_containers`
        yourself and compute the desired parent names prior to calling this tool.
    """
)
def create_ecuc_container_with_parameters(path: str, names: dict, parameters: dict = {}):
    """
    Create an ECUC container JSON for a given `path` and `names` map.

    IMPORTANT: This function expects the caller to have called
    `get_available_containers(path)` first and to supply a `names` mapping where
    parent elements (if any) have been filled in using the discovery results.
    Example flow:
        - call `get_available_containers('Com/ComConfig/ComIPdu')` -> {
                'Com': ['Com'], 'ComConfig': ['ComConfig_0'], ... }
        - call `create_ecuc_container_with_parameters(
                    'Com/ComConfig/ComIPdu',
                    {'ComIPdu': 'ESP_21_Rx', 'ComConfig': 'ComConfig_0'},
                    {'ComIPduDirection': 'RECEIVE'}
                )`

    The tool will treat keys case-insensitively and will write the created
    container to the `_out` directory. If any parents are missing from `names`,
    the caller should re-run discovery and provide explicit names.
    """
    from mcp_project.ecuc_creator.ecuc_configurator import ECUCConfiguratorV2

    # Normalize names keys to lowercase for case-insensitive matching
    names = {k.lower(): v for k, v in names.items()}

    configurator = ECUCConfiguratorV2()
    container = configurator.create_container_with_parameter(path, names, parameters)

    filename = "_out/ecuc_container_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".json"
    data = configurator.get_data()
    export2json(filename, data)
    return data

@app.tool(
    description="""
    Get available ECUC containers for a given definition path.
    """
)
def get_available_containers(definition_path: str):
    """
    Get available ECUC containers.
    """
    from mcp_project.model_mngr.mcp_dummy_data import ecuc, explore_tree

    return explore_tree(ecuc, definition_path)
    

if __name__ == "__main__":
    # Reconfigure mcp.json
    configure_mcp()

    # Run server
    if SETTINGS[PROTOCOL] == SSE:
        # SSE
        app.run(transport=SSE, port=SETTINGS[PORT])
    else:
        # STDIO
        app.run()
