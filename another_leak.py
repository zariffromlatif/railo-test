import os
def test_another_leak():
    # Another test for railo Fix PR!
    AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
    return AWS_ACCESS_KEY_ID
