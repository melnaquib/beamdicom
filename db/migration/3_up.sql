ALTER  TABLE "study" ADD COLUMN 	`patient_id`	TEXT;
ALTER  TABLE "serie" ADD COLUMN 	`study_iuid`	TEXT;
ALTER  TABLE "sop" ADD COLUMN 	`series_iuid`	TEXT;
