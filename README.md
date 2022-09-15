# Return To Learn Dashboard Date Updater
## Overview
The [UC San Diego COVID-19 Daily Dashboard](https://returntolearn.ucsd.edu/dashboard/index.html) provides various campus related COVID-19 data. A part of which is the Potential Exposure Locations table which maintained by the EH&S team. The table lists the locations and dates that COVID-19 positive individuals were present at within the last 14 days. All dates are manually entered and removed.
## Objective
Automate the removing of dates older than 14 days and archive them correctly.
## Motivation
There is currently, a near 500 locations in the table and it takes a significant amount of time to go through and check that all dates are in the 14-day period. Because of this, it is done infrequently and the table is full of old dates. 
## Learning and Practical Focuses
* Python unittest
* Modular Programming
* Self explanitory code
* Simple logging and nested exceptions
* Creating Python executables
* Python annotations
## Instructions
1. Download the dist folder.
1. Paste the "On-site infectivity dates" column into current_date.txt.
1. Paste the "Older Dates" column into archived_dates.txt.
1. Run date_updater.
1. Check log.txt to see all the errors that need to be fixed.
1. Fix errors.
1. Repeat running date_updater and fixing errors until there are none.
1. Paste content of current_dates_updated.txt into the "On-site infectivity dates" column.
1. Paste content of archived_dates_updated.txt into the "Older Dates" column.
## Notes to User
* The dist folder contains the executable file.
* User must have personal access to RTL table.
* Dates must be in mm/dd/yy format.
* Dates are to be separated by commas.
* Date ranges (1/2/3 - 1/20/3) are not valid.
* Folder and file names cannot be changed.
* No need to manually add dates to the Older Dates column, this will do it for you.
## Before
![Before](./Pictures/Before.png)
## After
![After](./Pictures/After.png)