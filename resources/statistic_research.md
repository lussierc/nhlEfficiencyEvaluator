# NHL Statistic Research

Provides basic notes on the major variables currently used to track NHL statistics and predict future outcomes.

View the Glossary of Hockey Statistics [here](https://www.hockey-reference.com/about/glossary.html). It describes all widely used statistics.

## Research-Identified Key Stats
Will need to do some actual research in this area quickly though off the top my head I am thinking:
- Goals
- Assists
- (Points)
- +/-
- SOG
- ATOI (Average Time on Ice)
- Salary

## Ways to Scrape NHL Statistics
There are a variety of libraries that make it easy to scrape NHL statistical data. One library I found previously is in *Python* and is called `nhlscrapi`. [This library](https://pythonhosted.org/nhlscrapi/) accesses "NHL game data including play-by-play, game summaries, player stats, etc". The library hides the backend of the NHL website scraping process and gathers data with ease.

In *R*, there is a widely used package called `nhlscrapr` that could be used in correlation with a Stepwise Regression implementation in R if that is the route I chose to take.
