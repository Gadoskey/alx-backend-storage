-- Author: Gadoskey
-- File: 5-valid_email.sql
-- SQL script to create a trigger that resets the valid_email attribute when the email is changed

DELIMITER $$

CREATE TRIGGER reset_valid_email_after_update
BEFORE UPDATE ON users
FOR EACH ROW
BEGIN
    IF NEW.email <> OLD.email THEN
        UPDATE users
        SET valid_email = 0
        WHERE id = NEW.id;
    END IF;
END$$

DELIMITER ;
