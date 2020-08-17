from datetime import datetime, timedelta


class Timer:
    def __init__(self):
        self.start_time = datetime.now()
        self.end_time = None

    def stop_timer(self):
        self.end_time = datetime.now()

    def print_elapsed_time(self):
        elapsed_time = self.end_time - self.start_time
        hours = round(divmod(elapsed_time.total_seconds(), 3600)[0])
        minutes = round(divmod(elapsed_time.total_seconds(), 60)[0])
        seconds = round(elapsed_time.total_seconds(), 2)
        print(f'================ RUN_TIME: {hours}:{minutes}:{seconds} ================')
