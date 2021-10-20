from automates.program_analysis.GCC2GrFN.gcc_ast_to_cast import GCC2CAST
import json

gcc_ast_obj = json.load(open("test_if_gcc_ast.json"))
cast = GCC2CAST([gcc_ast_obj]).to_cast()
print(cast.to_json_str())

json.dump(cast.to_json_object(), open(f"test_if--CAST.json", "w"))
