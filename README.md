FAIRSHARE DATADIVE 2018
=======================
INSTALLATION
------------
These scripts are written in Python 3. Use pip to install the file _requirements.txt_ as
    pip install -r requirements.txt

Place the data files _gladys.txt_, _survey.txt_ and the modified cluster file _gladys_with_cluster_names.txt_ in the same file as the code.

USAGE
-----
Run the scripts using python as
    python question1.py
    python question2.py
    python question3.py

Question 1:
^^^^^^^^^^^
_What are the most common client groups, projects natures and member services of FareShare’s charity members as listed in the GLADYS warehouse system?_

question1.py attempts to answer this. It produces 6 plots: 'client_group', 'project_nature' and 'member_service' in normal and 'perc' versions.
They present the total count of each of the top 10, and a percentage version. The following settings can be changed at the top of the file:
*top_n*: This is the top N groups/natures/services to be plotted on the graph. Currently 10.
*text_size*: The text size for the labels.
*wrap_length*: The number of letters to wrap each label on.

The columns used and plot labels can be changed in the 'simple_histogram()' calls at the end of the file.

Question 2:
^^^^^^^^^^^
_Can we use this information (and possibly other variables) from the GLADYS warehouse system to define meaningful clusters of similar charities?_

question2.py attempts to answer this. It produces 2d histograms of the client groups, project natures and member services- showing both raw counts (map_??.png), and the 'Cramer's V' values for each (map_??\_cramer.png). Cramer's V describes whether or not a given combination is more likely than chance or less likely. 0 means 'If all pairings were random, this is what we'd expect', 1 means 'This pairing *always* occurs together'. They use the same settings variables as question 1 to tweak the output plots.

Question 3:
^^^^^^^^^^^
_Do charities that are similar (e.g. in the same cluster from question 2) indicate similar food requirements in the survey (i.e. in the ‘ideal usage frequency’ questions)?_

question3.py attempts to answer this. It combines the clustered Gladys warehouse file produced by 


FAQ
---
_Why did you write your own histogram? Why not use numpy?_

Because under time pressure I apparently revert to being a FORTRAN/C programmer and writing everything in terms of array indexes.
