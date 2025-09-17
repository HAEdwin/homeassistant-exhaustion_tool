"""
Sensor platform for Exhaustion Meter integration.
Defines a sensor entity to monitor socket usage.
"""

import psutil
from homeassistant.components.sensor import SensorEntity

DEFAULT_NAME = "Open sockets"


async def async_setup_entry(hass, config_entry, async_add_entities):
    """
    Set up the Exhaustion Meter sensor entities from a config entry.
    """
    sensors = [
        SocketExhaustionSensor(),
        TimeWaitSocketSensor(),
        FileDescriptorSensor(),
        ProcessCountSensor(),
        DiskIOSensor(),
        OpenFilesSensor(),
        EstablishedSocketSensor(),
        CloseWaitSocketSensor(),
        ListenSocketSensor(),
        SocketFailSensor(),
        # EventLoopLagSensor()  # See note below
    ]
    async_add_entities(sensors)


# Sensor that attempts to open a socket and reports if it fails
import socket


class SocketFailSensor(SensorEntity):
    """
    Sensor that reports if a new socket cannot be created (proxy for socket exhaustion).
    0 = success, 1 = failure
    """

    def __init__(self):
        self._attr_name = "Socket Creation Failure"
        self._attr_native_unit_of_measurement = "fail"
        self._attr_icon = "mdi:alert"
        self._attr_native_value = 0

    async def async_update(self):
        """Try to open a socket and report failure (1) or success (0)."""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.close()
            self._attr_native_value = 0
        except Exception:
            self._attr_native_value = 1


class OpenFilesSensor(SensorEntity):
    """
    Sensor that reports the number of open files by the Home Assistant process.
    """

    def __init__(self):
        """Initialize the open files sensor entity."""
        self._attr_name = "Open Files (HA Process)"
        self._attr_native_unit_of_measurement = "files"
        self._attr_icon = "mdi:file"
        self._attr_native_value = None

    async def async_update(self):
        """Async update for open files sensor."""
        try:
            from concurrent.futures import ThreadPoolExecutor

            with ThreadPoolExecutor() as executor:
                loop = self.hass.loop
                result = await loop.run_in_executor(
                    executor, lambda: len(psutil.Process().open_files())
                )
                self._attr_native_value = result
        except Exception:
            self._attr_native_value = None


class EstablishedSocketSensor(SensorEntity):
    """
    Sensor that reports the number of sockets in ESTABLISHED state.
    """

    def __init__(self):
        """Initialize the ESTABLISHED socket sensor entity."""
        self._attr_name = "Sockets in ESTABLISHED"
        self._attr_native_unit_of_measurement = "sockets"
        self._attr_icon = "mdi:lan-connect"
        self._attr_native_value = None

    async def async_update(self):
        """Async update for ESTABLISHED socket sensor."""
        try:
            self._attr_native_value = sum(
                1 for c in psutil.net_connections() if c.status == "ESTABLISHED"
            )
        except Exception:
            self._attr_native_value = None


class CloseWaitSocketSensor(SensorEntity):
    """
    Sensor that reports the number of sockets in CLOSE_WAIT state.
    """

    def __init__(self):
        """Initialize the CLOSE_WAIT socket sensor entity."""
        self._attr_name = "Sockets in CLOSE_WAIT"
        self._attr_native_unit_of_measurement = "sockets"
        self._attr_icon = "mdi:lan-disconnect"
        self._attr_native_value = None

    async def async_update(self):
        """Async update for CLOSE_WAIT socket sensor."""
        try:
            self._attr_native_value = sum(
                1 for c in psutil.net_connections() if c.status == "CLOSE_WAIT"
            )
        except Exception:
            self._attr_native_value = None


class ListenSocketSensor(SensorEntity):
    """
    Sensor that reports the number of sockets in LISTEN state.
    """

    def __init__(self):
        """Initialize the LISTEN socket sensor entity."""
        self._attr_name = "Sockets in LISTEN"
        self._attr_native_unit_of_measurement = "sockets"
        self._attr_icon = "mdi:lan-pending"
        self._attr_native_value = None

    async def async_update(self):
        """Async update for LISTEN socket sensor."""
        try:
            self._attr_native_value = sum(
                1 for c in psutil.net_connections() if c.status == "LISTEN"
            )
        except Exception:
            self._attr_native_value = None


# Note: Event loop lag is best measured using Home Assistant's built-in system monitor or custom integration.
# Implementing a reliable event loop lag sensor in a polling sensor is not recommended here.


class FileDescriptorSensor(SensorEntity):
    """
    Sensor that reports the number of open file descriptors (Linux/Unix only).
    """

    def __init__(self):
        """Initialize the file descriptor sensor entity."""
        self._attr_name = "Open File Descriptors"
        self._attr_native_unit_of_measurement = "fds"
        self._attr_icon = "mdi:file-document-outline"
        self._attr_native_value = None

    async def async_update(self):
        """Async update for file descriptor sensor."""
        try:
            import os

            self._attr_native_value = (
                os.sysconf("SC_OPEN_MAX") if hasattr(os, "sysconf") else None
            )
            # For the current process only:
            if hasattr(psutil.Process(), "num_fds"):
                self._attr_native_value = psutil.Process().num_fds()
        except Exception:
            self._attr_native_value = None


class ProcessCountSensor(SensorEntity):
    """
    Sensor that reports the number of running processes.
    """

    def __init__(self):
        """Initialize the process count sensor entity."""
        self._attr_name = "Process Count"
        self._attr_native_unit_of_measurement = "processes"
        self._attr_icon = "mdi:application"
        self._attr_native_value = None

    async def async_update(self):
        """Async update for process count sensor."""
        try:
            self._attr_native_value = len(psutil.pids())
        except Exception:
            self._attr_native_value = None


class DiskIOSensor(SensorEntity):
    """
    Sensor that reports disk I/O statistics (read/write count).
    """

    def __init__(self):
        """Initialize the disk I/O sensor entity."""
        self._attr_name = "Disk I/O Operations"
        self._attr_native_unit_of_measurement = "ops"
        self._attr_icon = "mdi:harddisk"
        self._attr_native_value = None

    async def async_update(self):
        """Async update for disk I/O sensor."""
        try:
            io = psutil.disk_io_counters()
            if io:
                self._attr_native_value = io.read_count + io.write_count
            else:
                self._attr_native_value = None
        except Exception:
            self._attr_native_value = None


class TimeWaitSocketSensor(SensorEntity):
    """
    Sensor that reports the number of sockets in TIME_WAIT state.
    """

    def __init__(self):
        """Initialize the TIME_WAIT sensor entity."""
        self._attr_name = "Sockets in TIME_WAIT"
        self._attr_native_unit_of_measurement = "sockets"
        self._attr_icon = "mdi:timer-sand"
        self._attr_native_value = None

    async def async_update(self):
        """Async update for TIME_WAIT socket sensor."""
        try:
            self._attr_native_value = sum(
                1 for c in psutil.net_connections() if c.status == "TIME_WAIT"
            )
        except Exception:
            self._attr_native_value = None


class SocketExhaustionSensor(SensorEntity):
    """
    Sensor that reports the number of open network connections (sockets).
    """

    def __init__(self):
        """Initialize the sensor entity."""
        self._attr_name = DEFAULT_NAME
        self._attr_native_unit_of_measurement = "sockets"
        self._attr_icon = "mdi:lan"
        self._attr_native_value = None

    async def async_update(self):
        """Async update for open sockets sensor."""
        try:
            self._attr_native_value = len(psutil.net_connections())
        except Exception:
            self._attr_native_value = None
