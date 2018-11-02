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

			self.addValue(offset / 2 - random.randint(0, offset))
		else:
			if random.randint(0, 100) < 50:
				self.setValue(self.min)
			else:
				self.setValue(self.max)

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
		self.xAirTemp=SensorSim(CONF_TEMPERATURE_MIN,CONF_TEMPERATURE_MAX / 10) 
		self.xMotorTemp=SensorSim(CONF_TEMPERATURE_MIN,CONF_TEMPERATURE_MAX / 10) 
		self.xDriveTemp=SensorSim(CONF_TEMPERATURE_MIN,CONF_TEMPERATURE_MAX / 10) 
		self.xDischargeTemp=SensorSim(CONF_TEMPERATURE_MIN,CONF_TEMPERATURE_MAX / 10) 
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
		self.xBearingTemp=SensorSim(CONF_TEMPERATURE_MIN,CONF_TEMPERATURE_MAX / 10) 
		self.xNumber=SensorSim(0, 10000)

	def	run(self):
		while True:
			self.xReset.addRandomValue()
			self.xRunOper.addRandomValue()
			self.xStopOper.addRandomValue()
			self.xSpeedOper.addRandomValue()
			self.xFlowOper.addRandomValue()
			self.xPowerOper.addRandomValue()
			self.xPropotionOper.addRandomValue()
			self.xDOxygenOper.addRandomValue()
			self.xPresOper.addRandomValue()
			self.xMCPEmrgRls.addRandomValue()
			self.xRemoteCheckPulse.addRandomValue()
			self.xPrimarySV.addRandomValue()
			self.xSecondarySV.addRandomValue()
			self.xRepeatOper.addRandomValue()
			self.xBOVRun.addRandomValue()
			self.xAuxRun.addRandomValue()
			self.xRestartDelay.addRandomValue()
			self.xSurgeControl.addRandomValue()
			self.xPowerControl.addRandomValue()
			self.xDriveReady.addRandomValue()
			self.xBlowReady.addRandomValue()
			self.xRunStatus.addRandomValue()
			self.xStopStatus.addRandomValue()
			self.xResetStatus.addRandomValue()
			self.xEmrgStopRlsTrip.addRandomValue()
			self.xEOCRlsTrip.addRandomValue()
			self.xFeedTrip.addRandomValue()
			self.xSurgeTrip.addRandomValue()
			self.xDriveCommTrip.addRandomValue()
			self.xRemoteCommTrip.addRandomValue()
			self.xDischargePresHighTrip.addRandomValue()
			self.xFilterPresHighTrip.addRandomValue()
			self.xPumpPresHighTrip.addRandomValue()
			self.xPumpPresLowTrip.addRandomValue()
			self.xSuctionPresHighTrip.addRandomValue()
			self.xMoterTempHighTrip.addRandomValue()
			self.xVibrationTrip.addRandomValue()
			self.xBearingTempHighTrip.addRandomValue()
			self.xDriveTempHighTrip.addRandomValue()
			self.xSuctionPresSensorFault.addRandomValue()
			self.xDischargePresSensorFault.addRandomValue()
			self.xFilterPresSensorFault.addRandomValue()
			self.xPumpPresSensorFault.addRandomValue()
			self.xUnknownDriveTrip.addRandomValue()
			self.xOvervoltageTrip.addRandomValue()
			self.xLowvoltageTrip.addRandomValue()
			self.xDixoTrip.addRandomValue()
			self.xDooxTrip.addRandomValue()
			self.xOverheatingTrip.addRandomValue()
			self.xFuseTrip.addRandomValue()
			self.xOverloadTrip.addRandomValue()
			self.xOvercurrentTrip.addRandomValue()
			self.xOverspeedTrip.addRandomValue()
			self.xDzsxTrip.addRandomValue()
			self.xShortTrip.addRandomValue()
			self.xCommErrorTrip.addRandomValue()
			self.xFanErrorTrip.addRandomValue()
			self.xMotorOvercurrentTrip.addRandomValue()
			self.xDriveReadyErrorTrip.addRandomValue()
			self.xStartReadyTrip.addRandomValue()
			self.xRemoteControlStatus.addRandomValue()
			self.xRunStatus.addRandomValue()
			self.xWarningStatus.addRandomValue()
			self.xFaultStatus.addRandomValue()
			self.xDriveRunStatus.addRandomValue()
			self.xSpeedModeStatus.addRandomValue()
			self.xFlowModeStatus.addRandomValue()
			self.xPowerModeStatus.addRandomValue()
			self.xPropotionModeStatus.addRandomValue()
			self.xDOxygenModeStatus.addRandomValue()
			self.xPresModeStatus.addRandomValue()
			self.xCommScanPluse.addRandomValue()
			self.xDischargePresWarning.addRandomValue()
			self.xFliterPresWarning.addRandomValue()
			self.xPumpPresUpWarning.addRandomValue()
			self.xPumpPresDownWarning.addRandomValue()
			self.xSuctionTempUpWarning.addRandomValue()
			self.xDischargeTempUpWarning.addRandomValue()
			self.xMotorTempUpWarning.addRandomValue()
			self.xAirTempUpWarning.addRandomValue()
			self.xAirTempDownWarning.addRandomValue()
			self.xDriveTempUpWarning.addRandomValue()
			self.xPresSensorFaultWarning.addRandomValue()
			self.xTempSensorFaultWarning.addRandomValue()
			self.xFlow.addRandomValue()
			self.xDischargePres.addRandomValue()
			self.xAirTemp.addRandomValue()
			self.xMotorTemp.addRandomValue()
			self.xDriveTemp.addRandomValue()
			self.xDischargeTemp.addRandomValue()
			self.xPowerConsumption.addRandomValue()
			self.xMotorCurrent.addRandomValue()
			self.xFrequency.addRandomValue()
			self.xMotorFrequency.addRandomValue()
			self.xStartCount.addRandomValue()
			self.xRunningDays.addRandomValue()
			self.xRunningHours.addRandomValue()
			self.xRunningMinutes.addRandomValue()
			self.xFilterPres.addRandomValue()
			self.xSuctionPres.addRandomValue()
			self.xVibration.addRandomValue()
			self.xBearingTemp.addRandomValue()
			self.xNumber.addRandomValue()

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
			self.xDisPres.addRandomValue()
			self.xDisSetPres.addRandomValue()
			self.xReloadPres.addRandomValue()
			self.xUnloadPres.addRandomValue()
	
			self.xMotorCurrent.addRandomValue()
			self.xMaxCurrent.addRandomValue()
			self.xMinCurrent.addRandomValue()
			self.xCompLoadRatio.addRandomValue()
			self.xLoadCurrent.addRandomValue()
			self.xSergePreventCurrent.addRandomValue()
			self.xModulationCurrent.addRandomValue()
	
			self.xOilPres.addRandomValue()
			self.xOilDPres.addRandomValue()
			self.xOilSupplyTemp.addRandomValue()
			self.xOilTankTemp.addRandomValue()
			self.xOilTankLevel.addRandomValue()
	
			self.x1stVib.addRandomValue()
			self.x2ndVib.addRandomValue()
			self.x3rdVib.addRandomValue()
	
			self.xMBearingDETemp.addRandomValue()
			self.xMBearingNDETemp.addRandomValue()
			self.xMWindingRTemp.addRandomValue()
			self.xMWindingSTemp.addRandomValue()
			self.xMWindingTTemp.addRandomValue()
	
			self.xSuctionFltrDPres.addRandomValue()
			self.x2ndInletTemp.addRandomValue()
			self.x3rdInletTemp.addRandomValue()
	
			self.xCoolSupplytemp.addRandomValue()
			self.xOilCoolerReturnTemp.addRandomValue()
			self.x1stIntercoolerReturnTemp.addRandomValue()
			self.x2ndIntercoolerReturnTemp.addRandomValue()
			self.xAfterCoolerReturnTemp.addRandomValue()
	
			self.xDisTemp.addRandomValue()
			self.xSystemTemp.addRandomValue()
	
			self.xBOVOpenOutput.addRandomValue()
			self.xBOVOpenFeedback.addRandomValue()
			self.xIGVOpenOutput.addRandomValue()
			self.xIGVOpenFeedback.addRandomValue()
	
			self.xCompRunTimeDay.addRandomValue()
			self.xCompRunTimeHour.addRandomValue()
			self.xCompRunCount10000.addRandomValue()
			self.xCompRunCount1.addRandomValue()
			self.xLoadRunTimeDay.addRandomValue()
			self.xLoadRunTimeHour.addRandomValue()
			self.xLoadRunCount10000.addRandomValue()
			self.xLoadRunCount1.addRandomValue()
			self.xPLCRunTimeDay.addRandomValue()
			self.xPLCRunTimeHour.addRandomValue()
	
			self.xOilSupplyPresHighAlarm.addRandomValue()
	
			self.xOilSupplyPresLowAlarm.addRandomValue()
			self.xOilSupplyPresLowTrip.addRandomValue()
			self.xOilFltrDPresHighAlarm.addRandomValue()
			self.xOilFltrDPresHighTrip.addRandomValue()
			self.xOilSupplyTempHighAlarm.addRandomValue()
			self.xOilSupplyTempHighTrip.addRandomValue()
			self.xOilSupplyTempLowAlarm.addRandomValue()
	
			self.xOilTankLevelLowAlarm.addRandomValue()
	
			self.x2ndInletTempHighAlarm.addRandomValue()
			self.x2ndInletTempHighTrip.addRandomValue()
			self.x3rdInletTempHighAlarm.addRandomValue()
			self.x3rdInletTempHighTrip.addRandomValue()
			self.xCoolSupplyTempHighAlarm.addRandomValue()
	
			self.xCompDisPresLowAlarm.addRandomValue()
			self.xSuctionFltrDPresHighAlarm.addRandomValue()
	
			self.xVibStartingHighAlarm.addRandomValue()
			self.xVibStartingHighTrip.addRandomValue()
			self.xVibRuningHighAlarm.addRandomValue()
			self.xVibRuningHighTrip.addRandomValue()
	
			self.xMBearingTempHighAlarm.addRandomValue()
			self.xMBearingTempHighTrip.addRandomValue()
			self.xMWindingTempHighAlarm.addRandomValue()
			self.xMWindingTempHighTrip.addRandomValue()
	
			self.xOilExchangeTime.addRandomValue()
			self.xPLCBATExchangeTime.addRandomValue()
	
			self.xDisPres.addRandomValue()
			self.xReloadPres.addRandomValue()

			self.xCommonTrip.addRandomValue()
			self.xCommonAlarm.addRandomValue()
			self.xCommonSensorFault.addRandomValue()
			self.xAlarmResetting.addRandomValue()
	
			self.xCompReady.addRandomValue()
			self.xOilTempReady.addRandomValue()
			self.xOilPresReady.addRandomValue()
			self.xNotReadyAlarm.addRandomValue()
			self.xCompRestartTime.addRandomValue()
	
			self.xCompRun.addRandomValue()
			self.xCompStop.addRandomValue()
			self.xCompTripStop.addRandomValue()
			self.xCompStarting.addRandomValue()
			self.xCompStopping.addRandomValue()
	
			self.xLocalgRemoteSelect.addRandomValue()
			self.xLoadgUnloadSelect.addRandomValue()
			self.xLoadMode.addRandomValue()
			self.xModulationMode.addRandomValue()
			self.xForceUnloading.addRandomValue()
	
			self.xAuxOilPumpRungStop.addRandomValue()
			self.xAuxOilPumpStopping.addRandomValue()
			self.xEjectorExhFanRungStop.addRandomValue()
			self.xOilHeaterOngOff.addRandomValue()
	
			self.xPLCRebooting.addRandomValue()
			self.xCompEmergencyStop.addRandomValue()
			self.xCompStarterPaneltrip.addRandomValue()
			self.xAuxOilPumpEOCRTrip.addRandomValue()
			self.xExhaustFanEOCRTrip.addRandomValue()
			self.xOilExchangeTimeAlarm.addRandomValue()
			self.xPLCBATVoltageLowAlarm.addRandomValue()
			self.xPLCBATExchangeTimeAlarm.addRandomValue()
	
			self.xSurgeUnload.addRandomValue()
			self.xSurgeHalfUnload.addRandomValue()
			self.xSurgeCount1.addRandomValue()
			self.xSurgeCount2.addRandomValue()
			self.xSurgeCount3.addRandomValue()
			self.xSurgeCount4.addRandomValue()
			self.xSurgeCount5.addRandomValue()
	
			self.x2ndInletTFault.addRandomValue()
			self.x2ndInletTempHighAlarm.addRandomValue()
			self.x2ndInletTempHighTrip.addRandomValue()
	
			self.x3rdInletTFault.addRandomValue()
			self.x3rdInletTempHighAlarm.addRandomValue()
			self.x3rdInletTempHighTrip.addRandomValue()
	
			self.xOilTFault.addRandomValue()
			self.xOilTempHighAlarm.addRandomValue()
			self.xOilTempHighTrip.addRandomValue()
			self.xOilTempLowAlarm.addRandomValue()
	
			self.xCoolSupplyTFault.addRandomValue()
			self.xCoolSupplyTempHighAlarm.addRandomValue()
	
			self.x1stIntercoolerReturnTFault.addRandomValue()
	
			self.x2ndIntercoolerReturnTFault.addRandomValue()
	
			self.xOilIntercoolerReturnTFault.addRandomValue()
	
			self.xMBearingDETSensorFaullt.addRandomValue()
			self.xMBearingDETempHighAlarm.addRandomValue()
			self.xMBearingDETempHighTrip.addRandomValue()
	
			self.xMBearingNDETSensorFaullt.addRandomValue()
			self.xMBearingNDETempHighAlarm.addRandomValue()
			self.xMBearingNDETempHighTrip.addRandomValue()
	
			self.xMWindingRTFault.addRandomValue()
			self.xMWindingRTempHighAlarm.addRandomValue()
			self.xMWindingRTempHighTrip.addRandomValue()
	
			self.xMWindingSTFault.addRandomValue()
			self.xMWindingSTempHighAlarm.addRandomValue()
			self.xMWindingSTempHighTrip.addRandomValue()
	
			self.xMWindingTTFault.addRandomValue()
			self.xMWindingTTempHighAlarm.addRandomValue()
			self.xMWindingTTempHighTrip.addRandomValue()
	
			self.xCompDisPresSensorFault.addRandomValue()
			self.xCompDisPresLowAlarm.addRandomValue()
	
			self.xMotorCurrentSensorFault.addRandomValue()
	
			self.xMotorCurrentLowTrip.addRandomValue()
			self.xMotorCurrentAbnormalTrip.addRandomValue()
	
			self.xOilPresSensorFault.addRandomValue()
			self.xOilPresHighAlarm.addRandomValue()
	
			self.xOilPresLowAlarm.addRandomValue()
			self.xOilPresLowTrip.addRandomValue()
			self.xOilPresLowTripStart.addRandomValue()
	
			self.xOilFltrDPresSensorFault.addRandomValue()
			self.xOilFltrDPresHighAlarm.addRandomValue()
			self.xOilFltrDPresHighTrip.addRandomValue()
	
			self.x1stVibSensorFault.addRandomValue()
			self.x1stVibHighAlarmStart.addRandomValue()
			self.x1stVibHighTripStart.addRandomValue()
			self.x1stVibHighAlarmRun.addRandomValue()
			self.x1stVibHighTripRun.addRandomValue()
			self.x1stVibAbnormalTrip.addRandomValue()
			self.x1stVibAverageAAlarm.addRandomValue()
			self.x1stVibAverageBAlarm.addRandomValue()
	
			self.x2ndVibSensorFault.addRandomValue()
			self.x2ndVibHighAlarmStart.addRandomValue()
			self.x2ndVibHighTripStart.addRandomValue()
			self.x2ndVibHighAlarmRun.addRandomValue()
			self.x2ndVibHighTripRun.addRandomValue()
			self.x2ndVibAbnormalTrip.addRandomValue()
			self.x2ndVibAverageAAlarm.addRandomValue()
			self.x2ndVibAverageBAlarm.addRandomValue()
	
			self.x3rdVibSensorFault.addRandomValue()
			self.x3rdVibHighAlarmStart.addRandomValue()
			self.x3rdVibHighTripStart.addRandomValue()
			self.x3rdVibHighAlarmRun.addRandomValue()
			self.x3rdVibHighTripRun.addRandomValue()
			self.x3rdVibAbnormalTrip.addRandomValue()
			self.x3rdVibAverageAAlarm.addRandomValue()
			self.x3rdVibAverageBAlarm.addRandomValue()
	
			self.xAfterCoolerReturnTFault.addRandomValue()
	
			self.xCompDisTFault.addRandomValue()
	
			self.xOilTankTFault.addRandomValue()
	
			self.xSystemTFault.addRandomValue()
	
			self.xSuctionFltrDPresSensorFault.addRandomValue()
			self.xSuctionFltrDPresHighAlarm.addRandomValue()
	
			self.xOilTankLevelSensorFault.addRandomValue()
			self.xOilTankLevelLowAlarm.addRandomValue()

			time.sleep(10)

class TESTCORE(threading.Thread):
	def __init__(self, inputRegisters, holdRegisters):
		threading.Thread.__init__(self) 
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


			self.holdRegisters[   1].clearFlags()
			self.holdRegisters[   1].addFlag( 0, self.blower.xReset)
			self.holdRegisters[   1].addFlag( 1, self.blower.xRunOper)
			self.holdRegisters[   1].addFlag( 2, self.blower.xStopOper)
			self.holdRegisters[   1].addFlag( 3, self.blower.xSpeedOper)
			self.holdRegisters[   1].addFlag( 4, self.blower.xFlowOper)
			self.holdRegisters[   1].addFlag( 5, self.blower.xPowerOper)
			self.holdRegisters[   1].addFlag( 6, self.blower.xPropotionOper)
			self.holdRegisters[   1].addFlag( 7, self.blower.xDOxygenOper)
			self.holdRegisters[   1].addFlag( 8, self.blower.xPresOper)
			self.holdRegisters[   1].addFlag(14, self.blower.xMCPEmrgRls)
			self.holdRegisters[   1].addFlag(15, self.blower.xRemoteCheckPulse)
			self.holdRegisters[   2].setValue(self.blower.xPrimarySV)
			self.holdRegisters[   3].setValue(self.blower.xSecondarySV)
			self.holdRegisters[   6].clearFlags()
			self.holdRegisters[   6].addFlag( 1, self.blower.xRepeatOper)
			self.holdRegisters[   6].addFlag( 2, self.blower.xBOVRun)
			self.holdRegisters[   6].addFlag( 3, self.blower.xAuxRun)
			self.holdRegisters[   6].addFlag( 4, self.blower.xRestartDelay)
			self.holdRegisters[   6].addFlag( 5, self.blower.xSurgeControl)
			self.holdRegisters[   6].addFlag( 6, self.blower.xPowerControl)
			self.holdRegisters[   6].addFlag( 8, self.blower.xDriveReady)
			self.holdRegisters[   6].addFlag( 9, self.blower.xBlowReady)
			self.holdRegisters[   6].addFlag(13, self.blower.xRunStatus)
			self.holdRegisters[   6].addFlag(14, self.blower.xStopStatus)
			self.holdRegisters[   6].addFlag(15, self.blower.xResetStatus)
			self.holdRegisters[   7].clearFlags()
			self.holdRegisters[   7].addFlag( 0, self.blower.xEmrgStopRlsTrip)
			self.holdRegisters[   7].addFlag( 1, self.blower.xEOCRlsTrip)
			self.holdRegisters[   7].addFlag( 4, self.blower.xFeedTrip)
			self.holdRegisters[   7].addFlag( 5, self.blower.xSurgeTrip)
			self.holdRegisters[   7].addFlag(14, self.blower.xDriveCommTrip)
			self.holdRegisters[   7].addFlag(15, self.blower.xRemoteCommTrip)
			self.holdRegisters[   8].clearFlags()
			self.holdRegisters[   8].addFlag( 1, self.blower.xDischargePresHighTrip)
			self.holdRegisters[   8].addFlag( 2, self.blower.xFilterPresHighTrip)
			self.holdRegisters[   8].addFlag( 3, self.blower.xPumpPresHighTrip)
			self.holdRegisters[   8].addFlag( 4, self.blower.xPumpPresLowTrip)
			self.holdRegisters[   8].addFlag( 5, self.blower.xSuctionPresHighTrip)
			self.holdRegisters[   8].addFlag( 7, self.blower.xMoterTempHighTrip)
			self.holdRegisters[   8].addFlag( 8, self.blower.xVibrationTrip)
			self.holdRegisters[   8].addFlag( 9, self.blower.xBearingTempHighTrip)
			self.holdRegisters[   8].addFlag(10, self.blower.xDriveTempHighTrip)
			self.holdRegisters[   8].addFlag(12, self.blower.xSuctionPresSensorFault)
			self.holdRegisters[   8].addFlag(13, self.blower.xDischargePresSensorFault)
			self.holdRegisters[   8].addFlag(14, self.blower.xFilterPresSensorFault)
			self.holdRegisters[   8].addFlag(15, self.blower.xPumpPresSensorFault)
			self.holdRegisters[   9].clearFlags()
			self.holdRegisters[   9].addFlag( 0, self.blower.xUnknownDriveTrip)
			self.holdRegisters[   9].addFlag( 1, self.blower.xOvervoltageTrip)
			self.holdRegisters[   9].addFlag( 2, self.blower.xLowvoltageTrip)
			self.holdRegisters[   9].addFlag( 3, self.blower.xDixoTrip)
			self.holdRegisters[   9].addFlag( 4, self.blower.xDooxTrip)
			self.holdRegisters[   9].addFlag( 5, self.blower.xOverheatingTrip)
			self.holdRegisters[   9].addFlag( 6, self.blower.xFuseTrip)
			self.holdRegisters[   9].addFlag( 7, self.blower.xOverloadTrip)
			self.holdRegisters[   9].addFlag( 8, self.blower.xOvercurrentTrip)
			self.holdRegisters[   9].addFlag( 9, self.blower.xOverspeedTrip)
			self.holdRegisters[   9].addFlag(10, self.blower.xDzsxTrip)
			self.holdRegisters[   9].addFlag(11, self.blower.xShortTrip)
			self.holdRegisters[   9].addFlag(12, self.blower.xCommErrorTrip)
			self.holdRegisters[   9].addFlag(13, self.blower.xFanErrorTrip)
			self.holdRegisters[   9].addFlag(14, self.blower.xMotorOvercurrentTrip)
			self.holdRegisters[   9].addFlag(15, self.blower.xDriveReadyErrorTrip)
			self.holdRegisters[  10].clearFlags()
			self.holdRegisters[  10].addFlag( 0, self.blower.xStartReadyTrip)
			self.holdRegisters[  10].addFlag( 1, self.blower.xRemoteControlStatus)
			self.holdRegisters[  10].addFlag( 2, self.blower.xRunStatus)
			self.holdRegisters[  10].addFlag( 3, self.blower.xWarningStatus)
			self.holdRegisters[  10].addFlag( 4, self.blower.xFaultStatus)
			self.holdRegisters[  10].addFlag( 5, self.blower.xDriveRunStatus)
			self.holdRegisters[  10].addFlag( 8, self.blower.xSpeedModeStatus)
			self.holdRegisters[  10].addFlag( 9, self.blower.xFlowModeStatus)
			self.holdRegisters[  10].addFlag(10, self.blower.xPowerModeStatus)
			self.holdRegisters[  10].addFlag(11, self.blower.xPropotionModeStatus)
			self.holdRegisters[  10].addFlag(12, self.blower.xDOxygenModeStatus)
			self.holdRegisters[  10].addFlag(13, self.blower.xPresModeStatus)
			self.holdRegisters[  10].addFlag(15, self.blower.xCommScanPluse)
			self.holdRegisters[  11].clearFlags()
			self.holdRegisters[  11].addFlag( 1, self.blower.xDischargePresWarning)
			self.holdRegisters[  11].addFlag( 2, self.blower.xFliterPresWarning)
			self.holdRegisters[  11].addFlag( 3, self.blower.xPumpPresUpWarning)
			self.holdRegisters[  11].addFlag( 4, self.blower.xPumpPresDownWarning)
			self.holdRegisters[  11].addFlag( 5, self.blower.xSuctionTempUpWarning)
			self.holdRegisters[  11].addFlag( 6, self.blower.xDischargeTempUpWarning)
			self.holdRegisters[  11].addFlag( 7, self.blower.xMotorTempUpWarning)
			self.holdRegisters[  11].addFlag( 8, self.blower.xAirTempUpWarning)
			self.holdRegisters[  11].addFlag( 9, self.blower.xAirTempDownWarning)
			self.holdRegisters[  11].addFlag(10, self.blower.xDriveTempUpWarning)
			self.holdRegisters[  11].addFlag(14, self.blower.xPresSensorFaultWarning)
			self.holdRegisters[  11].addFlag(15, self.blower.xTempSensorFaultWarning)
			self.holdRegisters[  12].setValue(self.blower.xFlow)
			self.holdRegisters[  13].setValue(self.blower.xDischargePres)
			self.holdRegisters[  14].setValue(self.blower.xAirTemp)
			self.holdRegisters[  15].setValue(self.blower.xMotorTemp)
			self.holdRegisters[  16].setValue(self.blower.xDriveTemp)
			self.holdRegisters[  17].setValue(self.blower.xDischargeTemp)
			self.holdRegisters[  18].setValue(self.blower.xPowerConsumption)
			self.holdRegisters[  19].setValue(self.blower.xMotorCurrent)
			self.holdRegisters[  20].setValue(self.blower.xFrequency)
			self.holdRegisters[  21].setValue(self.blower.xMotorFrequency)
			self.holdRegisters[  22].setValue(self.blower.xStartCount)
			self.holdRegisters[  23].setValue(self.blower.xRunningDays)
			self.holdRegisters[  24].setValue(self.blower.xRunningHours)
			self.holdRegisters[  25].setValue(self.blower.xRunningMinutes)
			self.holdRegisters[  26].setValue(self.blower.xFilterPres)
			self.holdRegisters[  27].setValue(self.blower.xSuctionPres)
			self.holdRegisters[  28].setValue(self.blower.xVibration)
			self.holdRegisters[  29].setValue(self.blower.xBearingTemp)
			self.holdRegisters[  30].setValue(self.blower.xNumber)
			
			time.sleep(1)

class MBTCPSERVER(threading.Thread):
	def __init__(self, inputRegisters, holdRegisters):
		threading.Thread.__init__(self) 
		# A very simple data store which maps addresses against their values.
		self.inputRegisters = inputRegisters
		self.holdRegisters = holdRegisters

		# Enable values to be signed (default is False).
		conf.SIGNED_VALUES = True

		TCPServer.allow_reuse_address = True
		self.app = get_server(TCPServer, ('0.0.0.0', 502), RequestHandler)
		print(self.app)

		@self.app.route(slave_ids=[1], function_codes=[1, 3, 4], addresses=list(range(0, 1000)))
		def read_data_store(slave_id, function_code, address):
			try:
				value = 0
				"""" Return value of address. """
				if (function_code == 3):
					value = self.holdRegisters[address].getValue()
				elif (function_code == 4):
					value = self.inputRegisters[address].getValue()
				else:
					value = 0
				print('Read Data :', function_code, address, value)
				if (value < 32768):
					return	value
				else:
					return	value - 65536
			except Exception as inst:
				print('Read Data :', function_code, address)
				print('Ecception :', inst)
				return 0


		@self.app.route(slave_ids=[1], function_codes=[5, 15], addresses=list(range(0, 1000)))
		def write_data_store(slave_id, function_code, address, value):
			try:
				"""" Set value for address. """
				print('Write Data :', function_code, address, value)
				if (function_code == 5):
					self.holdRegisters[address].setValue(value)
			except:
				print('Exception')

	def run(self):
		self.app.serve_forever()
	
	def stop(self):
		self.app.shutdown()
		self.app.server_close()
  
if __name__ == '__main__':
	try:
		inputRegisters=  defaultdict(ValueSet)
		holdRegisters =  defaultdict(ValueSet)
		test = TESTCORE(inputRegisters, holdRegisters)
		server = MBTCPSERVER(inputRegisters, holdRegisters)
		test.start()
		server.start()
	except Exception as err:
		print(err)
