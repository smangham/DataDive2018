=======================
FAIRSHARE DATADIVE 2018
=======================

-----------
Question 1:
-----------
_What are the most common client groups, projects natures and member services of FareShare’s charity members as listed in the GLADYS warehouse system?_

question1.py attempts to answer this. It produces 6 plots: 'client_group', 'project_nature' and 'member_service' in normal and 'perc' versions.
They present the total count of each of the top 10, and a percentage version. The following settings can be changed at the top of the file:
*top_n*: This is the top N groups/natures/services to be plotted on the graph. Currently 10.
*text_size*: The text size for the labels.
*wrap_length*: The number of letters to wrap each label on.

The columns used and plot labels can be changed in the 'simple_histogram()' calls at the end of the file.

-----------
Question 2:
-----------
_Can we use this information (and possibly other variables) from the GLADYS warehouse system to define meaningful clusters of similar charities?_

question2.py attempts to answer this. It produces 
