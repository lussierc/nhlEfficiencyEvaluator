# Stepwise Regression

This folder contains the code/data related to performing Stepwise Regression on NHL statistics. Stepwise Regression is a method of fitting regression models in which the choice of predictive variables is carried out automatically. Within this procedure, in each step a variable is considered to be added or subtracted from the rest of the explanatory variables, which were selected using some form of previously specified criteria.

## Files
- `stepwise_regression.r`: Contains R code that performs a stepwise regression on NHL stats.
- `formatted_nhl_full_stats.csv`: The data used for stepwise regression. Removes many unneeded statistics, such as duplicate player keys, and statistics that could confuse the model.
- `nhl_full_stats_18-19.csv`: The overall stats from which the formatted ones are derived. Not used in stepwise regression tasks.
