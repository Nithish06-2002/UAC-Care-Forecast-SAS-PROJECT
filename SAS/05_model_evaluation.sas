/* FORECAST ACCURACY */


proc arima data=uac_sorted;
identify var=HHS_Care_num(1);
estimate p=1 q=1;

forecast lead=30
         back=30
         out=forecast_eval;
run;

data accuracy;
    set forecast_eval;

    error     = HHS_Care_num - forecast;
    abs_error = abs(error);
    sq_error  = error**2;
run;

proc means data=accuracy mean;
var abs_error sq_error;
run;
