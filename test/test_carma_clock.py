import os
import sys 
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
SYSTEM_SLEEP_TIME = 150
import time
from carma_clock import *

def test_system_time_initialization():
    # Create a CarmaClock instance
    clock = CarmaClock()
    # Get the start time
    start = time.time()
    # Wait for initialization
    clock.wait_for_initialization()
    # Get the time after initialization
    after = time.time()
    # Calculate the elapsed time in milliseconds
    ms_count = int((after - start) * 1000)
    # Check if the initialization happened immediately
    assert abs(0 - ms_count) <= 5, "Initialization did not happen immediately"

def test_system_time_sleep_until():
    # Assuming CarmaClock is already defined as in the previous Python implementation
    # Create a CarmaClock instance
    clock = CarmaClock()
    # Wait for initialization
    clock.wait_for_initialization()
    # Get the start time
    start = time.time()
    # Get the current time in milliseconds from CarmaClock
    clock_now = clock.now_in_milliseconds()
    # Calculate the elapsed time since epoch in milliseconds using system clock
    start_epoch_ms = int(start * 1000)
    # Check if the current time from CarmaClock matches the system clock
    assert abs(clock_now - start_epoch_ms) <= 1, "ClockNow does not match system time"
    # Calculate future time in milliseconds
    future_time_ms = start_epoch_ms + SYSTEM_SLEEP_TIME
    # Sleep until future time
    clock.sleep_until(future_time_ms) 
    # Get the time after sleeping
    after = time.time()
    # Calculate the elapsed time after sleeping in milliseconds
    ms_count = (after - start) * 1000
    # Check if it slept approximately what was asked
    assert abs(SYSTEM_SLEEP_TIME - ms_count) <= 5, "Did not sleep approximately what was asked"


def test_system_time_update_exception():
    # Create a CarmaClock instance
    clock = CarmaClock()
    # Initialize flag to track exception
    exception_thrown = False
    try:
        # Try to update with a value (0 in this case)
        clock.update(0)
    except Exception as e:
        # Catch any exception and set flag to True
        exception_thrown = True
    # Assert if an exception was thrown
    assert exception_thrown, "Exception was not thrown"

def test_sim_time_initialization():
    # Create a sim clock
    clock = CarmaClock(simulation_mode=True)

    # Measure start time
    start = time.time()

    # Thread function to update clock after sleeping
    def update_clock_after_sleep():
        time.sleep(SYSTEM_SLEEP_TIME / 1000)  # Convert milliseconds to seconds
        clock.update(1)

    # Create a thread to update clock after sleeping
    t = threading.Thread(target=update_clock_after_sleep)

    # Start the thread
    t.start()

    # Block until clock initialized
    clock.wait_for_initialization()

    # Measure end time
    after = time.time()

    # Calculate elapsed time in milliseconds
    ms_count = int((after - start) * 1000)

    # Check if elapsed time matches the expected sleep time
    print(ms_count)
    assert abs(SYSTEM_SLEEP_TIME - ms_count) <= 10, "Elapsed time does not match expected sleep time"

    # Join the thread
    t.join()


def test_sim_time_initialization_multiple_threads():
    
    # Create a sim clock
    clock = CarmaClock(simulation_mode=True)

    # Measure start time
    start = time.time()

    # Thread function to update clock after sleeping
    def update_clock_after_sleep():
        time.sleep(SYSTEM_SLEEP_TIME / 1000)  # Convert milliseconds to seconds
        clock.update(1)

    # Thread function to wait for initialization
    def wait_for_initialization():
        clock.wait_for_initialization()

    # Create a thread to update clock after sleeping
    update_thread = threading.Thread(target=update_clock_after_sleep)

    # Three threads to wait for initialization
    t1 = threading.Thread(target=wait_for_initialization)
    t2 = threading.Thread(target=wait_for_initialization)
    t3 = threading.Thread(target=wait_for_initialization)

    # Start the threads
    update_thread.start()
    t1.start()
    t2.start()
    t3.start()

    # Join all the threads
    update_thread.join()
    t1.join()
    t2.join()
    t3.join()

    # Measure end time
    after = time.time()

    # Calculate elapsed time in milliseconds
    ms_count = int((after - start) * 1000)

    # Check if elapsed time matches the expected sleep time
    assert abs(SYSTEM_SLEEP_TIME - ms_count) <= 10, "Elapsed time does not match expected sleep time"

def test_sim_time_initialization_early():
    
    # Create a sim clock
    clock = CarmaClock(simulation_mode=True)

    # Update the clock early
    clock.update(1)

    # Thread function to sleep
    def sleep_thread():
        time.sleep(SYSTEM_SLEEP_TIME / 1000)  # Convert milliseconds to seconds

    # Create a thread to sleep
    t = threading.Thread(target=sleep_thread)
    t.start()
    # Measure start time
    start = time.time()

    # Wait for initialization (should happen immediately)
    clock.wait_for_initialization()

    # Measure end time
    after = time.time()

    # Calculate elapsed time in milliseconds
    ms_count = int((after - start) * 1000)

    # Check if elapsed time is close to 0 (should happen immediately)
    assert abs(ms_count) <= 5, "Initialization did not happen immediately"

    # Join the thread
    t.join()

def test_sim_time_not_initialized():
    
    # Create a sim clock
    clock = CarmaClock(simulation_mode=True)

    # Check if exception is thrown for nowInMilliseconds
    exception_thrown_milliseconds = False
    try:
        time_value = clock.now_in_milliseconds()
    except Exception as e:
        exception_thrown_milliseconds = True

    # Assert that exception was thrown
    assert exception_thrown_milliseconds, "Exception was not thrown for nowInMilliseconds"

    # Check if exception is thrown for nowInSeconds
    exception_thrown_seconds = False
    try:
        time_value = clock.now_in_seconds()
    except Exception as e:
        exception_thrown_seconds = True

    # Assert that exception was thrown
    assert exception_thrown_seconds, "Exception was not thrown for nowInSeconds"


def test_sim_time_not_initialized_for_sleep():
    # Create a sim clock
    clock = CarmaClock(simulation_mode=True)

    # Check if exception is thrown for sleep_until
    exception_thrown = False
    try:
        clock.sleep_until(1)
    except Exception as e:
        exception_thrown = True

    # Assert that exception was thrown
    assert exception_thrown, "Exception was not thrown for sleep_until"


def test_sim_time_sleep_until():
    
    # Create a sim clock
    clock = CarmaClock(simulation_mode=True)

    # Update the clock
    clock.update(1)

    # Thread function to update clock after sleeping
    def update_clock_after_sleep():
        time.sleep(SYSTEM_SLEEP_TIME / 1000)  # Convert milliseconds to seconds
        clock.update(2)

    # Create a thread to update clock after sleeping
    t = threading.Thread(target=update_clock_after_sleep)
    
    # Wait for initialization
    clock.wait_for_initialization()

    # Check if sim time matches expected value
    sim_time_now = clock.now_in_milliseconds()
    assert sim_time_now == 1, f"Sim time is {sim_time_now} instead of 1"

    # Measure start time
    start = time.time()

    # Sleep until sim time + 1
    clock.sleep_until((sim_time_now + 1))

    # Measure end time
    after = time.time()

    # Calculate elapsed time in milliseconds
    ms_count = (after - start) * 1000

    # Join the thread
    t.start()

    # Check if elapsed time matches expected sleep time
    assert abs(SYSTEM_SLEEP_TIME - ms_count) <= 5, f"Elapsed time: {ms_count}ms, Expected: {SYSTEM_SLEEP_TIME}ms"
