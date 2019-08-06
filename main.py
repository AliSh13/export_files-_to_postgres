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




def export_csv_to_sql(path_to_file, table_name, index, columns_names=[],
                    rename_column={}):
    """ Функция переводит csv файл в базу данных """
    file = path_to_file
    df = pd.read_csv(file) # создает DataFrame файл

    #определяем названия колонок при разных заданных аргументах
    if columns_names:
        df.columns=[c.lower() for c in columns_names]
    else:
        df.columns = [c.lower() for c in df.columns]
    if rename_column:
        df.rename(columns=rename_column, inplace=True)
    # проверяем наличие таблицы и, если существует, проверяем новый файл на уникальность строк
    if exists_table(db_connect(), table_name) :
        df = unique_lines_only(df, table_name, db_connect(), list(df.columns))

    df.to_sql(table_name, db_connect(), if_exists='append', index=index)


def export_excel_to_sql(path_to_file, table_name, index, sheet=1,
                        columns_names=[], rename_column={}):
    """ Функция переводит excel файл в базу данных """
    wb = load_workbook(path_to_file)
    #читаем определенный лист документ ( по умолчанию - 1 )
    sheet = wb.get_sheet_by_name(wb.get_sheet_names()[sheet-1])
    data = list(sheet.values)
    df = pd.DataFrame(data)

    #определяем названия колонок при разных заданных аргументах
    if columns_names:
        df.columns=[c.lower() for c in columns_names]
    else:
        cols = data[0]
        data = data[1:]
        df = pd.DataFrame(data, columns=cols)
        df.columns = [c.lower() for c in df.columns]
    if rename_column:
        df.rename(columns=rename_column, inplace=True)
    # проверяем наличие таблицы и, если существует, проверяем новый файл на уникальность строк    
    if exists_table(db_connect(), table_name) :
        df = unique_lines_only(df, table_name, db_connect(), list(df.columns))

    df.to_sql(table_name, db_connect(), if_exists='append', index=index)



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
