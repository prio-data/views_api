# Predicted fatalities, *cm* level, **sb** conflict (sc_cm_sb_main)

## Variable ID
sc_cm_sb_main

## Originating from
Main ensemble model for number of fatalities in state-based conflict at the country-month level of analysis.

## Development ID
fatalities001, please see https://github.com/prio-data/viewsforecasting/blob/main/CHANGELOG.md.

## Outcome
Predicted fatalities per country-month in impending state-based conflict, expressed in natural logged form plus 1 (`ln(fatalities+1)`).

## Type of violence
State-based conflict (**sb**), see https://viewsforecasting.org/methodology/definitions for details.

## Level of analysis
Country-month (*cm*), see https://viewsforecasting.org/methodology/definitions for details.

## Description
Predicted number of fatalities in impending conflict at country-month level of analysis, expressed in natural logged form plus 1 [ln(Y+1)]. The predictions are produced by a genetic ensemble trained for this type of violence and level of analysis. For more information about the ensemble and the current composition of its constituent models (sub-models), please see https://github.com/prio-data/viewsforecasting/blob/main/CHANGELOG.md and https://www.diva-portal.org/smash/get/diva2:1667048/FULLTEXT01.pdf.

# Predicted fatalities, *pgm* level, **sb** conflict (sc_pgm_sb_main)

## Variable ID
sc_pgm_sb_main

## Originating from
Main ensemble model for number of fatalities in state-based conflict at the PRIO-GRID-month level of analysis.

## Development ID
fatalities001, please see https://github.com/prio-data/viewsforecasting/blob/main/CHANGELOG.md.

## Outcome
Predicted fatalities per PRIO-GRID-month in impending state-based conflict, expressed in natural logged form plus 1 (`ln(fatalities+1)`).

## Type of violence
State-based conflict (**sb**), see https://viewsforecasting.org/methodology/definitions for details.

## Level of analysis
PRIO-GRID-month (*pgm*), see https://viewsforecasting.org/methodology/definitions for details.

## Description
Predicted number of fatalities in impending conflict at PRIO-GRID-month level of analysis, expressed in natural logged form plus 1 [ln(Y+1)]. The predictions are produced by an unweighted ensemble trained for this type of violence and level of analysis. For more information about the ensemble and the current composition of its constituent models (sub-models), please see https://github.com/prio-data/viewsforecasting/blob/main/CHANGELOG.md and https://www.diva-portal.org/smash/get/diva2:1667048/FULLTEXT01.pdf.

# Predicted probability of conflict, *cm* level, **sb** conflict (sc_cm_sb_dich_main)

## Variable ID
sc_cm_sb_dich_main

## Originating from
Main ensemble model for number of fatalities in state-based conflict at the country-month level of analysis.

## Development ID
fatalities001, please see https://github.com/prio-data/viewsforecasting/blob/main/CHANGELOG.md.

## Outcome
Dichotomous predictions for the probability of at least 25 BRDs per country-month in impending state-based conflict.

## Type of violence
State-based conflict (**sb**), see https://viewsforecasting.org/methodology/definitions for details.

## Level of analysis
Country-month (*cm*), see https://viewsforecasting.org/methodology/definitions for details.

## Description
Predicted probability of at least 25 battle-related deaths (BRDs) per country-month on a scale from 0 to 1, derived from the country-level ensemble predictions. For more information about the ensemble underlying these predictions (sc_cm_sb_main) and the current composition of its constituent models (sub-models), please see https://github.com/prio-data/viewsforecasting/blob/main/CHANGELOG.md and https://www.diva-portal.org/smash/get/diva2:1667048/FULLTEXT01.pdf.

# Predicted probability of conflict, *pgm* level, **sb** conflict (sc_pgm_sb_dich_main)

## Variable ID
sc_pgm_sb_dich_main

## Originating from
Main ensemble model for number of fatalities in state-based conflict at the PRIO-GRID-month level of analysis.

## Development ID
fatalities001, please see https://github.com/prio-data/viewsforecasting/blob/main/CHANGELOG.md.

## Outcome
Dichotomous predictions for the probability of at least 1 BRD per PRIO-GRID-month in impending state-based conflict.

## Type of violence
State-based conflict (**sb**), see https://viewsforecasting.org/methodology/definitions for details.

## Level of analysis
PRIO-GRID-month (*pgm*), see https://viewsforecasting.org/methodology/definitions for details.

## Description
Predicted probability of at least 1 battle-related death (BRD) per PRIO-GRID-month on a scale from 0 to 1, derived from the PRIO-GRID-level ensemble predictions. For more information about the ensemble underlying these predictions (sc_pgm_sb_main) and the current composition of its constituent models (sub-models), please see https://github.com/prio-data/viewsforecasting/blob/main/CHANGELOG.md and https://www.diva-portal.org/smash/get/diva2:1667048/FULLTEXT01.pdf

# Surrogate model prediction: relative importance of conflict history at *cm* level, **sb** conflict (sc_cm_sb_surrogate_ch)

## Variable ID
sc_cm_sb_surrogate_ch

## Development ID
fatalities001, please see https://github.com/prio-data/viewsforecasting/blob/main/CHANGELOG.md.

## Outcome
Predicted fatalities in state-based conflict per country-month, given the history of state-based conflict in the country at hand. Expressed in natural logged form plus 1 (`ln(fatalities+1)`).

## Type of violence
State-based conflict (**sb**), see https://viewsforecasting.org/methodology/definitions for details.

## Level of analysis
Country-month (*cm*), see https://viewsforecasting.org/methodology/definitions for details.

## Description
Predicted fatalities in state-based conflict per country-month, given the history of state-based conflict (as recorded by the UCDP GED datasets) in the country at hand. Expressed as natural log(fatalities+1). The prediction is generated by a ‘surrogate’/interpretation model that shows how much of the main VIEWS conflict prediction can be related to variable `ln_ged_sb_dep` — in practice, a regression model with the main prediction as the dependent variable and a flexible function of `ln_ged_sb_dep` as the independent one. The surrogate model results should be seen as an indication of the relative importance of specific independent variables (predictors), rather than point predictions of their own – they do not sum up to the point predictions from the main ensemble model. To learn more about the surrogate models, please see https://www.diva-portal.org/smash/get/diva2:1667048/FULLTEXT01.pdf

# Surrogate model prediction: relative importance of liberal democracy at *cm* level, **sb** conflict (sc_cm_sb_surrogate_dem)

## Variable ID
sc_cm_sb_surrogate_dem

## Development ID
fatalities001, please see https://github.com/prio-data/viewsforecasting/blob/main/CHANGELOG.md.

## Outcome
Predicted fatalities in state-based conflict per country-month, given the liberal democracy index in the country at hand. Expressed in natural logged form plus 1 (`ln(fatalities+1)`).

## Type of violence
State-based conflict (**sb**), see https://viewsforecasting.org/methodology/definitions for details.

## Level of analysis
Country-month (*cm*), see https://viewsforecasting.org/methodology/definitions for details.

## Description
Predicted fatalities in state-based conflict per country-month, given the liberal democracy index (as coded by V-Dem) in the country at hand. Expressed as natural log(fatalities+1). The prediction is generated by a ‘surrogate’/interpretation model that shows how much of the main VIEWS conflict prediction can be related to variable `vdem_v2x_libdem` — in practice, a regression model with the main prediction as the dependent variable and a flexible function of `vdem_v2x_libdem` as the independent one. The surrogate model results should be seen as an indication of the relative importance of specific independent variables (predictors), rather than point predictions of their own – they do not sum up to the point predictions from the main ensemble model. To learn more about the surrogate models, please see https://www.diva-portal.org/smash/get/diva2:1667048/FULLTEXT01.pdf


# Surrogate model prediction: relative importance of population size at *cm* level, **sb** conflict (sc_cm_sb_surrogate_pop)

## Variable ID
sc_cm_sb_surrogate_pop

## Development ID
fatalities001, please see https://github.com/prio-data/viewsforecasting/blob/main/CHANGELOG.md.

## Outcome
Predicted fatalities in state-based conflict per country-month, given the population size in the country at hand. Expressed in natural logged form plus 1 (`ln(fatalities+1)`).

## Type of violence
State-based conflict (**sb**), see https://viewsforecasting.org/methodology/definitions for details.

## Level of analysis
Country-month (*cm*), see https://viewsforecasting.org/methodology/definitions for details.

## Description
Predicted fatalities in state-based conflict per country-month, given the population size in the country at hand. Expressed as natural log(fatalities+1). The prediction is generated by a ‘surrogate’/interpretation model that shows how much of the main VIEWS conflict prediction can be related to variable `wdi_sp_pop_totl` — in practice, a regression model with the main prediction as the dependent variable and a flexible function of `wdi_sp_pop_totl` as the independent one. The surrogate model results should be seen as an indication of the relative importance of specific independent variables (predictors), rather than point predictions of their own – they do not sum up to the point predictions from the main ensemble model. To learn more about the surrogate models, please see https://www.diva-portal.org/smash/get/diva2:1667048/FULLTEXT01.pdf


# Surrogate model prediction: relative importance of infant mortality rate at *cm* level, **sb** conflict (sc_cm_sb_surrogate_imr)

## Variable ID
sc_cm_sb_surrogate_imr

## Development ID
fatalities001, please see https://github.com/prio-data/viewsforecasting/blob/main/CHANGELOG.md.

## Outcome
Predicted fatalities in state-based conflict per country-month, given the infant mortality rate in the country at hand. Expressed in natural logged form plus 1 (`ln(fatalities+1)`).

## Type of violence
State-based conflict (**sb**), see https://viewsforecasting.org/methodology/definitions for details.

## Level of analysis
Country-month (*cm*), see https://viewsforecasting.org/methodology/definitions for details.

## Description
Predicted fatalities in state-based conflict per country-month, given the infant mortality rate in the country at hand. Expressed as natural log(fatalities+1). The prediction is generated by a ‘surrogate’/interpretation model that shows how much of the main VIEWS conflict prediction can be related to variable `wdi_sp_dyn_imrt_in` — in practice, a regression model with the main prediction as the dependent variable and a flexible function of `wdi_sp_dyn_imrt_in` as the independent one. The surrogate model results should be seen as an indication of the relative importance of specific independent variables (predictors), rather than point predictions of their own – they do not sum up to the point predictions from the main ensemble model. To learn more about the surrogate models, please see https://www.diva-portal.org/smash/get/diva2:1667048/FULLTEXT01.pdf

# Surrogate model prediction: relative importance of neighborhood conflict history at *cm* level, **sb** conflict (sc_cm_sb_surrogate_nch)

## Variable ID
sc_cm_sb_surrogate_nch

## Development ID
fatalities001, please see https://github.com/prio-data/viewsforecasting/blob/main/CHANGELOG.md.

## Outcome
Predicted fatalities in state-based conflict per country-month, given the neighborhood conflict history in the country at hand. Expressed in natural logged form plus 1 (`ln(fatalities+1)`).

## Type of violence
State-based conflict (**sb**), see https://viewsforecasting.org/methodology/definitions for details.

## Level of analysis
Country-month (*cm*), see https://viewsforecasting.org/methodology/definitions for details.

## Description
Predicted fatalities in state-based conflict per country-month, given the neighborhood conflict history in the country at hand. Expressed as natural log(fatalities+1). The prediction is generated by a ‘surrogate’/interpretation model that shows how much of the main VIEWS conflict prediction can be related to variable `splag_1_decay_ged_sb_5` — in practice, a regression model with the main prediction as the dependent variable and a flexible function of `splag_1_decay_ged_sb_5` as the independent one. The surrogate model results should be seen as an indication of the relative importance of specific independent variables (predictors), rather than point predictions of their own – they do not sum up to the point predictions from the main ensemble model. To learn more about the surrogate models, please see https://www.diva-portal.org/smash/get/diva2:1667048/FULLTEXT01.pdf

# Surrogate model prediction: relative importance of the 'conflict and conflict shock' media topic at *cm* level, **sb** conflict (sc_cm_sb_surrogate_topic10)

## Variable ID
sc_cm_sb_surrogate_topic10

## Development ID
fatalities001, please see https://github.com/prio-data/viewsforecasting/blob/main/CHANGELOG.md.

## Outcome
Predicted fatalities in state-based conflict per country-month, as derived from a content analysis of the 'conflict and conflict shock' topic in news media in the country at hand. Expressed in natural logged form plus 1 (`ln(fatalities+1)`).

## Type of violence
State-based conflict (**sb**), see https://viewsforecasting.org/methodology/definitions for details.

## Level of analysis
Country-month (*cm*), see https://viewsforecasting.org/methodology/definitions for details.

## Description
Predicted fatalities in state-based conflict per country-month, as derived from a content analysis of the 'conflict and conflict shock' topic in news media. Expressed as natural log(fatalities+1). The prediction is generated by a ‘surrogate’/interpretation model that shows how much of the main VIEWS conflict prediction can be related to variable `ste_theta10` and `ste_theta10_stock` — in practice, a regression model with the main prediction as the dependent variable and a flexible function of `ste_theta10` and `ste_theta10_stock` as the independent one. The surrogate model results should be seen as an indication of the relative importance of specific independent variables (predictors), rather than point predictions of their own – they do not sum up to the point predictions from the main ensemble model. To learn more about the surrogate models, please see https://www.diva-portal.org/smash/get/diva2:1667048/FULLTEXT01.pdf
