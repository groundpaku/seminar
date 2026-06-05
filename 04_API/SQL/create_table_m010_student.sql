CREATE TABLE m010_student (
    student_id     INTEGER GENERATED ALWAYS AS IDENTITY
                   PRIMARY KEY,
    delete_flg     VARCHAR(1)  NOT NULL DEFAULT '0',
    create_date    TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP,
    update_date    TIMESTAMP,
    name           VARCHAR(20) NOT NULL,
    name_kana      VARCHAR(20) NOT NULL,
    joining_year   VARCHAR(4)  NOT NULL,
    team_cd        VARCHAR(2)  NOT NULL
);

COMMENT ON TABLE m010_student IS '受講者マスタ';
COMMENT ON COLUMN m010_student.student_id IS '受講者ID';
COMMENT ON COLUMN m010_student.delete_flg IS '0:有効 1:論理削除';
COMMENT ON COLUMN m010_student.create_date IS '作成日時';
COMMENT ON COLUMN m010_student.update_date IS '更新日時';
COMMENT ON COLUMN m010_student.name IS '受講者名';
COMMENT ON COLUMN m010_student.name_kana IS '受講者名かな';
COMMENT ON COLUMN m010_student.joining_year IS '入社年';
COMMENT ON COLUMN m010_student.team_cd IS '所属部コード';

GRANT ALL ON m010_student TO api_user01;