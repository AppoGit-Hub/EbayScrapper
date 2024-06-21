import time

def wait(current_time: int, interval: int, wait_time: int) -> tuple[int, bool]:
    print(current_time)
    time.sleep(interval)
    current_time -= 1
    is_done = current_time == 0
    return wait_time if is_done else current_time, is_done

def wait_alt(wait_time: int):
    chrono = wait_time
    is_done = False
    while not is_done:
        chrono, is_done = wait(chrono, 1, wait_time)
        if not is_done:
            continue
        
        print("Done")

wait_alt(10)