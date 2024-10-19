import os
import time
import webbrowser

import pygame
import pyttsx3
import speech_recognition as sr

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Initialize pygame and its mixer
pygame.init()
pygame.mixer.init()

# Load your WAV sound file (Make sure the path is correct)
Going_Dark_path = r'Going_Dark.mp3'  # Change this to your actual file path
Dark_sound = pygame.mixer.Sound(Going_Dark_path)
Operation_Ghost_path= r'Voicy_Hostile Swarm Inbound.mp3'
Ghost_sound = pygame.mixer.Sound(Operation_Ghost_path)


def darken_screen():
  """Make the screen go black for 2 seconds."""
  screen = pygame.display.set_mode((1920, 1080))  # Adjust size as necessary
  screen.fill((0, 0, 0))  # Fill the screen with black
  pygame.display.flip()  # Update the display
  time.sleep(2)  # Keep the screen dark for 2 seconds
  pygame.display.flip()  # Update the display

#def on_hotkey():
    #"""Function to be called when the hotkey is pressed."""
    #print("Hotkey activated! Performing action...")  # You can replace this with your desired functionality


# Setup the hotkey to listen for 'Ctrl + Shift + G'
#keyboard.add_hotkey('ctrl+shift+g', on_hotkey)

# Print instructions to the user
#print("Press Ctrl + Shift + G to initiate your command.")

# Keep the program running to listen for the hotkey
#keyboard.wait('esc')  # Optional: Press 'Esc' to exit the loop

def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()


def listen_to_user():
    """Listen to user for their search query."""
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Please say your search query...")
        audio = recognizer.listen(source)

        try:
            command = recognizer.recognize_google(audio).lower()
            print(f"You said: {command}")
            return command
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
            return None
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return None


def listen_for_activation_phrase():
    """Listen continuously for the activation phrase."""
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening for 'Hey Ghost'...")
        recognizer.energy_threshold = 4000  # Adjust as needed
        recognizer.dynamic_energy_threshold = True  # Automatically adjust energy threshold

        while True:
            try:
                audio = recognizer.listen(source, timeout=5)
                command = recognizer.recognize_google(audio).lower()
                print(f"You said: {command}")

                if "hey ghost" in command:
                    print("Activation phrase detected!")
                    speak("How can I help you?")
                    handle_command()  # Call the function to handle user commands

            except sr.WaitTimeoutError:
                print("Listening timeout, let's keep listening...")
            except sr.UnknownValueError:
                continue  # If speech is unintelligible
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")
                break


def handle_command():
    """Handle user commands after activation phrase is detected."""
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("What would you like to do?")
        audio = recognizer.listen(source)

        try:
            command = recognizer.recognize_google(audio).lower()
            print(f"You said: {command}")

            if "email" in command:
                Dark_sound.play()
                time.sleep(13)  # Adjust based on sound length
                print("Checking your emails...")
                darken_screen()
                outlook_path = r'C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Outlook (classic).lnk'
                os.startfile(outlook_path)  # Opens the Outlook shortcut

            elif "youtube" in command:
                #speak("Opening YouTube.")
                youtube_url = "https://www.youtube.com/"
                #webbrowser.open(youtube_url)

                # Wait for YouTube to load
                time.sleep(2)  # Wait for the page to load

                # Ask the user what they want to search for on YouTube
                speak("What do you want to search for on YouTube?")
                search_query = listen_to_user()  # Listen for the search query

                # Make sure search_query is treated as a string
                if isinstance(search_query, str) and search_query:  # Confirm it's a non-empty string
                    time.sleep(5)  # Delay to ensure browser is ready
                    # Use pyautogui to type the search term into the YouTube search box
                    search_url = f"https://www.youtube.com/results?search_query={search_query}"
                    webbrowser.open(search_url)
                else:
                  speak("I didn't catch that. Please try again.")

            elif "jira" in command:
                speak("Opening Jira.")
                jira_url = "https://aria-invokeinc.atlassian.net/jira/software/c/projects/PSRP/boards/79"
                webbrowser.open(jira_url)  # Opens Jira page

            elif "github" in command:
              speak("Opening GitHub.")
              github_url = "https://www.github.com"
              webbrowser.open(github_url)  # Opens GitHub

            elif "projector" in command:
              speak("Opening Projector.")
              projector_url = "https://app4.projectorpsa.com/x/Dashboard"
              webbrowser.open(projector_url)  # Opens Projector

            elif "execute operation ghost" in command:
              speak("Operation Ghost is a go.")
              Ghost_sound.play()
              projector_url = "https://app4.projectorpsa.com/x/Dashboard"
              webbrowser.open(projector_url)
              github_url = "https://www.github.com"
              webbrowser.open(github_url)
              jira_url = "https://app4.projectorpsa.com/x/Dashboard"
              webbrowser.open(jira_url)
              outlook_path = r'C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Outlook (classic).lnk'
              os.startfile(outlook_path)  # Opens the Outlook shortcut


            # You can add more command checks as needed
            else:
              speak("I'm not sure what you mean.")

        except sr.UnknownValueError:
          print("Sorry, I did not understand that.")
        except sr.RequestError as e:
          print(f"Could not request results from Google Speech Recognition service; {e}")


if __name__ == "__main__":
  time.sleep(2)  # Allow some time before the script starts listening
  listen_for_activation_phrase()  # Start listening for the activation phrase
