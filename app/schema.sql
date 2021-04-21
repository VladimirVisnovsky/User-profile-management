CREATE TABLE user (
    id VARCHAR PRIMARY KEY,
    first_name VARCHAR NOT NULL,
    second_name VARCHAR NOT NULL,
    email VARCHAR UNIQUE NOT NULL,
    ui_lang VARCHAR NOT NULL,
    ui_settings VARCHAR NOT NULL,
    employee_account BOOLEAN NOT NULL,
    access_rights VARCHAR NOT NULL,
    logon_status INTEGER NOT NULL,
    logon_last_modif DATETIME NOT NULL,
);

-- CREATE TABLE user (id VARCHAR PRIMARY KEY,first_name VARCHAR NOT NULL,second_name VARCHAR NOT NULL,email VARCHAR UNIQUE NOT NULL,ui_lang VARCHAR NOT NULL,ui_settings VARCHAR NOT NULL,employee_account BOOLEAN NOT NULL,access_rights VARCHAR NOT NULL,logon_status INTEGER NOT NULL,logon_last_modif DATETIME NOT NULL);


