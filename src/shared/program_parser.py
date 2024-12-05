from datetime import datetime, timedelta, timezone
from zipfile import ZipFile
from .xlsx_parser import RowsReader, XlsxCellType, XlsxParser
from .models import TvProgramData
from .utils import fill_finish_date_by_next_start_date

class CommonParser:
    __response_timezone = timezone(timedelta(hours=-3))

    def __init__(self, options) -> None:
        pass

    def parse(self, xlsx_file: ZipFile):
        xlsx_parser = XlsxParser(xlsx_file)
        rows_reader = xlsx_parser.create_row_reader("sheet1.xml")

        parsed_programs = []
        for row in rows_reader:
            if (len(row) < 12 or not row[1].type == XlsxCellType.NUMBER):
                continue
            
            datetime_start = self.__parse_datetime(row)
            channel = row[0].str_value
            title = row[3].str_value
            description = row[9].str_value

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
        time = row[2].str_value.split(":")
        date = datetime.fromisoformat(row[1].str_value)
        return  date.replace(
            hour=int(time[0]),
            minute=int(time[1]),
            tzinfo=self.__response_timezone
        )
