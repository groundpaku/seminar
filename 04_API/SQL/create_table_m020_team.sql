CREATE TABLE m020_team (
    team_cd        VARCHAR(2)  PRIMARY KEY,
    delete_flg     VARCHAR(1)  NOT NULL DEFAULT '0',
    create_date    TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP,
    update_date    TIMESTAMP,
    team_name      VARCHAR(20) NOT NULL
);

COMMENT ON TABLE m020_team IS '部署マスタ';
COMMENT ON COLUMN m020_team.team_cd IS '部署コード';
COMMENT ON COLUMN m020_team.delete_flg IS '0:有効 1:論理削除';
COMMENT ON COLUMN m020_team.create_date IS '作成日時';
COMMENT ON COLUMN m020_team.update_date IS '更新日時';
COMMENT ON COLUMN m020_team.team_name IS '部署名';

GRANT ALL ON m020_team TO api_user01;
