


Here are some notes and comments about the methodology used in this app, and the metrics of the wishlist. 

# General
- The money is all transformed into usd, with the corresponding exchange rate registered by [SOURCE] as declared by the currency converter library. With the maximum exchange rate at 18/03/2025.
- For future pledges, the conversion rate used is the last available.

# Wishlist metrics calculus
## Objectics and Key Results
TODO: define fiscal year as the default option

Consistency cheks: By construction, Total Active Donors should be higher than Total Active Pledges.

## Money Moved
Asume Money Moved (monthly + total YTD) with the counterfactual are the same as the Objective Key Results metrics.

## Pledge Performance


# App
The data is mainly based on dash, dash_bootstrap_components, plotly. 
Has the same color palette as the oficial OFTW webpage.
Uses caching to memoize the data loads.
