import os
import subprocess
import time

# Path to the Ariel orchestrator
ORCHESTRATOR_PATH = os.path.join(os.path.dirname(__file__), '..', 'ariel', 'orchestrator.py')

def start_ariel():
    return subprocess.Popen(['python', ORCHESTRATOR_PATH])

def main():
    print("Starting Ariel Orchestrator...")
    ariel_proc = start_ariel()
    try:
        while True:
            # Check if Ariel is still running
            if ariel_proc.poll() is not None:
                print("Ariel crashed or exited. Restarting in 3 seconds...")
                time.sleep(3)
                ariel_proc = start_ariel()
            time.sleep(2)
    except KeyboardInterrupt:
        print("Shutting down Ariel orchestrator.")
        ariel_proc.terminate()
        ariel_proc.wait()

if __name__ == "__main__":
    main()
