# Query-Optimization-using-TLBO-algorithm
In the code section,the order of execution and  the functionalities of each of the files is as follows:
1. DB_util2 : is used to extract the commands from database_latest.sql file and move it to the database (database2_new) created using sqlite3
2. Database2: the extracted commands are executed in sqlite3 database
3. cost_calc2 : calculation of QAC, QLC and LPC to be given as inout to TLBO
4. TLBO : Teacher Learner Based Optimization

Distributed Query Processing Plans generation using Teacher Learner.pdf is the base paper we have refered to
and report gives further explantion to understand the code
