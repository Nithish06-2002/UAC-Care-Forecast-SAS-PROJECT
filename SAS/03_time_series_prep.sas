
 /* TIME SERIES PREPARATION */

proc sort data=uac_final
          out=uac_sorted;
by Date_only;
run;

proc timeseries data=uac_sorted
    plots=(series);
    id Date_only interval=day;
    var HHS_Care_num;
run;
