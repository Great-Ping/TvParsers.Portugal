import os
from inspect import getsourcefile
from os.path import abspath
from shared.options import read_command_line_options, read_config_json
from shared.program_parser import CommonParser
from shared.output import run_parser_out_to_csv

if (__name__=="__main__"):
    project_path = abspath(getsourcefile(lambda:0))
    config_path = os.path.join(os.path.dirname(project_path), "default_config.json")

    defaults = read_config_json("cnbc", config_path)
    options = read_command_line_options(defaults)
    parser = CommonParser(options.parser_options)
    run_parser_out_to_csv(parser, options.save_options)
    
