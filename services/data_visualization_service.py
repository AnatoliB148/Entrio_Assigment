import matplotlib.pyplot as plt
import pandas as pd


def plot_companies_per_city(city_count_df):
    
    threshold=10
    figsize=(12, 6)
    bar_color='skyblue'
    text_color='black'
    # Optional: Aggregate smaller categories
    top_cities = city_count_df.head(threshold)
    others = pd.DataFrame({'city': ['Others'], 'city_count': [city_count_df['city_count'][threshold:].sum()]})
    city_count_df_aggregated = pd.concat([top_cities, others])

    # Plotting the data
    plt.figure(figsize=figsize)
    bars = plt.bar(city_count_df_aggregated['city'], city_count_df_aggregated['city_count'], color=bar_color)
    plt.ylabel('Number of Companies')
    plt.xlabel('City')
    plt.title('Number of Companies per City')
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Adding the count above each bar
    for bar in bars:
        plt.text(
            bar.get_x() + bar.get_width() / 2,  # x-coordinate (center of the bar)
            bar.get_height(),                   # y-coordinate (top of the bar)
            f'{bar.get_height():,}',            # Text to display (formatted count)
            ha='center',                        # Horizontal alignment
            va='bottom',                        # Vertical alignment
            fontsize=10,                        # Font size
            color=text_color                    # Text color
        )

    plt.tight_layout()

    # Show the plot
    plt.show()