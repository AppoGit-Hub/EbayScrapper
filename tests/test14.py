from utils import wait

seconds_left: int = 10
while True:
    print("->")
    seconds_left, is_done = wait(seconds_left, 1, 10)        
    if not is_done:
        continue
            