
/* ARIMA FORECAST MODEL */


/* Identification */
proc arima data=uac_sorted;
identify var=HHS_Care_num(1);
run;

/* Estimation */
proc arima data=uac_sorted;
identify var=HHS_Care_num(1);
estimate p=1 q=1;
run;

/* Forecast */
proc arima data=uac_sorted;
identify var=HHS_Care_num(1);
estimate p=1 q=1;

forecast lead=30
         out=forecast_30days;
run;
quit;
