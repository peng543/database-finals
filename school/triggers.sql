DELIMITER $$

CREATE TRIGGER trg_update_tuition_payment
AFTER INSERT ON PAYMENT
FOR EACH ROW
BEGIN
    DECLARE total_paid DECIMAL(10,2);
    DECLARE total_fee DECIMAL(10,2);

    SELECT SUM(amount) INTO total_paid 
    FROM PAYMENT 
    WHERE fee_id = NEW.fee_id;

    SELECT total_amount INTO total_fee
    FROM TUITION_FEE
    WHERE fee_id = NEW.fee_id;

    UPDATE TUITION_FEE
    SET amount_paid = total_paid,
        payment_status = CASE 
            WHEN total_paid >= total_fee THEN 'Fully Paid'
            WHEN total_paid > 0 THEN 'Partially Paid'
            ELSE 'Unpaid'
        END
    WHERE fee_id = NEW.fee_id;
END$$

DELIMITER ;


