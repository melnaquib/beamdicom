CREATE TABLE IF NOT EXISTS `study` (
	`study_iuid`	TEXT UNIQUE,
	`datetime`	DATE,
	`accession_no`	INTEGER,
	`patient_id`	TEXT,
	`status`	INT,
	`thumbnail`	BLOB,
	`update_timestamp`	INTEGER,
	`to_image`	INTEGER DEFAULT 0,
	`to_pacs`	INTEGER DEFAULT 0,
	`workflow_phase`	INTEGER DEFAULT 0,
	`referring_physician`	TEXT,
	`id`	INTEGER PRIMARY KEY AUTOINCREMENT
);
CREATE TABLE IF NOT EXISTS `sop` (
	`sop_iuid`	TEXT UNIQUE,
	`instance_no`	INTEGER,
	`series_iuid`	TEXT
);
CREATE TABLE IF NOT EXISTS `serie` (
	`series_iuid`	TEXT UNIQUE,
	`series_no`	INTEGER,
	`modality`	TEXT,
	`study_iuid`	TEXT
);
CREATE TABLE IF NOT EXISTS `routes` (
	`id`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`referring_physician`	TEXT,
	`address`	TEXT,
	`port`	INTEGER,
	`aet`	TEXT
);
CREATE TABLE IF NOT EXISTS `patient` (
	`patient_id`	TEXT UNIQUE,
	`name`	TEXT,
	`dob`	DATE,
	`gender`	CHAR
);
