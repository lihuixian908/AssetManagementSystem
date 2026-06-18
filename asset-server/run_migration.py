import pymysql
import re

conn = pymysql.connect(
    host='localhost',
    user='asset_user',
    password='123456',
    database='asset_db'
)

try:
    cursor = conn.cursor()
    
    # 读取 SQL 文件
    with open('../docs/step1_migration.sql', 'r', encoding='utf-8') as f:
        sql_content = f.read()
    
    # 移除单行注释 (-- 开头)
    sql_content = re.sub(r'--.*$', '', sql_content, flags=re.MULTILINE)
    # 移除多行注释 (/* ... */)
    sql_content = re.sub(r'/\*.*?\*/', '', sql_content, flags=re.DOTALL)
    
    # 分割语句
    statements = [s.strip() for s in sql_content.split(';') if s.strip()]
    
    for stmt in statements:
        print(f'执行: {stmt[:60]}...')
        cursor.execute(stmt)
    
    conn.commit()
    
    # 验证
    print('\n=== 验证结果 ===')
    
    cursor.execute("SHOW TABLES LIKE 'asset_%'")
    print('\n资产相关表:')
    for row in cursor.fetchall():
        print(f'  {row[0]}')
    
    cursor.execute("SELECT status, COUNT(*) FROM assets GROUP BY status")
    print('\n状态分布:')
    for row in cursor.fetchall():
        print(f'  {row[0]}: {row[1]}')
    
finally:
    conn.close()