from pynput import keyboard
import os
from RecordClass2 import RecordThread2 
rec = RecordThread2()

def on_press(key):
    try:
        upper_char = key.char.upper()
        # We don't need this
        #if ((ord(upper_char) <= 90 and ord(upper_char) >= 65) or
        #        (ord(upper_char) <= 57 and ord(upper_char) >= 48)):
            
        rec.addToList(upper_char, 'P')
        print('alphanumeric key {0} pressed'.format(key.char))
        
    except AttributeError:
        print('special key {0} pressed'.format(key))
    except UnicodeDecodeError:
        print('Not ASCII KEY')
    except UnicodeEncodeError:
        print('Not ASCII KEY')
        
        
def on_release(key):
    try:
        upper_char = key.char.upper()
        
        #if ((ord(upper_char) <= 90 and ord(upper_char) >= 65) or
        #        (ord(upper_char) <= 57 and ord(upper_char) >= 48)):
        rec.addToList(upper_char, 'R')
        print('alphanumeric key {0} released'.format(key.char))
    except AttributeError:   
        print('{0} released'.format(key))
        if key == keyboard.Key.esc:
            # Stop listener
            rec.change_condition()
            return False
    except UnicodeDecodeError:
        print('Not ASCII KEY')
    except UnicodeEncodeError:
        print('Not ASCII KEY')
            
   
# Collect events until released


rec.start()

with keyboard.Listener(on_press=on_press,on_release=on_release) as listener:
    listener.join()
    

    

wav_path = rec.get_output_name()
key_path = rec.get_key_name()

