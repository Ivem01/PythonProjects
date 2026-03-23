import pandas as pd
import matplotlib.pyplot as plt

def load_data():
    data = pd.read_csv("music-analysis/spotify-tracks-dataset.csv")

    data = data.drop(columns=["Unnamed: 0", "Unnamed: 0.1"])

    return data

data = load_data()

average_tempo = data["tempo"].mean()

average_popularity = data["popularity"].mean()

duration = data["duration_ms"] / 60000
average_duration = duration.mean()

average_energy = data["energy"].mean()

average_loudness = data["loudness"].mean()

print(f"""
Average tempo: {average_tempo:.2f} BPM
Average popularity: {average_popularity:.2f}
Average duration: {average_duration:.2f} minutes
Average energy: {average_energy:.2f}
Average loudness: {average_loudness:.2f} dB
""")

def tempo_distribution_hist(data):
    plt.hist(data["tempo"], bins=50)
    plt.title("Tempo Distribution")
    plt.xlabel("Tempo (BPM)")
    plt.ylabel("Number of Songs")
    plt.grid(True)

    plt.show()

def danceability_genre_barchart(data):
    dance_genre = data.groupby("track_genre")["danceability"].mean()

    top_dance_genre = dance_genre.sort_values(ascending=False).head(10)

    plt.barh(top_dance_genre.index, top_dance_genre.values)
    plt.title("Top 10 Genres by Average Danceability")
    plt.xlabel("Average Danceability")
    plt.ylabel("Genre")

    plt.gca().invert_yaxis()
    plt.show()

def popularity_piechart(data):
    data["popularity_group"] = data["popularity"].apply(lambda x: "Low" if x < 30 else "Medium" if x < 70 else "High")
    
    counts = data["popularity_group"].value_counts()
    
    plt.pie(counts.values,labels=counts.index, autopct='%1.1f%%')
    plt.title("Songs by Popularity Level")
    plt.show()

popularity_piechart(data)
tempo_distribution_hist(data)
danceability_genre_barchart(data)
