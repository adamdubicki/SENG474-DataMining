# Travis Torrent Miner

A project that uses machine learning to assess the health of projects in the (travis torrent data)[https://travistorrent.testroots.org/]

# Creating the data for cross validation
In your directory, create 11 csvs. d0.csv -> d9.csv, and output.csv. Then run data_processor.py to fill those csvs with data. After words, adjust log_reg.py to choose your testing and training datasets. 