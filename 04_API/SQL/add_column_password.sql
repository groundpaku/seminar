ALTER TABLE m010_student
ADD COLUMN password_hash VARCHAR(255)
NOT NULL DEFAULT '';

COMMENT ON COLUMN m010_student.password_hash IS 'bcrypt等でハッシュ化したパスワード';