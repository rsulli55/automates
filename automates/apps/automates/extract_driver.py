import json

from automates.model_assembly.networks import GroundedFunctionNetwork
from automates.model_assembly.expression_trees.expression_walker import (
    expr_trees_from_grfn
)
from automates.model_assembly.model_dynamics import extract_model_dynamics

def extract_io_from_grfn(GrFN):
    GrFN.inputs
    GrFN.literal_vars
    GrFN.outputs

    # TODO return variable types 

    optional_inputs = [{
        "variable_identifier": str(v.identifier),
        "variable_type": None,
        "required": False
    } for v in GrFN.literal_vars]

    optional_input_identifiers = {v["variable_identifier"] for v in optional_inputs}
    required_inputs = [{
        "variable_identifier": str(v.identifier),
        "variable_type": None,
        "required": True
    } for v in GrFN.inputs if str(v.identifier) not in optional_input_identifiers]

    outputs = [{
        "variable_identifier": str(v.identifier),
        "variable_type": None,
    } for v in GrFN.outputs]

    return {
        "execution_inputs": optional_inputs + required_inputs,
        "execution_outputs": outputs
    }

def extract_expr_trees(GrFN):
    return expr_trees_from_grfn(GrFN)

def extract_model_dynamics_from_grfn(GrFN):
    potential_dynamics_grfns = extract_model_dynamics(GrFN)
    return [{
        "model": json.loads(g.to_json()),
        "variable_io": extract_io_from_grfn(g)
     } 
     for g in potential_dynamics_grfns]

def extract_io_from_grfn_json(grfn_json):
    GrFN = GroundedFunctionNetwork.from_dict(grfn_json)
    return extract_io_from_grfn(GrFN)

def extract_expr_trees_from_grfn_json(grfn_json):
    GrFN = GroundedFunctionNetwork.from_dict(grfn_json)
    return extract_expr_trees(GrFN)

def extract_model_dynamics_from_grfn_json(grfn_json):
    GrFN = GroundedFunctionNetwork.from_dict(grfn_json)
    return extract_model_dynamics_from_grfn(GrFN) 