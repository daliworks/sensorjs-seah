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

CONF_PRESSURE_MAX=10000
CONF_TEMPERATURE_MIN=200
CONF_TEMPERATURE_MAX=1000
CONF_VIBRATION_MAX=10000
CONF_CURRENT_MAX=1000
CONF_RATIO_MAX=1000
CONF_COUNT_MAX=32767

# Add stream handler to logger 'uModbus'.
log_to_stream(level=logging.DEBUG)
class	SensorSim:
	def __init__(self, min=0, max=1):
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
		if (self.max > 1):
			offset = (self.max - self.min + 1) * rate / 100
			if offset == 0:
				offset = 1

			try: 
				self.addValue(offset / 2 - random.randint(0, offset))
			except Exception as inst:
				print('addValue :', offset)

		else:
			if random.randint(0, 100) < 50:
				self.setValue(self.min)
			else:
				self.setValue(self.max)

	def incValue(self, rate=1):
		try: 
			newValue = self.value + rate
			if self.min <= newValue and newValue <= self.max:
				self.value = newValue
			elif self.min > newValue:
				self.value = self.max
			else:
				self.value = self.min
		except Exception as inst:
			print('incValue :', rate)

	def	setValue(self, value):
		if self.min <= value and value <= self.max:
			self.value = value
		elif self.min > value:
			self.value = self.min
		else:
			self.value = self.max

	def getValue(self):
		return	self.value	

class	ValueSet(object):
	def __init__(self):
		self.value = 0

	def setValue(self, sensor = 0):
		if sensor != 0:
			self.value = sensor.getValue()

	def getValue(self):
		return	self.value

	def clearFlags(self):
		self.value=0

	def addFlag(self, index, flag):
		if flag.getValue() != 0:
			self.value = self.value | (1 << index)

class	DeviceBlower(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self) 
		self.xReset=SensorSim(0,1)
		self.xRunOper=SensorSim(0,1)
		self.xStopOper=SensorSim(0,1)
		self.xSpeedOper=SensorSim(0,1)
		self.xFlowOper=SensorSim(0,1)
		self.xPowerOper=SensorSim(0,1)
		self.xPropotionOper=SensorSim(0,1)
		self.xDOxygenOper=SensorSim(0,1)
		self.xPresOper=SensorSim(0,1)
		self.xMCPEmrgRls=SensorSim(0,1)
		self.xRemoteCheckPulse=SensorSim(0,1)
		self.xPrimarySV=SensorSim(0,1000) 
		self.xSecondarySV=SensorSim(0,1000) 
		self.xRepeatOper=SensorSim(0,1)
		self.xBOVRun=SensorSim(0,1)
		self.xAuxRun=SensorSim(0,1)
		self.xRestartDelay=SensorSim(0,1)
		self.xSurgeControl=SensorSim(0,1)
		self.xPowerControl=SensorSim(0,1)
		self.xDriveReady=SensorSim(0,1)
		self.xBlowReady=SensorSim(0,1)
		self.xRunStatus=SensorSim(0,1)
		self.xStopStatus=SensorSim(0,1)
		self.xResetStatus=SensorSim(0,1)
		self.xEmrgStopRlsTrip=SensorSim(0,1)
		self.xEOCRlsTrip=SensorSim(0,1)
		self.xFeedTrip=SensorSim(0,1)
		self.xSurgeTrip=SensorSim(0,1)
		self.xDriveCommTrip=SensorSim(0,1)
		self.xRemoteCommTrip=SensorSim(0,1)
		self.xDischargePresHighTrip=SensorSim(0,1)
		self.xFilterPresHighTrip=SensorSim(0,1)
		self.xPumpPresHighTrip=SensorSim(0,1)
		self.xPumpPresLowTrip=SensorSim(0,1)
		self.xSuctionPresHighTrip=SensorSim(0,1)
		self.xMoterTempHighTrip=SensorSim(0,1)
		self.xVibrationTrip=SensorSim(0,1)
		self.xBearingTempHighTrip=SensorSim(0,1)
		self.xDriveTempHighTrip=SensorSim(0,1)
		self.xSuctionPresSensorFault=SensorSim(0,1)
		self.xDischargePresSensorFault=SensorSim(0,1)
		self.xFilterPresSensorFault=SensorSim(0,1)
		self.xPumpPresSensorFault=SensorSim(0,1)
		self.xUnknownDriveTrip=SensorSim(0,1)
		self.xOvervoltageTrip=SensorSim(0,1)
		self.xLowvoltageTrip=SensorSim(0,1)
		self.xDixoTrip=SensorSim(0,1)
		self.xDooxTrip=SensorSim(0,1)
		self.xOverheatingTrip=SensorSim(0,1)
		self.xFuseTrip=SensorSim(0,1)
		self.xOverloadTrip=SensorSim(0,1)
		self.xOvercurrentTrip=SensorSim(0,1)
		self.xOverspeedTrip=SensorSim(0,1)
		self.xDzsxTrip=SensorSim(0,1)
		self.xShortTrip=SensorSim(0,1)
		self.xCommErrorTrip=SensorSim(0,1)
		self.xFanErrorTrip=SensorSim(0,1)
		self.xMotorOvercurrentTrip=SensorSim(0,1)
		self.xDriveReadyErrorTrip=SensorSim(0,1)
		self.xStartReadyTrip=SensorSim(0,1)
		self.xRemoteControlStatus=SensorSim(0,1)
		self.xRunStatus=SensorSim(0,1)
		self.xWarningStatus=SensorSim(0,1)
		self.xFaultStatus=SensorSim(0,1)
		self.xDriveRunStatus=SensorSim(0,1)
		self.xSpeedModeStatus=SensorSim(0,1)
		self.xFlowModeStatus=SensorSim(0,1)
		self.xPowerModeStatus=SensorSim(0,1)
		self.xPropotionModeStatus=SensorSim(0,1)
		self.xDOxygenModeStatus=SensorSim(0,1)
		self.xPresModeStatus=SensorSim(0,1)
		self.xCommScanPluse=SensorSim(0,1)
		self.xDischargePresWarning=SensorSim(0,1)
		self.xFliterPresWarning=SensorSim(0,1)
		self.xPumpPresUpWarning=SensorSim(0,1)
		self.xPumpPresDownWarning=SensorSim(0,1)
		self.xSuctionTempUpWarning=SensorSim(0,1)
		self.xDischargeTempUpWarning=SensorSim(0,1)
		self.xMotorTempUpWarning=SensorSim(0,1)
		self.xAirTempUpWarning=SensorSim(0,1)
		self.xAirTempDownWarning=SensorSim(0,1)
		self.xDriveTempUpWarning=SensorSim(0,1)
		self.xPresSensorFaultWarning=SensorSim(0,1)
		self.xTempSensorFaultWarning=SensorSim(0,1)
		self.xFlow=SensorSim(0,10000)
		self.xDischargePres=SensorSim(0,CONF_PRESSURE_MAX) 
		self.xAirTemp=SensorSim(CONF_TEMPERATURE_MIN / 10,CONF_TEMPERATURE_MAX / 10) 
		self.xMotorTemp=SensorSim(CONF_TEMPERATURE_MIN / 10,CONF_TEMPERATURE_MAX / 10) 
		self.xDriveTemp=SensorSim(CONF_TEMPERATURE_MIN / 10,CONF_TEMPERATURE_MAX / 10) 
		self.xDischargeTemp=SensorSim(CONF_TEMPERATURE_MIN / 10,CONF_TEMPERATURE_MAX / 10) 
		self.xPowerConsumption=SensorSim(0,10000)
		self.xMotorCurrent=SensorSim(0,CONF_CURRENT_MAX)
		self.xFrequency=SensorSim(0, 10000)
		self.xMotorFrequency=SensorSim(0, 10000)
		self.xStartCount=SensorSim(0, 10000)
		self.xRunningDays=SensorSim(0, 10000)
		self.xRunningHours=SensorSim(0, 10000)
		self.xRunningMinutes=SensorSim(0, 10000)
		self.xFilterPres=SensorSim(0,CONF_PRESSURE_MAX) 
		self.xSuctionPres=SensorSim(0,CONF_PRESSURE_MAX) 
		self.xVibration=SensorSim(0,CONF_VIBRATION_MAX)
		self.xBearingTemp=SensorSim(CONF_TEMPERATURE_MIN / 10,CONF_TEMPERATURE_MAX / 10) 
		self.xNumber=SensorSim(0, 10000)

	def	run(self):
		while True:
			self.xReset.incValue()
			self.xRunOper.incValue()
			self.xStopOper.incValue()
			self.xSpeedOper.incValue()
			self.xFlowOper.incValue()
			self.xPowerOper.incValue()
			self.xPropotionOper.incValue()
			self.xDOxygenOper.incValue()
			self.xPresOper.incValue()
			self.xMCPEmrgRls.incValue()
			self.xRemoteCheckPulse.incValue()
			self.xPrimarySV.incValue()
			self.xSecondarySV.incValue()
			self.xRepeatOper.incValue()
			self.xBOVRun.incValue()
			self.xAuxRun.incValue()
			self.xRestartDelay.incValue()
			self.xSurgeControl.incValue()
			self.xPowerControl.incValue()
			self.xDriveReady.incValue()
			self.xBlowReady.incValue()
			self.xRunStatus.incValue()
			self.xStopStatus.incValue()
			self.xResetStatus.incValue()
			self.xEmrgStopRlsTrip.incValue()
			self.xEOCRlsTrip.incValue()
			self.xFeedTrip.incValue()
			self.xSurgeTrip.incValue()
			self.xDriveCommTrip.incValue()
			self.xRemoteCommTrip.incValue()
			self.xDischargePresHighTrip.incValue()
			self.xFilterPresHighTrip.incValue()
			self.xPumpPresHighTrip.incValue()
			self.xPumpPresLowTrip.incValue()
			self.xSuctionPresHighTrip.incValue()
			self.xMoterTempHighTrip.incValue()
			self.xVibrationTrip.incValue()
			self.xBearingTempHighTrip.incValue()
			self.xDriveTempHighTrip.incValue()
			self.xSuctionPresSensorFault.incValue()
			self.xDischargePresSensorFault.incValue()
			self.xFilterPresSensorFault.incValue()
			self.xPumpPresSensorFault.incValue()
			self.xUnknownDriveTrip.incValue()
			self.xOvervoltageTrip.incValue()
			self.xLowvoltageTrip.incValue()
			self.xDixoTrip.incValue()
			self.xDooxTrip.incValue()
			self.xOverheatingTrip.incValue()
			self.xFuseTrip.incValue()
			self.xOverloadTrip.incValue()
			self.xOvercurrentTrip.incValue()
			self.xOverspeedTrip.incValue()
			self.xDzsxTrip.incValue()
			self.xShortTrip.incValue()
			self.xCommErrorTrip.incValue()
			self.xFanErrorTrip.incValue()
			self.xMotorOvercurrentTrip.incValue()
			self.xDriveReadyErrorTrip.incValue()
			self.xStartReadyTrip.incValue()
			self.xRemoteControlStatus.incValue()
			self.xRunStatus.incValue()
			self.xWarningStatus.incValue()
			self.xFaultStatus.incValue()
			self.xDriveRunStatus.incValue()
			self.xSpeedModeStatus.incValue()
			self.xFlowModeStatus.incValue()
			self.xPowerModeStatus.incValue()
			self.xPropotionModeStatus.incValue()
			self.xDOxygenModeStatus.incValue()
			self.xPresModeStatus.incValue()
			self.xCommScanPluse.incValue()
			self.xDischargePresWarning.incValue()
			self.xFliterPresWarning.incValue()
			self.xPumpPresUpWarning.incValue()
			self.xPumpPresDownWarning.incValue()
			self.xSuctionTempUpWarning.incValue()
			self.xDischargeTempUpWarning.incValue()
			self.xMotorTempUpWarning.incValue()
			self.xAirTempUpWarning.incValue()
			self.xAirTempDownWarning.incValue()
			self.xDriveTempUpWarning.incValue()
			self.xPresSensorFaultWarning.incValue()
			self.xTempSensorFaultWarning.incValue()
			self.xFlow.incValue()
			self.xDischargePres.incValue()
			self.xAirTemp.incValue()
			self.xMotorTemp.incValue()
			self.xDriveTemp.incValue()
			self.xDischargeTemp.incValue()
			self.xPowerConsumption.incValue()
			self.xMotorCurrent.incValue()
			self.xFrequency.incValue()
			self.xMotorFrequency.incValue()
			self.xStartCount.incValue()
			self.xRunningDays.incValue()
			self.xRunningHours.incValue()
			self.xRunningMinutes.incValue()
			self.xFilterPres.incValue()
			self.xSuctionPres.incValue()
			self.xVibration.incValue()
			self.xBearingTemp.incValue()
			self.xNumber.incValue()

			time.sleep(10)

class	DeviceCompressor(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self) 
		self.xDisPres=SensorSim(0,CONF_PRESSURE_MAX)
		self.xDisSetPres=SensorSim(0,CONF_PRESSURE_MAX)
		self.xReloadPres=SensorSim(0,CONF_PRESSURE_MAX)
		self.xUnloadPres=SensorSim(0,CONF_PRESSURE_MAX)

		self.xMotorCurrent=SensorSim(0,CONF_CURRENT_MAX)
		self.xMaxCurrent=SensorSim(0,CONF_CURRENT_MAX)
		self.xMinCurrent=SensorSim(0,CONF_CURRENT_MAX)
		self.xCompLoadRatio=SensorSim(0,CONF_RATIO_MAX)
		self.xLoadCurrent=SensorSim(0,CONF_CURRENT_MAX)
		self.xSergePreventCurrent=SensorSim(0,CONF_CURRENT_MAX)
		self.xModulationCurrent=SensorSim(0,CONF_CURRENT_MAX)

		self.xOilPres=SensorSim(0,CONF_PRESSURE_MAX)
		self.xOilDPres=SensorSim(0,CONF_PRESSURE_MAX)
		self.xOilSupplyTemp=SensorSim(CONF_TEMPERATURE_MIN,CONF_TEMPERATURE_MAX)
		self.xOilTankTemp=SensorSim(CONF_TEMPERATURE_MIN,CONF_TEMPERATURE_MAX)
		self.xOilTankLevel=SensorSim(0,CONF_RATIO_MAX)

		self.x1stVib=SensorSim(0,CONF_VIBRATION_MAX)
		self.x2ndVib=SensorSim(0,CONF_VIBRATION_MAX)
		self.x3rdVib=SensorSim(0,CONF_VIBRATION_MAX)

		self.xMBearingDETemp=SensorSim(CONF_TEMPERATURE_MIN,CONF_TEMPERATURE_MAX)
		self.xMBearingNDETemp=SensorSim(CONF_TEMPERATURE_MIN,CONF_TEMPERATURE_MAX)
		self.xMWindingRTemp=SensorSim(CONF_TEMPERATURE_MIN,CONF_TEMPERATURE_MAX)
		self.xMWindingSTemp=SensorSim(CONF_TEMPERATURE_MIN,CONF_TEMPERATURE_MAX)
		self.xMWindingTTemp=SensorSim(CONF_TEMPERATURE_MIN,CONF_TEMPERATURE_MAX)

		self.xSuctionFltrDPres=SensorSim(0,CONF_PRESSURE_MAX)
		self.x2ndInletTemp=SensorSim(CONF_TEMPERATURE_MIN,CONF_TEMPERATURE_MAX)
		self.x3rdInletTemp=SensorSim(CONF_TEMPERATURE_MIN,CONF_TEMPERATURE_MAX)

		self.xCoolSupplytemp=SensorSim(CONF_TEMPERATURE_MIN,CONF_TEMPERATURE_MAX)
		self.xOilCoolerReturnTemp=SensorSim(CONF_TEMPERATURE_MIN,CONF_TEMPERATURE_MAX)
		self.x1stIntercoolerReturnTemp=SensorSim(CONF_TEMPERATURE_MIN,CONF_TEMPERATURE_MAX)
		self.x2ndIntercoolerReturnTemp=SensorSim(CONF_TEMPERATURE_MIN,CONF_TEMPERATURE_MAX)
		self.xAfterCoolerReturnTemp=SensorSim(CONF_TEMPERATURE_MIN,CONF_TEMPERATURE_MAX)

		self.xDisTemp=SensorSim(CONF_TEMPERATURE_MIN,CONF_TEMPERATURE_MAX)
		self.xSystemTemp=SensorSim(CONF_TEMPERATURE_MIN,CONF_TEMPERATURE_MAX)

		self.xBOVOpenOutput=SensorSim(0,CONF_RATIO_MAX)
		self.xBOVOpenFeedback=SensorSim(0,CONF_RATIO_MAX)
		self.xIGVOpenOutput=SensorSim(0,CONF_RATIO_MAX)
		self.xIGVOpenFeedback=SensorSim(0,CONF_RATIO_MAX)

		self.xCompRunTimeDay=SensorSim(0,CONF_COUNT_MAX)
		self.xCompRunTimeHour=SensorSim(0,CONF_COUNT_MAX)
		self.xCompRunCount10000=SensorSim(0,CONF_COUNT_MAX)
		self.xCompRunCount1=SensorSim(0,CONF_COUNT_MAX)
		self.xLoadRunTimeDay=SensorSim(0,CONF_COUNT_MAX)
		self.xLoadRunTimeHour=SensorSim(0,CONF_COUNT_MAX)
		self.xLoadRunCount10000=SensorSim(0,CONF_COUNT_MAX)
		self.xLoadRunCount1=SensorSim(0,CONF_COUNT_MAX)
		self.xPLCRunTimeDay=SensorSim(0,CONF_COUNT_MAX)
		self.xPLCRunTimeHour=SensorSim(0,CONF_COUNT_MAX)

		self.xOilSupplyPresHighAlarm=SensorSim(0,CONF_PRESSURE_MAX)

		self.xOilSupplyPresLowAlarm=SensorSim(0,CONF_PRESSURE_MAX)
		self.xOilSupplyPresLowTrip=SensorSim(0,CONF_PRESSURE_MAX)
		self.xOilFltrDPresHighAlarm=SensorSim(0,CONF_PRESSURE_MAX)
		self.xOilFltrDPresHighTrip=SensorSim(0,CONF_PRESSURE_MAX)
		self.xOilSupplyTempHighAlarm=SensorSim(CONF_TEMPERATURE_MIN,CONF_TEMPERATURE_MAX)
		self.xOilSupplyTempHighTrip=SensorSim(CONF_TEMPERATURE_MIN,CONF_TEMPERATURE_MAX)
		self.xOilSupplyTempLowAlarm=SensorSim(CONF_TEMPERATURE_MIN,CONF_TEMPERATURE_MAX)

		self.xOilTankLevelLowAlarm=SensorSim(0,CONF_RATIO_MAX)

		self.x2ndInletTempHighAlarm=SensorSim(CONF_TEMPERATURE_MIN,CONF_TEMPERATURE_MAX)
		self.x2ndInletTempHighTrip=SensorSim(CONF_TEMPERATURE_MIN,CONF_TEMPERATURE_MAX)
		self.x3rdInletTempHighAlarm=SensorSim(CONF_TEMPERATURE_MIN,CONF_TEMPERATURE_MAX)
		self.x3rdInletTempHighTrip=SensorSim(CONF_TEMPERATURE_MIN,CONF_TEMPERATURE_MAX)
		self.xCoolSupplyTempHighAlarm=SensorSim(CONF_TEMPERATURE_MIN,CONF_TEMPERATURE_MAX)

		self.xCompDisPresLowAlarm=SensorSim(0,CONF_PRESSURE_MAX)
		self.xSuctionFltrDPresHighAlarm=SensorSim(0,CONF_PRESSURE_MAX)

		self.xVibStartingHighAlarm=SensorSim(0,CONF_VIBRATION_MAX)
		self.xVibStartingHighTrip=SensorSim(0,CONF_VIBRATION_MAX)
		self.xVibRuningHighAlarm=SensorSim(0,CONF_VIBRATION_MAX)
		self.xVibRuningHighTrip=SensorSim(0,CONF_VIBRATION_MAX)

		self.xMBearingTempHighAlarm=SensorSim(CONF_TEMPERATURE_MIN,CONF_TEMPERATURE_MAX)
		self.xMBearingTempHighTrip=SensorSim(CONF_TEMPERATURE_MIN,CONF_TEMPERATURE_MAX)
		self.xMWindingTempHighAlarm=SensorSim(CONF_TEMPERATURE_MIN,CONF_TEMPERATURE_MAX)
		self.xMWindingTempHighTrip=SensorSim(CONF_TEMPERATURE_MIN,CONF_TEMPERATURE_MAX)

		self.xOilExchangeTime=SensorSim(0,CONF_COUNT_MAX)
		self.xPLCBATExchangeTime=SensorSim(0,CONF_COUNT_MAX)

		self.xDisPres=SensorSim(0,CONF_PRESSURE_MAX)
		self.xReloadPres=SensorSim(0,CONF_PRESSURE_MAX)

		self.xCommonTrip=SensorSim(0,1)
		self.xCommonAlarm=SensorSim(0,1)
		self.xCommonSensorFault=SensorSim(0,1)
		self.xAlarmResetting=SensorSim(0,1)

		self.xCompReady=SensorSim(0,1)
		self.xOilTempReady=SensorSim(0,1)
		self.xOilPresReady=SensorSim(0,1)
		self.xNotReadyAlarm=SensorSim(0,1)
		self.xCompRestartTime=SensorSim(0,1)

		self.xCompRun=SensorSim(0,1)
		self.xCompStop=SensorSim(0,1)
		self.xCompTripStop=SensorSim(0,1)
		self.xCompStarting=SensorSim(0,1)
		self.xCompStopping=SensorSim(0,1)

		self.xLocalgRemoteSelect=SensorSim(0,1)
		self.xLoadgUnloadSelect=SensorSim(0,1)
		self.xLoadMode=SensorSim(0,1)
		self.xModulationMode=SensorSim(0,1)
		self.xForceUnloading=SensorSim(0,1)

		self.xAuxOilPumpRungStop=SensorSim(0,1)
		self.xAuxOilPumpStopping=SensorSim(0,1)
		self.xEjectorExhFanRungStop=SensorSim(0,1)
		self.xOilHeaterOngOff=SensorSim(0,1)

		self.xPLCRebooting=SensorSim(0,1)
		self.xCompEmergencyStop=SensorSim(0,1)
		self.xCompStarterPaneltrip=SensorSim(0,1)
		self.xAuxOilPumpEOCRTrip=SensorSim(0,1)
		self.xExhaustFanEOCRTrip=SensorSim(0,1)
		self.xOilExchangeTimeAlarm=SensorSim(0,1)
		self.xPLCBATVoltageLowAlarm=SensorSim(0,1)
		self.xPLCBATExchangeTimeAlarm=SensorSim(0,1)

		self.xSurgeUnload=SensorSim(0,1)
		self.xSurgeHalfUnload=SensorSim(0,1)
		self.xSurgeCount1=SensorSim(0,1)
		self.xSurgeCount2=SensorSim(0,1)
		self.xSurgeCount3=SensorSim(0,1)
		self.xSurgeCount4=SensorSim(0,1)
		self.xSurgeCount5=SensorSim(0,1)

		self.x2ndInletTFault=SensorSim(0,1)
		self.x2ndInletTempHighAlarm=SensorSim(0,1)
		self.x2ndInletTempHighTrip=SensorSim(0,1)

		self.x3rdInletTFault=SensorSim(0,1)
		self.x3rdInletTempHighAlarm=SensorSim(0,1)
		self.x3rdInletTempHighTrip=SensorSim(0,1)

		self.xOilTFault=SensorSim(0,1)
		self.xOilTempHighAlarm=SensorSim(0,1)
		self.xOilTempHighTrip=SensorSim(0,1)
		self.xOilTempLowAlarm=SensorSim(0,1)

		self.xCoolSupplyTFault=SensorSim(0,1)
		self.xCoolSupplyTempHighAlarm=SensorSim(0,1)

		self.x1stIntercoolerReturnTFault=SensorSim(0,1)

		self.x2ndIntercoolerReturnTFault=SensorSim(0,1)

		self.xOilIntercoolerReturnTFault=SensorSim(0,1)

		self.xMBearingDETSensorFaullt=SensorSim(0,1)
		self.xMBearingDETempHighAlarm=SensorSim(0,1)
		self.xMBearingDETempHighTrip=SensorSim(0,1)

		self.xMBearingNDETSensorFaullt=SensorSim(0,1)
		self.xMBearingNDETempHighAlarm=SensorSim(0,1)
		self.xMBearingNDETempHighTrip=SensorSim(0,1)

		self.xMWindingRTFault=SensorSim(0,1)
		self.xMWindingRTempHighAlarm=SensorSim(0,1)
		self.xMWindingRTempHighTrip=SensorSim(0,1)

		self.xMWindingSTFault=SensorSim(0,1)
		self.xMWindingSTempHighAlarm=SensorSim(0,1)
		self.xMWindingSTempHighTrip=SensorSim(0,1)

		self.xMWindingTTFault=SensorSim(0,1)
		self.xMWindingTTempHighAlarm=SensorSim(0,1)
		self.xMWindingTTempHighTrip=SensorSim(0,1)

		self.xCompDisPresSensorFault=SensorSim(0,1)
		self.xCompDisPresLowAlarm=SensorSim(0,1)

		self.xMotorCurrentSensorFault=SensorSim(0,1)

		self.xMotorCurrentLowTrip=SensorSim(0,1)
		self.xMotorCurrentAbnormalTrip=SensorSim(0,1)

		self.xOilPresSensorFault=SensorSim(0,1)
		self.xOilPresHighAlarm=SensorSim(0,1)

		self.xOilPresLowAlarm=SensorSim(0,1)
		self.xOilPresLowTrip=SensorSim(0,1)
		self.xOilPresLowTripStart=SensorSim(0,1)

		self.xOilFltrDPresSensorFault=SensorSim(0,1)
		self.xOilFltrDPresHighAlarm=SensorSim(0,1)
		self.xOilFltrDPresHighTrip=SensorSim(0,1)

		self.x1stVibSensorFault=SensorSim(0,1)
		self.x1stVibHighAlarmStart=SensorSim(0,1)
		self.x1stVibHighTripStart=SensorSim(0,1)
		self.x1stVibHighAlarmRun=SensorSim(0,1)
		self.x1stVibHighTripRun=SensorSim(0,1)
		self.x1stVibAbnormalTrip=SensorSim(0,1)
		self.x1stVibAverageAAlarm=SensorSim(0,1)
		self.x1stVibAverageBAlarm=SensorSim(0,1)

		self.x2ndVibSensorFault=SensorSim(0,1)
		self.x2ndVibHighAlarmStart=SensorSim(0,1)
		self.x2ndVibHighTripStart=SensorSim(0,1)
		self.x2ndVibHighAlarmRun=SensorSim(0,1)
		self.x2ndVibHighTripRun=SensorSim(0,1)
		self.x2ndVibAbnormalTrip=SensorSim(0,1)
		self.x2ndVibAverageAAlarm=SensorSim(0,1)
		self.x2ndVibAverageBAlarm=SensorSim(0,1)

		self.x3rdVibSensorFault=SensorSim(0,1)
		self.x3rdVibHighAlarmStart=SensorSim(0,1)
		self.x3rdVibHighTripStart=SensorSim(0,1)
		self.x3rdVibHighAlarmRun=SensorSim(0,1)
		self.x3rdVibHighTripRun=SensorSim(0,1)
		self.x3rdVibAbnormalTrip=SensorSim(0,1)
		self.x3rdVibAverageAAlarm=SensorSim(0,1)
		self.x3rdVibAverageBAlarm=SensorSim(0,1)

		self.xAfterCoolerReturnTFault=SensorSim(0,1)

		self.xCompDisTFault=SensorSim(0,1)

		self.xOilTankTFault=SensorSim(0,1)

		self.xSystemTFault=SensorSim(0,1)

		self.xSuctionFltrDPresSensorFault=SensorSim(0,1)
		self.xSuctionFltrDPresHighAlarm=SensorSim(0,1)

		self.xOilTankLevelSensorFault=SensorSim(0,1)
		self.xOilTankLevelLowAlarm=SensorSim(0,1)

	def	run(self):
		while True:
			self.xDisPres.incValue()
			self.xDisSetPres.incValue()
			self.xReloadPres.incValue()
			self.xUnloadPres.incValue()
	
			self.xMotorCurrent.incValue()
			self.xMaxCurrent.incValue()
			self.xMinCurrent.incValue()
			self.xCompLoadRatio.incValue()
			self.xLoadCurrent.incValue()
			self.xSergePreventCurrent.incValue()
			self.xModulationCurrent.incValue()
	
			self.xOilPres.incValue()
			self.xOilDPres.incValue()
			self.xOilSupplyTemp.incValue()
			self.xOilTankTemp.incValue()
			self.xOilTankLevel.incValue()
	
			self.x1stVib.incValue()
			self.x2ndVib.incValue()
			self.x3rdVib.incValue()
	
			self.xMBearingDETemp.incValue()
			self.xMBearingNDETemp.incValue()
			self.xMWindingRTemp.incValue()
			self.xMWindingSTemp.incValue()
			self.xMWindingTTemp.incValue()
	
			self.xSuctionFltrDPres.incValue()
			self.x2ndInletTemp.incValue()
			self.x3rdInletTemp.incValue()
	
			self.xCoolSupplytemp.incValue()
			self.xOilCoolerReturnTemp.incValue()
			self.x1stIntercoolerReturnTemp.incValue()
			self.x2ndIntercoolerReturnTemp.incValue()
			self.xAfterCoolerReturnTemp.incValue()
	
			self.xDisTemp.incValue()
			self.xSystemTemp.incValue()
	
			self.xBOVOpenOutput.incValue()
			self.xBOVOpenFeedback.incValue()
			self.xIGVOpenOutput.incValue()
			self.xIGVOpenFeedback.incValue()
	
			self.xCompRunTimeDay.incValue()
			self.xCompRunTimeHour.incValue()
			self.xCompRunCount10000.incValue()
			self.xCompRunCount1.incValue()
			self.xLoadRunTimeDay.incValue()
			self.xLoadRunTimeHour.incValue()
			self.xLoadRunCount10000.incValue()
			self.xLoadRunCount1.incValue()
			self.xPLCRunTimeDay.incValue()
			self.xPLCRunTimeHour.incValue()
	
			self.xOilSupplyPresHighAlarm.incValue()
	
			self.xOilSupplyPresLowAlarm.incValue()
			self.xOilSupplyPresLowTrip.incValue()
			self.xOilFltrDPresHighAlarm.incValue()
			self.xOilFltrDPresHighTrip.incValue()
			self.xOilSupplyTempHighAlarm.incValue()
			self.xOilSupplyTempHighTrip.incValue()
			self.xOilSupplyTempLowAlarm.incValue()
	
			self.xOilTankLevelLowAlarm.incValue()
	
			self.x2ndInletTempHighAlarm.incValue()
			self.x2ndInletTempHighTrip.incValue()
			self.x3rdInletTempHighAlarm.incValue()
			self.x3rdInletTempHighTrip.incValue()
			self.xCoolSupplyTempHighAlarm.incValue()
	
			self.xCompDisPresLowAlarm.incValue()
			self.xSuctionFltrDPresHighAlarm.incValue()
	
			self.xVibStartingHighAlarm.incValue()
			self.xVibStartingHighTrip.incValue()
			self.xVibRuningHighAlarm.incValue()
			self.xVibRuningHighTrip.incValue()
	
			self.xMBearingTempHighAlarm.incValue()
			self.xMBearingTempHighTrip.incValue()
			self.xMWindingTempHighAlarm.incValue()
			self.xMWindingTempHighTrip.incValue()
	
			self.xOilExchangeTime.incValue()
			self.xPLCBATExchangeTime.incValue()
	
			self.xDisPres.incValue()
			self.xReloadPres.incValue()

			self.xCommonTrip.incValue()
			self.xCommonAlarm.incValue()
			self.xCommonSensorFault.incValue()
			self.xAlarmResetting.incValue()
	
			self.xCompReady.incValue()
			self.xOilTempReady.incValue()
			self.xOilPresReady.incValue()
			self.xNotReadyAlarm.incValue()
			self.xCompRestartTime.incValue()
	
			self.xCompRun.incValue()
			self.xCompStop.incValue()
			self.xCompTripStop.incValue()
			self.xCompStarting.incValue()
			self.xCompStopping.incValue()
	
			self.xLocalgRemoteSelect.incValue()
			self.xLoadgUnloadSelect.incValue()
			self.xLoadMode.incValue()
			self.xModulationMode.incValue()
			self.xForceUnloading.incValue()
	
			self.xAuxOilPumpRungStop.incValue()
			self.xAuxOilPumpStopping.incValue()
			self.xEjectorExhFanRungStop.incValue()
			self.xOilHeaterOngOff.incValue()
	
			self.xPLCRebooting.incValue()
			self.xCompEmergencyStop.incValue()
			self.xCompStarterPaneltrip.incValue()
			self.xAuxOilPumpEOCRTrip.incValue()
			self.xExhaustFanEOCRTrip.incValue()
			self.xOilExchangeTimeAlarm.incValue()
			self.xPLCBATVoltageLowAlarm.incValue()
			self.xPLCBATExchangeTimeAlarm.incValue()
	
			self.xSurgeUnload.incValue()
			self.xSurgeHalfUnload.incValue()
			self.xSurgeCount1.incValue()
			self.xSurgeCount2.incValue()
			self.xSurgeCount3.incValue()
			self.xSurgeCount4.incValue()
			self.xSurgeCount5.incValue()
	
			self.x2ndInletTFault.incValue()
			self.x2ndInletTempHighAlarm.incValue()
			self.x2ndInletTempHighTrip.incValue()
	
			self.x3rdInletTFault.incValue()
			self.x3rdInletTempHighAlarm.incValue()
			self.x3rdInletTempHighTrip.incValue()
	
			self.xOilTFault.incValue()
			self.xOilTempHighAlarm.incValue()
			self.xOilTempHighTrip.incValue()
			self.xOilTempLowAlarm.incValue()
	
			self.xCoolSupplyTFault.incValue()
			self.xCoolSupplyTempHighAlarm.incValue()
	
			self.x1stIntercoolerReturnTFault.incValue()
	
			self.x2ndIntercoolerReturnTFault.incValue()
	
			self.xOilIntercoolerReturnTFault.incValue()
	
			self.xMBearingDETSensorFaullt.incValue()
			self.xMBearingDETempHighAlarm.incValue()
			self.xMBearingDETempHighTrip.incValue()
	
			self.xMBearingNDETSensorFaullt.incValue()
			self.xMBearingNDETempHighAlarm.incValue()
			self.xMBearingNDETempHighTrip.incValue()
	
			self.xMWindingRTFault.incValue()
			self.xMWindingRTempHighAlarm.incValue()
			self.xMWindingRTempHighTrip.incValue()
	
			self.xMWindingSTFault.incValue()
			self.xMWindingSTempHighAlarm.incValue()
			self.xMWindingSTempHighTrip.incValue()
	
			self.xMWindingTTFault.incValue()
			self.xMWindingTTempHighAlarm.incValue()
			self.xMWindingTTempHighTrip.incValue()
	
			self.xCompDisPresSensorFault.incValue()
			self.xCompDisPresLowAlarm.incValue()
	
			self.xMotorCurrentSensorFault.incValue()
	
			self.xMotorCurrentLowTrip.incValue()
			self.xMotorCurrentAbnormalTrip.incValue()
	
			self.xOilPresSensorFault.incValue()
			self.xOilPresHighAlarm.incValue()
	
			self.xOilPresLowAlarm.incValue()
			self.xOilPresLowTrip.incValue()
			self.xOilPresLowTripStart.incValue()
	
			self.xOilFltrDPresSensorFault.incValue()
			self.xOilFltrDPresHighAlarm.incValue()
			self.xOilFltrDPresHighTrip.incValue()
	
			self.x1stVibSensorFault.incValue()
			self.x1stVibHighAlarmStart.incValue()
			self.x1stVibHighTripStart.incValue()
			self.x1stVibHighAlarmRun.incValue()
			self.x1stVibHighTripRun.incValue()
			self.x1stVibAbnormalTrip.incValue()
			self.x1stVibAverageAAlarm.incValue()
			self.x1stVibAverageBAlarm.incValue()
	
			self.x2ndVibSensorFault.incValue()
			self.x2ndVibHighAlarmStart.incValue()
			self.x2ndVibHighTripStart.incValue()
			self.x2ndVibHighAlarmRun.incValue()
			self.x2ndVibHighTripRun.incValue()
			self.x2ndVibAbnormalTrip.incValue()
			self.x2ndVibAverageAAlarm.incValue()
			self.x2ndVibAverageBAlarm.incValue()
	
			self.x3rdVibSensorFault.incValue()
			self.x3rdVibHighAlarmStart.incValue()
			self.x3rdVibHighTripStart.incValue()
			self.x3rdVibHighAlarmRun.incValue()
			self.x3rdVibHighTripRun.incValue()
			self.x3rdVibAbnormalTrip.incValue()
			self.x3rdVibAverageAAlarm.incValue()
			self.x3rdVibAverageBAlarm.incValue()
	
			self.xAfterCoolerReturnTFault.incValue()
	
			self.xCompDisTFault.incValue()
	
			self.xOilTankTFault.incValue()
	
			self.xSystemTFault.incValue()
	
			self.xSuctionFltrDPresSensorFault.incValue()
			self.xSuctionFltrDPresHighAlarm.incValue()
	
			self.xOilTankLevelSensorFault.incValue()
			self.xOilTankLevelLowAlarm.incValue()

			time.sleep(10)

class TESTCORE(threading.Thread):
	def __init__(self, coilRegisters, discreteRegisters, inputRegisters, holdRegisters):
		threading.Thread.__init__(self) 
		self.coilRegisters = coilRegisters
		self.discreteRegisters = discreteRegisters
		self.inputRegisters = inputRegisters
		self.holdRegisters = holdRegisters
		self.compressor = DeviceCompressor()
		self.blower = DeviceBlower()

	def run(self):
		self.compressor.start()
		self.blower.start()

		while True:
			self.inputRegisters[  25].clearFlags()
			self.inputRegisters[  25].addFlag(0, self.compressor.xCommonTrip)
			self.inputRegisters[  25].addFlag(1, self.compressor.xCommonAlarm)
			self.inputRegisters[  25].addFlag(2, self.compressor.xCommonSensorFault)
			self.inputRegisters[  25].addFlag(3, self.compressor.xAlarmResetting)
	
			self.inputRegisters[  26].clearFlags()
			self.inputRegisters[  26].addFlag(0, self.compressor.xCompReady)
			self.inputRegisters[  26].addFlag(1, self.compressor.xOilTempReady)
			self.inputRegisters[  26].addFlag(2, self.compressor.xOilPresReady)
			self.inputRegisters[  26].addFlag(3, self.compressor.xNotReadyAlarm)
			self.inputRegisters[  26].addFlag(4, self.compressor.xCompRestartTime)
	
			self.inputRegisters[  27].clearFlags()
			self.inputRegisters[  27].addFlag(0, self.compressor.xCompRun)
			self.inputRegisters[  27].addFlag(1, self.compressor.xCompStop)
			self.inputRegisters[  27].addFlag(2, self.compressor.xCompTripStop)
			self.inputRegisters[  27].addFlag(3, self.compressor.xCompStarting)
			self.inputRegisters[  27].addFlag(4, self.compressor.xCompStopping)
	
			self.inputRegisters[  28].clearFlags()
			self.inputRegisters[  28].addFlag(0, self.compressor.xLocalgRemoteSelect)
			self.inputRegisters[  28].addFlag(1, self.compressor.xLoadgUnloadSelect)
			self.inputRegisters[  28].addFlag(2, self.compressor.xLoadMode)
			self.inputRegisters[  28].addFlag(3, self.compressor.xModulationMode)
			self.inputRegisters[  28].addFlag(4, self.compressor.xForceUnloading)
	
			self.inputRegisters[  29].clearFlags()
			self.inputRegisters[  29].addFlag(0, self.compressor.xAuxOilPumpRungStop)
			self.inputRegisters[  29].addFlag(1, self.compressor.xAuxOilPumpStopping)
			self.inputRegisters[  29].addFlag(2, self.compressor.xEjectorExhFanRungStop)
			self.inputRegisters[  29].addFlag(3, self.compressor.xOilHeaterOngOff)
	
			self.inputRegisters[  30].clearFlags()
			self.inputRegisters[  30].addFlag(0, self.compressor.xPLCRebooting)
			self.inputRegisters[  30].addFlag(1, self.compressor.xCompEmergencyStop)
			self.inputRegisters[  30].addFlag(2, self.compressor.xCompStarterPaneltrip)
			self.inputRegisters[  30].addFlag(3, self.compressor.xAuxOilPumpEOCRTrip)
			self.inputRegisters[  30].addFlag(4, self.compressor.xExhaustFanEOCRTrip)
			self.inputRegisters[  30].addFlag(5, self.compressor.xOilExchangeTimeAlarm)
			self.inputRegisters[  30].addFlag(6, self.compressor.xPLCBATVoltageLowAlarm)
			self.inputRegisters[  30].addFlag(7, self.compressor.xPLCBATExchangeTimeAlarm)
	
			self.inputRegisters[  31].clearFlags()
			self.inputRegisters[  31].addFlag(0, self.compressor.xSurgeUnload)
			self.inputRegisters[  31].addFlag(1, self.compressor.xSurgeHalfUnload)
			self.inputRegisters[  31].addFlag(2, self.compressor.xSurgeCount1)
			self.inputRegisters[  31].addFlag(3, self.compressor.xSurgeCount2)
			self.inputRegisters[  31].addFlag(4, self.compressor.xSurgeCount3)
			self.inputRegisters[  31].addFlag(5, self.compressor.xSurgeCount4)
			self.inputRegisters[  31].addFlag(6, self.compressor.xSurgeCount5)
	
			self.inputRegisters[  32].clearFlags()
			self.inputRegisters[  32].addFlag(0, self.compressor.x2ndInletTFault)
			self.inputRegisters[  32].addFlag(1, self.compressor.x2ndInletTempHighAlarm)
			self.inputRegisters[  32].addFlag(2, self.compressor.x2ndInletTempHighTrip)
	
			self.inputRegisters[  32].addFlag(8, self.compressor.x3rdInletTFault)
			self.inputRegisters[  32].addFlag(9, self.compressor.x3rdInletTempHighAlarm)
			self.inputRegisters[  32].addFlag(10, self.compressor.x3rdInletTempHighTrip)
	
			self.inputRegisters[  33].clearFlags()
			self.inputRegisters[  33].addFlag(0, self.compressor.xOilTFault)
			self.inputRegisters[  33].addFlag(1, self.compressor.xOilTempHighAlarm)
			self.inputRegisters[  33].addFlag(2, self.compressor.xOilTempHighTrip)
			self.inputRegisters[  33].addFlag(3, self.compressor.xOilTempLowAlarm)
	
			self.inputRegisters[  33].addFlag(8, self.compressor.xCoolSupplyTFault)
			self.inputRegisters[  33].addFlag(9, self.compressor.xCoolSupplyTempHighAlarm)
	
			self.inputRegisters[  34].clearFlags()
			self.inputRegisters[  34].addFlag(0, self.compressor.x1stIntercoolerReturnTFault)
	
			self.inputRegisters[  34].addFlag(8, self.compressor.x2ndIntercoolerReturnTFault)
	
			self.inputRegisters[  35].clearFlags()
			self.inputRegisters[  35].addFlag(0, self.compressor.xOilIntercoolerReturnTFault)
	
			self.inputRegisters[  35].addFlag(8, self.compressor.xMBearingDETSensorFaullt)
			self.inputRegisters[  35].addFlag(9, self.compressor.xMBearingDETempHighAlarm)
			self.inputRegisters[  35].addFlag(10, self.compressor.xMBearingDETempHighTrip)
	
			self.inputRegisters[  36].clearFlags()
			self.inputRegisters[  36].addFlag(0, self.compressor.xMBearingNDETSensorFaullt)
			self.inputRegisters[  36].addFlag(1, self.compressor.xMBearingNDETempHighAlarm)
			self.inputRegisters[  36].addFlag(2, self.compressor.xMBearingNDETempHighTrip)
	
			self.inputRegisters[  36].addFlag(8, self.compressor.xMWindingRTFault)
			self.inputRegisters[  36].addFlag(9, self.compressor.xMWindingRTempHighAlarm)
			self.inputRegisters[  36].addFlag(10, self.compressor.xMWindingRTempHighTrip)
	
			self.inputRegisters[  37].clearFlags()
			self.inputRegisters[  37].addFlag(0, self.compressor.xMWindingSTFault)
			self.inputRegisters[  37].addFlag(1, self.compressor.xMWindingSTempHighAlarm)
			self.inputRegisters[  37].addFlag(2, self.compressor.xMWindingSTempHighTrip)
	
			self.inputRegisters[  37].addFlag(8, self.compressor.xMWindingTTFault)
			self.inputRegisters[  37].addFlag(9, self.compressor.xMWindingTTempHighAlarm)
			self.inputRegisters[  37].addFlag(10, self.compressor.xMWindingTTempHighTrip)
	
			self.inputRegisters[  38].clearFlags()
			self.inputRegisters[  38].addFlag(0, self.compressor.xCompDisPresSensorFault)
			self.inputRegisters[  38].addFlag(1, self.compressor.xCompDisPresLowAlarm)
	
			self.inputRegisters[  38].addFlag(8, self.compressor.xMotorCurrentSensorFault)
	
			self.inputRegisters[  38].addFlag(10, self.compressor.xMotorCurrentLowTrip)
			self.inputRegisters[  38].addFlag(11, self.compressor.xMotorCurrentAbnormalTrip)
	
			self.inputRegisters[  39].clearFlags()
			self.inputRegisters[  39].addFlag(0, self.compressor.xOilPresSensorFault)
			self.inputRegisters[  39].addFlag(1, self.compressor.xOilPresHighAlarm)
	
			self.inputRegisters[  39].addFlag(3, self.compressor.xOilPresLowAlarm)
			self.inputRegisters[  39].addFlag(4, self.compressor.xOilPresLowTrip)
			self.inputRegisters[  39].addFlag(5, self.compressor.xOilPresLowTripStart)
	
			self.inputRegisters[  39].addFlag(8, self.compressor.xOilFltrDPresSensorFault)
			self.inputRegisters[  39].addFlag(9, self.compressor.xOilFltrDPresHighAlarm)
			self.inputRegisters[  39].addFlag(10, self.compressor.xOilFltrDPresHighTrip)
	
			self.inputRegisters[  40].clearFlags()
			self.inputRegisters[  40].addFlag(0, self.compressor.x1stVibSensorFault)
			self.inputRegisters[  40].addFlag(1, self.compressor.x1stVibHighAlarmStart)
			self.inputRegisters[  40].addFlag(2, self.compressor.x1stVibHighTripStart)
			self.inputRegisters[  40].addFlag(3, self.compressor.x1stVibHighAlarmRun)
			self.inputRegisters[  40].addFlag(4, self.compressor.x1stVibHighTripRun)
			self.inputRegisters[  40].addFlag(5, self.compressor.x1stVibAbnormalTrip)
			self.inputRegisters[  40].addFlag(6, self.compressor.x1stVibAverageAAlarm)
			self.inputRegisters[  40].addFlag(7, self.compressor.x1stVibAverageBAlarm)
	
			self.inputRegisters[  40].addFlag(8, self.compressor.x2ndVibSensorFault)
			self.inputRegisters[  40].addFlag(9, self.compressor.x2ndVibHighAlarmStart)
			self.inputRegisters[  40].addFlag(10, self.compressor.x2ndVibHighTripStart)
			self.inputRegisters[  40].addFlag(11, self.compressor.x2ndVibHighAlarmRun)
			self.inputRegisters[  40].addFlag(12, self.compressor.x2ndVibHighTripRun)
			self.inputRegisters[  40].addFlag(13, self.compressor.x2ndVibAbnormalTrip)
			self.inputRegisters[  40].addFlag(14, self.compressor.x2ndVibAverageAAlarm)
			self.inputRegisters[  40].addFlag(15, self.compressor.x2ndVibAverageBAlarm)
	
			self.inputRegisters[  41].clearFlags()
			self.inputRegisters[  41].addFlag(0, self.compressor.x3rdVibSensorFault)
			self.inputRegisters[  41].addFlag(1, self.compressor.x3rdVibHighAlarmStart)
			self.inputRegisters[  41].addFlag(2, self.compressor.x3rdVibHighTripStart)
			self.inputRegisters[  41].addFlag(3, self.compressor.x3rdVibHighAlarmRun)
			self.inputRegisters[  41].addFlag(4, self.compressor.x3rdVibHighTripRun)
			self.inputRegisters[  41].addFlag(5, self.compressor.x3rdVibAbnormalTrip)
			self.inputRegisters[  41].addFlag(6, self.compressor.x3rdVibAverageAAlarm)
			self.inputRegisters[  41].addFlag(7, self.compressor.x3rdVibAverageBAlarm)
	
			self.inputRegisters[  41].addFlag(8, self.compressor.xAfterCoolerReturnTFault)
	
			self.inputRegisters[  41].addFlag(12, self.compressor.xCompDisTFault)
	
			self.inputRegisters[  42].clearFlags()
			self.inputRegisters[  42].addFlag(0, self.compressor.xOilTankTFault)
	
			self.inputRegisters[  42].addFlag(4, self.compressor.xSystemTFault)
	
			self.inputRegisters[  42].addFlag(8, self.compressor.xSuctionFltrDPresSensorFault)
			self.inputRegisters[  42].addFlag(9, self.compressor.xSuctionFltrDPresHighAlarm)
	
			self.inputRegisters[  42].addFlag(12, self.compressor.xOilTankLevelSensorFault)
			self.inputRegisters[  42].addFlag(13, self.compressor.xOilTankLevelLowAlarm)
	
			self.inputRegisters[ 100].setValue(self.compressor.xDisPres)
			self.inputRegisters[ 101].setValue(self.compressor.xDisSetPres)
			self.inputRegisters[ 102].setValue(self.compressor.xReloadPres)
			self.inputRegisters[ 103].setValue(self.compressor.xUnloadPres)
	
			self.inputRegisters[ 105].setValue(self.compressor.xMotorCurrent)
			self.inputRegisters[ 106].setValue(self.compressor.xMaxCurrent)
			self.inputRegisters[ 107].setValue(self.compressor.xMinCurrent)
			self.inputRegisters[ 108].setValue(self.compressor.xCompLoadRatio)
			self.inputRegisters[ 109].setValue(self.compressor.xLoadCurrent)
			self.inputRegisters[ 110].setValue(self.compressor.xSergePreventCurrent)
			self.inputRegisters[ 111].setValue(self.compressor.xModulationCurrent)
	
			self.inputRegisters[ 115].setValue(self.compressor.xOilPres)
			self.inputRegisters[ 116].setValue(self.compressor.xOilDPres)
			self.inputRegisters[ 117].setValue(self.compressor.xOilSupplyTemp)
			self.inputRegisters[ 118].setValue(self.compressor.xOilTankTemp)
			self.inputRegisters[ 119].setValue(self.compressor.xOilTankLevel)
	
			self.inputRegisters[ 120].setValue(self.compressor.x1stVib)
			self.inputRegisters[ 121].setValue(self.compressor.x2ndVib)
			self.inputRegisters[ 122].setValue(self.compressor.x3rdVib)
	
			self.inputRegisters[ 125].setValue(self.compressor.xMBearingDETemp)
			self.inputRegisters[ 126].setValue(self.compressor.xMBearingNDETemp)
			self.inputRegisters[ 127].setValue(self.compressor.xMWindingRTemp)
			self.inputRegisters[ 128].setValue(self.compressor.xMWindingSTemp)
			self.inputRegisters[ 129].setValue(self.compressor.xMWindingTTemp)
	
			self.inputRegisters[ 130].setValue(self.compressor.xSuctionFltrDPres)
			self.inputRegisters[ 131].setValue(self.compressor.x2ndInletTemp)
			self.inputRegisters[ 132].setValue(self.compressor.x3rdInletTemp)
	
			self.inputRegisters[ 135].setValue(self.compressor.xCoolSupplytemp)
			self.inputRegisters[ 136].setValue(self.compressor.xOilCoolerReturnTemp)
			self.inputRegisters[ 137].setValue(self.compressor.x1stIntercoolerReturnTemp)
			self.inputRegisters[ 138].setValue(self.compressor.x2ndIntercoolerReturnTemp)
			self.inputRegisters[ 139].setValue(self.compressor.xAfterCoolerReturnTemp)
	
			self.inputRegisters[ 140].setValue(self.compressor.xDisTemp)
			self.inputRegisters[ 141].setValue(self.compressor.xSystemTemp)
	
			self.inputRegisters[ 145].setValue(self.compressor.xBOVOpenOutput)
			self.inputRegisters[ 146].setValue(self.compressor.xBOVOpenFeedback)
			self.inputRegisters[ 147].setValue(self.compressor.xIGVOpenOutput)
			self.inputRegisters[ 148].setValue(self.compressor.xIGVOpenFeedback)
	
			self.inputRegisters[ 180].setValue(self.compressor.xCompRunTimeDay)
			self.inputRegisters[ 181].setValue(self.compressor.xCompRunTimeHour)
			self.inputRegisters[ 182].setValue(self.compressor.xCompRunCount10000)
			self.inputRegisters[ 183].setValue(self.compressor.xCompRunCount1)
			self.inputRegisters[ 184].setValue(self.compressor.xLoadRunTimeDay)
			self.inputRegisters[ 185].setValue(self.compressor.xLoadRunTimeHour)
			self.inputRegisters[ 186].setValue(self.compressor.xLoadRunCount10000)
			self.inputRegisters[ 187].setValue(self.compressor.xLoadRunCount1)
			self.inputRegisters[ 188].setValue(self.compressor.xPLCRunTimeDay)
			self.inputRegisters[ 189].setValue(self.compressor.xPLCRunTimeHour)

			self.inputRegisters[  25].clearFlags()
			self.inputRegisters[  25].addFlag(0, self.compressor.xCommonTrip)
			self.inputRegisters[  25].addFlag(1, self.compressor.xCommonAlarm)
			self.inputRegisters[  25].addFlag(2, self.compressor.xCommonSensorFault)
			self.inputRegisters[  25].addFlag(3, self.compressor.xAlarmResetting)
	
			self.inputRegisters[  26].clearFlags()
			self.inputRegisters[  26].addFlag(0, self.compressor.xCompReady)
			self.inputRegisters[  26].addFlag(1, self.compressor.xOilTempReady)
			self.inputRegisters[  26].addFlag(2, self.compressor.xOilPresReady)
			self.inputRegisters[  26].addFlag(3, self.compressor.xNotReadyAlarm)
			self.inputRegisters[  26].addFlag(4, self.compressor.xCompRestartTime)
	
			self.inputRegisters[  27].clearFlags()
			self.inputRegisters[  27].addFlag(0, self.compressor.xCompRun)
			self.inputRegisters[  27].addFlag(1, self.compressor.xCompStop)
			self.inputRegisters[  27].addFlag(2, self.compressor.xCompTripStop)
			self.inputRegisters[  27].addFlag(3, self.compressor.xCompStarting)
			self.inputRegisters[  27].addFlag(4, self.compressor.xCompStopping)
	
			self.inputRegisters[  28].clearFlags()
			self.inputRegisters[  28].addFlag(0, self.compressor.xLocalgRemoteSelect)
			self.inputRegisters[  28].addFlag(1, self.compressor.xLoadgUnloadSelect)
			self.inputRegisters[  28].addFlag(2, self.compressor.xLoadMode)
			self.inputRegisters[  28].addFlag(3, self.compressor.xModulationMode)
			self.inputRegisters[  28].addFlag(4, self.compressor.xForceUnloading)
	
			self.inputRegisters[  29].clearFlags()
			self.inputRegisters[  29].addFlag(0, self.compressor.xAuxOilPumpRungStop)
			self.inputRegisters[  29].addFlag(1, self.compressor.xAuxOilPumpStopping)
			self.inputRegisters[  29].addFlag(2, self.compressor.xEjectorExhFanRungStop)
			self.inputRegisters[  29].addFlag(3, self.compressor.xOilHeaterOngOff)
	
			self.inputRegisters[  30].clearFlags()
			self.inputRegisters[  30].addFlag(0, self.compressor.xPLCRebooting)
			self.inputRegisters[  30].addFlag(1, self.compressor.xCompEmergencyStop)
			self.inputRegisters[  30].addFlag(2, self.compressor.xCompStarterPaneltrip)
			self.inputRegisters[  30].addFlag(3, self.compressor.xAuxOilPumpEOCRTrip)
			self.inputRegisters[  30].addFlag(4, self.compressor.xExhaustFanEOCRTrip)
			self.inputRegisters[  30].addFlag(5, self.compressor.xOilExchangeTimeAlarm)
			self.inputRegisters[  30].addFlag(6, self.compressor.xPLCBATVoltageLowAlarm)
			self.inputRegisters[  30].addFlag(7, self.compressor.xPLCBATExchangeTimeAlarm)
	
			self.inputRegisters[  31].clearFlags()
			self.inputRegisters[  31].addFlag(0, self.compressor.xSurgeUnload)
			self.inputRegisters[  31].addFlag(1, self.compressor.xSurgeHalfUnload)
			self.inputRegisters[  31].addFlag(2, self.compressor.xSurgeCount1)
			self.inputRegisters[  31].addFlag(3, self.compressor.xSurgeCount2)
			self.inputRegisters[  31].addFlag(4, self.compressor.xSurgeCount3)
			self.inputRegisters[  31].addFlag(5, self.compressor.xSurgeCount4)
			self.inputRegisters[  31].addFlag(6, self.compressor.xSurgeCount5)
	
			self.inputRegisters[  32].clearFlags()
			self.inputRegisters[  32].addFlag(0, self.compressor.x2ndInletTFault)
			self.inputRegisters[  32].addFlag(1, self.compressor.x2ndInletTempHighAlarm)
			self.inputRegisters[  32].addFlag(2, self.compressor.x2ndInletTempHighTrip)
	
			self.inputRegisters[  32].addFlag(8, self.compressor.x3rdInletTFault)
			self.inputRegisters[  32].addFlag(9, self.compressor.x3rdInletTempHighAlarm)
			self.inputRegisters[  32].addFlag(10, self.compressor.x3rdInletTempHighTrip)
	
			self.inputRegisters[  33].clearFlags()
			self.inputRegisters[  33].addFlag(0, self.compressor.xOilTFault)
			self.inputRegisters[  33].addFlag(1, self.compressor.xOilTempHighAlarm)
			self.inputRegisters[  33].addFlag(2, self.compressor.xOilTempHighTrip)
			self.inputRegisters[  33].addFlag(3, self.compressor.xOilTempLowAlarm)
	
			self.inputRegisters[  33].addFlag(8, self.compressor.xCoolSupplyTFault)
			self.inputRegisters[  33].addFlag(9, self.compressor.xCoolSupplyTempHighAlarm)
	
			self.inputRegisters[  34].clearFlags()
			self.inputRegisters[  34].addFlag(0, self.compressor.x1stIntercoolerReturnTFault)
	
			self.inputRegisters[  34].addFlag(8, self.compressor.x2ndIntercoolerReturnTFault)
	
			self.inputRegisters[  35].clearFlags()
			self.inputRegisters[  35].addFlag(0, self.compressor.xOilIntercoolerReturnTFault)
	
			self.inputRegisters[  35].addFlag(8, self.compressor.xMBearingDETSensorFaullt)
			self.inputRegisters[  35].addFlag(9, self.compressor.xMBearingDETempHighAlarm)
			self.inputRegisters[  35].addFlag(10, self.compressor.xMBearingDETempHighTrip)
	
			self.inputRegisters[  36].clearFlags()
			self.inputRegisters[  36].addFlag(0, self.compressor.xMBearingNDETSensorFaullt)
			self.inputRegisters[  36].addFlag(1, self.compressor.xMBearingNDETempHighAlarm)
			self.inputRegisters[  36].addFlag(2, self.compressor.xMBearingNDETempHighTrip)
	
			self.inputRegisters[  36].addFlag(8, self.compressor.xMWindingRTFault)
			self.inputRegisters[  36].addFlag(9, self.compressor.xMWindingRTempHighAlarm)
			self.inputRegisters[  36].addFlag(10, self.compressor.xMWindingRTempHighTrip)
	
			self.inputRegisters[  37].clearFlags()
			self.inputRegisters[  37].addFlag(0, self.compressor.xMWindingSTFault)
			self.inputRegisters[  37].addFlag(1, self.compressor.xMWindingSTempHighAlarm)
			self.inputRegisters[  37].addFlag(2, self.compressor.xMWindingSTempHighTrip)
	
			self.inputRegisters[  37].addFlag(8, self.compressor.xMWindingTTFault)
			self.inputRegisters[  37].addFlag(9, self.compressor.xMWindingTTempHighAlarm)
			self.inputRegisters[  37].addFlag(10, self.compressor.xMWindingTTempHighTrip)
	
			self.inputRegisters[  38].clearFlags()
			self.inputRegisters[  38].addFlag(0, self.compressor.xCompDisPresSensorFault)
			self.inputRegisters[  38].addFlag(1, self.compressor.xCompDisPresLowAlarm)
	
			self.inputRegisters[  38].addFlag(8, self.compressor.xMotorCurrentSensorFault)
	
			self.inputRegisters[  38].addFlag(10, self.compressor.xMotorCurrentLowTrip)
			self.inputRegisters[  38].addFlag(11, self.compressor.xMotorCurrentAbnormalTrip)
	
			self.inputRegisters[  39].clearFlags()
			self.inputRegisters[  39].addFlag(0, self.compressor.xOilPresSensorFault)
			self.inputRegisters[  39].addFlag(1, self.compressor.xOilPresHighAlarm)
	
			self.inputRegisters[  39].addFlag(3, self.compressor.xOilPresLowAlarm)
			self.inputRegisters[  39].addFlag(4, self.compressor.xOilPresLowTrip)
			self.inputRegisters[  39].addFlag(5, self.compressor.xOilPresLowTripStart)
	
			self.inputRegisters[  39].addFlag(8, self.compressor.xOilFltrDPresSensorFault)
			self.inputRegisters[  39].addFlag(9, self.compressor.xOilFltrDPresHighAlarm)
			self.inputRegisters[  39].addFlag(10, self.compressor.xOilFltrDPresHighTrip)
	
			self.inputRegisters[  40].clearFlags()
			self.inputRegisters[  40].addFlag(0, self.compressor.x1stVibSensorFault)
			self.inputRegisters[  40].addFlag(1, self.compressor.x1stVibHighAlarmStart)
			self.inputRegisters[  40].addFlag(2, self.compressor.x1stVibHighTripStart)
			self.inputRegisters[  40].addFlag(3, self.compressor.x1stVibHighAlarmRun)
			self.inputRegisters[  40].addFlag(4, self.compressor.x1stVibHighTripRun)
			self.inputRegisters[  40].addFlag(5, self.compressor.x1stVibAbnormalTrip)
			self.inputRegisters[  40].addFlag(6, self.compressor.x1stVibAverageAAlarm)
			self.inputRegisters[  40].addFlag(7, self.compressor.x1stVibAverageBAlarm)
	
			self.inputRegisters[  40].addFlag(8, self.compressor.x2ndVibSensorFault)
			self.inputRegisters[  40].addFlag(9, self.compressor.x2ndVibHighAlarmStart)
			self.inputRegisters[  40].addFlag(10, self.compressor.x2ndVibHighTripStart)
			self.inputRegisters[  40].addFlag(11, self.compressor.x2ndVibHighAlarmRun)
			self.inputRegisters[  40].addFlag(12, self.compressor.x2ndVibHighTripRun)
			self.inputRegisters[  40].addFlag(13, self.compressor.x2ndVibAbnormalTrip)
			self.inputRegisters[  40].addFlag(14, self.compressor.x2ndVibAverageAAlarm)
			self.inputRegisters[  40].addFlag(15, self.compressor.x2ndVibAverageBAlarm)
	
			self.inputRegisters[  41].clearFlags()
			self.inputRegisters[  41].addFlag(0, self.compressor.x3rdVibSensorFault)
			self.inputRegisters[  41].addFlag(1, self.compressor.x3rdVibHighAlarmStart)
			self.inputRegisters[  41].addFlag(2, self.compressor.x3rdVibHighTripStart)
			self.inputRegisters[  41].addFlag(3, self.compressor.x3rdVibHighAlarmRun)
			self.inputRegisters[  41].addFlag(4, self.compressor.x3rdVibHighTripRun)
			self.inputRegisters[  41].addFlag(5, self.compressor.x3rdVibAbnormalTrip)
			self.inputRegisters[  41].addFlag(6, self.compressor.x3rdVibAverageAAlarm)
			self.inputRegisters[  41].addFlag(7, self.compressor.x3rdVibAverageBAlarm)
	
			self.inputRegisters[  41].addFlag(8, self.compressor.xAfterCoolerReturnTFault)
	
			self.inputRegisters[  41].addFlag(12, self.compressor.xCompDisTFault)
	
			self.inputRegisters[  42].clearFlags()
			self.inputRegisters[  42].addFlag(0, self.compressor.xOilTankTFault)
	
			self.inputRegisters[  42].addFlag(4, self.compressor.xSystemTFault)
	
			self.inputRegisters[  42].addFlag(8, self.compressor.xSuctionFltrDPresSensorFault)
			self.inputRegisters[  42].addFlag(9, self.compressor.xSuctionFltrDPresHighAlarm)
	
			self.inputRegisters[  42].addFlag(12, self.compressor.xOilTankLevelSensorFault)
			self.inputRegisters[  42].addFlag(13, self.compressor.xOilTankLevelLowAlarm)

			self.inputRegisters[6000].setValue(self.compressor.xDisSetPres)
			self.inputRegisters[6001].setValue(self.compressor.xReloadPres)
			self.inputRegisters[6002].setValue(self.compressor.xUnloadPres)
	
			self.inputRegisters[6003].setValue(self.compressor.xMaxCurrent)
			self.inputRegisters[6004].setValue(self.compressor.xMinCurrent)
			self.inputRegisters[6005].setValue(self.compressor.xCompLoadRatio)
			self.inputRegisters[6006].setValue(self.compressor.xLoadCurrent)
			self.inputRegisters[6007].setValue(self.compressor.xSergePreventCurrent)
			self.inputRegisters[6008].setValue(self.compressor.xModulationCurrent)
	
			self.inputRegisters[6009].setValue(self.compressor.xOilSupplyTemp)
			self.inputRegisters[6010].setValue(self.compressor.xOilTankTemp)
			self.inputRegisters[6011].setValue(self.compressor.x2ndInletTemp)
			self.inputRegisters[6012].setValue(self.compressor.x3rdInletTemp)
	
			self.inputRegisters[6013].setValue(self.compressor.xMBearingDETemp)
			self.inputRegisters[6014].setValue(self.compressor.xMBearingNDETemp)
			self.inputRegisters[6015].setValue(self.compressor.xMWindingRTemp)
			self.inputRegisters[6016].setValue(self.compressor.xMWindingSTemp)
			self.inputRegisters[6017].setValue(self.compressor.xMWindingTTemp)

			self.inputRegisters[6018].setValue(self.compressor.xDisPres)
			self.inputRegisters[6019].setValue(self.compressor.xDisPres)
			self.inputRegisters[6020].setValue(self.compressor.xMotorCurrent)
			self.inputRegisters[6021].setValue(self.compressor.xOilPres)

			self.inputRegisters[6022].setValue(self.compressor.x1stVib)
			self.inputRegisters[6023].setValue(self.compressor.x2ndVib)
			self.inputRegisters[6024].setValue(self.compressor.x3rdVib)
	
			self.inputRegisters[6025].setValue(self.compressor.xBOVOpenOutput)
	
			self.inputRegisters[6026].setValue(self.compressor.xCompRunTimeDay)
			self.inputRegisters[6027].setValue(self.compressor.xCompRunTimeHour)
			self.inputRegisters[6028].setValue(self.compressor.xCompRunCount10000)
			self.inputRegisters[6029].setValue(self.compressor.xCompRunCount1)
			self.inputRegisters[6030].setValue(self.compressor.xLoadRunTimeDay)
			self.inputRegisters[6031].setValue(self.compressor.xLoadRunTimeHour)
			self.inputRegisters[6032].setValue(self.compressor.xLoadRunCount10000)
			self.inputRegisters[6033].setValue(self.compressor.xLoadRunCount1)
			self.inputRegisters[6034].setValue(self.compressor.xPLCRunTimeDay)
			self.inputRegisters[6035].setValue(self.compressor.xPLCRunTimeHour)
			
			self.holdRegisters[ 200].setValue(self.compressor.xOilSupplyPresHighAlarm)
	
			self.holdRegisters[ 202].setValue(self.compressor.xOilSupplyPresLowAlarm)
			self.holdRegisters[ 203].setValue(self.compressor.xOilSupplyPresLowTrip)
			self.holdRegisters[ 204].setValue(self.compressor.xOilFltrDPresHighAlarm)
			self.holdRegisters[ 205].setValue(self.compressor.xOilFltrDPresHighTrip)
			self.holdRegisters[ 206].setValue(self.compressor.xOilSupplyTempHighAlarm)
			self.holdRegisters[ 207].setValue(self.compressor.xOilSupplyTempHighTrip)
			self.holdRegisters[ 208].setValue(self.compressor.xOilSupplyTempLowAlarm)
	
			self.holdRegisters[ 210].setValue(self.compressor.xOilTankLevelLowAlarm)
	
			self.holdRegisters[ 220].setValue(self.compressor.x2ndInletTempHighAlarm)
			self.holdRegisters[ 221].setValue(self.compressor.x2ndInletTempHighTrip)
			self.holdRegisters[ 222].setValue(self.compressor.x3rdInletTempHighAlarm)
			self.holdRegisters[ 223].setValue(self.compressor.x3rdInletTempHighTrip)
			self.holdRegisters[ 224].setValue(self.compressor.xCoolSupplyTempHighAlarm)
	
			self.holdRegisters[ 226].setValue(self.compressor.xCompDisPresLowAlarm)
			self.holdRegisters[ 227].setValue(self.compressor.xSuctionFltrDPresHighAlarm)
	
			self.holdRegisters[ 240].setValue(self.compressor.xVibStartingHighAlarm)
			self.holdRegisters[ 241].setValue(self.compressor.xVibStartingHighTrip)
			self.holdRegisters[ 242].setValue(self.compressor.xVibRuningHighAlarm)
			self.holdRegisters[ 243].setValue(self.compressor.xVibRuningHighTrip)
	
			self.holdRegisters[ 260].setValue(self.compressor.xMBearingTempHighAlarm)
			self.holdRegisters[ 261].setValue(self.compressor.xMBearingTempHighTrip)
			self.holdRegisters[ 262].setValue(self.compressor.xMWindingTempHighAlarm)
			self.holdRegisters[ 263].setValue(self.compressor.xMWindingTempHighTrip)
	
			self.holdRegisters[ 280].setValue(self.compressor.xOilExchangeTime)
			self.holdRegisters[ 281].setValue(self.compressor.xPLCBATExchangeTime)
	
			self.holdRegisters[ 300].setValue(self.compressor.xDisPres)
			self.holdRegisters[ 301].setValue(self.compressor.xReloadPres)


			self.holdRegisters[6100].setValue(self.compressor.xOilSupplyPresHighAlarm)
			self.holdRegisters[6101].setValue(self.compressor.xOilSupplyPresHighAlarm)
			self.holdRegisters[6102].setValue(self.compressor.xOilSupplyPresLowAlarm)
			self.holdRegisters[6103].setValue(self.compressor.xOilSupplyPresLowTrip)
			self.holdRegisters[6104].setValue(self.compressor.xOilFltrDPresHighAlarm)
			self.holdRegisters[6105].setValue(self.compressor.xOilFltrDPresHighTrip)
			self.holdRegisters[6106].setValue(self.compressor.xOilSupplyTempHighAlarm)
			self.holdRegisters[6107].setValue(self.compressor.xOilSupplyTempHighTrip)
			self.holdRegisters[6108].setValue(self.compressor.xOilSupplyTempLowAlarm)
			self.holdRegisters[6119].setValue(self.compressor.xOilTankLevelLowAlarm)
			self.holdRegisters[6110].setValue(self.compressor.x2ndInletTempHighAlarm)
			self.holdRegisters[6111].setValue(self.compressor.x2ndInletTempHighTrip)
			self.holdRegisters[6112].setValue(self.compressor.x3rdInletTempHighAlarm)
			self.holdRegisters[6113].setValue(self.compressor.x3rdInletTempHighTrip)
			self.holdRegisters[6114].setValue(self.compressor.xCoolSupplyTempHighAlarm)
			self.holdRegisters[6115].setValue(self.compressor.xCompDisPresLowAlarm)
			self.holdRegisters[6116].setValue(self.compressor.xSuctionFltrDPresHighAlarm)
			self.holdRegisters[6117].setValue(self.compressor.xVibStartingHighAlarm)
			self.holdRegisters[6118].setValue(self.compressor.xVibStartingHighTrip)
			self.holdRegisters[6119].setValue(self.compressor.xVibRuningHighAlarm)
			self.holdRegisters[6120].setValue(self.compressor.xVibRuningHighTrip)
			self.holdRegisters[6121].setValue(self.compressor.xMBearingTempHighAlarm)
			self.holdRegisters[6122].setValue(self.compressor.xMBearingTempHighTrip)

			self.holdRegisters[   0].clearFlags()
			self.holdRegisters[   0].addFlag( 0, self.blower.xReset)
			self.holdRegisters[   0].addFlag( 1, self.blower.xRunOper)
			self.holdRegisters[   0].addFlag( 2, self.blower.xStopOper)
			self.holdRegisters[   0].addFlag( 3, self.blower.xSpeedOper)
			self.holdRegisters[   0].addFlag( 4, self.blower.xFlowOper)
			self.holdRegisters[   0].addFlag( 5, self.blower.xPowerOper)
			self.holdRegisters[   0].addFlag( 6, self.blower.xPropotionOper)
			self.holdRegisters[   0].addFlag( 7, self.blower.xDOxygenOper)
			self.holdRegisters[   0].addFlag( 8, self.blower.xPresOper)
			self.holdRegisters[   0].addFlag(14, self.blower.xMCPEmrgRls)
			self.holdRegisters[   0].addFlag(15, self.blower.xRemoteCheckPulse)
			self.holdRegisters[   1].setValue(self.blower.xPrimarySV)
			self.holdRegisters[   2].setValue(self.blower.xSecondarySV)
			self.holdRegisters[   5].clearFlags()
			self.holdRegisters[   5].addFlag( 1, self.blower.xRepeatOper)
			self.holdRegisters[   5].addFlag( 2, self.blower.xBOVRun)
			self.holdRegisters[   5].addFlag( 3, self.blower.xAuxRun)
			self.holdRegisters[   5].addFlag( 4, self.blower.xRestartDelay)
			self.holdRegisters[   5].addFlag( 5, self.blower.xSurgeControl)
			self.holdRegisters[   5].addFlag( 6, self.blower.xPowerControl)
			self.holdRegisters[   5].addFlag( 8, self.blower.xDriveReady)
			self.holdRegisters[   5].addFlag( 9, self.blower.xBlowReady)
			self.holdRegisters[   5].addFlag(13, self.blower.xRunStatus)
			self.holdRegisters[   5].addFlag(14, self.blower.xStopStatus)
			self.holdRegisters[   5].addFlag(15, self.blower.xResetStatus)
			self.holdRegisters[   6].clearFlags()
			self.holdRegisters[   6].addFlag( 0, self.blower.xEmrgStopRlsTrip)
			self.holdRegisters[   6].addFlag( 1, self.blower.xEOCRlsTrip)
			self.holdRegisters[   6].addFlag( 4, self.blower.xFeedTrip)
			self.holdRegisters[   6].addFlag( 5, self.blower.xSurgeTrip)
			self.holdRegisters[   6].addFlag(14, self.blower.xDriveCommTrip)
			self.holdRegisters[   6].addFlag(15, self.blower.xRemoteCommTrip)
			self.holdRegisters[   7].clearFlags()
			self.holdRegisters[   7].addFlag( 1, self.blower.xDischargePresHighTrip)
			self.holdRegisters[   7].addFlag( 2, self.blower.xFilterPresHighTrip)
			self.holdRegisters[   7].addFlag( 3, self.blower.xPumpPresHighTrip)
			self.holdRegisters[   7].addFlag( 4, self.blower.xPumpPresLowTrip)
			self.holdRegisters[   7].addFlag( 5, self.blower.xSuctionPresHighTrip)
			self.holdRegisters[   7].addFlag( 7, self.blower.xMoterTempHighTrip)
			self.holdRegisters[   7].addFlag( 8, self.blower.xVibrationTrip)
			self.holdRegisters[   7].addFlag( 9, self.blower.xBearingTempHighTrip)
			self.holdRegisters[   7].addFlag(10, self.blower.xDriveTempHighTrip)
			self.holdRegisters[   7].addFlag(12, self.blower.xSuctionPresSensorFault)
			self.holdRegisters[   7].addFlag(13, self.blower.xDischargePresSensorFault)
			self.holdRegisters[   7].addFlag(14, self.blower.xFilterPresSensorFault)
			self.holdRegisters[   7].addFlag(15, self.blower.xPumpPresSensorFault)
			self.holdRegisters[   8].clearFlags()
			self.holdRegisters[   8].addFlag( 0, self.blower.xUnknownDriveTrip)
			self.holdRegisters[   8].addFlag( 1, self.blower.xOvervoltageTrip)
			self.holdRegisters[   8].addFlag( 2, self.blower.xLowvoltageTrip)
			self.holdRegisters[   8].addFlag( 3, self.blower.xDixoTrip)
			self.holdRegisters[   8].addFlag( 4, self.blower.xDooxTrip)
			self.holdRegisters[   8].addFlag( 5, self.blower.xOverheatingTrip)
			self.holdRegisters[   8].addFlag( 6, self.blower.xFuseTrip)
			self.holdRegisters[   8].addFlag( 7, self.blower.xOverloadTrip)
			self.holdRegisters[   8].addFlag( 8, self.blower.xOvercurrentTrip)
			self.holdRegisters[   8].addFlag( 9, self.blower.xOverspeedTrip)
			self.holdRegisters[   8].addFlag(10, self.blower.xDzsxTrip)
			self.holdRegisters[   8].addFlag(11, self.blower.xShortTrip)
			self.holdRegisters[   8].addFlag(12, self.blower.xCommErrorTrip)
			self.holdRegisters[   8].addFlag(13, self.blower.xFanErrorTrip)
			self.holdRegisters[   8].addFlag(14, self.blower.xMotorOvercurrentTrip)
			self.holdRegisters[   8].addFlag(15, self.blower.xDriveReadyErrorTrip)
			self.holdRegisters[   9].clearFlags()
			self.holdRegisters[   9].addFlag( 0, self.blower.xStartReadyTrip)
			self.holdRegisters[   9].addFlag( 1, self.blower.xRemoteControlStatus)
			self.holdRegisters[   9].addFlag( 2, self.blower.xRunStatus)
			self.holdRegisters[   9].addFlag( 3, self.blower.xWarningStatus)
			self.holdRegisters[   9].addFlag( 4, self.blower.xFaultStatus)
			self.holdRegisters[   9].addFlag( 5, self.blower.xDriveRunStatus)
			self.holdRegisters[   9].addFlag( 8, self.blower.xSpeedModeStatus)
			self.holdRegisters[   9].addFlag( 9, self.blower.xFlowModeStatus)
			self.holdRegisters[   9].addFlag(10, self.blower.xPowerModeStatus)
			self.holdRegisters[   9].addFlag(11, self.blower.xPropotionModeStatus)
			self.holdRegisters[   9].addFlag(12, self.blower.xDOxygenModeStatus)
			self.holdRegisters[   9].addFlag(13, self.blower.xPresModeStatus)
			self.holdRegisters[   9].addFlag(15, self.blower.xCommScanPluse)
			self.holdRegisters[  10].clearFlags()
			self.holdRegisters[  10].addFlag( 1, self.blower.xDischargePresWarning)
			self.holdRegisters[  10].addFlag( 2, self.blower.xFliterPresWarning)
			self.holdRegisters[  10].addFlag( 3, self.blower.xPumpPresUpWarning)
			self.holdRegisters[  10].addFlag( 4, self.blower.xPumpPresDownWarning)
			self.holdRegisters[  10].addFlag( 5, self.blower.xSuctionTempUpWarning)
			self.holdRegisters[  10].addFlag( 6, self.blower.xDischargeTempUpWarning)
			self.holdRegisters[  10].addFlag( 7, self.blower.xMotorTempUpWarning)
			self.holdRegisters[  10].addFlag( 8, self.blower.xAirTempUpWarning)
			self.holdRegisters[  10].addFlag( 9, self.blower.xAirTempDownWarning)
			self.holdRegisters[  10].addFlag(10, self.blower.xDriveTempUpWarning)
			self.holdRegisters[  10].addFlag(14, self.blower.xPresSensorFaultWarning)
			self.holdRegisters[  10].addFlag(15, self.blower.xTempSensorFaultWarning)
			self.holdRegisters[  11].setValue(self.blower.xFlow)
			self.holdRegisters[  12].setValue(self.blower.xDischargePres)
			self.holdRegisters[  13].setValue(self.blower.xAirTemp)
			self.holdRegisters[  14].setValue(self.blower.xMotorTemp)
			self.holdRegisters[  15].setValue(self.blower.xDriveTemp)
			self.holdRegisters[  16].setValue(self.blower.xDischargeTemp)
			self.holdRegisters[  17].setValue(self.blower.xPowerConsumption)
			self.holdRegisters[  18].setValue(self.blower.xMotorCurrent)
			self.holdRegisters[  19].setValue(self.blower.xFrequency)
			self.holdRegisters[  20].setValue(self.blower.xMotorFrequency)
			self.holdRegisters[  21].setValue(self.blower.xStartCount)
			self.holdRegisters[  22].setValue(self.blower.xRunningDays)
			self.holdRegisters[  23].setValue(self.blower.xRunningHours)
			self.holdRegisters[  24].setValue(self.blower.xRunningMinutes)
			self.holdRegisters[  25].setValue(self.blower.xFilterPres)
			self.holdRegisters[  26].setValue(self.blower.xSuctionPres)
			self.holdRegisters[  27].setValue(self.blower.xVibration)
			self.holdRegisters[  28].setValue(self.blower.xBearingTemp)
			self.holdRegisters[  29].setValue(self.blower.xNumber)
			
			time.sleep(1)

class MBTCPSERVER(threading.Thread):
	def __init__(self, host, port, coilRegisters, discreteRegisters, inputRegisters, holdRegisters):
		threading.Thread.__init__(self) 
		# A very simple data store which maps addresses against their values.
		self.coilRegisters = coilRegisters
		self.discreteRegisters = discreteRegisters
		self.inputRegisters = inputRegisters
		self.holdRegisters = holdRegisters

		# Enable values to be signed (default is False).
		conf.SIGNED_VALUES = True

		TCPServer.allow_reuse_address = True
		self.app = get_server(TCPServer, (host, port), RequestHandler)
		print(self.app)

		@self.app.route(slave_ids=[1, 2], function_codes=[1, 2, 3, 4], addresses=list(range(0, 9999)))
		def read_data_store(slave_id, function_code, address):
			try:
				value = 0
				"""" Return value of address. """
				if (function_code == 0):
					value = randint(0, 1)
				elif (function_code == 1):
					value = randint(0, 1)
				elif (function_code == 3):
					value = randint(0, 1000)
				elif (function_code == 4):
					value = randint(0, 1000)
				else:
					value = 0
				#print('Read Data :', function_code, address, value)
				if (value < 32768):
					return	value
				else:
					return	value - 65536
			except Exception as inst:
				print('Read Data :', function_code, address)
				print('Ecception :', inst)
				return 0


		@self.app.route(slave_ids=[1, 2], function_codes=[5, 15], addresses=list(range(0, 9999)))
		def write_data_store(slave_id, function_code, address, value):
			try:
				"""" Set value for address. """
				#print('Write Data :', function_code, address, value)
				if (function_code == 5):
					self.holdRegisters[address].setValue(value)
			except:
				print('Write Data :', function_code, address, value)
				print('Exception')

	def run(self):
		self.app.serve_forever()
	
	def stop(self):
		self.app.shutdown()
		self.app.server_close()
  
if __name__ == '__main__':
	try:
		coilRegisters=  defaultdict(ValueSet)
		discreteRegisters=  defaultdict(ValueSet)
		inputRegisters=  defaultdict(ValueSet)
		holdRegisters =  defaultdict(ValueSet)
		test = TESTCORE(coilRegisters, discreteRegisters, inputRegisters, holdRegisters)
		test.start()
		servers = []
		servers.append(MBTCPSERVER('0.0.0.0', 502, coilRegisters, discreteRegisters, inputRegisters, holdRegisters))
		servers.append(MBTCPSERVER('0.0.0.0', 503, coilRegisters, discreteRegisters, inputRegisters, holdRegisters))
		servers.append(MBTCPSERVER('0.0.0.0', 504, coilRegisters, discreteRegisters, inputRegisters, holdRegisters))
		for server in servers:
			server.start()
	except Exception as err:
		print(err)
