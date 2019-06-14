'use strict';

var _ = require('lodash');
var util = require('util');
var ModbusDevice = require('./modbusRTUDevice');

function SeahEngDevice(master, config) {
  var self = this;

  self.type = config.type;
  self.lastUpdatedTime = 0;
  ModbusDevice.call(self, master, config);
}

util.inherits(SeahEngDevice, ModbusDevice);

SeahEngDevice.prototype.onDone = function (startAddress, count, registers) {
  var self = this;

  SeahEngDevice.super_.prototype.onDone.call(self, startAddress, count, registers);

  _.each(self.registers, function(register) {
    if (register.activated && (startAddress <= register.address) && (register.address < startAddress + count)) {
      self.log('trace', 'self.emit(', register.name, ',', {value: register.value, time: register.time}, ')');
      self.emit(register.name, {value: register.value, time: register.time});
    }
  });
};

SeahEngDevice.prototype.activeField = function(name) {
  var self = this;

  var register = _.find(self.registers, { name: name});
  if (register) {
    register.activated = true;
  }
};

SeahEngDevice.prototype.getValue = function(name) {
  var self = this;

  var register = _.find(self.registers, { name: name});
  if (!register) {
    return  undefined;
  }

  return { value: register.value, time: register.time};
};

SeahEngDevice.prototype.getConnectionTimeout = function() {
  return  10000;
};

SeahEngDevice.prototype.updateSimulationValue = function(register) {
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

SeahEngDevice.prototype.updateSimulation = function() {
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

SeahEngDevice.makeRegisterDescription = function(address, min, max, readType, scale) {
  
  var description = {
    name : ('00000' + address.toString()).slice(-5),
    address: address,
    scale : 1
  };

  if (!_.isUndefined(min) && !_.isUndefined(max) && !_.isUndefined(readType)) {
    description.min = min;
    description.max = max;
    description.readType = readType;
    if (!_.isUndefined(scale)) { 
      description.scale = scale;
    }
    else {
      description.scale = 1;
    }
  }
  else {
    if (!_.isUndefined(min)) {
      description.readType = 'readUInt16BE';
      description.converter = function(value) { return  (value >> min) & 1; }; // jshint ignore:line
      description.name = description.name + '.' + min;
    }
    description.readType = 'readUInt16BE';
  }

  return  description;
};

 SeahEngDevice.makeWriteRegisterDescription = function(address, min, max, readType, writeType, scale) {
  var description = {
    name : ('00000' + address.toString()).slice(-5),
    address: address
  };

  if (!_.isUndefined(min) && !_.isUndefined(max) && !_.isUndefined(readType) && !_.isUndefined(writeType)) {
    description.min = min;
    description.max = max;
    description.readType = readType;
    description.writeType = writeType;
    if (!_.isUndefined(scale)) { 
      description.scale = scale;
    }
    else {
      description.scale = 1;
    }
  }
  else {
    if (!_.isUndefined(min)) {
      description.name = description.name + '.' + min;
    }
    description.readType = 'readUInt16BE';
    description.writeType = 'writeUInt16BE';
  }

  return  description;
};

module.exports = SeahEngDevice;