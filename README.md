### Personal Python projects developed in VS Code. 

Please note this page is not about impeccable or professional software development — if it can even be called that. It's about curiosity, experimentation, learning and letting your creativity run free. 🐍

**Various projects that I've developed in Python, including:**

- AI video/image enhancement with open source code Real-ESRGAN (this is ML/DL*).
- Checking if NVIDIA's CUDA is enabled after installation.
- Speech recognition and transcription/translation (PT to EN) (this is ML/DL).
- Automatic creation of subtitle file (.srt) from transcribed/translated audio. [Ana Paula](https://drive.google.com/file/d/1B6sfs_E2MWkTN-DnnCS2a-nTI4polJzJ/view?usp=sharing)
- Upward shifting of speech pitch (baby voice). This is ML/DL.
- Play counts syncing between iTunes and Windows Media Player.
- Moving MP3 files under their right folder and creating complete log files with changes.
- Search, download and attachment of MP3 artwork (Apple or Discogs), with log files creation.
- Image pattern recognition (trying to check if an MP3 cover is a generic vinyl/LP so it can be automatically replaced). This is done by comparing the cover with a given vinyl image (this is ML/DL).
- Searching and populating MP3 tags on the Discogs website automatically.
- Making MP3 tag names in sync with the actual file names (to detect and resolve conflicts)
- Downloading of videos from Youtube (use "YT-DLP CMD LINE.txt" to see command line usage, as Youtube credentials may be needed and are taken from browser cookies). 
- Codes for video download will only work if the video doesn't requires credentials. The command line works always (install module yt-dlp).
- Creation of stand-alone/static executables from Python codes.
- Installed, configured and debugged PySpark on Windows, with Python 3.11.8, Java 11.0 and Hadoop 3.3.5. This will allow me to achieve the below task (free Azure account is constrained).
- Fitting models such as Logistics Regression using PySpark ML for parameter and goodness-of-fit optimization (results below). 
- Fitting ML time series models to stocks, though it's not much use if the market is not stable (in consideration).
- Web scraping of tables on Wikipedia using BeautifulSoup.
- Automatic creation of formatted PPT slides with data scraped from Wikipedia. [Brazilian actresses**](https://drive.google.com/file/d/1l_Zxaq1p-71HO2b6AdjMkAQa74wRyHxH/view?usp=sharing)
- Calling function by passing another function as parameter and feeding variables to it from called function with lambda.
- Image, audio and video processing using ffmpeg.
- Submitting Windows commands from Python.


*ML: Machine Learning.<br>
*DL: Deep Learning.

**Video created from the PPT deck created in Python (soundtrack added with ffmpeg).

**Fitting of a logistics regression with PySpark to a credit risk file available on the internet.**<br>
*It's a credit risk dataset (sometimes called the "Give Me Some Credit" dataset from Kaggle), used for predicting if someone will default on loans.*<br>
The binary response variable is called SeriousDlqin2yrs and indicates whether a given customer became seriously delinquent in a 2-year time horizon (1=Yes, 0=No).

The area under the ROC curve (a measure of the goodness-of-fit of the model) is modest at best:<br>
AUC: 0.687

For the first-time PySpark ML user this can come out as a bit disappointing. They were probably expecting the PySpark ML engine to do more "magic" like automatically selecting the best features, tuning hyperparameters, or trying multiple models to find the absolute best fit all on its own. But it's still just the classic logistics regression, which surprisingly also falls under the umbrella of ML.

Train dataset (80% of the data)
| Actual | Prediction | Count |
|--------|------------|-------|
| 0      | 0          | 89285 |
| 0      | 1          |   191 |
| 1      | 0          |  6407 |
| 1      | 1          |   252 |
| **Total** |            | **96135** |



Test dataset (20% of the data)
| Actual | Prediction | Count |
|--------|------------|-------|
| 0      | 0          | 22384 |
| 0      | 1          |    52 |
| 1      | 0          |  1618 |
| 1      | 1          |    80 |
| **Total** |            | **24134** |
