'use strict';

var logger = require('log4js').getLogger('Sensor');

function initDrivers() {
  var actuator;
  var sensor;

  try {
    actuator = require('./driver/actuator');
  } catch (e) {
    logger.error('Cannot load ./driver/actuator', e);
  }

  try {
    sensor = require('./driver/sensor');
  } catch (e) {
    logger.error('Cannot load ./driver/sensor', e);
  }

  return {
    neopisSmartPMSPMSActuator: actuator,
    neopisSmartPMSPMSSensor: sensor,
    neopisSmartPMSEMSSensor: sensor,
    neopisSmartPMSSPSensor: sensor,
    neopisSmartPMSPCSSensor: sensor,
    neopisSmartPMSBATSensor: sensor
  };
}

function initNetworks() {
  var network;

  try {
    network = require('./network/neopisSmartPMS');
  } catch (e) {
    logger.error('Cannot load ./network/neopisSmartPMS', e);
  }

  return {
    neopisSmartPMS: network
  };
}

module.exports = {
  networks: ['neopisSmartPMS'],
  drivers: {
    neopisSmartPMSPMSActuator: [
      'neopisSmartPMSPMSChargeModeSet',
      'neopisSmartPMSPMSChargePowerSet',
      'neopisSmartPMSPMSConfigSet',
      'neopisSmartPMSPMSControlModeSet',
      'neopisSmartPMSPMSOperationModeSet'
    ],
    neopisSmartPMSPMSSensor: [
      'neopisSmartPMSPMSChargeModeStatus',
      'neopisSmartPMSPMSCommunicationError',
      'neopisSmartPMSPMSControlModeStatus',
      'neopisSmartPMSPMSDate',
      'neopisSmartPMSPMSEnergy',
      'neopisSmartPMSPMSFailureStatus',
      'neopisSmartPMSPMSOperationStatus',
      'neopisSmartPMSPMSPower',
      'neopisSmartPMSPMSPowerCapacity',
      'neopisSmartPMSPMSPowerRating',
      'neopisSmartPMSPMSSOCStatus',
      'neopisSmartPMSPMSTime',
      'neopisSmartPMSPMSPercent'
    ],
    neopisSmartPMSEMSSensor: [
      'neopisSmartPMSEMSEnergy'
    ],
    neopisSmartPMSSPSensor: [
      'neopisSmartPMSSPStatus',
      'neopisSmartPMSSPTemperature',
      'neopisSmartPMSSPVoltage',
      'neopisSmartPMSSPCurrent',
      'neopisSmartPMSSPPower',
      'neopisSmartPMSSPEnergy',
      'neopisSmartPMSSPError'
    ],
    neopisSmartPMSPCSSensor: [
      'neopisSmartPMSPCSStatus',
      'neopisSmartPMSPCSError',
      'neopisSmartPMSPCSControlMode',
      'neopisSmartPMSPCSTemperature',
      'neopisSmartPMSPCSVoltage',
      'neopisSmartPMSPCSCurrent',
      'neopisSmartPMSPCSPower',
      'neopisSmartPMSPCSEnergy',
      'neopisSmartPMSPCSPowerFactor',
      'neopisSmartPMSPCSFrequency',
      'neopisSmartPMSPCSFrequencyStatus',
      'neopisSmartPMSPCSOperationStatus',
      'neopisSmartPMSPCSError',
      'neopisSmartPMSPCSErrorStatus',
      'neopisSmartPMSPCSLocationStatus',
      'neopisSmartPMSPCSFrequencyStatus',
      'neopisSmartPMSPCSVoltageStatus',
      'neopisSmartPMSPCSCurrentStatus',
      'neopisSmartPMSPCSControlMode',
      'neopisSmartPMSPCSEmergencyBell'
    ],
    neopisSmartPMSBATSensor: [
      'neopisSmartPMSBATTemperature',
      'neopisSmartPMSBATVoltage',
      'neopisSmartPMSBATCurrent',
      'neopisSmartPMSBATPercent',
      'neopisSmartPMSBATCellVoltage',
      'neopisSmartPMSBATStatus',
      'neopisSmartPMSBATError',
      'neopisSmartPMSBATVoltageUnbalance',
      'neopisSmartPMSBATTemperatureUnbalance',
      'neopisSmartPMSBATTemperatureStatus',
      'neopisSmartPMSBATVoltageStatus',
      'neopisSmartPMSBATCurrentStatus',
      'neopisSmartPMSBATErrorStatus',
      'neopisSmartPMSBATOperationStatus',
      'neopisSmartPMSBATContactorStatus',
      'neopisSmartPMSBATFuseStatus',
      'neopisSmartPMSBATEmergencyBell'
    ]
  },
  initNetworks: initNetworks,
  initDrivers: initDrivers
};
