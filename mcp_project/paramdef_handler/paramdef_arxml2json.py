#!/usr/bin/env python3
"""
Simple ARXML parameter definition to JSON converter.

Generates a JSON structure similar to `_out/com_paramdef.json` but
includes explicit `type` fields for Module, Container and Parameter levels.

Usage: .venv\Scripts\python .\paramdef_arxml2json.py <arxml-file> [-o out.json]
"""
import argparse
import json
import sys
import xml.etree.ElementTree as ET
from typing import Dict


NS = {'ar': 'http://autosar.org/schema/r4.0'}


def text(elem):
    return elem.text.strip() if elem is not None and elem.text else ''


def multiplicity(elem):
    low = text(elem.find('ar:LOWER-MULTIPLICITY', NS)) or '1'
    up = text(elem.find('ar:UPPER-MULTIPLICITY', NS)) or '1'
    if elem.find('ar:UPPER-MULTIPLICITY-INFINITE', NS) is not None and text(elem.find('ar:UPPER-MULTIPLICITY-INFINITE', NS)) in ('true', 'True'):
        return f"{low}..*"
    if up == '*':
        return f"{low}..*"
    if low == up:
        return low
    return f"{low}..{up}"


def parse_parameter(param_elem) -> Dict:
    tag = param_elem.tag.split('}')[-1]
    type_map = {
        'ECUC-BOOLEAN-PARAM-DEF': 'BOOLEAN',
        'ECUC-INTEGER-PARAM-DEF': 'INTEGER',
        'ECUC-FLOAT-PARAM-DEF': 'FLOAT',
        'ECUC-STRING-PARAM-DEF': 'STRING',
        'ECUC-ENUMERATION-PARAM-DEF': 'ENUMERATION',
        'ECUC-FUNCTION-NAME-DEF': 'FUNCTION_NAME',
    }

    name = text(param_elem.find('ar:SHORT-NAME', NS))
    desc = text(param_elem.find('ar:DESC/ar:L-2[@L="EN"]', NS))
    param = {
        'type': 'PARAMETER',
        'param_type': type_map.get(tag, tag),
    }

    # Add same compact style as com_paramdef.json: only include keys when present
    # include multiplicity if not default
    mult = multiplicity(param_elem)
    if mult and mult != '1':
        param['multiplicity'] = mult

    maxv = text(param_elem.find('ar:MAX', NS))
    minv = text(param_elem.find('ar:MIN', NS))
    default = text(param_elem.find('ar:DEFAULT-VALUE', NS))
    if maxv:
        param['maxValue'] = maxv
    if minv:
        param['minValue'] = minv
    if default:
        param['defaultValue'] = default
    if desc:
        param['description'] = desc

    # For enums collect literals
    lits = []
    literals_elem = param_elem.find('ar:LITERALS', NS)
    if literals_elem is not None:
        for lit in literals_elem.findall('ar:ECUC-ENUMERATION-LITERAL-DEF', NS):
            n = text(lit.find('ar:SHORT-NAME', NS))
            if n:
                lits.append(n)
    if lits:
        param['literals'] = lits

    return name, param


def parse_container(cont_elem) -> Dict:
    name = text(cont_elem.find('ar:SHORT-NAME', NS))
    desc = text(cont_elem.find('ar:DESC/ar:L-2[@L="EN"]', NS))
    container: Dict = {'type': 'CONTAINER'}
    if desc:
        container['description'] = desc

    # Parameters
    params = {}
    params_parent = cont_elem.find('ar:PARAMETERS', NS)
    if params_parent is not None:
        for p in params_parent:
            pname, pjson = parse_parameter(p)
            params[pname] = pjson

    # Sub-containers
    subs = {}
    subs_parent = cont_elem.find('ar:SUB-CONTAINERS', NS)
    if subs_parent is not None:
        for s in subs_parent:
            sname, sjson = parse_container(s)
            subs[sname] = sjson

    # Choices (treated as containers)
    choices_parent = cont_elem.find('ar:CHOICES', NS)
    if choices_parent is not None:
        for c in choices_parent:
            cname, cjson = parse_container(c)
            subs[cname] = cjson

    # Merge parameters and sub-containers into a single dict to mimic com_paramdef.json
    # Put parameters first
    for k, v in params.items():
        container[k] = v
    for k, v in subs.items():
        container[k] = v

    return name, container


def find_module(root) -> Dict:
    # Try to find ECUC-MODULE-DEF element
    module_def = root.find('.//ar:ECUC-MODULE-DEF', NS)
    if module_def is None:
        raise SystemExit('No ECUC-MODULE-DEF found in ARXML')

    module_name = text(module_def.find('ar:SHORT-NAME', NS))
    module_desc = text(module_def.find('ar:DESC/ar:L-2[@L="EN"]', NS))

    module = {
        'type': 'MODULE',
        'description': module_desc,
    }

    containers_parent = module_def.find('ar:CONTAINERS', NS)
    if containers_parent is not None:
        for c in containers_parent:
            cname, cjson = parse_container(c)
            module[cname] = cjson

    return module_name, module


def convert_paramdef_to_json(arxml_path: str) -> Dict:
    """
    Parse the ARXML file at `arxml_path` and return the JSON-like dict.

    Returns a dict where the top-level key is the module short-name and the
    value contains the module object (including `type` and children).
    """
    tree = ET.parse(arxml_path)
    root = tree.getroot()
    mod_name, mod_json = find_module(root)
    return {mod_name: mod_json}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('arxml', help='ARXML paramdef file')
    parser.add_argument('-o', '--output', help='Output JSON file (default stdout)')
    args = parser.parse_args()

    out = convert_paramdef_to_json(args.arxml)
    s = json.dumps(out, indent=4, ensure_ascii=False)
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(s)
    else:
        print(s)


if __name__ == '__main__':
    main()
