'use strict';

var _ = require('lodash');
var util = require('util');
var EventEmitter = require('events').EventEmitter;
var logger = require('.').Sensor.getLogger('Sensor');

function ModbusRTUDevice(master, config) {
  var self = this;

  EventEmitter.call(self);

  self.id = new Date().getTime();
  self.master = master;
  self.run = false;
  self.interval = 10000;

  self.memoryZones = [];
  self.registers = [];

  self.config = {
    log : {
      title: 'MBTCPD',
      trace: true,
      error: true,
      info: true
    }
  };

  _.each(config.memoryZones, function(memoryInfo) {
    if (memoryInfo.address && memoryInfo.count) {
      var memoryZone = {
        address: memoryInfo.address,
        count: memoryInfo.count,
        registers: []
      };

      self.memoryZones.push(memoryZone);
    }
  });

  _.each(config.registers, function(registerInfo) {
    if (registerInfo && registerInfo.address) {
      var memorySize = 2;
      var register = _.cloneDeep(registerInfo);

      var memoryZone = _.find(self.memoryZones, function(memoryZone) {
        return ((memoryZone.address <= register.address) &&
          ((register.address + memorySize) < memoryZone.address + memoryZone.count * 2));
      });

      if (!memoryZone) {
        memoryZone = {
          address: register.address,
          count: memorySize / 2,
          registers: []
        };

        self.memoryZones.push(memoryZone);
      }

      memoryZone.registers.push(register);
      self.registers.push(register);
    }
  });

  self.on('done', self.onDone);
}

util.inherits(ModbusRTUDevice, EventEmitter);

ModbusRTUDevice.prototype.onDone = function (startAddress, count, registers) {
  var self = this;

  _.each(self.registers, function (register) {
    if (startAddress <= register.address && register.address < startAddress + count * 2) {
      try{
        var buffer = new Buffer(4);
  
        registers[register.address - startAddress].copy(buffer, 0);
        registers[register.address - startAddress + 1].copy(buffer, 2);
  
        if (register.converter) {
          register.value = register.converter(buffer[register.readType](0) || 0);
        } 
        else if (register.scale) {
          register.value = (buffer[register.readType](0) || 0) * register.scale;
        }
        else {
          register.value = (buffer[register.readType](0) || 0);
        }
        register.time = new Date().getTime();
      }
      catch(err) {
        self.log('trace', register);
        self.log('error', err);
      }
    }
  });
};

ModbusRTUDevice.prototype.setValue = function (register, value) {
  var self = this;

  return  new Promise(function(resolve) {
    var registers = [];

    registers[0] = new Buffer(4);
    registers[0][register.writeType](value, 0);
    self.master.setValue(register.address, 1, registers, function(err, result) { resolve(err, result); });
  });
};

ModbusRTUDevice.prototype.log = function(level) {
  var self = this;

  if (self.config && self.config.log && self.config.log[level] && logger[level]) {
    var i;
    var message = self.config.log.title + '[' + self.constructor.name + ':' + self.id + ']:';

    for(i = 1 ; i < arguments.length ; i++) {
      if (_.isObject(arguments[i])) {
        try{
          message = message + ' ' + JSON.stringify(arguments[i], null, 2);
        }
        catch(e) {
          message = message + ' ' + arguments[i];
        }
      }
      else {
        message = message + ' ' + arguments[i];
      }
    }

    logger[level](message);
  }
};

module.exports = ModbusRTUDevice;
