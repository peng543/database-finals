CREATE DATABASE IF NOT EXISTS StudentManagement CHARACTER SET utf8mb4 COLLATE
utf8mb4_unicode_ci;
USE StudentManagement;

CREATE TABLE PROGRAM (
    program_id       INT PRIMARY KEY AUTO_INCREMENT,
    program_name     VARCHAR(100) NOT NULL,
    department       VARCHAR(100) NOT NULL,
    duration_years   INT CHECK (duration_years > 0),
    degree_type      ENUM('Bachelor', 'Master', 'PhD')
);

CREATE TABLE STUDENT (
    student_id       INT PRIMARY KEY AUTO_INCREMENT,
    full_name        VARCHAR(100) NOT NULL,
    date_of_birth    DATE NOT NULL,
    gender           ENUM('Male', 'Female', 'Other'),
    email            VARCHAR(100) UNIQUE NOT NULL,
    phone_number     VARCHAR(20),
    address          VARCHAR(255),
    program_id       INT NOT NULL,
    enrollment_year  INT CHECK (enrollment_year >= 1990),

    FOREIGN KEY (program_id) REFERENCES PROGRAM(program_id)
);

CREATE TABLE INSTRUCTOR (
    instructor_id    INT PRIMARY KEY AUTO_INCREMENT,
    full_name        VARCHAR(100) NOT NULL,
    email            VARCHAR(100) UNIQUE NOT NULL,
    specialization   VARCHAR(100),
    office_location  VARCHAR(50)
);

CREATE TABLE COURSE (
    course_id        INT PRIMARY KEY AUTO_INCREMENT,
    course_name      VARCHAR(100) NOT NULL,
    credit_hours     INT CHECK (credit_hours > 0),
    semester_offered ENUM('Spring', 'Summer', 'Fall'),
    program_id       INT NOT NULL,

    FOREIGN KEY (program_id) REFERENCES PROGRAM(program_id)
);

CREATE TABLE ENROLLMENT (
    enrollment_id    INT PRIMARY KEY AUTO_INCREMENT,
    student_id       INT NOT NULL,
    course_id        INT NOT NULL,
    semester         ENUM('Spring', 'Summer', 'Fall', 'Winter'),
    academic_year    VARCHAR(9) NOT NULL,
    grade            VARCHAR(2),
    status           ENUM('Enrolled', 'Completed', 'Withdrawn'),

    FOREIGN KEY (student_id) REFERENCES STUDENT(student_id),
    FOREIGN KEY (course_id) REFERENCES COURSE(course_id)
);

CREATE TABLE TUITION_FEE (
    fee_id           INT PRIMARY KEY AUTO_INCREMENT,
    student_id       INT NOT NULL,
    academic_year    VARCHAR(9) NOT NULL,
    semester         ENUM('Spring', 'Summer', 'Fall'),
    total_amount     DECIMAL(10,2) NOT NULL CHECK (total_amount >= 0),
    amount_paid      DECIMAL(10,2) DEFAULT 0 CHECK (amount_paid >= 0),
    payment_status   ENUM('Unpaid', 'Partially Paid', 'Fully Paid'),

    FOREIGN KEY (student_id) REFERENCES STUDENT(student_id)
);

CREATE TABLE ADVISOR_ASSIGNMENT (
    assignment_id    INT PRIMARY KEY AUTO_INCREMENT,
    instructor_id    INT NOT NULL,
    student_id       INT NOT NULL,
    assigned_date    DATE NOT NULL,

    FOREIGN KEY (instructor_id) REFERENCES INSTRUCTOR(instructor_id),
    FOREIGN KEY (student_id) REFERENCES STUDENT(student_id)
);

CREATE TABLE PAYMENT (
	payment_id		 INT PRIMARY KEY AUTO_INCREMENT,
    fee_id			 INT NOT NULL,
    payment_date 	 DATE NOT NULL,
    payment_method   ENUM('Cash', 'Bank', 'Transfer', 'Card'),
    amount 			 INT,
    remarks			 VARCHAR(255),
    
    FOREIGN KEY (fee_id) REFERENCES TUITION_FEE(fee_id)
    );

    
    
    
    
    




