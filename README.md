# О проекте:
Парсеры португальских xlsx файлов. <br>
<br>
Пример использования<br>
```shell
python src/cnbc.py -i ./file.xlsx
```
<br>

## Параметры по умолчанию
В файле [default_config.json](src/default_config.json)
Для описания используется следующая структура данных 
```json
{
    "Имя Парсера":{
        "input": "путь к файлу",
        "ismb": false, // указывает на использование smb для доступа к файлу
        "username": null, // для smb
        "password": null, // для smb
        "output": "выходной путь", 
        "separator": "\t" // разделитель по умолчанию
    }
}
```