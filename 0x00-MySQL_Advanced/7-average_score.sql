-- Creates a stored procedure `ComputeAverageScoreForUser` that computes and store the average score for a student.
DROP PROCEDURE IF EXISTS ComputeAverageScoreForUser;
DELIMITER $$
CREATE PROCEDURE ComputeAverageScoreForUser (IN user_id INT)
BEGIN
    DECLARE avg_score FLOAT;
    SELECT AVG(score) INTO avg_score
    FROM corrections
    WHERE user_id = user_id;
    UPDATE users
    SET average_score = COALESCE(avg_score, 0)  -- Use 0 if avg_score is NULL
    WHERE id = user_id;
END $$
DELIMITER ;
