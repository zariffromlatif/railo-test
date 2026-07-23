import os

def connect_to_aws():
    # Hardcoded AWS key for testing Railo
    AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
    print("Connecting to AWS with key:", AWS_ACCESS_KEY_ID)
    return True
