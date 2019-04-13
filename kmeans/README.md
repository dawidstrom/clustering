## K-means clustering
Classifies datapoints into k clusters based on the euclidean distance between
point and each cluster center. A point belongs to the closest cluster.

As a standalone program it takes an image as input and produces an image using
only the clustered image colors. 

## Requirements
* python3
* Pillow
* Matplotlib

## Usage:
1. Run `pip install -r requirements.txt`
3. Run `python3 kmeans.py` for help.
2. Run `python3 kmeans.py image.jpg` to process ´image.jpg´
