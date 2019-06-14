'use strict';

var _ = require('lodash');
var util = require('util');
var SeAHEngDevice = require('./seahEngDevice');

function SeAHEngDeviceBlower(master, unitId) {
  var self = this;

  var config = {
    type: 'BL',
    unitId : unitId || 1,
    memoryZones: [
      { address: 40001, count: 30 }
    ],
    registers : [
      SeAHEngDevice.makeWriteRegisterDescription(40001,0),
      SeAHEngDevice.makeWriteRegisterDescription(40001,1),
      SeAHEngDevice.makeWriteRegisterDescription(40001,2),
      SeAHEngDevice.makeWriteRegisterDescription(40001,3),
      SeAHEngDevice.makeWriteRegisterDescription(40001,4),
      SeAHEngDevice.makeWriteRegisterDescription(40001,5),
      SeAHEngDevice.makeWriteRegisterDescription(40001,6),
      SeAHEngDevice.makeWriteRegisterDescription(40001,7),
      SeAHEngDevice.makeWriteRegisterDescription(40001,8),
      SeAHEngDevice.makeWriteRegisterDescription(40001,14),
      SeAHEngDevice.makeWriteRegisterDescription(40001,15),
      SeAHEngDevice.makeWriteRegisterDescription(40002),
      SeAHEngDevice.makeWriteRegisterDescription(40003),
      SeAHEngDevice.makeRegisterDescription(40006,1),
      SeAHEngDevice.makeRegisterDescription(40006,2),
      SeAHEngDevice.makeRegisterDescription(40006,3),
      SeAHEngDevice.makeRegisterDescription(40006,4),
      SeAHEngDevice.makeRegisterDescription(40006,5),
      SeAHEngDevice.makeRegisterDescription(40006,6),
      SeAHEngDevice.makeRegisterDescription(40006,8),
      SeAHEngDevice.makeRegisterDescription(40006,9),
      SeAHEngDevice.makeRegisterDescription(40006,13),
      SeAHEngDevice.makeRegisterDescription(40006,14),
      SeAHEngDevice.makeRegisterDescription(40006,15),
      SeAHEngDevice.makeRegisterDescription(40007,0),
      SeAHEngDevice.makeRegisterDescription(40007,1),
      SeAHEngDevice.makeRegisterDescription(40007,4),
      SeAHEngDevice.makeRegisterDescription(40007,5),
      SeAHEngDevice.makeRegisterDescription(40007,14),
      SeAHEngDevice.makeRegisterDescription(40007,15),
      SeAHEngDevice.makeRegisterDescription(40008,1),
      SeAHEngDevice.makeRegisterDescription(40008,2),
      SeAHEngDevice.makeRegisterDescription(40008,3),
      SeAHEngDevice.makeRegisterDescription(40008,4),
      SeAHEngDevice.makeRegisterDescription(40008,5),
      SeAHEngDevice.makeRegisterDescription(40008,7),
      SeAHEngDevice.makeRegisterDescription(40008,8),
      SeAHEngDevice.makeRegisterDescription(40008,9),
      SeAHEngDevice.makeRegisterDescription(40008,10),
      SeAHEngDevice.makeRegisterDescription(40008,12),
      SeAHEngDevice.makeRegisterDescription(40008,13),
      SeAHEngDevice.makeRegisterDescription(40008,14),
      SeAHEngDevice.makeRegisterDescription(40008,15),
      SeAHEngDevice.makeRegisterDescription(40009,0),
      SeAHEngDevice.makeRegisterDescription(40009,1),
      SeAHEngDevice.makeRegisterDescription(40009,2),
      SeAHEngDevice.makeRegisterDescription(40009,3),
      SeAHEngDevice.makeRegisterDescription(40009,4),
      SeAHEngDevice.makeRegisterDescription(40009,5),
      SeAHEngDevice.makeRegisterDescription(40009,6),
      SeAHEngDevice.makeRegisterDescription(40009,7),
      SeAHEngDevice.makeRegisterDescription(40009,8),
      SeAHEngDevice.makeRegisterDescription(40009,9),
      SeAHEngDevice.makeRegisterDescription(40009,10),
      SeAHEngDevice.makeRegisterDescription(40009,11),
      SeAHEngDevice.makeRegisterDescription(40009,12),
      SeAHEngDevice.makeRegisterDescription(40009,13),
      SeAHEngDevice.makeRegisterDescription(40009,14),
      SeAHEngDevice.makeRegisterDescription(40009,15),
      SeAHEngDevice.makeRegisterDescription(40010,0),
      SeAHEngDevice.makeRegisterDescription(40010,1),
      SeAHEngDevice.makeRegisterDescription(40010,2),
      SeAHEngDevice.makeRegisterDescription(40010,3),
      SeAHEngDevice.makeRegisterDescription(40010,4),
      SeAHEngDevice.makeRegisterDescription(40010,5),
      SeAHEngDevice.makeRegisterDescription(40010,8),
      SeAHEngDevice.makeRegisterDescription(40010,9),
      SeAHEngDevice.makeRegisterDescription(40010,10),
      SeAHEngDevice.makeRegisterDescription(40010,11),
      SeAHEngDevice.makeRegisterDescription(40010,12),
      SeAHEngDevice.makeRegisterDescription(40010,13),
      SeAHEngDevice.makeRegisterDescription(40010,15),
      SeAHEngDevice.makeRegisterDescription(40011,1),
      SeAHEngDevice.makeRegisterDescription(40011,2),
      SeAHEngDevice.makeRegisterDescription(40011,3),
      SeAHEngDevice.makeRegisterDescription(40011,4),
      SeAHEngDevice.makeRegisterDescription(40011,5),
      SeAHEngDevice.makeRegisterDescription(40011,6),
      SeAHEngDevice.makeRegisterDescription(40011,7),
      SeAHEngDevice.makeRegisterDescription(40011,8),
      SeAHEngDevice.makeRegisterDescription(40011,9),
      SeAHEngDevice.makeRegisterDescription(40011,10),
      SeAHEngDevice.makeRegisterDescription(40011,14),
      SeAHEngDevice.makeRegisterDescription(40011,15),
      SeAHEngDevice.makeRegisterDescription(40012),
      SeAHEngDevice.makeRegisterDescription(40013),
      SeAHEngDevice.makeRegisterDescription(40014),
      SeAHEngDevice.makeRegisterDescription(40015),
      SeAHEngDevice.makeRegisterDescription(40016),
      SeAHEngDevice.makeRegisterDescription(40017),
      SeAHEngDevice.makeRegisterDescription(40018),
      SeAHEngDevice.makeRegisterDescription(40019),
      SeAHEngDevice.makeRegisterDescription(40020),
      SeAHEngDevice.makeRegisterDescription(40021),
      SeAHEngDevice.makeRegisterDescription(40022),
      SeAHEngDevice.makeRegisterDescription(40023),
      SeAHEngDevice.makeRegisterDescription(40024),
      SeAHEngDevice.makeRegisterDescription(40025),
      SeAHEngDevice.makeRegisterDescription(40026),
      SeAHEngDevice.makeRegisterDescription(40027),
      SeAHEngDevice.makeRegisterDescription(40028),
      SeAHEngDevice.makeRegisterDescription(40029),
      SeAHEngDevice.makeRegisterDescription(40030)
    ]
  };

  SeAHEngDevice.call(self, master, config);
}

util.inherits(SeAHEngDeviceBlower, SeAHEngDevice);

module.exports = SeAHEngDeviceBlower;