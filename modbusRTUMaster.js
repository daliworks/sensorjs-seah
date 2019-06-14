'use strict';

var _ = require('lodash');
var net = require('net');
var util = require('util');
var async = require('async');
var modbus = require('modbus-tcp');
var EventEmitter = require('events').EventEmitter;
var logger = require('.').Sensor.getLogger('Sensor');
var ModbusTCPDevice = require('./modbusRTUDevice');

var CONFIG;

try {
  CONFIG = require('config');
} catch (e) {
  logger.warn('MODULES_NOT_SUPPORTED - config');
}

var MODBUS_UNIT_ID = 1;
var MODBUS_PORT   = 502;
var UPDATE_INTERVAL = 10000;
var RETRY_CONNECTION_INTERVAL = 60000;

// client: modbus client
// registerAddress: register address from 40000
// bufferReadFunc: read function name of Buffer object
// cb: function (err, value)


// client: modbus ct
// registerAddress: register address from 40000
// bufferReadFunc: read function name of Buffer object
// cb: function (err, value)


function ModbusRTUMaster(config) {
  var self = this;

  self.id = new Date().getTime();
  self.interval = UPDATE_INTERVAL;

  if (!_.isUndefined(config)) {
    self.host = config.host || '0.0.0.0';
    if (_.isUndefined(config.port)) {
      self.port = MODBUS_PORT;
    }
    else {
      self.port = parseInt(config.port);
    }
  }
  else {
    self.host = '0.0.0.0';
    self.port = MODBUS_PORT;
  }
  self.devices = [];
  self.connected = false;
  self.autoReconnect = true;
  self.retryConnectionInterval = RETRY_CONNECTION_INTERVAL;

  self.config = {
    log : {
      title: 'MBTCPM',
      trace: true,
      error: true,
      info: true
    }
  };

  self.readQueue = async.queue(function (task, done) {
    var client = task.client;
    var cb = task.readCb;
    var unitId = task.unitId;
    var from;
    var to;
    var readRegisters;

    if (task.registerAddress <= 9999) {
      readRegisters = client.readCoils;
      from = task.registerAddress - 10001;
      to = from + task.registerCount - 1;
    } else if (10000 <= task.registerAddress && task.registerAddress <= 19999) {
      readRegisters = client.readDiscreteInputs;
      from = task.registerAddress - 10000;
      to = from + task.registerCount;
    } else if (30000 <= task.registerAddress && task.registerAddress <= 39999) {
      readRegisters = client.readInputRegisters;
      from = task.registerAddress - 30000;
      to = from + task.registerCount;
    } else if (40000 <= task.registerAddress && task.registerAddress <= 49999) {
      readRegisters = client.readHoldingRegisters;
      from = task.registerAddress - 40000;
      to = from + task.registerCount;
    } else {
      return done('Invalid address : ' + task.registerAddress);
    }

    self.log('Read Register :', unitId, from, to);
    try {
      readRegisters(unitId, from, to, function readCb(err, data) {
        if (!err) {
          //    if (data.length < 2 || !Buffer.isBuffer(data[0]) || !Buffer.isBuffer(data[1])) {
          //      self.log('error', 'modbus-tcp.readRegisters() Error: bad data format');
          //       err = new Error('Bad data:', data);
          //     }
        } else {
          self.log('error', 'modbus-tcp.readRegisters() Error:', err);
        }

        cb && cb(err, task.registerAddress, task.registerCount, data);
        return done && done(err);
      });
    } catch (err) {
      return done && done(err);
    }
    });

  self.readQueue.drain = function () {
    self.log('debug', 'All the read tasks have been done.');
  };

  self.writeQueue = async.queue(function (task, done) {
    var client = task.client;
    var cb = task.writeCb;
    var unitId = task.unitId;
    var from = task.registerAddress - 4000;
    var to = from + task.registerCount;
    var data = task.data;

    self.log('debug', 'writeValue() registerAddress:', task.registerAddress);
    client.writeMultipleRegisters(unitId, from, to, data, function writeCb(err) {
      var result;

      if (!err) {
        result = '{ status: \'on\', duration: 0 }';
      }
      else {
        self.log('error', 'modbus-tcp.writeMultipleRegisters() Error:', err);
      }

      cb && cb(err, result);
      return done && done(err);
    });
  });

  self.writeQueue.drain = function () {
    self.log('debug', 'All the write tasks have been done.');
  };

  EventEmitter.call(self);

  self.on('connected', self.onConnected);
  self.on('disconnected', self.onDisconnected);

  self.client = new modbus.Client();
  self.socket = new net.Socket();

  self.client.writer().pipe(self.socket);
  self.socket.pipe(self.client.reader());

  self.socket.on('connect', function() {
    self.log('trace', 'Connected:', self.host);
    self.emit('connected');
  });

  self.socket.on('close', function () {
    self.readQueue.remove( function() { return true; });
    self.writeQueue.remove(function() { return true;});

    self.log('trace', 'Socket closed:', self.host, self.port);
    self.emit('disconnected');
  });

  self.socket.on('error', function (err) {
    self.log('error', 'Socket error:', err);
  });
}

util.inherits(ModbusRTUMaster, EventEmitter);

ModbusRTUMaster.prototype.onConnected = function () {
  var self = this;

  if (self.connectionTimeoutHandler) {
    clearTimeout(self.connectionTimeoutHandler);
    self.connectionTimeoutHandler = null;
  }

  self.connected = true;
  self.startLoop();
};

ModbusRTUMaster.prototype.onDisconnected = function () {
  var self = this;

  if (self.connected) {
    self.stopLoop();
    self.connected = false;
  }

  if (self.autoReconnect) {
    self.log('trace', 'Set retry connection :', self.retryConnectionInterval);
    self.connectionTimeoutHandler = setTimeout(function () {
      self.connect();
    }, self.retryConnectionInterval);
  }
};

ModbusRTUMaster.prototype.connect = function () {
  var self = this;

  return  new Promise(function(resolve) {
    if (!self.connected) {
      self.log('trace', 'Connect :', self.host, self.port);
      self.socket.connect({
        port: self.port,
        host: self.host
      }, function () { resolve('ok'); });
    }
    else {
      resolve('ok');
    }
  });
};

ModbusRTUMaster.prototype.disconnect = function () {
  var self = this;
 
  if (self.connected) {
    self.stopLoop();
    self.socket.close();
  }
};

ModbusRTUMaster.prototype.createDevice = function(config) {
  var   self = this;
  var   device = new ModbusTCPDevice(self, config);

  self.devices.push(device);

  return  device;
};

ModbusRTUMaster.prototype.getDevice = function (id) {
  var self = this;

  return  _.find(self.devices, function(device) {
    return  (device.id === id);
  });
};

ModbusRTUMaster.prototype.start = function () {
  var self = this;

  self.connect();
};

ModbusRTUMaster.prototype.startLoop = function () {
  var self = this;

  self.log('trace', 'Start loop');
  if (!self.intervalHandler) {
    self.log('trace', 'Set Interval :', self.interval);
    self.intervalHandler = setInterval(function () {
      self.log('trace', 'Call Loop');
      if (self.client) {
        self.log('trace', 'device count :', self.devices.length);
        self.devices.map(function (device) {
          function readDoneCB(err, address, count, registers) {
            if (!err) {
              device.emit('done', address, count, registers);
            }
            else {
              self.log('trace', 'Read Error :', address, count);
            }
          }

          function pushCB(err) {
            if (err) {
              self.log('error', 'pushCB error: ', err);
            }
          }

          self.log('trace', 'device.memoryZones : ', device.memoryZones.length);
          _.each(device.memoryZones, function (set) {
            var callArgs = {
              client: self.client,
              unitId: device.unitId,
              registerAddress: set.address,
              registerCount: set.count,
              readCb: readDoneCB
            };

            self.readQueue.push(callArgs, pushCB);
          });
        });
      }
      else {
        self.log('trace', 'Client is not assigned.');
      }
    }, self.interval);
  }
};

ModbusRTUMaster.prototype.stopLoop = function () {
  var self = this;

  self.log('trace', 'Stop loop');
  if (self.connected) {
    if (self.intervalHandler) {
      clearInterval(self.intervalHandler);
      self.intervalHandler = null;
    }
  }
};

ModbusRTUMaster.prototype.getInterval = function () {
  var self = this;

  return self.interval;
};

ModbusRTUMaster.prototype.setInterval = function (interval) {
  var self = this;

  if (self.interval !== parseInt(interval)) {
    self.interval = parseInt(interval);

    if (self.intervalHandler) {
      self.stopLoop();
      self.startLoop();
    }
  }
};

ModbusRTUMaster.prototype.getValue = function (id, field) {
  var self = this;

  if (!field) {
    field = id;
    id = 0;
  }

  if (id) {
    var device = self.getDevice(id);
    if (device) {
      return device.getValue(field);
    } else {
      return undefined;
    }
  }

  var item = _.find(self.items, function (item) {
    return (item.field === field);
  });

  if (item) {
    return item.value;
  }

  return undefined;
};

ModbusRTUMaster.prototype.setValue = function (unitId, address, count, registers, cb) {
  var self = this;

  if (self.client) {
    var callArgs = {
      client: self.client,
      unitId: unitId,
      registerAddress: address,
      registerCount: count,
      data: registers,
      writeCb: cb
    };

    self.writeQueue.push(callArgs, function pushCb(err) {
      if (err) {
        self.log('error', 'pushCB error: ', err);
      }
    });
  } else {
    self.log('debug', 'Client is undefined.');
  }
};

ModbusRTUMaster.prototype.log = function(level) {
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

module.exports = ModbusRTUMaster;
