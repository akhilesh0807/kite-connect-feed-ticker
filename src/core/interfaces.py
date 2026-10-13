from abc import ABC, abstractmethod

class BaseAuth(ABC):
    @abstractmethod
    def login(self) -> bool:
        """
        Perform the authentication flow with the brokerage API.

        Returns:
            bool: True if authentication was successful, False otherwise.
        """
        pass

class BaseDataFeed(ABC):
    @abstractmethod
    def start_feed(self):
        """Initialize and start the live data connection."""
        pass

    @abstractmethod
    def publish_tick(self, tick: 'Tick'):
        """
        Publish the normalized tick data to the ZeroMQ publisher.

        Args:
            tick (Tick): The normalized tick data model instance.
        """
        pass

    @abstractmethod
    def normalize_tick(self, tick: dict) -> 'Tick':
        """
        Convert raw tick data from the broker into the standardized Tick model.

        Args:
            tick (dict): Raw tick data received from the broker API.

        Returns:
            Tick: Normalized tick data instance.
        """
        pass