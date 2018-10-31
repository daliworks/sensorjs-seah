#!/usr/bin/env python
# scripts/examples/simple_data_store.py
import logging
import threading
import time
import random
from socketserver import TCPServer
from collections import defaultdict
 
from umodbus import conf
from umodbus.server.tcp import RequestHandler, get_server
from umodbus.utils import log_to_stream

OPERATION_STATUS_STOP = 0
OPERATION_STATUS_RUN = 1
OPERATION_STATUS_CHARGE = 2
OPERATION_STATUS_DISCHARGE = 3
OPERATION_STATUS_FAILURE = 4

CONTROL_STATUS_AUTO = 0
CONTROL_STATUS_MANUAL = 1
CONTROL_STATUS_MANUAL_CHARGE = 2
CONTROL_STATUS_MANUAL_DISCHARGE = 3

COMMUNICATION_STATUS_OK = 0
COMMUNICATION_STATUS_ERROR = 1

# Add stream handler to logger 'uModbus'.
log_to_stream(level=logging.DEBUG)
class	value_set:
	def __init__(self, min, max):
		self.value = 0
		self.max = max
		self.min = min

	def	addValue(self, value):
		temp = self.value + value
		self.setValue(temp)

	def	subValue(self, value):
		temp = self.value - value
		self.setValue(temp)

	def addRandomValue(self, rate=10):
		offset = (self.max - self.min + 1) * rate / 100 / 2
		if offset == 0:
			offset = 1

		self.addValue(random.randint(-offset, offset))

	def	setValue(self, value):
		if self.min <= value and value <= self.max:
			self.value = value
		elif self.min > value:
			self.value = self.min
		else:
			self.value = self.max

	def getValue(self):
		return	self.value	

class	DeviceEMS(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self) 
		self.storageCapacity = value_set(0, 30000)
		self.hourlyGenerationAmount = value_set(0, 30000)
		self.hourlyChargeAmount = value_set(0, 30000)
		self.hourlyDischargeAmount = value_set(0, 30000)
		self.hourlyOutputAmount = value_set(0, 30000)

	def	run(self):
		while True:
			generation = random.randint(1, 100)
			output = random.randint(1, 100)

			self.hourlyGenerationAmount.addValue(generation)
			if generation > output:
				diff = generation - output
				if diff > (self.storageCapacity.max - self.storageCapacity.value):
					diff = self.storageCapacity.max - self.storageCapacity.getValue()
				self.hourlyChargeAmount.addValue(diff)
				self.storageCapacity.addValue(diff)
			elif generation < output:
				diff = output - generation
				if self.storageCapacity.getValue() < diff:
					diff = self.storageCapacity.getValue()
					output = generation + diff	
				self.hourlyDischargeAmount.addValue(diff)
				self.storageCapacity.subValue(diff)
			self.hourlyOutputAmount.addValue(output)

			time.sleep(10)

class	DevicePMS(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.operationStatus = value_set(0, 4)
		self.controlStatus = value_set(0, 3)
		self.communicationStatus = value_set(0, 1)
		self.operationControl = value_set(0, 4)
		self.manualControl = value_set(-30000, 30000)

	def	run(self):
		while True:
			if self.operationStatus.getValue() == self.operationStatus.max:
				self.operationStatus.setValue(0)
			else:
				self.operationStatus.addValue(1)

			if self.controlStatus.getValue() == self.controlStatus.max:
				self.controlStatus.setValue(0)
			else:
				self.controlStatus.addValue(1)

			if random.randint(1, 100) == 1:
				self.communicationStatus.setValue(0)
			else:
				self.communicationStatus.addValue(1)
			time.sleep(10)
    				
class	DeviceSP(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self) 
		self.linePower  = value_set(-30000, 30000)
		self.breakerStatusLine = value_set(0, 2)
		self.breakerStatusGenerator = value_set(0, 2)
		self.breakerStausESS = value_set(0, 2)
		self.voltageInputDC = value_set(0, 10000)
		self.currentInputDC = value_set(0, 30000)
		self.voltageUV = value_set(0, 5000)
		self.voltageVW = value_set(0, 5000)
		self.voltageWU = value_set(0, 5000)
		self.currentAB = value_set(0, 30000)
		self.currentBC = value_set(0, 30000)
		self.currentCA = value_set(0, 30000)
		self.currentOuptut = value_set(0, 30000)
		self.temperature = value_set(0, 990)
		self.status = value_set(0, 3)
		self.errorCode = value_set(0, 10)

	def	run(self):
		while True:
			self.linePower.addRandomValue()
			self.breakerStatusLine.addRandomValue()
			self.breakerStatusGenerator.addRandomValue()
			self.breakerStausESS.addRandomValue()
			self.voltageInputDC.addRandomValue()
			self.currentInputDC.addRandomValue()
			self.voltageUV.addRandomValue()
			self.voltageVW.addRandomValue()
			self.voltageWU.addRandomValue()
			self.currentAB.addRandomValue()
			self.currentBC.addRandomValue()
			self.currentCA.addRandomValue()
			self.currentOuptut.addRandomValue()
			self.temperature.addRandomValue()
			self.status.addRandomValue()
			self.errorCode.addRandomValue()

			time.sleep(10)

class	DevicePCS(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self) 
		self.voltageInput = value_set(0, 10000)
		self.currentInput = value_set(0, 30000)
		self.voltageUV = value_set(0, 5000)
		self.voltageVW = value_set(0, 5000)
		self.voltageWU = value_set(0, 5000)
		self.currentAB = value_set(0, 30000)
		self.currentBC = value_set(0, 30000)
		self.currentCA = value_set(0, 30000)
		self.chargeDischargePower = value_set(0, 30000)
		self.temperature = value_set(0, 990)
		self.status = value_set(0, 4)
		self.controlMode = value_set(0, 1)
		self.warningCode = value_set(0, 10)
		self.errorCode = value_set(0, 10)		

	def	run(self):
		while True:
			self.voltageInput.addRandomValue()
			self.currentInput.addRandomValue()
			self.voltageUV.addRandomValue()
			self.voltageVW.addRandomValue()
			self.voltageWU.addRandomValue()
			self.currentAB.addRandomValue()
			self.currentBC.addRandomValue()
			self.currentCA.addRandomValue()
			self.chargeDischargePower.addRandomValue()
			self.temperature.addRandomValue()
			self.status.addRandomValue()
			self.controlMode.addRandomValue()
			self.warningCode.addRandomValue()
			self.errorCode.addRandomValue()

			time.sleep(10)
    			
class	DeviceBAT(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self) 
		self.voltage = value_set(0, 10000)
		self.current = value_set(1, 30000)
		self.soc = value_set(1, 1000)
		self.soh = value_set(0, 1000)
		self.cellMaxTemperature = value_set(0, 990)
		self.cellMinTemperature = value_set(0, 990)
		self.cellMaxVoltage = value_set(0, 8000)
		self.cellMinVoltage = value_set(0, 8000)
		self.status = value_set(0, 4)
		self.waringCode = value_set(0, 10)
		self.errorCode = value_set(0, 10)

	def	run(self):
		while True:
			self.voltage.addRandomValue()
			self.current.addRandomValue()
			self.soc.addRandomValue()
			self.soh.addRandomValue()
			self.cellMaxTemperature.addRandomValue()
			self.cellMinTemperature.addRandomValue()
			self.cellMaxVoltage.addRandomValue()
			self.cellMinVoltage.addRandomValue()
			self.status.addRandomValue()
			self.waringCode.addRandomValue()
			self.errorCode.addRandomValue()

class TESTCORE(threading.Thread):
	def __init__(self, data_store):
		threading.Thread.__init__(self) 
		self.data_store = data_store
		self.ems = DeviceEMS()
		self.pms = DevicePMS()
		self.sp = DeviceSP()
		self.pcs = DevicePCS()
		self.bat = DeviceBAT()
		self.data_store[40001] = self.ems.hourlyGenerationAmount
		self.data_store[40002] = self.ems.hourlyChargeAmount
		self.data_store[40003] = self.ems.hourlyDischargeAmount
		self.data_store[40004] = self.ems.hourlyOutputAmount
		self.data_store[40011] = self.pms.operationStatus
		self.data_store[40012] = self.pms.controlStatus
		self.data_store[40013] = self.pms.communicationStatus
		self.data_store[40014] = self.pms.operationControl
		self.data_store[40015] = self.pms.manualControl
		self.data_store[40061] = self.sp.linePower
		self.data_store[40062] = self.sp.breakerStatusLine
		self.data_store[40064] = self.sp.breakerStatusGenerator
		self.data_store[40064] = self.sp.breakerStausESS
		self.data_store[40071] = self.sp.voltageInputDC
		self.data_store[40072] = self.sp.currentInputDC
		self.data_store[40073] = self.sp.voltageUV
		self.data_store[40074] = self.sp.voltageVW
		self.data_store[40075] = self.sp.voltageWU
		self.data_store[40076] = self.sp.currentAB
		self.data_store[40077] = self.sp.currentBC
		self.data_store[40078] = self.sp.currentCA
		self.data_store[40079] = self.sp.currentOuptut
		self.data_store[40080] = self.sp.temperature
		self.data_store[40081] = self.sp.status
		self.data_store[40082] = self.sp.errorCode
		self.data_store[40091] = self.pcs.voltageInput
		self.data_store[40092] = self.pcs.currentInput
		self.data_store[40093] = self.pcs.voltageUV
		self.data_store[40094] = self.pcs.voltageVW
		self.data_store[40095] = self.pcs.voltageWU
		self.data_store[40096] = self.pcs.currentAB
		self.data_store[40097] = self.pcs.currentBC
		self.data_store[40098] = self.pcs.currentCA
		self.data_store[40099] = self.pcs.chargeDischargePower
		self.data_store[40100] = self.pcs.temperature
		self.data_store[40101] = self.pcs.status
		self.data_store[40102] = self.pcs.controlMode
		self.data_store[40103] = self.pcs.warningCode
		self.data_store[40108] = self.pcs.errorCode
		self.data_store[40115] = self.bat.voltage
		self.data_store[40116] = self.bat.current
		self.data_store[40117] = self.bat.soc
		self.data_store[40118] = self.bat.soh
		self.data_store[40119] = self.bat.cellMaxTemperature
		self.data_store[40120] = self.bat.cellMinTemperature
		self.data_store[40121] = self.bat.cellMaxVoltage
		self.data_store[40122] = self.bat.cellMinVoltage
		self.data_store[40123] = self.bat.status
		self.data_store[40124] = self.bat.waringCode
		self.data_store[40130] = self.bat.errorCode

	def run(self):
		self.ems.start()
		self.pms.start()
		self.sp.start()
		self.pcs.start()
		self.bat.start()

		while True:
			time.sleep(1)

class MBTCPSERVER(threading.Thread):
	def __init__(self, data_store):
		threading.Thread.__init__(self) 
		# A very simple data store which maps addresses against their values.
		self.data_store = data_store

		# Enable values to be signed (default is False).
		conf.SIGNED_VALUES = True

		TCPServer.allow_reuse_address = True
		self.app = get_server(TCPServer, ('0.0.0.0', 502), RequestHandler)
		print(self.app)

		@self.app.route(slave_ids=[1], function_codes=[1, 3, 4], addresses=list(range(0, 1000)))
		def read_data_store(slave_id, function_code, address):
			try:
				"""" Return value of address. """
				print('Read Data :', function_code, address)
				if (function_code == 3):
					return self.data_store[40000 + address].value
				else:
					return self.data_store[30000 + address].value
			except:
				return 0


		@self.app.route(slave_ids=[1], function_codes=[5, 15], addresses=list(range(0, 1000)))
		def write_data_store(slave_id, function_code, address, value):
			try:
 				"""" Set value for address. """
				print('Write Data :', function_code, address, value)
				self.data_store[function_code * 10000 + address].setValue(value)
			except:
				print('Exception')

	def run(self):
		self.app.serve_forever()
	
	def stop(self):
		self.app.shutdown()
		self.app.server_close()
  
if __name__ == '__main__':
    try:
		data_store =  defaultdict(value_set)
		test = TESTCORE(data_store)
		server = MBTCPSERVER(data_store)
		test.start()
		server.start()
    except Exception as err:
		print(err)