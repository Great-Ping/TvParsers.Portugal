from datetime import datetime, timedelta, timezone
from zipfile import ZipFile
from .base_parser import RowsReader, XlsxTvParser
from .models import TvProgramData
from .utils import fill_finish_date_by_next_start_date

class CommonParser(XlsxTvParser):
    __first_header_index = 7
    __response_timezone = timezone(timedelta(hours=-3))
    __min_date = datetime(year=1900, month=1, day=1) - timedelta(days=2)

    def parse(self, xlsx_file: ZipFile):
        row_strings = self._read_strings(xlsx_file)
        sheet_xml_tree = self._read_sheet_xml("sheet1.xml", xlsx_file)
        rows_reader = RowsReader(sheet_xml_tree, row_strings)
        parsed_programs = []

        for row in rows_reader.iter():
            if (len(row) < 12 or not row[1].isdigit()):
                continue
            
            datetime_start = self.__parse_datetime(row)
            channel = row[0]
            title = row[3]
            description = row[9]

            program = TvProgramData(
                datetime_start,
                None,
                channel,
                title,
                None,
                description,
                False                
            )
            parsed_programs.append(program)
            
        fill_finish_date_by_next_start_date(parsed_programs)
        return parsed_programs
    
    def __parse_datetime(self, row: list[str]):
        date = self.__min_date + timedelta(days=int(row[1]))
        date += timedelta(days=1)*float(row[2])
        return  date.replace(tzinfo=self.__response_timezone)
