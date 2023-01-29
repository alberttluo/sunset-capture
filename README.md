# Automatic Sunset Capture
Python code running on Raspberry Pi to automatically capture the sunset daily, getting the sunset time from the internet.

## Getting Started

### Enable Camera
```
sudo raspi-config
```
Select Interface and Enable Legacy Camera

### Install Libraries
Install the required libraries listed in ```requirements.txt```
```
sudo apt install python3-pip
pip install opencv-python
pip install schedule
pip install suntime
```
### Auto-Run Program on Start-Up
To run the program once system is turned on, run the following code in your terminal
```
vi .profile
```
Then go to the last line and add
```
cd SunsetProject/sunset-capture
source venv/bin/activate
python sunsetcap.py &
```

## Sample Images After HDR Imaging
![image](pictures/sunset.jpg)
