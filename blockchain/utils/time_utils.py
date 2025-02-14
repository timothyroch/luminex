import time
from datetime import datetime, timedelta

class TimeUtils:
    """Provides time-related utilities for the blockchain system."""

    @staticmethod
    def current_timestamp():
        """
        Returns the current Unix timestamp in seconds.
        :return: The current Unix timestamp as an integer.
        """
        return int(time.time())

    @staticmethod
    def current_utc_time():
        """
        Returns the current UTC time as a formatted string.
        :return: The current UTC time in ISO 8601 format.
        """
        return datetime.utcnow().isoformat()

    @staticmethod
    def timestamp_to_utc(timestamp):
        """
        Converts a Unix timestamp to a human-readable UTC time.
        :param timestamp: The Unix timestamp to convert.
        :return: The corresponding UTC time as a string.
        """
        return datetime.utcfromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def utc_to_timestamp(utc_time):
        """
        Converts a human-readable UTC time to a Unix timestamp.
        :param utc_time: The UTC time as a string (e.g., "2025-01-10 15:30:00").
        :return: The corresponding Unix timestamp as an integer.
        """
        dt = datetime.strptime(utc_time, "%Y-%m-%d %H:%M:%S")
        return int(dt.timestamp())

    @staticmethod
    def add_seconds_to_timestamp(timestamp, seconds):
        """
        Adds a number of seconds to a Unix timestamp.
        :param timestamp: The original Unix timestamp.
        :param seconds: The number of seconds to add.
        :return: The updated Unix timestamp.
        """
        return timestamp + seconds

    @staticmethod
    def delay(seconds):
        """
        Pauses execution for a specified number of seconds.
        :param seconds: The number of seconds to delay.
        """
        print(f"Delaying for {seconds} seconds...")
        time.sleep(seconds)

    @staticmethod
    def time_since(timestamp):
        """
        Calculates the time elapsed since a given Unix timestamp.
        :param timestamp: The past Unix timestamp.
        :return: A human-readable string indicating the time elapsed.
        """
        elapsed = datetime.utcnow() - datetime.utcfromtimestamp(timestamp)
        days, seconds = elapsed.days, elapsed.seconds
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60

        components = []
        if days > 0:
            components.append(f"{days} days")
        if hours > 0:
            components.append(f"{hours} hours")
        if minutes > 0:
            components.append(f"{minutes} minutes")
        if seconds > 0:
            components.append(f"{seconds} seconds")

        return ", ".join(components) + " ago"

    @staticmethod
    def is_timestamp_in_future(timestamp):
        """
        Checks if a given Unix timestamp is in the future.
        :param timestamp: The Unix timestamp to check.
        :return: True if the timestamp is in the future, False otherwise.
        """
        return timestamp > TimeUtils.current_timestamp()


# Example usage
if __name__ == "__main__":
    print("Current Timestamp:", TimeUtils.current_timestamp())
    print("Current UTC Time:", TimeUtils.current_utc_time())

    # Convert timestamp to UTC time
    example_timestamp = TimeUtils.current_timestamp()
    print("UTC Time for Current Timestamp:", TimeUtils.timestamp_to_utc(example_timestamp))

    # Convert UTC time to timestamp
    example_utc_time = "2025-01-10 15:30:00"
    print("Timestamp for UTC Time:", TimeUtils.utc_to_timestamp(example_utc_time))

    # Add seconds to timestamp
    print("Timestamp after adding 3600 seconds (1 hour):", TimeUtils.add_seconds_to_timestamp(example_timestamp, 3600))

    # Delay execution
    TimeUtils.delay(2)

    # Time since a past timestamp
    past_timestamp = TimeUtils.current_timestamp() - 3600  # 1 hour ago
    print("Time since past timestamp:", TimeUtils.time_since(past_timestamp))

    # Check if a timestamp is in the future
    future_timestamp = TimeUtils.current_timestamp() + 600  # 10 minutes from now
    print("Is future timestamp in the future?", TimeUtils.is_timestamp_in_future(future_timestamp))
