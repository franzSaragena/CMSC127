-- Create the database
CREATE DATABASE IF NOT EXISTS student_org_db;
USE student_org_db;

-- Create student table
CREATE TABLE IF NOT EXISTS student (
    student_no INT(9) NOT NULL PRIMARY KEY,
    first_name VARCHAR(30) NOT NULL,
    last_name VARCHAR(30) NOT NULL,
    gender VARCHAR(6) NOT NULL,
    degree_program VARCHAR(4) NOT NULL
);

-- Create organization table
CREATE TABLE IF NOT EXISTS organization (
    org_name VARCHAR(100) NOT NULL PRIMARY KEY
);

-- Create membership table
CREATE TABLE IF NOT EXISTS membership (
    student_no INT(9) NOT NULL,
    org_name VARCHAR(100) NOT NULL,
    acad_year CHAR(9) NOT NULL,
    semester INT(1) NOT NULL,
    role VARCHAR(50) NOT NULL,
    committee VARCHAR(100) NOT NULL,
    batch INT(4) NOT NULL,
    membership_status VARCHAR(9) NOT NULL,
    CONSTRAINT membership_student_no_fk 
        FOREIGN KEY(student_no) 
        REFERENCES student(student_no)
        ON UPDATE CASCADE 
        ON DELETE CASCADE,
    CONSTRAINT membership_org_name_fk 
        FOREIGN KEY(org_name) 
        REFERENCES organization(org_name)
        ON UPDATE CASCADE 
        ON DELETE CASCADE,
    PRIMARY KEY(student_no, org_name, acad_year, semester, role, committee, batch, membership_status)
);

-- Create fee table
CREATE TABLE IF NOT EXISTS fee (
    fee_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    student_no INT(9) NOT NULL,
    org_name VARCHAR(100) NOT NULL,
    amount_due DECIMAL(5,2) NOT NULL,
    due_date DATE NOT NULL,
    fee_semester INT(1) NOT NULL,
    is_fully_paid BOOLEAN GENERATED ALWAYS AS (amount_paid = amount_due) STORED,
    amount_paid DECIMAL(5,2) NOT NULL DEFAULT 0,
    payment_date DATE DEFAULT NULL,
    CONSTRAINT fee_student_org_fk 
        FOREIGN KEY(student_no, org_name) 
        REFERENCES membership(student_no, org_name)
        ON UPDATE CASCADE 
        ON DELETE CASCADE
);

-- Insert dummy organizations
INSERT INTO organization (org_name) VALUES
('UP ACM'),
('UP CS Club'),
('UP Math Circle');

-- Insert dummy students
INSERT INTO student (student_no, first_name, last_name, gender, degree_program) VALUES
(1, 'Juan', 'Dela Cruz', 'M', 'BSCS'),
(2, 'Maria', 'Santos', 'F', 'BSIT'),
(3, 'Pedro', 'Reyes', 'M', 'BSCS');

-- Insert dummy memberships
INSERT INTO membership (student_no, org_name, acad_year, semester, role, committee, batch, membership_status) VALUES
(1, 'UP ACM', '2024-2025', 1, 'Member', 'Logistics', 2022, 'Active'),
(1, 'UP CS Club', '2024-2025', 1, 'Secretary', 'Events', 2022, 'Active'),
(2, 'UP ACM', '2024-2025', 1, 'Treasurer', 'Finance', 2022, 'Active'),
(3, 'UP Math Circle', '2024-2025', 1, 'Member', 'Academic', 2021, 'Active');

-- Insert dummy fees
INSERT INTO fee (student_no, org_name, amount_due, due_date, fee_semester, amount_paid, payment_date) VALUES
(1, 'UP ACM', 100.00, '2025-01-10', 1, 100.00, '2025-01-09'),
(1, 'UP CS Club', 150.00, '2025-01-10', 1, 50.00, NULL),
(2, 'UP ACM', 120.00, '2025-01-10', 1, 120.00, '2025-01-10'),
(3, 'UP Math Circle', 90.00, '2025-01-10', 1, 90.00, '2025-01-08');