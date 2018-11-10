import math

from des import SchedulerDES
from event import Event, EventTypes
from process import ProcessStates

class FCFS(SchedulerDES):
        def scheduler_func(self, cur_event):
                proc_id = curr_event.process_id
                proc = self.processes[proc_id]
                print(proc)
                pass

        def dispatcher_func(self, cur_proc):
                pass

class SJF(SchedulerDES):
        def scheduler_func(self, cur_event):
                pass

        def dispatcher_func(self, cur_proc):
                pass

class RR(SchedulerDES):
        def scheduler_func(self, cur_event):
                pass

        def dispatcher_func(self, cur_proc):
                pass

class SRTF(SchedulerDES):
        def scheduler_func(self, cur_event):
                pass

        def dispatcher_func(self, cur_proc):
                pass