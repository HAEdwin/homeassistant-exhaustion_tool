# homeassistant-exhaustion_tool
An resource exhaustion tool to find integrations that are exhausting resources. After restarting HA wait 20 seconds before updates occur.

# Exhaustion Meter Sensors Explained

This document explains each sensor provided by the Exhaustion tool and how it relates to the health of your Home Assistant system.

---


## Open sockets
**What it does:**
- Reports the total number of open network connections (sockets) on the system, including all TCP/UDP sockets in all states.
**Health meaning:**
- A steadily increasing or very high value may indicate a socket leak or that your system is approaching its socket/file descriptor limit, which can cause connectivity issues or failures.
**Normal values:**
- For most Home Assistant installations, 20–200 is typical. Over 500 may indicate a problem unless you have many integrations or devices.


## Sockets in TIME_WAIT
**What it does:**
- Counts the number of sockets in the TIME_WAIT state (recently closed connections waiting to be fully released by the OS).
**Health meaning:**
- A high value is normal for busy systems, but if it grows without dropping, it may indicate rapid connection churn or improper socket handling by integrations.
**Normal values:**
- 0–100 is typical for most systems. Spikes up to 500 can occur on busy networks but should drop back down.


## Sockets in ESTABLISHED
**What it does:**
- Shows the number of sockets with active, established connections.
**Health meaning:**
- Indicates how many active network connections Home Assistant and other processes are maintaining. A sudden spike may indicate a flood of connections or a stuck integration.
**Normal values:**
- 5–50 is typical. Over 100 may indicate a busy system or a possible issue.


## Sockets in CLOSE_WAIT
**What it does:**
- Counts sockets waiting to be closed by the local process.
**Health meaning:**
- A growing number may indicate that some software is not closing sockets properly, which can eventually exhaust system resources.
**Normal values:**
- 0–5 is typical. Any sustained value above 10 may indicate a problem.


## Sockets in LISTEN
**What it does:**
- Reports the number of sockets in LISTEN state (waiting for incoming connections).
**Health meaning:**
- Shows how many services are waiting for connections. A sudden drop may indicate a crashed service; a sudden spike may indicate misconfiguration.
**Normal values:**
- 2–10 is typical for Home Assistant. Higher values may be normal if you run many add-ons or custom integrations.


## Socket Creation Failure
**What it does:**
- Attempts to create a test socket. Reports 0 if successful, 1 if it fails (indicating socket exhaustion).
**Health meaning:**
- If this sensor shows 1, your system cannot create new sockets, which will cause network failures in Home Assistant and other software. Immediate action is required.
**Normal values:**
- Should always be 0. If it is 1, your system is out of sockets or file descriptors.


## Open Files (HA Process)
**What it does:**
- Reports the number of files currently open by the Home Assistant process.
**Health meaning:**
- A steadily increasing value may indicate a file handle leak, which can eventually cause Home Assistant to crash or malfunction.
**Normal values:**
- 10–100 is typical. Over 200 may indicate a leak or heavy file usage.


## Open File Descriptors
**What it does:**
- Shows the number of open file descriptors (Linux/Unix only) for the Home Assistant process.
**Health meaning:**
- Similar to open files, a high or growing value may indicate a resource leak.
**Normal values:**
- 20–200 is typical. Over 500 may indicate a leak or resource exhaustion.


## Process Count
**What it does:**
- Reports the total number of running processes on the system.
**Health meaning:**
- A sudden increase may indicate runaway processes or a misbehaving integration. A very high value can exhaust system resources.
**Normal values:**
- 50–200 is typical for a Home Assistant system. Over 300 may indicate a problem.


## Disk I/O Operations
**What it does:**
- Shows the total number of disk read and write operations since system boot.
**Health meaning:**
- A rapidly increasing value may indicate heavy disk usage. If Home Assistant becomes slow or unresponsive, check this sensor for excessive I/O.
**Normal values:**
- The absolute value is less important than the rate of change. Rapid increases (thousands per second) may indicate excessive logging or database activity.

---

**General advice:**
- Watch for sudden spikes, steadily increasing values, or values that approach system limits.
- Use these sensors to set up Home Assistant automations or alerts for early warning of resource exhaustion.
- For more details on system health, also use Home Assistant's built-in system monitor integration.

