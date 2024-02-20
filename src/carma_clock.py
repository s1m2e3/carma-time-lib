import threading
import time

class CarmaClock:
    def __init__(self, simulation_mode=False):
        self._current_time = 0
        self._is_simulation_mode = simulation_mode
        self._is_initialized = not simulation_mode
        self._initialization_mutex = threading.Lock()
        self._initialization_cv = threading.Condition(lock=self._initialization_mutex)
        self._sleep_mutex = threading.Lock()
        self._sleep_holder = []

    def now_in_seconds(self) -> int:
        if self._is_simulation_mode:
            if not self._is_initialized:
                raise ValueError("Clock is not initialized!")
            # Round down as same behavior as chrono::duration_cast
            return int(self._current_time / 1000)
        else:
            return int(time.time())

    def now_in_milliseconds(self) -> int:
        if self._is_simulation_mode:
            if not self._is_initialized:
                raise ValueError("Clock is not initialized!")
            return int(self._current_time)
        else:
            return int(time.time() * 1000)

    def update(self, current_time: int) -> None:
        if not self._is_simulation_mode:
            raise ValueError("Clock is not in simulation mode!")

        self._current_time = current_time

        if not self._is_initialized:
            self._is_initialized = True
            with self._initialization_mutex:
                self._initialization_cv.notify_all()

        with self._sleep_mutex:
            self._process_sleeping_threads()

    def is_simulation_mode(self) -> bool:
        return self._is_simulation_mode

    def wait_for_initialization(self) -> None:
        if not self._is_initialized:
            with self._initialization_mutex:
                self._initialization_cv.wait_for(lambda: self._is_initialized)

    def sleep_until(self, future_time: int) -> None:
        if not self._is_initialized:
            raise ValueError("Clock is not initialized!")

        if self._is_simulation_mode:
            if future_time > self._current_time:
                sleep_cv_pair = threading.Condition(), threading.Lock()
                with self._sleep_mutex:
                    self._sleep_holder.append((future_time, sleep_cv_pair))
                               
                with sleep_cv_pair[1]:
                    with sleep_cv_pair[0]:
                        sleep_cv_pair[0].wait()

        else:
            time_to_sleep = max(0, (future_time - self.now_in_milliseconds()) / 1000)
            time.sleep(time_to_sleep)

    def sleep_for(self, time_to_sleep: int) -> None:
        self.sleep_until(self._current_time + time_to_sleep)

    def _process_sleeping_threads(self) -> None:
        current_time = self._current_time

        self._sleep_holder = [
            (time, cv_pair)
            for time, cv_pair in self._sleep_holder
            if current_time >= time
        ]

        for _, cv_pair in self._sleep_holder:
            with cv_pair[1]:
                cv_pair[0].notify()

# SYSTEM_SLEEP_TIME = 150

# # Create a sim clock
# clock = CarmaClock(simulation_mode=True)

# # Update the clock
# clock.update(1)

# # Thread function to update clock after sleeping
# def update_clock_after_sleep():
#     time.sleep(SYSTEM_SLEEP_TIME / 1000)  # Convert milliseconds to seconds
#     clock.update(2)

# # Create a thread to update clock after sleeping
# t = threading.Thread(target=update_clock_after_sleep)

# # Wait for initialization
# clock.wait_for_initialization()

# # Check if sim time matches expected value
# sim_time_now = clock.now_in_milliseconds()
# assert sim_time_now == 1, f"Sim time is {sim_time_now} instead of 1"

# # Measure start time
# start = time.time()

# # Sleep until sim time + 1
# clock.sleep_until((sim_time_now + 1))

# # Measure end time
# after = time.time()

# # Calculate elapsed time in milliseconds
# ms_count = int((after - start) * 1000)

# # Join the thread
# t.start()
# t.join()

# # Check if elapsed time matches expected sleep time
# assert abs(SYSTEM_SLEEP_TIME - ms_count) <= 5, f"Elapsed time: {ms_count}ms, Expected: {SYSTEM_SLEEP_TIME}ms"