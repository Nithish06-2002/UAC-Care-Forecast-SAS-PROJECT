/* CAPACITY RISK FLAGGING */


data capacity_risk;
    set forecast_30days;

    if forecast > 3000
    then breach_flag = 1;
    else breach_flag = 0;
run;
