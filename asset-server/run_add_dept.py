import pymysql

conn = pymysql.connect(
    host='localhost',
    user='asset_user',
    password='123456',
    database='asset_db'
)

try:
    cursor = conn.cursor()
    
    # 读取 SQL 文件
    with open('../docs/add_department.sql', 'r', encoding='utf-8') as f:
        sql_content = f.read()
    
    print(f'执行: {sql_content.strip()}')
    cursor.execute(sql_content)
    conn.commit()
    
    # 验证
    cursor.execute("SHOW COLUMNS FROM assets LIKE 'department'")
    print('\ndepartment列信息:')
    for row in cursor.fetchall():
        print(f'  {row}')
    
finally:
    conn.close()