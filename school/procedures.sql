DELIMITER $$

CREATE PROCEDURE sp_register_course(
    IN p_student_id INT,
    IN p_course_id INT,
    IN p_semester ENUM('Fall','Spring','Summer'),
    IN p_academic_year INT
)
BEGIN
    IF EXISTS (
        SELECT 1 FROM ENROLLMENT
        WHERE student_id = p_student_id
        AND course_id = p_course_id
        AND semester = p_semester
        AND academic_year = p_academic_year
    ) THEN
        SELECT 'Error: Student already enrolled in this course.' AS message;
    ELSE
        INSERT INTO ENROLLMENT(student_id, course_id, semester, academic_year)
        VALUES (p_student_id, p_course_id, p_semester, p_academic_year);
        SELECT 'Success: Course registration completed.' AS message;
    END IF;
END$$

DELIMITER ;

DELIMITER $$

CREATE PROCEDURE sp_semester_revenue_report(
    IN p_academic_year INT,
    IN p_semester ENUM('Fall','Spring','Summer')
)
BEGIN
    SELECT 
        p.program_name,
        SUM(tf.amount_paid) AS total_collected
    FROM TUITION_FEE tf
    JOIN STUDENT s ON s.student_id = tf.student_id
    JOIN PROGRAM p ON p.program_id = s.program_id
    WHERE tf.academic_year = p_academic_year
    AND tf.semester = p_semester
    GROUP BY p.program_name;
END$$

DELIMITER ;

