
 /* DATA IMPORT */

proc import
    datafile="data/HHS_UAC_Program.csv"
    out=PROJECT_HEALTHCARE
    dbms=csv
    replace;
    getnames=yes;
run;

/* Preview */
proc print data=PROJECT_HEALTHCARE(obs=20);
run;

proc contents data=PROJECT_HEALTHCARE;
run;
