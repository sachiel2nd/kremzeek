import pyautogui
import time
import numpy as np
from PIL import ImageGrab
import cv2


class AutomationFramework:
    def __init__(self):
        self.page_counter= 0
        self.delay_seconds = 2
        #myprint("created")


    def press_key(self):
        try:
            pyautogui.moveTo(100, 600, duration=1)
            pyautogui.click()
            pyautogui.mouseDown()
            pyautogui.moveTo(100, 700, duration=1)
            pyautogui.mouseUp()
           
        except Exception as e:
            self.myprint(f"Error: {e}")

    def send_to_print(self):
        pyautogui.keyDown('alt')
        pyautogui.write("j")
        pyautogui.keyUp('alt')
        pyautogui.press('p')
        pyautogui.press('enter')  ## only for testing purposes, delete in production
        print("job sent - waiting delay before next item")
        time.sleep(self.delay_seconds)

    def check_printer_status(self):     #####################   pending
        result = cv2.matchTemplate(self.screenshot, self.printer_status_img, cv2.TM_CCORR_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        if max_val > 0.999:
            print("printer is ready")
            return True
        else:
            print("printer ready status not found")
        return False

    def get_current_file_position(self):    #####################   pending
        result = cv2.matchTemplate(self.screenshot, self.next_file_img, cv2.TM_CCORR_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        if max_val > 0.999:
            self.current_file_position = [max_loc[0]+30,max_loc[1]+12]
            self.next_file_position = [max_loc[0]+30,max_loc[1]+24]
        else:
            print("no next file in queu found!")
            self.current_file_position = self.next_file_position
            self.next_file_position = [0,0]
        print(max_val)
        print(self.current_file_position)
        print(self.next_file_position)
        return

    def is_running_dummy(self):
        return(True)

    def main_logic(self,is_running_check, delay_sec):
        print("starting main logic")
        pyautogui.PAUSE = 0.3
        pyautogui.FAILSAFE = True
        self.delay_seconds = delay_sec
        time.sleep(1)
        
        self.is_first_file = True
        self.current_file_position = [0,0]        
        self.next_file_position = [0,0]
        
        self.is_printer_ready = False
        print("getting comparing files")
        self.next_file_img = cv2.imread('next_file_template.png',cv2.IMREAD_COLOR)
        self.printer_status_img = cv2.imread('printer_status_template.png',cv2.IMREAD_COLOR)

        print("ready for main loop")
        while (is_running_check()== True):
            # get screenshot, check versaworks  
            # if check_versaworks(picture) = False: break
            #get positions for current file, next file, read printer status and read scroll bar
            self.screenshot = cv2.cvtColor(np.array(ImageGrab.grab()), cv2.COLOR_RGB2BGR) 
            
            self.is_printer_ready=self.check_printer_status()
            #self.get_current_file_position()
            
            #print(self.current_file_position)
            #print(self.next_file_position)
            
            if self.is_printer_ready== False:
                time.sleep(0.5)
            else:
                self.get_current_file_position()

                if self.is_first_file == True and self.current_file_position != [0,0]:
                    self.is_first_file = False
                    ## move to the already selected file and send to print
                    #dummy logic
                    print("sending first value in queu")
                    pyautogui.moveTo(self.current_file_position[0],self.current_file_position[1],duration=0.5)
                    pyautogui.click()
                    self.send_to_print()
                 
                elif self.next_file_position != [0,0] :
                    print("sending next file in queu")
                    pyautogui.moveTo(self.next_file_position[0],self.next_file_position[1],duration=0.5)
                    pyautogui.click()
                    self.send_to_print()
    
                elif self.current_file_position != [0,0]:
                    print("attempting to scroll")
                    pyautogui.moveTo(self.current_file_position[0],self.current_file_position[1],duration=0.5)
                    pyautogui.click()
                    the_before_image = ImageGrab.grab()
                    pyautogui.scroll(-1)
                    time.sleep(0.1)
                    the_after_image = ImageGrab.grab()
                    if the_before_image == the_after_image:
                        the_after_image.save("unable_to_scroll_screenshot.png")
                        print("scrolling failed; stopping")
                        break
                    print("scrolling succeeded, continuing")
                    
                else: break
            time.sleep(1)  
        return()

def main():
    automation1 = AutomationFramework()
    automation1.main_logic(automation1.is_running_dummy,2)


    
    print("done!")
    
 

    

    
# min_val, max_val, min_loc, max_loc
if __name__ == "__main__":
    main()



#versaworks#                -10435984.0 8657769.0 (576, 742) (294, 160)
#geany#                     -11529466.0 4178019.5 (709, 742) (79, 174)
#versaworksPartial#         -10430428.0 8657769.0 (429, 742) (294, 160)
#                           -11418606.0 11223933.0 (709, 742) (835, 720)
# logic : press alt + j; P

# wait for printer to be ready
#--------------------------------
# Is there a next file?
   #yes: click next file, send to print then wait state
   #no: Is there a scroll bar and it is not on the buttom?
        #yes: move the mouse to the selection; scroll down; return to next file check
        #no: finish execution   
# click next file, loop again
