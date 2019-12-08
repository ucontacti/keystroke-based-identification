# keystroke-based-identification
This is the script to collect and authenticate using keystroke patterns.  
This code is a cooperation between Saleh Daghigh and Mahdi Paktinat under  
supervision of Dr. Michael Mock from Fraunhofer Institute.

To run:
1) If you have docker:
    ?) sudo docker build -t ucontacti/key-stroke:latest .  
    ?) sudo docker run -p 5000:5000 -it ucontacti/key-stroke

2) If you want to use the python directly,
    1) Make sure you are using python 3.6 or above  
    2) pip install -r requirements.txt  
    3) python app.py  

Either way, the web page is accessible from localhost:5000
