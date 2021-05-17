head(mtcars)
head(formatted.nhl.stats)

#define intercept-only model
intercept_only <- lm(data=formatted.nhl.stats)

#define model with all predictors
all <- lm(data=formatted.nhl.stats)

#perform forward stepwise regression
forward <- step(intercept_only, direction='both', scope=formula(all), trace=0)

#view results of forward stepwise regression
forward$anova

forward$coefficients

