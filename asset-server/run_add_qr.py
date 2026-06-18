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
    with open('../docs/step3_qr.sql', 'r', encoding='utf-8') as f:
        sql_content = f.read()
    
    # 分割为多条语句
    statements = [s.strip() for s in sql_content.split(';') if s.strip() and not s.strip().startswith('--')]
    
    for stmt in statements:
        if stmt:
            print(f'执行: {stmt}')
            cursor.execute(stmt)
            conn.commit()
    
    # 验证
    cursor.execute("SHOW COLUMNS FROM assets LIKE 'qr_code_url'")
    print('\nqr_code_url列:')
    for row in cursor.fetchall():
        print(f'  {row}')
    
    print('\nSQL执行成功')
    
finally:
    conn.close()