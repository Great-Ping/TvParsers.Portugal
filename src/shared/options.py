from datetime import datetime, UTC
from typing import Union
from argparse import ArgumentParser

class ParserOptions:
    pass

class SaveOptions:
    input_path: str
    output_path: str
    separator: str
    def __init__(
        self,
        input_path: str,
        output_path: str,
        separator: str = "\t"
    ):
        self.input_path = input_path
        self.separator = separator
        self.output_path = output_path


class Options:
    parser_options: ParserOptions
    save_options: SaveOptions
    
    def __init__(
        self,
        parser_options: ParserOptions,
        save_options: SaveOptions
    ):
        self.parser_options = parser_options
        self.save_options = save_options


def create_default_arg_parser() -> ArgumentParser:
    args_parser = ArgumentParser()
    args_parser.add_argument("-i", "--input", required=True)
    args_parser.add_argument("-o", "--output", default="out.csv")
    args_parser.add_argument("-sep", "--separator", default="\t")

    return args_parser

def read_command_line_options() -> Options:
    parser = create_default_arg_parser()
    args = parser.parse_args()
    
    parser_options = ParserOptions()
    save_options = SaveOptions(args.input, args.output, args.separator)

    return Options(parser_options, save_options)