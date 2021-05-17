library(tidyverse)
library(caret)
library(leaps)
library(MASS)

nhl_data = read.csv("nhl-stats.csv", header = TRUE)
# Fit the full model 
full.model <- lm(nhl_data)

# Stepwise regression model
step.model <- stepAIC(full.model, direction = "both", 
                      trace = FALSE)
summary(step.model)

models <- regsubsets(Fertility~., data = swiss, nvmax = 5,
                     method = "seqrep")
summary(models)

# Set seed for reproducibility
set.seed(123)
# Set up repeated k-fold cross-validation
train.control <- trainControl(method = "cv", number = 10)
# Train the model
step.model <- train(Fertility ~., data = swiss, method = "leapBackward", tuneGrid = data.frame(nvmax = 1:5), trControl = train.control)

step.model$results

step.model$bestTune

summary(step.model$finalModel)

coef(step.model$finalModel, 4)

lm(Fertility ~ Agriculture + Education + Catholic + Infant.Mortality, 
   data = swiss)

