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
    user_id INTEGER, -- Who created, null if available for everyone
    CONSTRAINT FK_mvt_userAccount_id FOREIGN KEY (user_id) REFERENCES user_account (id) ON DELETE CASCADE
);

CREATE TABLE movement (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    amount NUMERIC(12, 4) NOT NULL,
    is_deposit BOOLEAN NOT NULL, -- if TRUE is money IN if FALSE is money OUT
    done_at TIMESTAMP NOT NULL DEFAULT (now() AT TIME ZONE 'UTC'),
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


--######################################################################################################################
-- Default data
--######################################################################################################################
INSERT INTO user_account (username, password, is_active)
VALUES ('dev', '$argon2id$v=19$m=16,t=4,p=1$cXlxUWFxc2hmWXVQYmdrdQ$a/pIKF1sqjISk0pGkQWM8+/iR1J0jRN7WdBOAwrh9gw', True);

INSERT INTO movement_category (title, description, color)
VALUES ('Adjustment', 'Movement created to adjust the balance of the budget', '#FFFFFF');

INSERT INTO movement_category (title, description, color)
VALUES ('Income', 'Monthly income', '#FFFFFF');

INSERT INTO movement_category (title, description, color)
VALUES ('Expense', 'General one time expense', '#FFFFFF');

INSERT INTO movement_category (title, description, color)
VALUES ('Recurring', 'Recurring expense', '#FFFFFF');

INSERT INTO movement_category (title, description, color)
VALUES ('Deposit', 'One time deposit', '#FFFFFF');