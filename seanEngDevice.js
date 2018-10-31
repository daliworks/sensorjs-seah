'use strict';

var _ = require('lodash');
var util = require('util');
var ModbusDevice = require('./modbusRTUDevice');

function SmartPMSDevice(master, config) {
  var self = this;

  self.type = config.type;
  self.lastUpdatedTime = 0;
  ModbusDevice.call(self, master, config);
}

util.inherits(SmartPMSDevice, ModbusDevice);

SmartPMSDevice.prototype.onDone = function (startAddress, count, registers) {
  var self = this;

  SmartPMSDevice.super_.prototype.onDone.call(self, startAddress, count, registers);

  _.each(self.registers, function(register) {
    if (register.activated) {
      self.log('trace', 'self.emit(', register.name, ',', {value: register.value, time: register.time}, ')');
      self.emit(register.name, {value: register.value, time: register.time});
    }
  });
};

SmartPMSDevice.prototype.activeField = function(name) {
  var self = this;

  var register = _.find(self.registers, function(register) {
    return  (register.name === name);
  });

  if (register) {
    register.activated = true;
  }
};

SmartPMSDevice.prototype.getValue = function(name) {
  var self = this;

  var register = _.find(self.registers, function(register) {
    return  (register.name === name);
  });

  var result;

  if (register) {
    result = { value: register.value, time: register.time};
  }

  return  result;
};

SmartPMSDevice.prototype.getConnectionTimeout = function() {
  return  10000;
};

SmartPMSDevice.prototype.updateSimulationValue = function(register) {
  var self = this;

  try {
    if (!_.isUndefined(register.value)) {
      var step = Math.floor((register.max - register.min) * 0.10);
      self.log('trace', 'New Step :', step);
      if (step > 1) {
        register.value += Math.floor(Math.random() * step) - step / 2;
      }
      else {
        if (Math.floor(Math.random() * 100) % 2 !== 0){
          register.value += 1;
        }
  
      }
    }
    else {
      register.value = Math.floor(Math.random() * (register.max - register.min)) + register.min;
    }

    if (register.value < register.min) {
      register.value = register.min;
    }
    else if (register.value > register.max) {
      register.value =register.max;
    }
  
    register.time = new Date().getTime();
  }
  catch(err) {
    self.log('trace', 'Exception :', err.message);
  }
};

SmartPMSDevice.prototype.updateSimulation = function() {
  var self = this;

  if (_.isUndefined(self.lastUpdatedTime) || ((new Date().getTime() - self.lastUpdatedTime) > 1000)) {
    self.log('trace', 'Time :', new Date().getTime(), 'Last Updated Time :', self.lastUpdatedTime);
    _.each(self.registers, function (register) {
      if (!_.isUndefined(register.min)) {
        var result = {};
        self.updateSimulationValue(register);

        if (!_.isUndefined(register.scale)) {
          result.value = register.value * register.scale;
          result.time = register.time;
        }
        else {
          result.value = register.value;
          result.time = register.time;
        }

        self.log('trace', 'self.emit(', register.name, result, ')');
        self.emit(register.name, result);
      }
    });

    self.lastUpdatedTime = new Date().getTime();
  }
};

module.exports = SmartPMSDevice;