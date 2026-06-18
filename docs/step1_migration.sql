-- ============================================
-- 第二轮 Step 1: 数据库调整
-- 执行顺序: 建表 → 建表 → 状态迁移
-- ============================================

-- 1. 创建资产出借记录表
CREATE TABLE IF NOT EXISTS asset_borrow_record (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键',
    asset_id INT NOT NULL COMMENT '资产ID',
    borrower VARCHAR(50) NOT NULL COMMENT '借用人',
    department VARCHAR(100) NULL COMMENT '借用人部门',
    borrow_date DATE NOT NULL COMMENT '借出日期',
    expected_return_date DATE NULL COMMENT '预计归还日期',
    actual_return_date DATE NULL COMMENT '实际归还日期',
    status VARCHAR(20) NOT NULL DEFAULT 'borrowed' COMMENT '状态: borrowed/returned',
    remark TEXT NULL COMMENT '备注',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX idx_asset_id (asset_id),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='资产出借记录';

-- 2. 创建资产变动记录表
CREATE TABLE IF NOT EXISTS asset_change_record (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键',
    asset_id INT NOT NULL COMMENT '资产ID',
    change_type VARCHAR(20) NOT NULL COMMENT '变动类型: owner/dept/location/category',
    old_value VARCHAR(200) NULL COMMENT '旧值',
    new_value VARCHAR(200) NOT NULL COMMENT '新值',
    operator VARCHAR(50) NOT NULL COMMENT '操作人',
    remark TEXT NULL COMMENT '备注',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX idx_asset_id (asset_id),
    INDEX idx_change_type (change_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='资产变动记录';

-- 3. 状态迁移 (enabled → normal, disabled → scrapped)
UPDATE assets SET status = 'normal' WHERE status = 'enabled';
UPDATE assets SET status = 'scrapped' WHERE status = 'disabled';

-- ============================================
-- 验证
-- ============================================
-- SHOW TABLES LIKE 'asset_%';
-- SELECT status, COUNT(*) FROM assets GROUP BY status;
