
INSERT INTO Flats (flat_no, floor_no, block, intercom, is_occupied) VALUES
(101, 1, 1, 2101, TRUE), (102, 1, 1, 2102, TRUE), (103, 1, 1, 2103, FALSE),
(201, 2, 1, 2201, TRUE), (202, 2, 1, 2202, TRUE), (203, 2, 1, 2203, FALSE),
(301, 3, 2, 2301, TRUE), (302, 3, 2, 2302, TRUE), (303, 3, 2, 2303, TRUE),
(401, 4, 2, 2401, TRUE), (402, 4, 2, 2402, FALSE), (403, 4, 2, 2403, TRUE),
(501, 5, 3, 2501, TRUE), (502, 5, 3, 2502, TRUE), (503, 5, 3, 2503, TRUE),
(601, 6, 3, 2601, FALSE), (602, 6, 3, 2602, TRUE), (603, 6, 3, 2603, TRUE),
(701, 7, 3, 2701, TRUE), (702, 7, 3, 2702, TRUE);

INSERT INTO Residents (RID, r_name, flat_no, is_primary, email, contact, move_in_date, emergency_contact, password) VALUES
(1, 'Amit Sharma', 101, TRUE, 'amit@example.com', '9876543210', '2023-01-15', '9123456789', 'pass123'),
(2, 'Neha Verma', 102, TRUE, 'neha@example.com', '9876543211', '2023-03-10', '9123456790', 'pass456'),
(3, 'Ravi Singh', 201, TRUE, 'ravi@example.com', '9876543212', '2022-11-05', '9123456791', 'pass789'),
(4, 'Sneha Kapoor', 202, TRUE, 'sneha@example.com', '9876543213', '2023-02-20', '9123456792', 'pass321'),
(5, 'Manoj Joshi', 301, TRUE, 'manoj@example.com', '9876543214', '2023-04-01', '9123456793', 'pass654'),
(6, 'Pooja Rani', 302, TRUE, 'pooja@example.com', '9876543215', '2023-05-12', '9123456794', 'pass987'),
(7, 'Vikram Chauhan', 303, TRUE, 'vikram@example.com', '9876543216', '2023-06-18', '9123456795', 'pass111'),
(8, 'Anjali Mehta', 401, TRUE, 'anjali@example.com', '9876543217', '2023-07-22', '9123456796', 'pass222'),
(9, 'Rohit Das', 403, TRUE, 'rohit@example.com', '9876543218', '2023-08-30', '9123456797', 'pass333'),
(10, 'Kavita Nair', 501, TRUE, 'kavita@example.com', '9876543219', '2023-09-05', '9123456798', 'pass444'),
(11, 'Arjun Rao', 502, TRUE, 'arjun@example.com', '9876543220', '2023-10-10', '9123456799', 'pass555'),
(12, 'Meera Iyer', 503, TRUE, 'meera@example.com', '9876543221', '2023-11-01', '9123456700', 'pass666'),
(13, 'Suresh Patil', 602, TRUE, 'suresh@example.com', '9876543222', '2023-11-10', '9123456701', 'pass777'),
(14, 'Divya Bhatt', 603, TRUE, 'divya@example.com', '9876543223', '2023-11-15', '9123456702', 'pass888'),
(15, 'Nikhil Jain', 701, TRUE, 'nikhil@example.com', '9876543224', '2023-11-17', '9123456703', 'pass999');

INSERT INTO Visitors (VID, v_name, contact, no_of_visits, is_frequent) VALUES
(1, 'Karan Mehta', '8887776660', 5, FALSE),
(2, 'Priya Das', '8887776661', 12, TRUE),
(3, 'Anil Kapoor', '8887776662', 2, FALSE),
(4, 'Ramesh Yadav', '8887776663', 20, TRUE),
(5, 'Snehal Joshi', '8887776664', 1, FALSE);

INSERT INTO SecurityGuards (GID, g_name, contact, shift_start, shift_end, is_active, assigned_block, gua_password) VALUES
(1, 'Rajesh Kumar', '9998887770', '2025-11-17 08:00:00', '2025-11-17 16:00:00', TRUE, 1, 'guardpass1'),
(2, 'Sunita Devi', '9998887771', '2025-11-17 16:00:00', '2025-11-17 00:00:00', TRUE, 2, 'guardpass2'),
(3, 'Mohit Rana', '9998887772', '2025-11-17 00:00:00', '2025-11-17 08:00:00', TRUE, 3, 'guardpass3');

INSERT INTO EntryExitLogs (visitor_name, visitor_contact, flat_no, purpose, entry_time, exit_time, entry_gate, exit_gate, status, verified_by_guard) VALUES
('Karan Mehta', '8887776660', 101, 'Delivery', '2025-11-17 10:00:00', '2025-11-17 10:15:00', 1, 1, 'Normal', 1),
('Priya Das', '8887776661', 102, 'Cleaning', '2025-11-17 09:00:00', '2025-11-17 12:00:00', 2, 2, 'Normal', 2),
('Anil Kapoor', '8887776662', 201, 'Maintenance', '2025-11-17 11:30:00', NULL, 3, NULL, 'Suspicious', 3),
('Ramesh Yadav', '8887776663', 301, 'Milk Delivery', '2025-11-17 06:00:00', '2025-11-17 06:15:00', 1, 1, 'Normal', 1),
('Snehal Joshi', '8887776664', 401, 'Guest Visit', '2025-11-17 18:00:00', '2025-11-17 20:00:00', 2, 2, 'Normal', 2);

INSERT INTO fixed_visitors (fix_visitor_id, full_name, visitor_type, gender, phone_number, alt_phone_number, address, assigned_house_id, allowed_days, allowed_time_start, allowed_time_end, remarks) VALUES
(1, 'Priya Das', 'Maid', 'Female', '8887776661', NULL, 'Sector 12, Noida', 102, 'Mon,Tue,Wed,Thu,Fri', '08:00:00', '12:00:00', 'Trusted maid'),
(2, 'Ramesh Yadav', 'Milkman', 'Male', '8887776663', NULL, 'Sector 15, Noida', 301, 'All', '06:00:00', '07:00:00', 'Daily delivery');

INSERT INTO OverstayNotifications (visitor_name, visitor_contact, flat_no, entry_time, allowed_time_end, notified_guard, message) VALUES
('Anil Kapoor', '8887776662', 201, '2025-11-17 11:30:00', '12:30:00', 3, 'Visitor has not exited beyond allowed time.');