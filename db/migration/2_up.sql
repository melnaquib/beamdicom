CREATE TABLE "patient" (
	`patient_id`	TEXT UNIQUE,
	`name`	TEXT,
	`dob`	DATE,
	`gender`	CHAR
);
CREATE TABLE "study" (
	`study_iuid`	TEXT UNIQUE ,
	`datetime`	DATE,
	`accession_no`	INTEGER
);
CREATE TABLE `serie` (
	`series_iuid`	TEXT UNIQUE,
	`series_no`	INTEGER,
	`modality`	TEXT
);
CREATE TABLE `sop` (
	`sop_iuid`	TEXT UNIQUE,
	`instance_no`	INTEGER
);
