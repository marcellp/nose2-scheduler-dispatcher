import math

from des import SchedulerDES
from event import Event, EventTypes
from process import ProcessStates

class FCFS(SchedulerDES):
	def scheduler_func(self, cur_event):
		print("[{}]	Event arrives ({})".format(self.time, cur_event.event_type))
		
		# The only state we allow here is a new event, send it to the scheduler to run until it finishes.
		if cur_event.event_type == EventTypes.PROC_ARRIVES:
			print("[{}]	Process {} sent to dispatcher.".format(self.time, cur_event.process_id))
			return self.processes[cur_event.process_id]
		
	def dispatcher_func(self, cur_proc):
		print("[{}]	Dispatcher gets process #{}, in state {}, service time: {}".format(
			self.time, cur_proc.process_id, cur_proc.process_state, cur_proc.service_time))

		if cur_proc.process_state == ProcessStates.READY:
			cur_proc.process_state = ProcessStates.RUNNING
			cur_proc.run_for(cur_proc.service_time, self.time)
			cur_proc.process_state = ProcessStates.TERMINATED

			print("[{}]	Dispatcher ran process #{}, for {}.".format(self.time, cur_proc.process_id, cur_proc.service_time))

			return Event(   process_id = cur_proc.process_id,
					event_type=EventTypes.PROC_CPU_DONE,
					event_time = self.time + cur_proc.service_time)



class SJF(SchedulerDES):
	def scheduler_func(self, cur_event):
		print("[{}]	Event arrives ({})".format(self.time, cur_event.event_type))

		if cur_event.event_type == EventTypes.PROC_ARRIVES:
			valid_procs = filter(lambda proc: proc.process_state == ProcessStates.READY, self.processes)
			best_proc = min(valid_procs, key=lambda proc: proc.service_time)

			print("[{}]	Shortest process is {} with service time {}, sending to dispatcher.".format(self.time, best_proc.process_id, best_proc.service_time))
			return best_proc

	def dispatcher_func(self, cur_proc):
		print("[{}]	Dispatcher gets process #{}, in state {}, service time: {}".format(
			self.time, cur_proc.process_id, cur_proc.process_state, cur_proc.service_time))

		if cur_proc.process_state == ProcessStates.READY:
			cur_proc.process_state = ProcessStates.RUNNING
			cur_proc.run_for(cur_proc.service_time, self.time)
			cur_proc.process_state = ProcessStates.TERMINATED

			print("[{}]	Dispatcher ran process #{}, for {}.".format(self.time, cur_proc.process_id, cur_proc.service_time))

			return Event(   process_id = cur_proc.process_id,
					event_type=EventTypes.PROC_CPU_DONE,
					event_time = self.time + cur_proc.service_time)

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