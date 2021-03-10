# Stepwise Regression Research

Provides notes on what stepwise regression is & how it could be valuable for this independent study project.

## What is Stepwise Regression?
Stepwise Regression is a method of fitting regression models in which the choice of predictive variables is carried out automatically. Within this procedure, in each step a variable is considered to be added or subtracted from the rest of the explanatory variables, which were selected using some form of previously specified criteria. The model is built by adding or removing predictor variables, usually via a series of F-tests or T-tests.


### How does it work?
According to [statisticshowto.com](https://www.statisticshowto.com/stepwise-regression/), there are two ways by which stepwise regression can be performed:
1. **Start the test with all available predictor variables (the "Backward Method"):** This involves deleting one variable at a time as the regression model progresses. This model should be used if you have a modest number of prediction variables and want to eliminate a few. At each step, the variable with the lowest "F-to-remove" statistic is removed from the model.
2. **Start the test with no predictor variables (the "Forward Method"):** Add one variable at a time as the regression model progresses. This model should be used if you have a large set of predictor variables. The "F-to-add" stat is created using the same steps from the above "Backward" method, but the system will calculate the stats for each variable not in the model instead. The variable with the highest "F-to-add" rating is added to the model.

#### "F-to-remove"
The **"F-to-remove"** statistic mentioned above is calculated as follows:
1. A t-statistic is calculated for the estimated coefficient of each variable in the model.
2. The t-statistic is squared, creating the final "F-to-remove" stat!

### Advantages & Disadvantages of Stepwise Regression
There are a variety of advantages and disadvantages that come with Stepwise regression again according to [statisticshowto.com](https://www.statisticshowto.com/stepwise-regression/).

#### Advantages:
- Can manage large amounts of potential predictor variables, fine-tuning the model to chose the best predictor variables from the available options.
- Faster than other automatic model-selection models.
- Watching the order by which variables are added/removed can provide valuable info about the quality of variables.

#### Disadvantages:
- Oftentimes there are too many potential predictor variables but too little data to estimate coefficients meaningly.
- If two predictor variables in the model are highly correlated, *only one may make it into the model*.
- R-squared values are usuall to high.
- Regression coefficients can be biased and coefficients for other variables are too high.
- Collinearity is usually a major issue: excessive collinearity may cause the program to dump predictor variables into the model.
- Some variables may be removed the model even when they are deemed important to be included.
- etc.

## How can this project use it?
### Python:
### R:
