# Conversational Chatbot (with AI augmentation)

To deploy the website, first clone this repo, then

0. (optional) Activate virtual environment: for Window
```
python -m venv venv
venv/Scripts/activate.bat
```
or for Linux, create a new `conda` virtual environment.

1. To install all the packages, run
```
pip install -r requirements.txt
```
Disclaimer: If you encounter errors when installing these packages, please remove the determined version (e.g `==x.xx.x`) of the package corresponding to the errors.

2. To run the website, run
```
python app.py
```
![image](https://user-images.githubusercontent.com/30380242/166956340-e293d9e8-6ed4-44ac-be96-060209af78ae.png)

3. Open browser and visit http://127.0.0.1:4651 (local server) or http://\<public-dns>:\<port> (according to input of `port` in `app.py`)

![image](https://user-images.githubusercontent.com/100040846/168464011-fd88dec2-a624-4722-8d20-b4f6a3a6a9e2.png)
![image](https://user-images.githubusercontent.com/30380242/167367734-42c5d252-db9f-481e-8389-f8d5865ce987.png)
![image](https://user-images.githubusercontent.com/30380242/167367810-2da8ecd2-d3dd-4dc5-bf2e-6c3bf9c9f09a.png)

<br><br>
**Remarks:**
* See `Group_Report.pdf` for the details of the project
* See `Data_Analysis.pdf` for the data analyses (using Spark)
* See `Run_demo.ipynb` for the demo output if using a Virtual Machine (e.g. AWS)
* See `Run_demo_colab.ipynb` for how to run it without a VM using Google Colab with Ngrok (recommended)
