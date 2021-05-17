head(mtcars)
head(formatted.nhl.stats)

#define intercept-only model
#formatted.nhl.stats
#> formatted_nhl_full_stats <- read.csv("~/cs590s2021/nhlStatisticProjections/src/formatted_nhl_full_stats.csv", row.names=1)
#>   View(formatted_nhl_full_stats)

intercept_only <- lm(PTS ~ 1, data=formatted_nhl_full_stats)

#define model with all predictors
all <- lm(PTS ~ .,data=formatted_nhl_full_stats)

#perform forward stepwise regression
forward <- step(intercept_only, direction='forward', scope=formula(all), trace=0)

#view results of forward stepwise regression
forward$anova

forward$coefficients

