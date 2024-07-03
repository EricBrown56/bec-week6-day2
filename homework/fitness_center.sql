USE fitness_center;
CREATE DATABASE fitness_center;



CREATE TABLE members (
id INT AUTO_INCREMENT PRIMARY KEY,
member_name VARCHAR(75) NOT NULL,
email VARCHAR(150) NULL
);

CREATE TABLE workout_sessions (
id INT AUTO_INCREMENT PRIMARY KEY,
session_name VARCHAR(50) NOT NULL,
session_time TIME NOT NULL,
session_date DATE NOT NULL,
member_id INT,
FOREIGN KEY (member_id) REFERENCES members(id)
);
DROP TABLE workout_sessions;

INSERT INTO members (member_name, email)
VALUES ('Mark Smith', 'msmith@email.com'),
('Jerry Anderson', 'janderson@smith.com'),
('Eric Brown', 'eric@brown.org'),
('Michael Green', 'mgreen@meangreen.co'),
('Frank Emerson', 'femerson@gmail.com');

INSERT INTO workout_sessions (session_name, session_time, session_date, member_id)
VALUES ('hiit fat burner', ':30', '2024-07-05', 1),
('belly destroyer 5000', '01:30', '2024-07-09', 2),
('hulk arms', ':45', '2024-07-15', 3),
('tree trunk thighs', '01:15', '2024-07-11', 4),
('core focus', '01:00', '2024-07-08', 5);

SELECT * FROM workout_sessions;
SELECT * FROM members;


