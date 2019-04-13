SELECT * FROM boodb.Users;

DELETE FROM `boodb`.`Users`;

# 서울 시간 설정.  
set time_zone = 'Asia/Seoul';


--  댓글을 달면 해당 cmt_count 이 1 증가하는 트리거.

DELIMITER $$

CREATE TRIGGER  tr_cmt_lists AFTER INSERT ON Cmt FOR EACH ROW
BEGIN
		update Lists set cmt_count  = cmt_count + 1 where Cmt.list_id = Lists.list_id;
END$$
DELIMITER ;
