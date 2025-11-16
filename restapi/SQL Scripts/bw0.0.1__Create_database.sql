-- CREATE DATABASE budgetwallet;

--######################################################################################################################
-- TABLES
--######################################################################################################################
CREATE TABLE "user" (
    id SERIAL PRIMARY KEY,
    username VARCHAR(16) NOT NULL,
    password TEXT NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT FALSE,
    is_admin BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT (now() AT TIME ZONE 'UTC'),
    updated_at TIMESTAMP NOT NULL DEFAULT (now() AT TIME ZONE 'UTC'),
    CONSTRAINT UQ_user_username UNIQUE (username)
);

CREATE TABLE "wallet" (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    icon_path TEXT,
    color_hex VARCHAR(7),
    created_at TIMESTAMP NOT NULL DEFAULT (now() AT TIME ZONE 'UTC'),
    updated_at TIMESTAMP NOT NULL DEFAULT (now() AT TIME ZONE 'UTC'),
    user_id INTEGER NOT NULL, -- Owner
    CONSTRAINT FK_wallet_user_id FOREIGN KEY (user_id) REFERENCES "user" (id)
);

CREATE TABLE "budget" (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    icon_name TEXT,
    color_hex VARCHAR(7),
    is_permanent BOOLEAN DEFAULT FALSE, -- only deletes when wallet is deleted
    created_at TIMESTAMP NOT NULL DEFAULT (now() AT TIME ZONE 'UTC'),
    updated_at TIMESTAMP NOT NULL DEFAULT (now() AT TIME ZONE 'UTC'),
    wallet_id INTEGER NOT NULL,
    CONSTRAINT FK_budget_wallet_id FOREIGN KEY (wallet_id) REFERENCES "wallet" (id)
);

CREATE TABLE "movement_category" (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    color_hex VARCHAR(7)
);

CREATE TABLE "movement" (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    amount REAL NOT NULL,
    is_deposit BOOLEAN NOT NULL, -- if TRUE is money IN if FALSE is money OUT
    is_manual BOOLEAN NOT NULL, -- if TRUE means that is a management type movement (fix the actual balance)
    done_at TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT (now() AT TIME ZONE 'UTC'),
    updated_at TIMESTAMP NOT NULL DEFAULT (now() AT TIME ZONE 'UTC'),
    budget_id INTEGER NOT NULL,
    CONSTRAINT FK_movement_budget_id FOREIGN KEY (budget_id) REFERENCES "budget" (id),
    category_id INTEGER,
    CONSTRAINT FK_movement_movementCategory_id FOREIGN KEY (category_id) REFERENCES "movement_category" (id)
);

--######################################################################################################################
-- TRIGGERS
--######################################################################################################################
CREATE OR REPLACE FUNCTION create_default_budget()
RETURNS TRIGGER AS $$
BEGIN
   INSERT INTO "budget" (name, description, is_permanent, icon_name, wallet_id)
   VALUES ('Money', 'Default budget, where you money uncategorized is stored. This budget cannot be deleted', TRUE, 'money', NEW.id);

   RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER TRG_AI_Wallet
AFTER INSERT ON "wallet"
FOR EACH ROW
EXECUTE FUNCTION create_default_budget();

--######################################################################################################################
-- Default data
--######################################################################################################################
INSERT INTO "user" (username, password, is_active)
VALUES ('dev', '$argon2id$v=19$m=16,t=4,p=1$cXlxUWFxc2hmWXVQYmdrdQ$a/pIKF1sqjISk0pGkQWM8+/iR1J0jRN7WdBOAwrh9gw', True);