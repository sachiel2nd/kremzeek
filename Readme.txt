.exe found in the "executable" folder.
For it to work, the .exe must be copied together with the PNG images next to it.

to create the executable based on the code, Python and PyInstaller need to be installed
Then the following commands need to be executed.
python -m PyInstaller --onefile --name "PrinterAutomation" --hidden-import=cv2 --hidden-import=PIL --hidden-import=numpy --hidden-import=pyautogui --hidden-import=printer_automation_logic --add-data "next_file_template.png:." --add-data "printer_status_template.png:." printer_GUI.py


The logic of the program once "start" is clicked is as follows:

1) Search in the screen, trying to find current selected item + a valid next item in queue, and send current item to print.
2) Wait for a timeout before doing anything else (default 120 seconds)
3) Search in the screen, try to find "ready to print" status. Repeat every 2 seconds until found.
4) Search in the screen, trying to find current selected item + a valid next item in queue
	4a) If found, click the next item in queue and send to print
	4b) If (selection + next item in queu) is not found, scroll down
		4b1) If after scrolling there is still no match, stop the program
5) Go back to step 2


*Because of the logic, the program will fail to send an item if:
-Printer's queue is not on the screen
-Printer's status is not on the screen
-Printer's queue has a single item on it
-Printer's queue requires to scroll at the very start

Library dependencies:
pip install opencv-python
pip install numpy
pip install pyautogui
