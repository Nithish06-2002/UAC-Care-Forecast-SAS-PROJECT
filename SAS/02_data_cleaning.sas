
/* DATA CLEANING & TYPE CONVERSION */

data uac_clean;
    set PROJECT_HEALTHCARE;

    /* Convert datetime → date */
    Date_only = datepart(Date);
    format Date_only yymmdd10.;

    /* Character → numeric */
    HHS_Care_num =
        input(compress(Children_in_HHS_Care, ','), best12.);
run;

/* Remove missing rows */
data uac_final;
    set uac_clean;

    if Date_only ne .;
    if HHS_Care_num ne .;
run;
