-- CREATE DATABASE budgetwallet;

--######################################################################################################################
-- TABLES
--######################################################################################################################
CREATE TABLE user_account (
    id SERIAL PRIMARY KEY,
    username VARCHAR(16) NOT NULL,
    password TEXT NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT FALSE,
    is_admin BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT (now() AT TIME ZONE 'UTC'),
    updated_at TIMESTAMP NOT NULL DEFAULT (now() AT TIME ZONE 'UTC'),
    CONSTRAINT UQ_userAccount_username UNIQUE (username)
);

CREATE TABLE wallet (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    iconify_name TEXT,
    color VARCHAR(7),
    start_balance REAL NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT (now() AT TIME ZONE 'UTC'),
    updated_at TIMESTAMP NOT NULL DEFAULT (now() AT TIME ZONE 'UTC'),
    user_id INTEGER NOT NULL, -- Owner
    CONSTRAINT FK_wallet_userAccount_id FOREIGN KEY (user_id) REFERENCES user_account (id) ON DELETE CASCADE
);

CREATE TABLE budget (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    iconify_name TEXT,
    color VARCHAR(7),
    is_permanent BOOLEAN DEFAULT FALSE, -- only deletes when wallet is deleted
    created_at TIMESTAMP NOT NULL DEFAULT (now() AT TIME ZONE 'UTC'),
    updated_at TIMESTAMP NOT NULL DEFAULT (now() AT TIME ZONE 'UTC'),
    wallet_id INTEGER NOT NULL,
    CONSTRAINT FK_budget_wallet_id FOREIGN KEY (wallet_id) REFERENCES wallet (id) ON DELETE CASCADE
);

CREATE TABLE movement_category (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    color VARCHAR(7),
    is_system BOOLEAN NOT NULL DEFAULT FALSE -- if set only the admin can edit this records!
);

CREATE TABLE movement (
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
    CONSTRAINT FK_movement_budget_id FOREIGN KEY (budget_id) REFERENCES budget (id) ON DELETE CASCADE,
    category_id INTEGER,
    CONSTRAINT FK_movement_movementCategory_id FOREIGN KEY (category_id) REFERENCES movement_category (id) ON DELETE SET NULL
);

--######################################################################################################################
-- TRIGGERS
--######################################################################################################################
CREATE OR REPLACE FUNCTION create_default_budget()
RETURNS TRIGGER AS $$
DECLARE
    budget_id budget.id%TYPE;
BEGIN
   INSERT INTO budget (name, description, is_permanent, wallet_id)
   VALUES ('Money', 'Default budget, where you money uncategorized is stored. This budget cannot be deleted', TRUE, NEW.id)
   RETURNING id INTO budget_id;

   IF NEW.start_balance <> 0 THEN
       INSERT INTO movement (title, description, amount, is_deposit, is_manual, done_at, budget_id, category_id)
       VALUES ('Start balance (automatic)',
               'This movement represents a movement which is the start money',
               NEW.start_balance,
               true,
               false,
               (now() AT TIME ZONE 'UTC'),
               budget_id,
               1);
   END IF;

   RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER TRG_AI_Wallet
AFTER INSERT ON wallet
FOR EACH ROW
EXECUTE FUNCTION create_default_budget();

--######################################################################################################################
-- Default data
--######################################################################################################################
INSERT INTO user_account (username, password, is_active)
VALUES ('dev', '$argon2id$v=19$m=16,t=4,p=1$cXlxUWFxc2hmWXVQYmdrdQ$a/pIKF1sqjISk0pGkQWM8+/iR1J0jRN7WdBOAwrh9gw', True);

INSERT INTO movement_category (title, description, color, is_system)
VALUES ('SYSTEM', 'Movements made automatically by the system', '#FFFFFF', TRUE);