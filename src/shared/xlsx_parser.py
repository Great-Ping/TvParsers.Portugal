
from datetime import datetime, timedelta
from enum import Enum
import math
from types import UnionType
from typing import Any, Iterable, Union
from xml.dom.minidom import Element
from zipfile import ZipFile

from shared.models import TvProgramData
from shared.utils import get_xml_node_text
from .options import ParserOptions
from xml.etree import ElementTree


MIN_DATE_TIME = datetime(year=1900, month=1, day=1) - timedelta(days=2)

class XlsxCellType(Enum):
    STRING = 0,
    NUMBER = 1,
    OTHER = 2

class XlsxCell:
    value: Element
    style: Union[Element|None]
    type: XlsxCellType
    str_value: Union[str|None]

    def __init__(self, value, style, type, str_value) -> None:
        self.value = value
        self.style = style
        self.type = type
        self.str_value = str_value

class RowsReader(Iterable):
    _rows: list[Element]
    _styles: list[Element]
    _strings: list[str]
    _xmlns: str
    _current_index = -1

    def __init__(self, rows:list[Element], strings: list[str], styles:list[Element], xmlns: str):
        self._rows = rows 
        self._strings = strings
        self._styles = styles
        self._xmlns = xmlns


    def __get_vtag_value(self, column):
        value = column.find(f"{{{self._xmlns}}}v")
        if (value is None):
            return None

        return value.text

    def _try_format_number(self, cell, number_format):
        if (cell.str_value == None): #нет значения
            return        

        cell.type = XlsxCellType.NUMBER
        if (number_format == "0"): #Общий формат
            return

        if (number_format == "14"): #Дата 05.12.2024
            number = int(cell.str_value)
            date =MIN_DATE_TIME + timedelta(days=number)
            cell.str_value = date.isoformat()
            return
        
        if (number_format == "20"): #Время 20:00
            number = float(cell.str_value)
            time = 24 * number
            minutes, hours = math.modf(time)
            cell.str_value = f"{int(hours):02d}:{int(minutes*60):02d}"
            return

        #Not supported ??? other format
        cell.type = XlsxCellType.OTHER
    
    def __prepare_row(self, row: Element) -> list[str]:
        cells = []

        for column in row:
            style_id = column.attrib.get("s", None)
            
            style = None
            numfmt = None
            if (style_id != None):
                style = self._styles[int(style_id)]
                numfmt = style.attrib.get("numFmtId", None)
            
            cell = XlsxCell(
                column, 
                style, 
                XlsxCellType.OTHER, 
                self.__get_vtag_value(column)
            )

            if (cell.value.attrib.get("t", None) != None):
                cell.type = XlsxCellType.STRING
                str_index = self.__get_vtag_value(column)
                cell.str_value = self._strings[int(str_index)] 
            elif cell.str_value != None and numfmt != None:
                self._try_format_number(cell, numfmt)
                    
            cells.append(cell)

        return cells

    def __next__(self) -> list[XlsxCell]:
        if (self._current_index >= len(self._rows)):
            raise StopIteration()
        
        row = self._rows[self._current_index]
        self._current_index += 1
        return self.__prepare_row(row)

    def __iter__(self):
        return self



class XlsxParser:    
    def __init__(self, xlsx_file: ZipFile) -> None:
        self._zip = xlsx_file
        self._xmlns = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"

    def _read_strings(self) -> list[str]:
        strings = []
        with self._zip.open("xl/sharedStrings.xml", "r") as xml_file:
            xml_tree = ElementTree.parse(xml_file)
            xml_root = xml_tree.getroot()
            for string_node in xml_root:
                strings.append(
                    get_xml_node_text(string_node).replace("\n", " ")
                )
                
        return strings
    
    def _read_styles(self):
        with self._zip.open(f"xl/styles.xml", "r") as xml_file:
            tree = ElementTree.parse(xml_file)
            root = tree.getroot()
            return list(root.findall(f"{{{self._xmlns}}}cellXfs/{{{self._xmlns}}}xf"))

    def _read_sheet_xml_rows(self, sheet_file_name) -> ElementTree:
        with self._zip.open(f"xl/worksheets/{sheet_file_name}", "r") as xml_file:
            tree = ElementTree.parse(xml_file)
            root = tree.getroot()
            return list(root.findall(f"{{{self._xmlns}}}sheetData/{{{self._xmlns}}}row"))
   
    def create_row_reader(self, sheet_name: str) -> Iterable[list[XlsxCell]]:
        rows = self._read_sheet_xml_rows(sheet_name)
        styles = self._read_styles()
        strings = self._read_strings()

        return RowsReader(rows, strings, styles, self._xmlns)


