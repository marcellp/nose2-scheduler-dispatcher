import math

from des import SchedulerDES
from event import Event, EventTypes
from process import ProcessStates


class FCFS(SchedulerDES):
    def scheduler_func(self, cur_event):

        # If we get news that a process has arrived, send it to the dispatcher immediately.
        if cur_event.event_type == EventTypes.PROC_ARRIVES:
            return self.processes[cur_event.process_id]

    def dispatcher_func(self, cur_proc):

        """
        If we get the process from the scheduler, run it on the CPU until
        its service time is exhausted. Then, the process has been terminated.
        """
        if cur_proc.process_state == ProcessStates.READY:
            cur_proc.process_state = ProcessStates.RUNNING
            run_for = cur_proc.run_for(cur_proc.service_time, self.time)
            cur_proc.process_state = ProcessStates.TERMINATED

            return Event(process_id=cur_proc.process_id,
                         event_type=EventTypes.PROC_CPU_DONE,
                         event_time=self.time + run_for)


class SJF(SchedulerDES):
    def scheduler_func(self, cur_event):

        """
        If a new process arrives, look at our queue of processes.
        Find the one with the lowest service time and send it to the
        dispatcher for execution.
        """
        if cur_event.event_type == EventTypes.PROC_ARRIVES:
            valid_procs = filter(lambda proc: proc.process_state == ProcessStates.READY, self.processes)
            best_proc = min(valid_procs, key=lambda proc: proc.service_time)

            return best_proc

    def dispatcher_func(self, cur_proc):

        """
        Similarly, run the process on the CPU until its service time
        is exhausted. Then, the process is terminated.
        """
        if cur_proc.process_state == ProcessStates.READY:
            cur_proc.process_state = ProcessStates.RUNNING
            run_for = cur_proc.run_for(cur_proc.service_time, self.time)
            cur_proc.process_state = ProcessStates.TERMINATED

            return Event(process_id=cur_proc.process_id,
                         event_type=EventTypes.PROC_CPU_DONE,
                         event_time=self.time + run_for)


class RR(SchedulerDES):
    def scheduler_func(self, cur_event):
        """
        partition the list on the event that triggered the scheduler, default proc returned if
        there is a wrap around
        """

        host_proc = next(filter(lambda x: x.process_id == cur_event.process_id, self.processes))
        default_procs = list(filter(lambda x: x.process_state == ProcessStates.READY, self.processes))
        partition = filter(lambda x: x.arrival_time >= host_proc.arrival_time,default_procs)

        return next(partition,default_procs[0])

    def dispatcher_func(self, cur_proc):

        # Run the process up to the quantum time.
        cur_proc.process_state = ProcessStates.RUNNING
        run_for = cur_proc.run_for(self.quantum, self.time)

        """
        If we still have time left on this process, set it to be ready so we can get it again
        when we come back to it the next time. Also, send an interrupt to the scheduler so
        it can select the next process to be run.

        If we have execued this process to completion, we can terminate it.
        """
        if cur_proc.remaining_time > 0:
            cur_proc.process_state = ProcessStates.READY
            return Event(process_id=cur_proc.process_id,
                         event_type=EventTypes.PROC_CPU_REQ,
                         event_time=self.time + run_for)
        else:

            cur_proc.process_state = ProcessStates.TERMINATED
            return Event(process_id=cur_proc.process_id,
                         event_type=EventTypes.PROC_CPU_DONE,
                         event_time=self.time + run_for)


class SRTF(SchedulerDES):
    def scheduler_func(self, cur_event):

        """
        Get the process with the shortest remaining time of any ready process.
        Then, send it to the dispatcher.
        """
        valid_procs = filter(lambda proc: proc.process_state == ProcessStates.READY, self.processes)
        best_proc = min(valid_procs, key=lambda proc: proc.remaining_time)

        return best_proc

    def dispatcher_func(self, cur_proc):

        """
        If the process is ready to be executed, run it until the next event is scheduled to occur and interrupt,
        or if there are no more outstanding events, until the processs has been exhausted and terminated.
        """
        if cur_proc.process_state == ProcessStates.READY:
            cur_proc.process_state = ProcessStates.RUNNING
            run_for = cur_proc.run_for(self.next_event_time() - self.time, self.time)

            if cur_proc.remaining_time > 0:
                cur_proc.process_state = ProcessStates.READY
                return Event(process_id=cur_proc.process_id,
                             event_type=EventTypes.PROC_CPU_REQ,
                             event_time=self.time + run_for)
            else:
                cur_proc.process_state = ProcessStates.TERMINATED
                return Event(process_id=cur_proc.process_id,
                             event_type=EventTypes.PROC_CPU_DONE,
                             event_time=self.time + run_for)
