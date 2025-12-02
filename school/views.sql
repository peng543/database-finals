CREATE VIEW v_students_by_program AS
SELECT 
    p.program_id,
    p.program_name,
    s.student_id,
    s.full_name AS student_name,
    s.enrollment_year
FROM STUDENT s
JOIN PROGRAM p ON s.program_id = p.program_id;

CREATE VIEW v_outstanding_tuition AS
SELECT 
    s.student_id,
    s.full_name AS student_name,
    t.academic_year,
    t.semester,
    t.total_amount,
    t.amount_paid,
    (t.total_amount - t.amount_paid) AS remaining_amount
FROM TUITION_FEE t
JOIN STUDENT s ON s.student_id = t.student_id
WHERE t.total_amount > t.amount_paid;

CREATE VIEW v_course_performance AS
SELECT 
    c.course_id,
    c.course_name,
    AVG(e.grade) AS avg_grade,
    COALESCE(SUM(CASE WHEN e.grade >= 50 THEN 1 ELSE 0 END) / NULLIF(COUNT(e.student_id),0) * 100, 0) AS pass_rate
FROM COURSE c
LEFT JOIN ENROLLMENT e ON c.course_id = e.course_id
GROUP BY c.course_id, c.course_name;

