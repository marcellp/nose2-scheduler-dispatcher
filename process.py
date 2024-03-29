from enum import Enum
import logging
import math
import numbers

""" List of states in which a process can be.

A process starts in the NEW state. The runtime of a process is then alternating between CPU bursts
and waiting time (dependent on scheduling algorithm used). At the beginning of every CPU burst, the
process transitions to the READY state. When the scheduler assigns the CPU to a process P, it
transitions to the RUNNING state and remains at that state for as long as it has the CPU. When/if
the scheduler then preempts the process, it transitions back to the READY state and waits for the
scheduler to assign the CPU to it again. Finally, the process transitions to the TERMINATED state
when it has no more work to do.
"""
class ProcessStates(Enum):
        NEW = 0
        READY = 1
        RUNNING = 2
        TERMINATED = 3

""" Class that encodes all info related to a process

Contains the following fields:
- process_id: an integer uniquely identifying every process
- arrival_time: time point at which the process is added to the scheduler's list of processes
- process_state: the state in which the process is currently; starts at NEW (see ProcessStates)
- execution_times: a list of tuples each denoting when the CPU was given/taken away from the process
- departure_time: time point at which the process terminates
"""
class Process(object):

        """ Initialise a new process object
        
        - process_id: an integer uniquely identifying every process
        - arrival_time: time point at which the process is added to the scheduler's list of processes
        - service_time: duration of the process's CPU burst
        """
        def __init__(self, *, process_id, arrival_time, service_time):
                if not (isinstance(process_id, int) and process_id >= 0):
                        raise ValueError("Value {} not a non-negative (>= 0) integer.".format(process_id))
                if not (isinstance(arrival_time, numbers.Real) and arrival_time >= 0.0):
                        raise ValueError("Value {} not a positive (> 0) number.".format(arrival_time))
                if not (isinstance(service_time, numbers.Real) and service_time > 0.0):
                        raise ValueError("Value {} not a positive (> 0) number.".format(service_time))
                self._process_id = process_id
                self._arrival_time = arrival_time
                self._process_state = ProcessStates.NEW
                self._service_time = service_time
                self._remaining_time = service_time
                self._execution_times = []
                self._logger = logging.getLogger(__name__)

        @property
        def process_id(self):
                return self._process_id

        @property
        def arrival_time(self):
                return self._arrival_time

        @property
        def service_time(self):
                return self._service_time

        @property
        def process_state(self):
                return self._process_state

        @property
        def remaining_time(self):
                return self._remaining_time

        @process_state.setter
        def process_state(self, value):
                if not isinstance(value, ProcessStates):
                        raise ValueError("Value {} not a ProcessStates value.".format(value))
                self._process_state = value
        
        """ Returns the time at which this process terminated

        Will raise a ValueError if this process hasn't terminated at the time of calling this function
        """
        @property
        def departure_time(self):
                if self._process_state != ProcessStates.TERMINATED:
                        raise ValueError("Requested departure time of non-terminated process [#" + str(self._process_id) + "]")
                return self._execution_times[-1][1]

        """ Returns the total waiting time for this process
        """
        def waiting_time(self):
                sum_waiting_time = 0.0
                prev_time = self._arrival_time
                for t in self._execution_times:
                        sum_waiting_time += t[0] - prev_time
                        prev_time = t[1]
                return sum_waiting_time

        """ Returns the turnaround time for this process
        """
        def turnaround_time(self):
                return self.departure_time - self._arrival_time

        """ Returns a string representation of this Process object
        """
        def __str__(self):
                return "[#" + str(self._process_id) + "]: State: " + str(self._process_state) + ", Arrival: " + str(self._arrival_time) + ", Service: " + str(self._service_time) + ((", Departure: " + str(self.departure_time)) if self._process_state == ProcessStates.TERMINATED else (", Remaining: " + str(self._remaining_time)))

        """ Executes the current process for at most the requested quantum of time

        Arguments:
        - quantum: the maximum amount of time for which this process will execute
        - cur_time: the starting time for the execution

        This method takes into account the process's CPU burst. Specifically, if the process is currently in the
        midst of a CPU burst, it will execute it for the remainder of the burst or the quantum (whichever is smaller).

        Returns the amount of time for which the process actually executed.
        """
        def run_for(self, quantum, cur_time):
                actually_run_for = min(quantum, self._remaining_time)
                self._logger.debug("[#" + str(self._process_id) + "] actually run for " + str(actually_run_for))
                self._remaining_time -= actually_run_for

                self._execution_times.append((cur_time, cur_time + actually_run_for))
                return actually_run_for
