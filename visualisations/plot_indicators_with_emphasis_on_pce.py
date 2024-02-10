import matplotlib.pyplot as plt


def plot_indicators_with_emphasis_on_pce(df, columns):
    plt.figure(figsize=(15, 7))

    # Calculate 4-month moving averages for all columns in df
    df_ma = df.rolling(window=4).mean()

    # Extracting top features excluding 'PCE'
    top_features = [feature for feature in columns if feature != "PCE"]

    # Plotting other indicators with lesser opacity using a lighter shade of red
    for feature in top_features:
        plt.plot(df_ma.index, df_ma[feature], label=f"{feature} vs. PCE", color="dodgerblue", linewidth=1, alpha=0.2)  # Lighter red with opacity
    
    # Plotting 'PCE' with more prominence
    plt.plot(df_ma.index, df_ma['PCE'], label="PCE", color="#FF7F50", linewidth=2, alpha=1)  # Bright red, no opacity

    # Styling
    plt.title("All Indicators Against PCE (4-Month Moving Average)", fontsize=16)
    plt.xlabel("Date", fontsize=10,color='grey')
    plt.ylabel("Value", fontsize=10,color='grey')
    plt.xticks(df_ma.index[::20], fontsize=10, rotation=45,color='grey')  # Adjust for visibility
    plt.yticks(fontsize=10,color='grey')
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.tight_layout()

    # Enhancing visual appeal by adjusting spines and ticks
    ax = plt.gca()  # Get current axis
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_color('gray')
    ax.spines['bottom'].set_linestyle('--')
    ax.spines['left'].set_color('gray')
    ax.spines['left'].set_linestyle('--')
    
    #remove grid
    ax.grid(False)
    
    #make y and x axis labels and title grey
    ax.yaxis.label.set_color('grey')
    ax.xaxis.label.set_color('grey')

    #set y-axis range
    plt.ylim(-20, 20)

    plt.show()