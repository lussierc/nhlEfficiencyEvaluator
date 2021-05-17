# Stepwise Regression of NHL Statistics

# Import data:
### NOTE: Edit the path of the CSV document to your own -- if you are using my repo, find the location on your computer:
formatted_nhl_full_stats <- read.csv("~/cs590s2021/nhlStatisticProjections/src/formatted_nhl_full_stats.csv", row.names=1)

# View the imported statistics:
head(formatted_nhl_full_stats)

# Define intercept-only model:
## Use 'PTS' (player points) as the response variable
intercept_only <- lm(PTS ~ 1, data=formatted_nhl_full_stats)

# Define model with all predictors:
## Use 'PTS' (player points) as the response variable
all <- lm(PTS ~ .,data=formatted_nhl_full_stats)

# Perform forward stepwise regression:
forward <- step(intercept_only, direction='forward', scope=formula(all), trace=0)

# View results of forward stepwise regression:
forward$anova

# View the coefficient results of forward stepwise regression:
forward$coefficients
