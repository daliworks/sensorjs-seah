'use strict';

var logger = require('log4js').getLogger('Sensor');

function initDrivers() {
  var turboCompressorActuator;
  var turboCompressorSensor;
  var blowerActuator;
  var blowerSensor;

  try {
    blowerActuator = require('./driver/blowerActuator');
  } catch (e) {
    logger.error('Cannot load ./driver/blowerActuator', e);
  }

  try {
    blowerSensor = require('./driver/blowerSensor');
  } catch (e) {
    logger.error('Cannot load ./driver/blowerSensor', e);
  }

  try {
    turboCompressorActuator = require('./driver/turboCompressorActuator');
  } catch (e) {
    logger.error('Cannot load ./driver/turboCompressorActuator', e);
  }

  try {
    turboCompressorSensor = require('./driver/turboCompressorSensor');
  } catch (e) {
    logger.error('Cannot load ./driver/turboCompressorSensor', e);
  }

  return {
    seahEngBlowerSensor: blowerSensor,
    seahEngBlowerActuator: blowerActuator,
    seahEngTurboCompressorSensor: turboCompressorSensor,
    seahEngTurboCompressorActuator: turboCompressorActuator
  };
}

function initNetworks() {
  var network;

  try {
    network = require('./network/seahEng');
  } catch (e) {
    logger.error('Cannot load ./network/seahEng', e);
  }

  return {
    neopisSmartPMS: network
  };
}

module.exports = {
  networks: ['seahEng'],
  drivers: {
    seahEngBlowerSensor: [
      'seahEngBlowerCount',
      'seahEngBlowerCurrent',
      'seahEngBlowerFrequency',
      'seahEngBlowerPressureMMH2O',
      'seahEngBlowerNumber',
      'seahEngBlowerOnoff',
      'seahEngBlowerPercent',
      'seahEngBlowerPressure',
      'seahEngBlowerTemperature',
      'seahEngBlowerVibration',
      'seahEngBlowerVolume',
      'seahEngBlowerElectricPower',
    ],
    seahEngBlowerActuator: [
      'seahEngBlowerPowerSwitch',
      'seahEngBlowerStringActuator'
    ],
    seahEngTurboCompressorSensor: [
      'seahEngTurboCompressorCount',
      'seahEngTurboCompressorCurrent',
      'seahEngTurboCompressorFrequency',
      'seahEngTurboCompressorPressureMMH2O',
      'seahEngTurboCompressorNumber',
      'seahEngTurboCompressorOnoff',
      'seahEngTurboCompressorPercent',
      'seahEngTurboCompressorPressure',
      'seahEngTurboCompressorTemperature',
      'seahEngTurboCompressorVibration',
      'seahEngTurboCompressorVolume'
    ],
    seahEngTurboCompressorActuator: [
      'seahEngTurboCompressorPowerSwitch',
      'seahEngTurboCompressorStringActuator'
    ]
  },
  initNetworks: initNetworks,
  initDrivers: initDrivers
};
