from enum import Enum, auto
import numbers

""" Enumeration of possible event types

Values include:
- PROC_ARRIVES: Denotes when a process first arrives at the system
- PROC_CPU_REQ: Denotes when a process transitions to the READY state and thus requests access to the CPU
- PROC_CPU_DONE: Denotes when a process needs no more CPU time and is thus terminated
"""
class EventTypes(Enum):
        PROC_ARRIVES = auto()
        PROC_CPU_REQ = auto()
        PROC_CPU_DONE = auto()
        
""" Encapsulates all necessary info for our events, to be used in queues

This class comes with three member variables: process_id, event_type and event_time
- process_id: The ID of the process that generated this event
- event_time: The time point at which this event takes place
- event_type: The type of this event (see EventTypes)
"""
class Event(object):
        """ Instantiates an Event object

        Parameters: 
        - process_id: The ID of the process that generated this event
        - event_time: The time point at which this event takes place
        - event_type: The type of this event (see EventTypes)
        """
        def __init__(self, *, process_id, event_type, event_time):
                if not isinstance(event_type, EventTypes):
                        raise ValueError("Value {} not an EventTypes object.".format(event_type))
                if not (isinstance(event_time, numbers.Real) and event_time >= 0):
                        raise ValueError("Value {} not a non-negative number.".format(event_time))
                if not (isinstance(process_id, int) and process_id >= 0):
                        raise ValueError("Value {} not a non-negative integer.".format(process_id))
                self._event_type = event_type
                self._event_time = event_time
                self._process_id = process_id

        @property
        def event_type(self):
                return self._event_type

        @property
        def event_time(self):
                return self._event_time

        @property
        def process_id(self):
                return self._process_id

        """ Less-than comparator, necessary as Event objects will be stored on a heap

        Sorts based solely on event time
        """
        def __lt__(self, other):
                if not isinstance(other, Event):
                        raise ValueError("Value {} not an Event.".format(other))
                return self.event_time < other.event_time

        """ Returns a string representation of this Event object
        """
        def __str__(self):
                return str(self.event_type) + " @ " + str(self.event_time) + " [#" + str(self.process_id) + "]"
