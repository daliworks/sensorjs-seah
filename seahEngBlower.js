'use strict';

var _ = require('lodash');
var util = require('util');
var SeAHEngDevice = require('./seahEngDevice');

function camelize(str) {
  return str.replace(/(?:^\w|[A-Z]|\b\w)/g, function(letter, index) {
          return index === 0 ? letter.toLowerCase() : letter.toUpperCase();
          }).replace(/[^a-zA-Z0-9]+|\s+/g, '');
}

function makeRegisterDescription(name, address, bit, scale) {
  var description = {
    name: camelize(name),
    address: address,
    readType: 'readUInt16BE',
  };

  if (!_.isUndefined(bit)) {
    description.converter = function(value) {
      return  ((value >> bit) & 1);
    };        
  }

  if (!_.isUndefined(scale)) {
    description.scale = scale;
  }

  return  description;
}

function makeWriteOnlyRegisterDescription(name, address, bit, scale) {
  var description = {
    name: camelize(name),
    address: address
  };

  if (!_.isUndefined(bit)) {
    description.converter = function(value) {
      return  ((value >> bit) & 1);
    };        
  }

  if (!_.isUndefined(scale)) {
    description.scale = scale;
  }

  return  description;
}

function SeAHEngDeviceBlower(master, unitId) {
  var self = this;

  var config = {
    type: 'blower',
    unitId : unitId || 1,
    memoryZones: [
      { address: 40001, count: 30 }
    ],
    registers : [
      makeWriteOnlyRegisterDescription('Reset',40001,0),
      makeWriteOnlyRegisterDescription('Run Oper.',40001,1),
      makeWriteOnlyRegisterDescription('Stop Oper.',40001,2),
      makeWriteOnlyRegisterDescription('Speed Oper.',40001,3),
      makeWriteOnlyRegisterDescription('Flow Oper.',40001,4),
      makeWriteOnlyRegisterDescription('Power Oper.',40001,5),
      makeWriteOnlyRegisterDescription('Propotion Oper.',40001,6),
      makeWriteOnlyRegisterDescription('DOxygen Oper.',40001,7),
      makeWriteOnlyRegisterDescription('Pres. Oper.',40001,8),
      makeWriteOnlyRegisterDescription('MCP Emrg Rls',40001,14),
      makeWriteOnlyRegisterDescription('Remote Check Pulse',40001,15),
      makeWriteOnlyRegisterDescription('Primary SV',40002),
      makeWriteOnlyRegisterDescription('Secondary SV',40003),
      makeRegisterDescription('Repeat Oper.',40006,1),
      makeRegisterDescription('BOV Run',40006,2),
      makeRegisterDescription('Aux Run',40006,3),
      makeRegisterDescription('Restart Delay',40006,4),
      makeRegisterDescription('Surge Control',40006,5),
      makeRegisterDescription('Power Control',40006,6),
      makeRegisterDescription('Drive Ready',40006,8),
      makeRegisterDescription('Blow Ready',40006,9),
      makeRegisterDescription('Run Status',40006,13),
      makeRegisterDescription('Stop Status',40006,14),
      makeRegisterDescription('Reset Status',40006,15),
      makeRegisterDescription('Emrg Stop Rls Trip',40007,0),
      makeRegisterDescription('EOC Rls Trip',40007,1),
      makeRegisterDescription('Feed Trip',40007,4),
      makeRegisterDescription('Surge Trip',40007,5),
      makeRegisterDescription('Drive Comm Trip',40007,14),
      makeRegisterDescription('Remote Comm Trip',40007,15),
      makeRegisterDescription('Discharge Pres. High Trip',40008,1),
      makeRegisterDescription('Filter Pres. High Trip',40008,2),
      makeRegisterDescription('Pump Pres. High Trip',40008,3),
      makeRegisterDescription('Pump Pres. Low Trip',40008,4),
      makeRegisterDescription('Suction Pres. High Trip',40008,5),
      makeRegisterDescription('Moter Temp. High Trip',40008,7),
      makeRegisterDescription('Vibration Trip',40008,8),
      makeRegisterDescription('Bearing Temp. High Trip',40008,9),
      makeRegisterDescription('Drive Temp. High Trip',40008,10),
      makeRegisterDescription('Suction Pres. Sensor Fault',40008,12),
      makeRegisterDescription('Discharge Pres. Sensor Fault',40008,13),
      makeRegisterDescription('Filter Pres. Sensor Fault',40008,14),
      makeRegisterDescription('Pump Pres. Sensor Fault',40008,15),
      makeRegisterDescription('Unknown Drive Trip',40009,0),
      makeRegisterDescription('Overvoltage Trip',40009,1),
      makeRegisterDescription('Lowvoltage Trip',40009,2),
      makeRegisterDescription('Dixo Trip',40009,3),
      makeRegisterDescription('Doox Trip',40009,4),
      makeRegisterDescription('Overheating Trip',40009,5),
      makeRegisterDescription('Fuse Trip',40009,6),
      makeRegisterDescription('Overload Trip',40009,7),
      makeRegisterDescription('Overcurrent Trip',40009,8),
      makeRegisterDescription('Overspeed Trip',40009,9),
      makeRegisterDescription('Dzsx Trip',40009,10),
      makeRegisterDescription('Short Trip',40009,11),
      makeRegisterDescription('Comm Error Trip',40009,12),
      makeRegisterDescription('Fan Error Trip',40009,13),
      makeRegisterDescription('Motor Overcurrent Trip',40009,14),
      makeRegisterDescription('Drive Ready Error Trip',40009,15),
      makeRegisterDescription('Start Ready Trip',40010,0),
      makeRegisterDescription('Remote Control Status',40010,1),
      makeRegisterDescription('Run Status',40010,2),
      makeRegisterDescription('Warning Status',40010,3),
      makeRegisterDescription('Fault Status',40010,4),
      makeRegisterDescription('Drive Run Status',40010,5),
      makeRegisterDescription('Speed Mode Status',40010,8),
      makeRegisterDescription('Flow Mode Status',40010,9),
      makeRegisterDescription('Power Mode Status',40010,10),
      makeRegisterDescription('Propotion Mode Status',40010,11),
      makeRegisterDescription('DOxygen Mode Status',40010,12),
      makeRegisterDescription('Pres. Mode Status',40010,13),
      makeRegisterDescription('Comm Scan Pluse',40010,15),
      makeRegisterDescription('Discharge Pres. Warning',40011,1),
      makeRegisterDescription('Fliter Pres. Warning',40011,2),
      makeRegisterDescription('Pump Pres. Up Warning',40011,3),
      makeRegisterDescription('Pump Pres. Down Warning',40011,4),
      makeRegisterDescription('Suction Temp. Up Warning',40011,5),
      makeRegisterDescription('Discharge Temp. Up Warning',40011,6),
      makeRegisterDescription('Motor Temp. Up Warning',40011,7),
      makeRegisterDescription('Air Temp. Up Warning',40011,8),
      makeRegisterDescription('Air Temp. Down Warning',40011,9),
      makeRegisterDescription('Drive Temp. Up Warning',40011,10),
      makeRegisterDescription('Pres. Sensor Fault Warning',40011,14),
      makeRegisterDescription('Temp. Sensor Fault Warning',40011,15),
      makeRegisterDescription('Flow ',40012),
      makeRegisterDescription('Discharge Pres.',40013),
      makeRegisterDescription('Air Temp.',40014),
      makeRegisterDescription('Motor Temp.',40015),
      makeRegisterDescription('Drive Temp.',40016),
      makeRegisterDescription('Discharge Temp.',40017),
      makeRegisterDescription('Power Consumption',40018),
      makeRegisterDescription('Motor Current',40019),
      makeRegisterDescription('Frequency',40020),
      makeRegisterDescription('Motor Frequency',40021),
      makeRegisterDescription('Start Count',40022),
      makeRegisterDescription('Running Days',40023),
      makeRegisterDescription('Running Hours',40024),
      makeRegisterDescription('Running Minutes',40025),
      makeRegisterDescription('Filter Pres.',40026),
      makeRegisterDescription('Suction Pres.',40027),
      makeRegisterDescription('Vibration',40028),
      makeRegisterDescription('Bearing Temp.',40029),
      makeRegisterDescription('Number',40030)
    ]
  };

  SeAHEngDevice.call(self, master, config);
}

util.inherits(SeAHEngDeviceBlower, SeAHEngDevice);

module.exports = SeAHEngDeviceBlower;