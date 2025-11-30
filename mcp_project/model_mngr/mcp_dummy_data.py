ecuc = {
    "com" : {
        "type" : "Com",
        "containers": {
            "ComConfig_0" : {
                "type" : "ComConfig",
                "containers": {
                    "ComIPdu_ESP_10" : {
                        "type" : "ComIPdu",
                        "parameters": {
                            "ComIPduDirection" : "RECEIVE",
                            "ComIPduSignalProcessing" : "DEFERRED"
                        }
                    },
                    "ComIPdu_ESP_19" : {
                        "type" : "ComIPdu",
                        "parameters": {
                            "ComIPduDirection" : "SEND",
                            "ComIPduSignalProcessing" : "IMMEDIATE"
                        }
                    }
                }
            }
        }
    },
    "pdur" : {
        "type" : "PduR",
        "containers": {
            "PduRGeneral" : {
                "type" : "PduRGeneral",
                "parameters": {
                    "PduRDevErrorDetect" : True
                }
            }
        }
    }
}

def explore_tree(tree: dict, definition_path: str = None):
    """
    Generic explorer for an ECUC-like `tree` structure.

    If `definition_path` is provided (e.g. 'Com/ComConfig/ComIPdu'), the
    function will search the tree case-insensitively and return a nested
    mapping where the first path part is the top key and the final-level
    instances are mapped to empty dicts. Example return for
    'Com/ComConfig/ComIPdu':

    { 'Com': { 'ComConfig_0': { 'ComIPdu_ESP_10': {}, ... } } }

    If `definition_path` is None, the function will attempt to infer a path
    starting from the first top-level key and collect two levels of
    containers beneath it.
    """
    def child_containers(node):
        if not isinstance(node, dict):
            return {}
        cont = node.get("containers") if "containers" in node else None
        if isinstance(cont, dict):
            return cont
        return {k: v for k, v in node.items() if isinstance(v, dict)}

    # If a definition_path is provided, use it to guide extraction
    if definition_path:
        parts = [p for p in definition_path.strip("/").split("/") if p]
        if not parts:
            return {}

        # find top-level matching key in tree (case-insensitive)
        top_node = None
        for k, v in tree.items():
            if isinstance(k, str) and k.lower() == parts[0].lower():
                top_node = v
                break
        if top_node is None:
            # fallback: try to find any key that starts with the part
            for k, v in tree.items():
                if isinstance(k, str) and k.lower().startswith(parts[0].lower()):
                    top_node = v
                    break
        if top_node is None:
            return {}

        out = {parts[0]: {}}

        # recursive builder
        def build_level(node, idx):
            # idx is index in parts for the current level to match
            conts = child_containers(node)
            matched = []
            for name, child in conts.items():
                if isinstance(name, str) and name.lower().startswith(parts[idx].lower()):
                    matched.append((name, child))
            if idx == len(parts) - 1:
                return {name: {} for name, _ in matched}
            result = {}
            for name, child in matched:
                result[name] = build_level(child, idx + 1)
            return result

        # If only top-level requested
        if len(parts) == 1:
            conts = child_containers(top_node)
            return {parts[0]: {name: {} for name in conts.keys()}}

        out[parts[0]] = build_level(top_node, 1)
        return out

    # No definition_path: fallback to previous heuristic — take first top key
    # and collect two levels of containers beneath it.
    # find first dict top entry
    top_key = None
    top_node = None
    for k, v in tree.items():
        if isinstance(v, dict):
            top_key = k
            top_node = v
            break
    if top_node is None:
        return {}

    out = {str(top_key): {}}
    level1 = child_containers(top_node)
    for name1, node1 in level1.items():
        out[str(top_key)][name1] = {}
        level2 = child_containers(node1)
        for name2 in level2.keys():
            out[str(top_key)][name1][name2] = {}
    return out
