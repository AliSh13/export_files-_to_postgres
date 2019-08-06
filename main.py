import pandas as pd
from sqlalchemy import types, create_engine
from openpyxl import load_workbook


def db_connect():
    """ подключение к бд """
    user = 'my_user'
    password = 'mypas'
    host = 'localhost'
    name_db = 'test_db'
    conn = create_engine(f'postgresql://{user}:{password}@{host}/{name_db}')
    return conn





def main(path_to_file, format, table_name, index=False, sheet=1,
         columns_names=[], rename_column={} ):
    """определяет нужный формат и выбирает функцию. """
    if format == 'csv':
        export_csv_to_sql(path_to_file, table_name, columns_names=columns_names,
                        rename_column=rename_column, index=index)
    elif format == 'xlsx':
        export_excel_to_sql(path_to_file, table_name, sheet=sheet,
                            columns_names=columns_names, index=index,
                            rename_column=rename_column)



if __name__ == '__main__':
    """Принимает следующие аргументы:
    Обязательные:
     path_to_file - путь до файла,
     format - тип файла(csv, xlsx),
     table_name - название таблицы в бд
    Не обязательные:
      index - по умалчанию False,
      sheet - только для xlsx (Лист файла, по умолчанию - 1),
      columns_names=[] - имя столбцов ,если задаем сами,
      rename_column={} - преименовать существующие столбцы"""
    main()
