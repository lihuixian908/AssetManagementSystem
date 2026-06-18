ALTER TABLE assets ADD COLUMN company_code VARCHAR(100) NULL COMMENT '公司编号';
ALTER TABLE assets ADD COLUMN sn VARCHAR(100) NULL COMMENT 'SN号';
ALTER TABLE assets ADD INDEX idx_company_code (company_code);
ALTER TABLE assets ADD INDEX idx_sn (sn);
