import time
import statistics
import numpy as np 

### functions/ process
def spin_process():
	# mu: 180s, sigma: 120s
	return abs(np.random.normal(3,2)) # in mins

def weave_process():
	# mean: 360s
	return np.random.exponential(1/6)

def finish_process():
	# mu: 300s, sigma: 300s
	return abs(np.random.normal(5,5))

def pack_process():
	# mean: 60s
	return np.random.exponential(1.0)


####################################
class simulation:
	
	def __init__(self):
		self.max_sp_mech = 10
		self.max_wv_mech = 10
		self.max_fn_mech = 10
		self.max_pk_mech = 10
		self.idle_sp_mech = self.max_sp_mech
		self.idle_wv_mech = self.max_wv_mech
		self.idle_fn_mech = self.max_fn_mech
		self.idle_pk_mech = self.max_pk_mech
		self.num_in_sys = 25 # start with 25 units in the system, add when 1 unit pass the packing process
		self.num_in_sp_queue = self.num_in_sys ## self.num_in_sys - self.idle_sp_mech # 10 unit will be put in the machine, then the queue will be 25 unit - idle machine
		self.num_in_wv_queue = 0
		self.num_in_fn_queue = 0
		self.num_in_pk_queue = 0
		self.final_product = 0
		self.clock = 0.0

		####
		self.sp_idle_time = 0
		self.wv_idle_time = 0
		self.fn_idle_time = 0
		self.pk_idle_time = 0

		####
		self.sp_q_cost = 150
		self.wv_q_cost = 250
		self.fn_q_cost = 300
		self.pk_q_cost = 450
		self.sp_q_no = 0
		self.wv_q_no = 0
		self.fn_q_no = 0
		self.pk_q_no = 0

	def batch(self):
		self.spining()
		self.weaving()
		self.finishing()
		self.packing()

	def advance_time(self):
		self.batch()
		
		try:
			P1 = min(spin_proc)
		except ValueError:
			P1 = float('inf')
		try:
			P2 = min(weav_proc)
		except ValueError:
			P2 = float('inf')
		try:
			P3 = min(fini_proc) 
		except ValueError:
			P3 = float('inf')
		try:
			P4 = min(pack_proc)
		except ValueError:
			P4 = float('inf')
		
		t_event = min(P1, P2, P3, P4)

		#### 
		self.sp_idle_time = self.idle_sp_mech * t_event
		self.wv_idle_time = self.idle_wv_mech * t_event
		self.fn_idle_time = self.idle_fn_mech * t_event
		self.pk_idle_time = self.idle_pk_mech * t_event

		####
		self.sp_q_no += self.num_in_sp_queue
		self.wv_q_no += self.num_in_wv_queue
		self.fn_q_no += self.num_in_fn_queue
		self.pk_q_no += self.num_in_pk_queue


		if t_event == P1:
			self.handle_sp_process()
		if t_event == P2:
			self.handle_wv_process()
		if t_event == P3:
			self.handle_fn_process()
		if t_event == P4:
			self.handle_pk_process()

		self.clock = self.clock + t_event


	def handle_sp_process(self):
		spin_proc.pop(spin_proc.index(min(spin_proc)))
		self.idle_sp_mech += 1
		# self.num_in_sp_queue -= 1 # finished 1 unit(e.g. unit A)
		self.num_in_wv_queue += 1
	
	def handle_wv_process(self):
		weav_proc.pop(weav_proc.index(min(weav_proc)))
		self.idle_wv_mech += 1
		# self.num_in_wv_queue -= 1
		self.num_in_fn_queue += 1

	def handle_fn_process(self):
		fini_proc.pop(fini_proc.index(min(fini_proc)))
		self.idle_fn_mech += 1
		# self.num_in_fn_queue -= 1
		self.num_in_pk_queue += 1
		pass

	def handle_pk_process(self):
		pack_proc.pop(pack_proc.index(min(pack_proc)))
		self.idle_pk_mech += 1
		# self.num_in_pk_queue -= 1
		self.num_in_sys -= 1
		self.final_product += 1
		if self.clock <= 480: # one shift is 480min(8hrs)
			self.num_in_sys += 1
			self.num_in_sp_queue += 1
		else:
			pass		

	def spining(self):
		# after the first batch of units, idling of sp_mach will happen when they are waiting one of those 25 units finish by the pack stage
		proc_added = 0
		if self.num_in_sp_queue > self.idle_sp_mech:
			if self.idle_sp_mech != 0:
				for _ in range(self.idle_sp_mech):
					self.num_in_sp_queue -= 1 # testing
					spin_proc.append(spin_process()) # finish time of the process
					proc_added += 1
		else: # I > Q run Q times
			for _ in range(self.num_in_sp_queue):
				self.num_in_sp_queue -= 1 # testing
				spin_proc.append(spin_process())
				proc_added += 1
		self.idle_sp_mech -= proc_added

	def weaving(self):
		proc_added = 0
		if self.num_in_wv_queue > self.idle_wv_mech:
			if self.idle_wv_mech != 0:
				for _ in range(self.idle_wv_mech):
					self.num_in_wv_queue -= 1 # testing
					weav_proc.append(weave_process()) # finish time of the process
					proc_added += 1
		else:
			for _ in range(self.num_in_wv_queue):
				self.num_in_wv_queue -= 1
				weav_proc.append(weave_process())
				proc_added += 1
		self.idle_wv_mech -= proc_added

	def finishing(self):
		proc_added = 0
		if self.num_in_fn_queue > self.idle_fn_mech:
			if self.idle_fn_mech != 0:
				for _ in range(self.idle_fn_mech):
					self.num_in_fn_queue -= 1
					fini_proc.append(finish_process()) # finish time of the process
					proc_added += 1
		else:
			for _ in range(self.num_in_fn_queue):
				self.num_in_fn_queue -= 1
				fini_proc.append(finish_process())
				proc_added += 1
		self.idle_fn_mech -= proc_added

	def packing(self):
		proc_added = 0
		if self.num_in_pk_queue > self.idle_pk_mech:
			if self.idle_pk_mech != 0:
				for _ in range(self.idle_pk_mech):
					self.num_in_pk_queue -= 1
					pack_proc.append(pack_process()) # finish time of the process
					proc_added += 1
		else:
			for _ in range(self.num_in_pk_queue):
				self.num_in_pk_queue -= 1
				pack_proc.append(pack_process())
				proc_added += 1
		self.idle_pk_mech -= proc_added
		if inf in pack_proc:
			pack_proc.pop(pack_proc.index(inf))

##########################
spin_proc = []
weav_proc = []
fini_proc = []
pack_proc = []

inf = float('inf')
# np.random.seed(0) # lock the random state


result_idle_sp = []
result_idle_wv = []
result_idle_fn = []
result_idle_pk = []
result_idle_ttl = []
result_qc_sp = []
result_qc_wv = []
result_qc_fn = []
result_qc_pk = []
result_qc_ttl = []

weekly = 21
monthly = weekly * 4
trials = monthly

### lock random seed
start = time.perf_counter()
record_idx_1 = []
record_ttl_idle_1 = []
record_ttl_qc_1 = []
for sp in range(1,3):
  for wv in range(1,11):
    for fn in range(1,11):
      for pk in range(1,11):
        # np.random.seed(488) # lock the random state
        x = simulation()
        x.max_sp_mech = sp
        x.max_wv_mech = wv
        x.max_fn_mech = fn
        x.max_pk_mech = pk

        result_idle_sp = []
        result_idle_wv = []
        result_idle_fn = []
        result_idle_pk = []
        result_idle_ttl = []
        result_qc_sp = []
        result_qc_wv = []
        result_qc_fn = []
        result_qc_pk = []
        result_qc_ttl = []

        for _ in range(21):
          while x.clock <= 480:
            x.advance_time()
          result_idle_sp.append(x.sp_idle_time)
          result_idle_wv.append(x.wv_idle_time)
          result_idle_fn.append(x.fn_idle_time)
          result_idle_pk.append(x.pk_idle_time)
          idle = x.sp_idle_time + x.wv_idle_time + x.fn_idle_time + x.pk_idle_time
          result_idle_ttl.append(idle)
          qc_sp = x.sp_q_no / x.clock * x.sp_q_cost
          qc_wv = x.wv_q_no / x.clock * x.wv_q_cost
          qc_fn = x.fn_q_no / x.clock * x.fn_q_cost
          qc_pk = x.pk_q_no / x.clock * x.pk_q_cost
          qc_ttl = qc_sp + qc_wv + qc_fn + qc_pk
          result_qc_sp.append(qc_sp)
          result_qc_wv.append(qc_wv)
          result_qc_fn.append(qc_fn)
          result_qc_pk.append(qc_pk)
          result_qc_ttl.append(qc_ttl)

        idx = []
        idx.append(sp)
        idx.append(wv)
        idx.append(fn)
        idx.append(pk)

        record_idx_1.append(idx)
        record_ttl_idle_1.append(statistics.mean(result_idle_ttl))
        record_ttl_qc_1.append(statistics.mean(result_qc_ttl))


print('min idle time machine comb: ', record_idx_1[record_ttl_idle_1.index(min(record_ttl_idle_1))])
# print('min queue cost machine comb:', record_idx_1[record_ttl_qc_1.index(min(record_ttl_qc_1))])
finish = time.perf_counter()
print(f'Finished in {round(finish-start, 2)} second(s)')
print()
print('max idle time:', max(record_ttl_idle_1))
print('min idle time:', min(record_ttl_idle_1))
print('avg idle time:', statistics.mean(record_ttl_idle_1))
# print()
# print('max queue c:  ', max(record_ttl_qc_1))
# print('min queue c:  ', min(record_ttl_qc_1))
# print('avg queue c:  ', statistics.mean(record_ttl_qc_1))

# print('min idle time machine comb: ', record_idx_1[record_ttl_idle_1.index(min(record_ttl_idle_1))])
# print('min queue cost machine comb:', record_idx_1[record_ttl_qc_1.index(min(record_ttl_qc_1))])
print('respective q cost: ', record_ttl_qc_1[record_ttl_idle_1.index(min(record_ttl_idle_1))])

new_save = open('.\\1stbatch.txt','w')
new_save.write('\nmin idle time machine comb: '+str(record_idx_1[record_ttl_idle_1.index(min(record_ttl_idle_1))]))
# new_save.write('min queue cost machine comb:'+str(record_idx_1[record_ttl_qc_1.index(min(record_ttl_qc_1))]))
new_save.write('\nmax idle time: '+str(max(record_ttl_idle_1)))
new_save.write('\nmin idle time: '+str(min(record_ttl_idle_1)))
new_save.write('\navg idle time: '+str(statistics.mean(record_ttl_idle_1)))
new_save.write('\nrespective queue cost: '+str(record_ttl_qc_1[record_ttl_idle_1.index(min(record_ttl_idle_1))]))
# new_save.write('max queue c:  '+str(max(record_ttl_qc_1)))
# new_save.write('min queue c:  '+str(min(record_ttl_qc_1)))
# new_save.write('avg queue c:  '+str(statistics.mean(record_ttl_qc_1)))
# new_save.write('min idle time machine comb: '+str(record_idx_1[record_ttl_idle_1.index(min(record_ttl_idle_1))]))
# new_save.write('min queue cost machine comb:'+str(record_idx_1[record_ttl_qc_1.index(min(record_ttl_qc_1))]))
new_save.close()
