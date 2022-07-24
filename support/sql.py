import pymysql

class face_sql:
    def __init__(self):
        self.conn=pymysql.connect(host="localhost",
            user="root",password="0925deng", db="face_recognition",port=3306,
            charset="utf8")

    def processFaceData(self, sqlstr, args=()):
        print(sqlstr)
        cursor = self.conn.cursor()
        try:
            cursor.execute(sqlstr,args)
            self.conn.commit()
        except Exception as e:
            # 如果发生错误则回滚并打印错误信息
            self.conn.rollback()
            print(e)
        finally:
            # 关闭游标 连接号
            cursor.close()

    def saveFaceData(self, name, class_no, no, encoding_str):
        self.processFaceData("insert into face_info(name, class_no, no, encode) values(%s,%s,%s,%s)", (name, class_no, no, encoding_str))

    # def updateFaceData(self, id, encoding_str):
    #     self.processFaceData("update face set encoding = %s where 学号 = %s", (encoding_str, id))

    def execute_float_sqlstr(self, sqlstr):
        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = self.conn.cursor()
        # SQL插入语句
        results = []
        try:
            # 执行sql语句
            cursor.execute(sqlstr)
            # 获取所有记录列表
            results = cursor.fetchall()
        except Exception as e:
            # 如果发生错误则回滚并打印错误信息
            self.conn.rollback()
            print(e)
        finally:
            # 关闭游标
            cursor.close()
            return results


    def get_all_info(self):
        return self.execute_float_sqlstr("select * from face_info")

    def get_face_info(self):
        return self.execute_float_sqlstr("select encode from face_info")

    def search_data(self, face_encoding_str):
        return self.execute_float_sqlstr("select * from face_info where encode='"+face_encoding_str+"'")
    # def sreachFaceData(self, id):
    #     return self.execute_float_sqlstr("select * from face where 学号=" + id)
    #
    # def sreach_Info(self, id):
    #     return self.execute_float_sqlstr("select * from zstustu where 学号='" + id + "'")




