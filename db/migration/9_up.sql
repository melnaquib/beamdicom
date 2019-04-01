CREATE TABLE "study_tmp" (
	`study_iuid`	TEXT UNIQUE ,
	`datetime`	DATE,
	`accession_no`	INTEGER,
	`patient_id`	TEXT,
	`status` INT,
	`thumbnail`	BLOB,
	`update_timestamp` INTEGER,
	`to_image`	INTEGER DEFAULT 0,
	`to_pacs`	INTEGER DEFAULT 0,
	`workflow_phase` 	INTEGER DEFAULT 0,
	`id` INTEGER PRIMARY KEY AUTOINCREMENT
);

INSERT INTO study_tmp
(study_iuid,
datetime,
accession_no,
patient_id,
status,
thumbnail,
update_timestamp,
to_image,
to_pacs,
workflow_phase
)
SELECT 
* FROM study;

DROP TABLE study;
ALTER TABLE study_tmp RENAME TO study;
