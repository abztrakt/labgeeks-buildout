/* This set of queries is used to migrate a labgeeksrpg site from the old structure to our new
structure introduced with making it ready for django 1.4 */


USE labgeeks;
ALTER TABLE chronos_location RENAME TO labgeeks_chronos_location;
ALTER TABLE chronos_location_active_users RENAME TO labgeeks_chronos_location_active_users;
ALTER TABLE chronos_punchclock RENAME TO labgeeks_chronos_punchclock;
ALTER TABLE chronos_shift RENAME TO labgeeks_chronos_shift;
ALTER TABLE labgeeksrpg_config_notification RENAME TO labgeeks_hermes_notification;
ALTER TABLE delphi_answer RENAME TO labgeeks_delphi_answer;
ALTER TABLE delphi_question RENAME TO labgeeks_delphi_question;
ALTER TABLE delphi_question_tags RENAME TO labgeeks_delphi_question_tags;
ALTER TABLE people_employmentstatus RENAME TO labgeeks_people_employmentstatus;
ALTER TABLE people_paygrade RENAME TO labgeeks_people_paygrade;
ALTER TABLE people_performancereview RENAME TO labgeeks_people_performancereview;
ALTER TABLE people_title RENAME TO labgeeks_people_title;
ALTER TABLE people_userprofile RENAME TO labgeeks_people_userprofile;
ALTER TABLE people_userprofile_wage RENAME TO labgeeks_people_userprofile_wage;
ALTER TABLE people_userprofile_working_periods RENAME TO labgeeks_people_userprofile_working_periods;
ALTER TABLE people_uwltreview RENAME TO labgeeks_people_uwltreview;
ALTER TABLE people_uwltreviewweights RENAME TO labgeeks_people_uwltreviewweights;
ALTER TABLE people_wagechangereason RENAME TO labgeeks_people_wagechangereason;
ALTER TABLE people_wagehistory RENAME TO labgeeks_people_wagehistory;
ALTER TABLE people_workgroup RENAME TO labgeeks_people_workgroup;
ALTER TABLE pythia_page RENAME TO labgeeks_pythia_page;
ALTER TABLE pythia_page_tags RENAME TO labgeeks_pythia_page_tags;
ALTER TABLE pythia_revisionhistory RENAME TO labgeeks_pythia_revisionhistory;
ALTER TABLE schedule_baseshift RENAME TO labgeeks_horae_baseshift;
ALTER TABLE schedule_closedhour RENAME TO labgeeks_horae_closedhour;
ALTER TABLE schedule_defaultshift RENAME TO labgeeks_horae_defaultshift;
ALTER TABLE schedule_shifttype RENAME TO labgeeks_horae_shifttype;
ALTER TABLE schedule_shifttype_allowed_groups RENAME TO labgeeks_horae_shifttype_allowed_groups;
ALTER TABLE schedule_timeperiod RENAME TO labgeeks_horae_timeperiod;
ALTER TABLE schedule_workshift RENAME TO labgeeks_horae_workshift;
ALTER TABLE sybil_screenshot RENAME TO labgeeks_sybil_screenshot;
ALTER TABLE sybil_tag RENAME TO labgeeks_sybil_tag;
