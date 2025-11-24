create database Visitor_management_db;
use Visitor_management_db;

create table Visitors(
VID int primary key,
v_name varchar(30),
contact char(10),
no_of_visits int,
is_frequent boolean
);

create table Residents(
RID int primary key,
r_name varchar(30),
flat_no int,
is_primary boolean,
email varchar(30),
contact char(10), 
move_in_date date,
emergency_contact char(10)
);
ALTER TABLE Residents
ADD COLUMN password VARCHAR(255) NOT NULL;

create table Flats(
flat_no int primary key,
floor_no int,
block int,
intercom int,
is_occupied boolean
);

create table SecurityGuards(
GID int primary key,
g_name varchar(30),
contact char(10),
shift_start timestamp,
shift_end timestamp,
is_active Boolean,
assigned_block int
);
ALTER TABLE securityguards
ADD COLUMN gua_password VARCHAR(255) NOT NULL;

create table EntryExitLogs(
log_id int primary key auto_increment,
visitor_name varchar(30),
visitor_contact char(10),
flat_no int, 
purpose varchar(30),
entry_time datetime,
exit_time datetime,
entry_gate int,
exit_gate int,
verified_by_guard int
);


alter table EntryExitLogs add foreign key(verified_by_guard) references SecurityGuards(GID);
alter table EntryExitLogs add foreign key(flat_no) references Flats(flat_no);
alter table Residents add foreign key(flat_no) references Flats(flat_no);

CREATE TABLE fixed_visitors (
    fix_visitor_id INT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    visitor_type ENUM('Maid','Tutor','Driver','Cook','Gardener','Milkman','Newspaper Vendor','Other') NOT NULL,
    gender ENUM('Male','Female','Other'),
    phone_number VARCHAR(15) NOT NULL,
    alt_phone_number VARCHAR(15),
    address VARCHAR(255),
    assigned_house_id INT,
    allowed_days VARCHAR(50),
    allowed_time_start TIME,
    allowed_time_end TIME,
    date_registered DATE DEFAULT (CURDATE()),
    status ENUM('Active','Inactive','Blacklisted') DEFAULT 'Active',
    remarks VARCHAR(255),
    FOREIGN KEY (assigned_house_id) REFERENCES Flats(flat_no)
);

DELIMITER $$
CREATE PROCEDURE emergency_lookup(
    IN incident_time DATETIME,
    IN flat_number INT
)
BEGIN
    SELECT 
        e.visitor_name,
        e.visitor_contact,
        e.flat_no,
        e.purpose,
        e.entry_time,
        e.exit_time,
        CASE 
            WHEN e.exit_time IS NULL THEN 'Still Inside'
            WHEN e.exit_time > incident_time THEN 'Inside During Incident'
            WHEN e.exit_time < incident_time THEN 'Already Left'
            ELSE 'Unknown'
        END AS visitor_status,
        g.g_name AS verified_guard,
        g.contact AS guard_contact
    FROM EntryExitLogs e
    LEFT JOIN SecurityGuards g ON e.verified_by_guard = g.GID
    WHERE 
        e.flat_no = flat_number
        AND (
            (e.entry_time <= incident_time AND (e.exit_time IS NULL OR e.exit_time >= incident_time))
            OR ABS(TIMESTAMPDIFF(MINUTE, e.entry_time, incident_time)) <= 30
        )
    ORDER BY e.entry_time DESC;
END$$
DELIMITER ;

DELIMITER $$
CREATE TRIGGER check_flat_occupied
BEFORE INSERT ON EntryExitLogs
FOR EACH ROW
BEGIN
    DECLARE flat_status BOOLEAN;
    SELECT is_occupied INTO flat_status
    FROM Flats
    WHERE flat_no = NEW.flat_no;
    IF flat_status IS NULL THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error: Flat number not found.';
    ELSEIF flat_status = FALSE THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error: Flat is unoccupied. Entry not allowed.';
    END IF;
END$$
DELIMITER ;

-- table was altered for easier VID generation..
ALTER TABLE Visitors 
MODIFY VID INT AUTO_INCREMENT PRIMARY KEY;

--deleting the temp function and trigger : add_new_visitor / update_new_visitor


DELIMITER $$
CREATE PROCEDURE UPDATEEXIT(IN visi_name varchar(30) , IN visi_contact varchar(10) ,IN exit_g int)
BEGIN
IF EXISTS(
SELECT 1 FROM EntryExitLogs WHERE visitor_name = visi_name 
AND visitor_contact = visi_contact
AND exit_time IS NULL
AND DATE(entry_time) = CURDATE()
) THEN
UPDATE EntryExitLogs SET exit_time=NOW(), exit_gate=exit_g WHERE visitor_name=visi_name AND visitor_contact=visi_contact AND DATE(entry_time)=CURDATE();
ELSE
		SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = "WARNING! NO ACTIVE ENTRY FOUND FOR THIS VISITOR TODAY";
END IF;
END$$
DELIMITER ;
