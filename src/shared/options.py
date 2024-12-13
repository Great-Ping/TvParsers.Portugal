import os
from os.path import abspath
from inspect import getsourcefile
import json
from datetime import datetime, UTC
from typing import Union
from argparse import ArgumentParser

class ParserOptions:
    pass

class SaveOptions:
    input_path: str
    output_path: str
    separator: str
    use_smb: bool
    user_name: Union[str|None]
    password: Union[str|None]

    def __init__(
        self,
        input_path: str,
        output_path: str,
        separator: str,
        use_smb: bool,
        user_name: Union[str|None],
        password: Union[str|None]
    ):
        self.separator = separator
        self.input_path = input_path
        self.output_path = output_path
        self.use_smb = use_smb
        self.user_name = user_name
        self.password = password 

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


def create_default_arg_parser(options: Options) -> ArgumentParser:
    args_parser = ArgumentParser()
    args_parser.add_argument("-i", "--input", default=options.save_options.input_path)
    args_parser.add_argument("-o", "--output", default=options.save_options.output_path)
    args_parser.add_argument("-sep", "--separator", default=options.save_options.separator)
    args_parser.add_argument("-ismb", "--use-smb-for-input", default=options.save_options.use_smb, action='store_true')
    args_parser.add_argument("-u", "--user-name", default=options.save_options.user_name)
    args_parser.add_argument("-p", "--password", default=options.save_options.password)
    return args_parser


def read_config_json(parser_name, config_path):
    with open(config_path) as file:
        config = json.load(file)
        config = config[parser_name]
        save_options = SaveOptions(
            config["input"],
            config["output"],
            config["separator"],
            config["ismb"],
            config["username"],
            config["password"]
        )

        return Options(ParserOptions(), save_options)
    


def read_command_line_options(default: Options) -> Options:
    parser = create_default_arg_parser(default)
    args = parser.parse_args()
    
    parser_options = ParserOptions()
    save_options = SaveOptions(args.input, args.output, args.separator, args.use_smb_for_input, args.user_name, args.password)

    return Options(parser_options, save_options)