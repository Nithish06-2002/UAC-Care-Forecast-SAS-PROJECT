/* PDF REPORT GENERATION */


ods pdf file="output/HHS_Forecast_Report.pdf"
        style=HTMLBlue;

title "Predictive Forecasting of Care Load";

/* Historical Trend */
proc sgplot data=uac_sorted;
series x=Date_only y=HHS_Care_num;
run;

/* Forecast Plot */
proc sgplot data=forecast_30days;
series x=Date_only y=forecast;
band x=Date_only lower=l95 upper=u95;
run;

ods pdf close;
