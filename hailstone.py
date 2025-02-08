import time
import string
import threading

class HailStone:
    def __init__(self, machine_id, start_time=1738851309614):
        """
            a simple version of snowflake algorithm, and convert to base62
            args:
                machine_id: int, the machine id
                start_time: int, the start time of the algorithm
        """
        self.machine_id = machine_id
        self.start_time = start_time
        self.sequence = 0
        self.last_timestamp = -1
        self.lock = threading.Lock()
        self._base62_alphabet = string.digits + string.ascii_letters

    def fakesnow(self):
        # it is a simple version of snowflake algorithm

        time_now = int(time.time() * 1000) - self.start_time
        
        with self.lock:
            # incremental sequence number in a single millisecond
            if(time_now == self.last_timestamp):
                self.sequence += 1
            else:
                self.sequence = 0
                self.last_timestamp = time_now
            
            # 41 bits for time, 10 bits for machine id, 5 bits for sequence
            return (time_now << 15) | (self.machine_id << 5) | self.sequence

    def _base62(self, num):
        # encode the number to base62
        if num == 0:
            return self._base62_alphabet[0]
        base62 = []
        while num:
            num, rem = divmod(num, 62)
            base62.append(self._base62_alphabet[rem])
        return ''.join(reversed(base62))

    def generate(self):
        return self._base62(self.fakesnow())