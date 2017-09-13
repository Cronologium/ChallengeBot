import sqlite3


class Repository(object):
    def __init__(self, db_path):
        self.db_path = db_path

    def select(self, table, columns=[], conditions={}):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        if len(columns) == 0 or table is None:
            return []
        query = 'SELECT ' + ', '.join([str(column) for column in columns]) + \
                ' FROM ' + table
        if len(conditions) > 0:
            query += ' WHERE ' + ' AND '.join([str(k) + '=(?)' for k in conditions])

        t = tuple([conditions[k] for k in conditions])
        #print query, t
        cursor.execute(query, t)
        result = []
        for r in cursor.fetchall():
            result.append({})
            for x in xrange(len(columns)):
                result[-1][columns[x]] = r[x]
        #print str(result)
        cursor.close()
        conn.close()
        return result

    def insert(self, table=None, values={}):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        if len(values) == 0 or table is None:
            return
        non_query = 'INSERT INTO ' + table + ' (' + ', '.join(str(key) for key in values.keys()) + ') VALUES (' + ', '.join(['(?)' for x in xrange(len(values))]) + ')'

        t = tuple([values[key] for key in values])
        #print non_query, t
        cursor.execute(non_query, t)
        cursor.close()
        conn.commit()
        conn.close()

    def update(self, table, values={}, conditions={}):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        if len(values) == 0 or table is None:
            return
        non_query = 'UPDATE ' + table + \
                    ' SET ' + ', '.join([str(k) + '=(?)' for k in values])
        if len(conditions) > 0:
            non_query += ' WHERE ' + ' AND '.join([str(k) + '=(?)' for k in conditions])

        t = tuple([values[k] for k in values]) + tuple([conditions[k] for k in conditions])
        #print non_query, t
        cursor.execute(non_query, t)
        cursor.close()
        conn.commit()
        conn.close()
