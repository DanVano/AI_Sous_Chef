last_spoken = ""

def remember(text):
    global last_spoken
    last_spoken = text

def recall():
    return last_spoken