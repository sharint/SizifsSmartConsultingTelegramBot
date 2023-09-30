import sqlite3

dbName = "sizifs.db"
tableName = "questionAndAnswers"

# Импорт базы данных из формата csv
def fromCsvToDb():
    import pandas as pd
    data = pd.read_csv ('./baseh.csv')   
    df = pd.DataFrame(data)


    con = sqlite3.connect(dbName)
    cur = con.cursor()

    for row in df.itertuples():
        data = [row.question.lower(), row.answer.lower(), row.context.lower()]
        cur.execute('''
                    INSERT INTO {0}
                    VALUES (?,?,?)
                    '''.format(tableName),
                    data,
                    )
    con.commit()
    con.close()

# Содание таблицы бд
def createTable():
    con = sqlite3.connect(dbName)
    cur = con.cursor()
    cur.execute("CREATE TABLE {0}(question varchar(255), answer varchar(255), contex varchar(255));".format(tableName))
    con.close()

# Запись в таблицу бд
def setData():
    con = sqlite3.connect(dbName)
    cur = con.cursor()
    querry = """
    INSERT INTO {0}(question, answer, contex) VALUES
        ('Quest', 'Ans', 'vadick');
    """.format(tableName)
    cur.execute(querry)
    con.commit()
    con.close()

# Получение ответа из вопроса
def getAnwerByQuestion(question):
    con = sqlite3.connect(dbName)
    cur = con.cursor()
    querry = """
    SELECT answer from {0} where question = "{1}";
    """.format(tableName,question)
    a = cur.execute(querry).fetchone()
    con.close()
    return a[0] if a!=None else a
