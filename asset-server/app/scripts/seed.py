"""
数据库初始化与种子数据脚本
运行: python -m app.scripts.seed
"""

from app.db.session import SessionLocal
from app.db.base import Base
from app.db.session import engine
from app.core.security import hash_password
from app.models.user import User
from app.models.category import Category
from app.models.asset import Asset
from app.models.record import AssetRecord
from app.models.asset_borrow_record import AssetBorrowRecord
from datetime import date


def init_db():
    """创建所有表"""
    Base.metadata.create_all(bind=engine)
    print("数据库表创建成功")


def seed_data():
    """插入演示数据"""
    db = SessionLocal()
    
    try:
        # 清空现有数据
        db.query(AssetRecord).delete()
        db.query(Asset).delete()
        db.query(Category).delete()
        db.query(User).delete()
        db.commit()
        
        # 创建管理员用户
        admin = User(
            username="admin",
            password=hash_password("admin123"),
            real_name="系统管理员",
            role="admin",
            status=1,
        )
        db.add(admin)
        
        # 创建普通用户
        user1 = User(
            username="zhangsan",
            password=hash_password("123456"),
            real_name="张三",
            role="user",
            status=1,
            department="技术部",
        )
        db.add(user1)
        
        user2 = User(
            username="lisi",
            password=hash_password("123456"),
            real_name="李四",
            role="user",
            status=1,
            department="财务部",
        )
        db.add(user2)
        
        db.flush()
        
        # 创建资产分类（一级扁平）
        cat_names = [
            ("电子设备", "ELEC"),
            ("办公家具", "FURN"),
            ("服务器设备", "SERVER"),
            ("网络设备", "NET"),
            ("其他设备", "OTHER"),
        ]
        cats = {}
        for i, (name, code) in enumerate(cat_names):
            cat = Category(name=name, code=code, parent_id=0, sort_order=i + 1)
            db.add(cat)
            db.flush()
            cats[code] = cat

        # 创建资产（混合状态）
        assets_data = [
            # 在库 normal
            ("AST20260001", "联想ThinkPad X1 Carbon", "ELEC", user1.id, "A栋3楼技术部", "normal", 12999.00, "高性能商务笔记本"),
            ("AST20260002", "戴尔PowerEdge R750", "SERVER", None, "数据中心A区", "normal", 89000.00, "2U机架式服务器"),
            ("AST20260003", "华为S6730交换机", "NET", None, "网络机房", "normal", 35000.00, "48口万兆交换机"),
            ("AST20260004", "施乐V180打印机", "OTHER", None, "A栋2楼文印室", "normal", 12800.00, "彩色生产型打印机"),
            ("AST20260005", "MacBook Pro 16寸", "ELEC", None, "仓库B区", "normal", 24999.00, "M3 Max/36GB/1TB"),
            ("AST20260006", "Herman Miller Aeron", "FURN", user2.id, "B栋2楼财务部", "normal", 8900.00, "人体工学椅旗舰款"),
            ("AST20260007", "Steelcase升降桌", "FURN", None, "C栋1楼行政部", "normal", 6200.00, "电动升降办公桌"),
            # 已借出 borrowed
            ("AST20260008", "iPad Pro 12.9寸", "ELEC", user1.id, "A栋3楼技术部", "borrowed", 10999.00, "M2芯片/256GB"),
            ("AST20260009", "戴尔U3223QE显示器", "ELEC", user2.id, "B栋2楼财务部", "borrowed", 5499.00, "32寸4K USB-C显示器"),
            ("AST20260010", "思科C9300交换机", "NET", user1.id, "网络机房", "borrowed", 42000.00, "企业级核心交换机"),
            ("AST20260011", "佳能R5相机", "OTHER", user2.id, "A栋1楼宣传部", "borrowed", 25999.00, "全画幅微单相机"),
            # 已报废 scrapped
            ("AST20260012", "旧联想T480", "ELEC", None, "报废仓库", "scrapped", 0.00, "已过保报废"),
            ("AST20260013", "旧打印机HP1020", "OTHER", None, "报废仓库", "scrapped", 0.00, "报废/无法维修"),
        ]

        assets = []
        for (code, name, cat_code, uid, loc, status, price, desc) in assets_data:
            a = Asset(
                asset_code=code,
                name=name,
                category_id=cats[cat_code].id,
                user_id=uid,
                location=loc,
                status=status,
                price=price,
                description=desc,
                company_code=f"CORP-{code[-3:]}",
                sn=f"SN{code[-5:]}",
            )
            db.add(a)
            assets.append(a)
        
        for asset in assets:
            db.add(asset)
        
        db.flush()

        # 为已借出设备创建出借记录
        today = date.today()
        borrows = [
            (assets[7], user1, "A栋3楼"),
            (assets[8], user2, "B栋2楼"),
            (assets[9], user1, "网络机房"),
            (assets[10], user2, "A栋1楼"),
        ]
        for a, u, loc in borrows:
            db.add(AssetBorrowRecord(
                asset_id=a.id, borrower=u.real_name, department=u.department,
                borrow_date=today, status="borrowed", location=loc,
            ))

        # 创建操作记录
        record_data = [
            (assets[0].id, user1.id, "create", "资产入库：联想ThinkPad X1 Carbon", "系统管理员"),
            (assets[1].id, None, "create", "资产入库：戴尔PowerEdge R750", "系统管理员"),
            (assets[2].id, None, "create", "资产入库：华为S6730交换机", "系统管理员"),
            (assets[3].id, None, "create", "资产入库：施乐V180打印机", "系统管理员"),
            (assets[4].id, None, "create", "资产入库：MacBook Pro 16寸", "系统管理员"),
            (assets[5].id, user2.id, "create", "资产入库：Herman Miller Aeron", "系统管理员"),
            (assets[5].id, user2.id, "assign", "资产领用：Herman Miller Aeron", "系统管理员"),
            (assets[6].id, None, "create", "资产入库：Steelcase升降桌", "系统管理员"),
            (assets[7].id, user1.id, "create", "资产入库：iPad Pro 12.9寸", "系统管理员"),
            (assets[7].id, user1.id, "borrow", "设备出借：iPad Pro 12.9寸", "系统管理员"),
            (assets[8].id, user2.id, "create", "资产入库：戴尔U3223QE显示器", "系统管理员"),
            (assets[8].id, user2.id, "borrow", "设备出借：戴尔U3223QE显示器", "系统管理员"),
            (assets[9].id, user1.id, "create", "资产入库：思科C9300交换机", "系统管理员"),
            (assets[9].id, user1.id, "borrow", "设备出借：思科C9300交换机", "系统管理员"),
            (assets[10].id, user2.id, "create", "资产入库：佳能R5相机", "系统管理员"),
            (assets[10].id, user2.id, "borrow", "设备出借：佳能R5相机", "系统管理员"),
            (assets[11].id, None, "create", "资产入库：旧联想T480", "系统管理员"),
            (assets[11].id, None, "scrap", "设备报废：旧联想T480", "系统管理员"),
            (assets[12].id, None, "create", "资产入库：旧打印机HP1020", "系统管理员"),
            (assets[12].id, None, "scrap", "设备报废：旧打印机HP1020", "系统管理员"),
        ]
        for (aid, uid, rtype, desc, op) in record_data:
            db.add(AssetRecord(asset_id=aid, user_id=uid, type=rtype, description=desc, operator=op))
        
        db.commit()
        print("种子数据插入成功！")
        print("\n演示账号信息：")
        print("  管理员: admin / admin123")
        print("  用户1: zhangsan / 123456")
        print("  用户2: lisi / 123456")
        
    except Exception as e:
        db.rollback()
        print(f"种子数据插入失败: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    init_db()
    seed_data()