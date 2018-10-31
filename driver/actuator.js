'use strict';

var util = require('util');
var SensorLib = require('..');
var Actuator = SensorLib.Actuator;
var logger = Actuator.getLogger('Sensor');
var SeAHEng = require('../seahEng');

function SeAHEngActuator(sensorInfo, options) {
  var self = this;
  var tokens;

  Actuator.call(self, sensorInfo, options);

  tokens = self.id.split('-');
  self.deviceId= tokens[1];
  self.field = tokens[2];
  self.lastTime = 0;

  self.device = SeAHEng.getDevice(self.deviceId);

  if (sensorInfo.model) {
    self.model = sensorInfo.model;
  }

  self.dataType = SeAHEngActuator.properties.dataTypes[self.model][0];
  self.device.activeField(self.field);
}

SeAHEngActuator.properties = {
  supportedNetworks: ['seahEng'],
  dataTypes: {
    'seahEngOnOff': ['powerSwitch'],
    'seahEngStringActuator': ['stringActuator']
  },
  models: [
    'seahEngOnOff',
    'seahEngStringActuator'
  ],
  commands: {
    'seahEngOnOff': {
      'on' : [],
      'off' : []
    }
  },
  discoverable: false,
  addressable: true,
  recommendedInterval: 60000,
  maxInstances: 1,
  maxRetries: 8,
  idTemplate: '{gatewayId}-{deviceAddress}-{sequence}',
  category: 'actuator'
};

util.inherits(SeAHEngActuator, Actuator);

SeAHEngActuator.prototype._set = function (cmd, options, cb) {
  var self = this;

  logger.debug('Called _set():', cmd, options);

  try {
    self.device.emit('set', self.field, cmd, options, cb);
  } catch (err) {
    return cb && cb(err);
  }

};

SeAHEngActuator.prototype._get = function() {
  var self = this;
  var result = {
    status: 'on',
    id: self.id,
    result: {},
    time: {}
  };

  var data = self.device.getValue(self.field);
  if (data) {
    result.result[self.dataType] = data.value;
    result.time[self.dataType] = data.time;
  }

  self.emit('data', result);
};

SeAHEngActuator.prototype.getStatus = function getStatus() {
  var self = this;

  self.myStatus = 'on';

  return self.myStatus;
};

SeAHEngActuator.prototype.connectListener = function connectListener() {
  var self = this;

  self.myStatus = 'on';
};

SeAHEngActuator.prototype.disconnectListener = function disconnectListener() {
  var self = this;

  var rtn = {
    status: 'off',
    id: self.id,
    message: 'disconnected'
  };

  self.myStatus = 'off';
  self.emit('data', rtn);
};

module.exports = SeAHEngActuator;
