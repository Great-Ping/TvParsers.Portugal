from datetime import datetime, timedelta
from typing import Union
from xml.etree.ElementTree import Element
from .models import TvProgramData

def get_monday_datetime(timezone):
    now = datetime.now(timezone)
    now -= timedelta(days=now.weekday())
    return now

def format_date(date: Union[datetime, None]):
    if (date is None):
        return ""

    return date.isoformat("T", "seconds")

#Заполняет дату и время для каждой программы, 
#основываясь на дате начала предыдущей программы.
#Для последней программы дата окончания 23:59 этого же дня
def fill_finish_date_by_next_start_date(tv_programs: list[TvProgramData], remove_last = False):
    for i in range(1, len(tv_programs)):
        tv_programs[i-1].datetime_finish = tv_programs[i].datetime_start

    if (len(tv_programs) == 0):
        return 

    if (remove_last):
        tv_programs.pop()
        return 
    
    last_program = tv_programs[-1]
    last_program.datetime_finish = last_program.datetime_start.replace(
        hour=23,
        minute=59
    )

def is_none_or_empty(string: str):
    if (string is None):
        return True
    
    return string == "" or string == " " or string == "\t" or string == "\n" or string == "\r"


def get_xml_node_text(node: Element):
        if (isinstance(node, str)):
            return node

        result = ""

        for i in node.itertext():
            result += i

        return result

#Удаляет пустые символы из начала и конца строк
def replace_spaces(string: str):
    start = 0
    end = len(string)
    for i in string:
        if (not is_none_or_empty(i)):
            break
        start += 1

    for i in reversed(string):
        if (not is_none_or_empty(i)):
            break
        end -= 1
    
    return string[start: end]