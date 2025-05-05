import mysql.connector
import dbconfig as cfg

class CourseDAO:
    connection = ""
    cursor = ""
    host = ''
    user = ''
    password = ''
    database = ''

    def __init__(self):
        self.host = cfg.mysql['host']
        self.user = cfg.mysql['user']
        self.password = cfg.mysql['password']
        self.database = cfg.mysql['database']

    def getcursor(self):
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
        )
        self.cursor = self.connection.cursor()
        return self.cursor

    def closeAll(self):
        self.cursor.close()
        self.connection.close()

    def getAll(self):
        cursor = self.getcursor()
        sql = "SELECT * FROM course"
        cursor.execute(sql)
        results = cursor.fetchall()
        returnArray = []
        for result in results:
            returnArray.append(self.convertToDictionary(result))
        self.closeAll()
        return returnArray

    def findByID(self, id):
        cursor = self.getcursor()
        sql = "SELECT * FROM course WHERE id = %s"
        values = (id,)
        cursor.execute(sql, values)
        result = cursor.fetchone()
        self.closeAll()
        return self.convertToDictionary(result)

    def create(self, course):
        cursor = self.getcursor()
        sql = "INSERT INTO course (CourseName, StudentName, Duration) VALUES (%s, %s, %s)"
        values = (course.get("CourseName"), course.get("StudentName"), course.get("Duration"))
        cursor.execute(sql, values)
        self.connection.commit()
        course["id"] = cursor.lastrowid
        self.closeAll()
        return course

    def update(self, id, course):
        cursor = self.getcursor()
        sql = "UPDATE course SET CourseName=%s, StudentName=%s, Duration=%s WHERE id=%s"
        values = (course.get("CourseName"), course.get("StudentName"), course.get("Duration"), id)
        cursor.execute(sql, values)
        self.connection.commit()
        self.closeAll()

    def delete(self, id):
        cursor = self.getcursor()
        sql = "DELETE FROM course WHERE id = %s"
        values = (id,)
        cursor.execute(sql, values)
        self.connection.commit()
        self.closeAll()

    def convertToDictionary(self, resultLine):
        attkeys = ['id', 'CourseName', 'StudentName', 'Duration']
        course = {}
        for i, attrib in enumerate(resultLine):
            course[attkeys[i]] = attrib
        return course

courseDAO = CourseDAO()
