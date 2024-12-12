import os
import smbclient
from zipfile import ZipFile
from datetime import datetime
from typing import *

from shared.xlsx_parser import XlsxParser
from shared.utils import replace_spaces

from .options import SaveOptions
from .models import TvProgramData

def escape(input: str):
    if (input is None):
        return "\"\""
    
    input = input.replace("\"", "\"\"")
    return f"\"{input}\""

def __format_date(date: Union[datetime, None]):
    if (date is None):
        return ""

    return date.isoformat("T", "seconds")
    
def __to_csv_line(data:TvProgramData, options: SaveOptions):
    data.channel = replace_spaces(data.channel)
    data.title = replace_spaces(data.title)
    if (data.description != None):
        data.description = replace_spaces(data.description)

    return (f"{escape(__format_date(data.datetime_start))}" 
    + f"{options.separator}{escape(__format_date(data.datetime_finish))}"
    + f"{options.separator}{escape(data.channel)}"
    + f"{options.separator}{escape(data.title)}"
    + f"{options.separator}{escape(data.channel_logo_url)}"
    + f"{options.separator}{escape(data.description)}"
    + f"{options.separator}{str(int(data.available_archive))}"
    + "\n")

def __out_to_csv(tvPrograms: list[TvProgramData], options: SaveOptions):
    dirname = os.path.dirname(options.output_path)
    if (dirname != None and dirname != ""):
        os.makedirs(dirname, exist_ok=True)
        
    with open(options.output_path, "w+", encoding="utf-8") as stream:
        stream.write(
            "\"datetime_start\""
            +f"{options.separator}\"datetime_finish\""
            +f"{options.separator}\"channel\""
            +f"{options.separator}\"title\""
            +f"{options.separator}\"channel_logo_url\""
            +f"{options.separator}\"description\""
            +f"{options.separator}\"available_archive\""
            +"\n")

        for tvProgram in tvPrograms:
            csv_line = __to_csv_line(tvProgram, options)
            stream.write(
                csv_line
            )


def __select_input_file_stream(options: SaveOptions):
    if options.use_smb:
        #singleton o_0
        smbclient.ClientConfig(
            username=options.user_name,
            password=options.password
        )

        return smbclient.open_file(
            options.input_path,
            "rb"
        )
    else: 
        return open(options.input_path, "rb")



def run_parser_out_to_csv(
        parser: XlsxParser, 
        options: SaveOptions
):
    with __select_input_file_stream(options) as zip_file:
        with ZipFile(zip_file) as xlsx_file:
            parsedData = parser.parse(xlsx_file)
            __out_to_csv(parsedData, options)