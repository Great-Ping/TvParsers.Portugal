from shared.options import read_command_line_options
from shared.program_parser import CommonParser
from shared.output import run_parser_out_to_csv

if (__name__=="__main__"):
    options = read_command_line_options()
    parser = CommonParser(options.parser_options)
    run_parser_out_to_csv(parser, options.save_options)
    
