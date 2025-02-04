import os
import subprocess
from dotenv import load_dotenv
import sys
import playsound  # Assuming you're using playsound to play the beep.mp3 sound

# Load environment variables from .env file
load_dotenv()

def resource_path(relative_path):
    """Get the absolute path to a resource (sound file)."""
    if hasattr(sys, '_MEIPASS'):  # If running as an executable (PyInstaller bundle)
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def create_exe(script_path, onefile=True, icon_path=None, noconsole=False, additional_binaries=None, cert_path=None):
    """
    Automates creating a Windows .exe file from a Python script using PyInstaller and signs it with a certificate.

    Parameters:
    - script_path (str): The path to the Python script to be converted.
    - onefile (bool): If True, creates a single .exe file. Default is True.
    - icon_path (str): Path to the .ico file for the executable icon (optional).
    - noconsole (bool): If True, hides the console window (for GUI apps). Default is False.
    - additional_binaries (list of tuples): List of binaries to include. Each tuple is (source_path, target_folder).
    - cert_path (str): Path to the signing certificate in PFX format.
    """
    if not os.path.isfile(script_path):
        print(f"Error: File '{script_path}' not found.")
        return

    # Base PyInstaller command# Base PyInstaller command
    command = ["pyinstaller", "--hidden-import=tensorflow", "--hidden-import=tensorflow.keras", script_path]


    # Add options
    if onefile:
        command.append("--onefile")
    if icon_path and os.path.isfile(icon_path):
        command.extend(["--icon", icon_path])
    if noconsole:
        command.append("--noconsole")

    # Add additional binaries
    if additional_binaries:
        for source, target in additional_binaries:
            if os.path.isfile(source):
                command.extend(["--add-binary", f"{source};{target}"])
            else:
                print(f"Warning: Binary file '{source}' not found. Skipping.")

    # Add the beep.mp3 sound file
    command.extend(["--add-data", "beep.mp3;."])

    # Run the PyInstaller command
    try:
        print("Creating .exe file...")
        subprocess.run(command, check=True)
        print("\nBuild complete. Check the 'dist' folder for the .exe file.")
    except subprocess.CalledProcessError as e:
        print(f"Error during build process: {e}")
        return
    except Exception as e:
        print(f"Unexpected error: {e}")
        return

    # Path to the generated .exe file
    exe_path = os.path.join("dist", os.path.splitext(os.path.basename(script_path))[0] + ".exe")

    if not os.path.isfile(exe_path):
        print(f"Error: Generated executable '{exe_path}' not found.")
        return

    # Get certificate password from environment
    cert_password = os.getenv("CERTIFICATION_PASSWORD", "shabeeb")

    if cert_path and os.path.isfile(cert_path) and cert_password:
        print(f"Signing {exe_path}...")
        try:
            sign_command = [
                "signtool", "sign",
                "/fd", "SHA256",
                "/a",
                "/f", cert_path,
                "/p", cert_password,
                exe_path
            ]
            subprocess.run(sign_command, check=True)
            print("Signing complete.")
        except subprocess.CalledProcessError as e:
            print(f"Error during signing process: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
    else:
        print("No certificate provided, invalid certificate path, or missing password. Skipping signing process.")

    # Play sound after execution (for example)
    play_sound()

def play_sound():
    """Play the beep.mp3 sound."""
    try:
        beep_path = resource_path("beep.mp3")  # Get the correct path for beep.mp3
        playsound.playsound(beep_path)
        print("Beep sound played successfully.")
    except Exception as e:
        print(f"Error playing sound: {e}")

if __name__ == "__main__":
    # Input script path from the user
    script_path = "./real_time_video.py"

    # Optional settings
    onefile = input("Do you want a single executable file? (y/n): ").strip().lower() == "y"
    icon_path = input("Enter the path to the .ico file for the icon (or leave blank): ").strip()
    noconsole = input("Hide console window? (y/n): ").strip().lower() == "y"

    # Handle additional binaries (e.g., libzbar-64.dll for pyzbar)
    additional_binaries = []
    libzbar_path = os.path.join(sys.prefix, "Lib", "site-packages", "pyzbar", "libzbar-64.dll")
    if os.path.isfile(libzbar_path):
        additional_binaries.append((libzbar_path, "pyzbar"))

    # Path to certificate
    cert_path = os.path.join("cert", "certificate.pfx")

    # Create the executable and sign it
    create_exe(script_path, onefile=onefile, icon_path=icon_path, noconsole=noconsole, additional_binaries=additional_binaries, cert_path=cert_path)
