import speech_recognition as sr
import pyautogui
import os

# --- CONFIGURATION ---
WAKE_WORD = "jarvis"
STOP_WORD = "jarvis stop"

def execute_local_command(speech):
    cmd = speech.lower().strip()
    
    # 1. DELETE LOGIC (Instant word delete)
    if "delete" in cmd or "backspace" in cmd:
        pyautogui.hotkey('ctrl', 'backspace')
        return

    # 2. KEY PRESSES
    if "press enter" in cmd:
        pyautogui.press('enter')
        return
    elif "press space" in cmd:
        pyautogui.press('space')
        return
    elif "press brackets" in cmd:
        pyautogui.typewrite("[]")
        pyautogui.press('left')
        return
    
    # 3. APP LAUNCHING
    if "open chrome" in cmd:
        os.startfile("chrome.exe")
        return
    elif "open edge" in cmd:
        os.startfile("msedge.exe")
        return
    
    # 4. TYPING (Zero interval for max speed)
    pyautogui.write(speech + " ", interval=0.0)

def start_jarvis():
    recognizer = sr.Recognizer()
    
    # --- SENSITIVITY TUNING ---
    # We increase the pause threshold slightly from the last version 
    # to make sure it doesn't cut off the wake word.
    recognizer.pause_threshold = 0.8  
    recognizer.dynamic_energy_threshold = True # Automatically adjusts to room noise
    
    is_active = False
    
    print(">>> JARVIS INITIALIZING...")
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print(">>> READY. SAY 'JARVIS' TO START.")

    while True:
        with sr.Microphone() as source:
            try:
                # We listen for a slightly longer chunk to catch the wake word clearly
                audio = recognizer.listen(source, timeout=None, phrase_time_limit=4)
                speech = recognizer.recognize_google(audio).lower()
                print(f"Heard: {speech}") # This helps you debug if it hears you

                # WAKE LOGIC
                if WAKE_WORD in speech and not is_active:
                    is_active = True
                    print("!!! JARVIS ACTIVE - START SPEAKING !!!")
                    continue

                # STOP LOGIC
                if STOP_WORD in speech:
                    is_active = False
                    print("... JARVIS SLEEPING ...")
                    continue

                # ACTIVE PROCESSING
                if is_active:
                    execute_local_command(speech)
                        
            except sr.UnknownValueError:
                # This happens if it hears noise but no words
                continue
            except Exception as e:
                print(f"Error: {e}")
                continue

if __name__ == "__main__":
    start_jarvis()

 