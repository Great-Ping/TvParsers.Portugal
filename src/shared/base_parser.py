
from typing import Iterable
from xml.dom.minidom import Element
from zipfile import ZipFile

from shared.models import TvProgramData
from shared.utils import get_xml_node_text
from .options import ParserOptions
from xml.etree import ElementTree

class RowsReader:
    _xmlns = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
    _row_full_name:str
    _strings: list[str]
    _sheet_xml: ElementTree
    _current_index = -1

    def __init__(self, sheet_xml, strings):
        self._row_full_name=f"{{{self._xmlns}}}sheetData/{{{self._xmlns}}}row"
        self._strings = strings
        self._sheet_xml = sheet_xml

    def __prepare_row(self, row: Element) -> list[str]:
        for column in row: 
            #Проверка на строку
            type = column.attrib.setdefault("t", None)
            value = column.find(f"{{{self._xmlns}}}v")

            if value is None:
                return None
            elif type != "s":
                yield value.text
            else:
                index = int(value.text)
                yield self._strings[index]


    def iter(self) -> Iterable[list[str]]:
        root = self._sheet_xml.getroot()
        for node in root.findall(self._row_full_name):
            node_strings = list(self.__prepare_row(node))
            yield node_strings

class XlsxTvParser:    
    options: ParserOptions

    def __init__(self, options: ParserOptions) -> None:
        self.options = options

    def _read_strings(self, xlsx_file: ZipFile) -> list[str]:
        strings = []
        with xlsx_file.open("xl/sharedStrings.xml", "r") as xml_file:
            xml_tree = ElementTree.parse(xml_file)
            xml_root = xml_tree.getroot()
            for string_node in xml_root:
                strings.append(
                    get_xml_node_text(string_node).replace("\n", " ")
                )
                
                
        return strings
    
    def _read_sheet_xml(self, sheet_file_name, xlsx_file) -> ElementTree:
        with xlsx_file.open(f"xl/worksheets/{sheet_file_name}", "r") as xml_file:
            return ElementTree.parse(xml_file)
            
    def parse(self, xlsx_file: ZipFile) ->  list[TvProgramData]:
        pass


