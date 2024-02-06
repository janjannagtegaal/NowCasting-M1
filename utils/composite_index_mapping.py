####################################################################################################
###Labor Market indices to be used in the composite index

composite_indices_info = {
    "Primary_Sector_Employment": (["All Employees: Mining and Logging: Mining"], "sum"),
    "Secondary_Sector_Employment": (
        [
            "All Employees: Construction",
            "All Employees: Durable goods",
            "All Employees: Nondurable goods",
            "All Employees: Manufacturing",
        ],
        "sum",
    ),
    "Tertiary_Sector_Employment": (
        [
            "All Employees: Financial Activities",
            "All Employees: Retail Trade",
            "All Employees: Service-Providing Industries",
            "All Employees: Trade, Transportation & Utilities",
            "All Employees: Wholesale Trade",
        ],
        "sum",
    ),
    "Public_Sector_Employment": (["All Employees: Government"], "sum"),
    "Avg_Hourly_Earnings_Employment": (
        [
            "Avg Hourly Earnings : Construction",
            "Avg Hourly Earnings : Goods-Producing",
            "Avg Hourly Earnings : Manufacturing",
        ],
        "mean",
    ),
    "Avg_weekly_hours_Employment": (
        [
            # "Avg Weekly Overtime Hours : Manufacturing",
            "Avg Weekly Hours : Goods-Producing",
            "Avg Weekly Hours : Manufacturing",
        ],
        "mean",
    ),
}

####################################################################################################

####Output and Income Indices
ip_indices = {
    "Output: Consumer_Goods_Index": (
        [
            "IP: Consumer Goods",
            "IP: Durable Consumer Goods",
            "IP: Nondurable Consumer Goods",
        ],
        "sum",
    ),
    "Output_Materials_Index": (
        ["IP: Durable Materials", "IP: Nondurable Materials", "IP: Materials"],
        "sum",
    ),
    "Output_Prod_Equipment_Index": (
        [
            "IP: Business Equipment",
            "IP: Manufacturing (SIC)",
            "IP: Final Products and Nonindustrial Supplies",
        ],
        "sum",
    ),
    "Outpit_Final_Products_Index": (["IP: Final Products (Market Group)"], "sum"),
}

# Update the composite_index dictionary
composite_indices_info.update(ip_indices)

####################################################################################################
####Interest and Exchange Rates
interest_and_exchange_rates = {
    "Short_Term_Rate_Index": (
        [
            "3-Month Treasury Bill:",
            "6-Month Treasury Bill:",
            "3-Month AA Financial Commercial Paper Rate",
        ],
        "mean",
    ),
    "Long_Term_Rate_Index": (
        ["1-Year Treasury Rate", "5-Year Treasury Rate", "10-Year Treasury Rate"],
        "mean",
    ),
    "Spread_Index": (
        [
            "1-Year Treasury C Minus FEDFUNDS",
            "3-Month Treasury C Minus FEDFUNDS",
            "5-Year Treasury C Minus FEDFUNDS",
            "10-Year Treasury C Minus FEDFUNDS",
            "3-Month Commercial Paper Minus FEDFUNDS",
            "6-Month Treasury C Minus FEDFUNDS",
        ],
        "mean",
    ),
    "Credit_Market_Index": (
        [
            # "E?ective Federal Funds Rate",
            "Moody s Aaa Corporate Bond Minus FEDFUNDS",
            "Moody s Baa Corporate Bond Minus FEDFUNDS",
            "Moody s Seasoned Aaa Corporate Bond Yield",
            "Moody s Seasoned Baa Corporate Bond Yield",
        ],
        "mean",
    ),
}

# Update the composite_index dictionary
composite_indices_info.update(interest_and_exchange_rates)

####################################################################################################
### Stock Market
stock_market = {
    "Stock_Market_Performance_Index": (
        [
            "S&P s Common Stock Price Index: Composite",
            "S&P s Common Stock Price Index: Industrials",
        ],
        "mean",
    )
    # 'Stock_Market_Valuation_Index':
    #     (['S&P s Composite Common Stock: Dividend Yield',
    #     'S&P s Composite Common Stock: Price-Earnings Ratio'],
    #     'mean')
}


# Update the composite_index dictionary
composite_indices_info.update(stock_market)

####################################################################################################

### prices

prices = {
    "Consumer_Spending_Index": (
        [
            "Personal Cons. Exp: Durable goods",
            "Personal Cons. Exp: Nondurable goods",
            "Personal Cons. Exp: Services",
        ],
        "sum",
    ),  # or 'mean', if average spending is preferred
    "Producer_Price_Index": (
        [
            "PPI: Crude Materials",
            "PPI: Finished Consumer Goods",
            "PPI: Finished Goods",
            "PPI: Intermediate Materials",
            "PPI: Metals and metal products:",
        ],
        "mean",
    ),  # PPIs typically averaged
}

# Update the composite_index dictionary
composite_indices_info.update(prices)


####################################################################################################
##Money and Credit

money_and_credit_indices = {
    "Consumer_Credit_Index": (
        [
            "Consumer Motor Vehicle Loans Outstanding",
            "Total Consumer Loans and Leases Outstanding",
        ],
        #'Total Nonrevolving Credit'],
        "mean",
    ),
    'Commercial_Credit_Index':
        (['Commercial and Industrial Loans',
        'Real Estate Loans at All Commercial Banks'],
        'mean'),
    'Monetary_Aggregates_Index':
        (['M1 Money Stock',
        'M2 Money Stock'
        ],
        'mean'), #'MZM Money Stock', 'St. Louis Adjusted Monetary Base','Securities in Bank Credit at All Commercial Banks'
}

# Update the composite_index dictionary
composite_indices_info.update(money_and_credit_indices)


# ####################################################################################################
# ### Consumption, Orders, and Inventories

consumption_orders_inventories = {
    # "Consumer_Demand_Composite_Index": (
    #     [
    #         "Real personal consumption expenditures",
    #         "Retail and Food Services Sales",
    #         "Total Business Inventories",
    #     ],
    #     "mean",
    # ),
    "New_Orders_Index": (
        [
            "New Orders for Durable Goods",
            "New Orders for Nondefense Capital Goods",
            "Un lled Orders for Durable Goods",
            "Real Manu. and Trade Industries Sales",
            "New Orders for Consumer Goods",
        ],
        "sum",
    ),
}
composite_indices_info.update(consumption_orders_inventories)

####################################################################################################

# housing_starts_and_permits = {
#     'Housing_Starts_Index':
#         (['Housing Starts, Midwest',
#           'Housing Starts, Northeast',
#           'Housing Starts, South',
#           'Housing Starts, West'],
#          'sum'),

#     'Housing_Permits_Index':
#         (['New Private Housing Permits, Midwest (SAAR)',
#           'New Private Housing Permits, Northeast (SAAR)',
#           'New Private Housing Permits, South (SAAR)',
#           'New Private Housing Permits, West (SAAR)'],
#          'sum')
# }

# composite_indices_info.update(housing_starts_and_permits)

# granular_cpi_data = {
#     # 'CPI_Excluding_Index':
#     #     (['CPI : All Items Less Food',
#     #       'CPI : All items less medical care',
#     #       'CPI : All items less shelter'],
#     #      'mean'),

#     'CPI_Specific_Categories_Index':
#         (['CPI : Apparel',
#           'CPI : Commodities',
#           'CPI : Durables',
#           'CPI : Medical Care',
#           'CPI : Services',
#           'CPI : Transportation'],
#          'mean')
# }

# composite_indices_info.update(granular_cpi_data)

# granular_unemployment_data = {
#     'Unemployment_Duration_Index':
#         (['Civilians Unemployed - 15 Weeks & Over',
#     'Civilians Unemployed - Less Than 5 Weeks',
#     'Civilians Unemployed for 15-26 Weeks',
#     'Civilians Unemployed for 27 Weeks and Over',
#     'Civilians Unemployed for 5-14 Weeks',],
#          'sum'),

# }

# composite_indices_info.update(granular_unemployment_data)
