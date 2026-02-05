
/* MACHINE LEARNING – RANDOM FOREST */

data ML_FEATURES;
    set uac_sorted;

    lag1  = lag1(HHS_Care_num);
    lag7  = lag7(HHS_Care_num);
    lag14 = lag14(HHS_Care_num);

    roll7 = mean(lag1, lag7);

    net_flow =
        Children_transferred_out_of_CBP -
        Children_discharged_from_HHS_Car;
run;

/* Train/Test Split */
data TRAIN TEST;
    set ML_FEATURES;

    if _N_ <= 650 then output TRAIN;
    else output TEST;
run;

/* Random Forest */
proc hpforest data=TRAIN;

    target HHS_Care_num;

    input lag1 lag7 lag14 roll7 net_flow
          Children_apprehended_and_placed
          Children_in_CBP_custody
          Children_transferred_out_of_CBP
          Children_discharged_from_HHS_Car;

    score data=TEST
          out=RF_FORECAST;
run;
