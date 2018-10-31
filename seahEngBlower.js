'use strict';

var util = require('util');
var SmartPMSDevice = require('./smartPMSDevice');

function SmartPMSDeviceBAT(master) {
  var self = this;

  var config = {
    type: 'BAT',
    memoryZones: [
      { address: 40091, count: 18 }
    ],
    registers : [
      {
        name: 'voltage',
        address: 40091,
        readType: 'readUInt16BE',
        scale: 0.1,
        min: 0,
        max: 10000
      }, {
        name: 'current',
        address: 40092,
        readType: 'readUInt16BE',
        scale: 0.1,
        min: -30000,
        max: 30000
      }, {
        name:'soc',
        address: 40093,
        readType: 'readUInt16BE',
        scale: 0.1,
        min: 0,
        max: 1000
      }, {
        name: 'soh',
        address: 40094,
        readType: 'readUInt16BE',
        scale: 0.1,
        min: 0,
        max: 1000
      }, {
        name: 'cellMaxTemperature',
        address: 40095,
        readType: 'readUInt16BE',
        scale: 0.1,
        min: 0,
        max: 990
      }, {
        name: 'cellMinTemperature',
        address: 40096,
        readType: 'readUInt16BE',
        scale: 0.1,
        min: 0,
        max: 990
      }, {
        name: 'cellMaxVoltage',
        address: 40097,
        readType: 'readUInt16BE',
        scale: 0.001,
        min: 0,
        max: 8000
      }, {
        name: 'cellMinVoltage',
        address: 40098,
        readType: 'readUInt16BE',
        scale: 0.001,
        min: 0,
        max: 8000
      }, {
        name: 'operationStatus',
        address: 40101,
        readType: 'readUInt16BE',
        converter: function(value) {
          if (value & 1) {
            return  1;
          }
          if ((value >> 1) & 1) {
            return  2;
          }
          else {
            return  0;
          }
        },        
        min: 0,
        max: 2
      }, {
        name: 'errorStatus',
        address: 40101,
        readType: 'readUInt16BE',
        converter: function(value) {
          if ((value >> 2) & 1) {
            return  1;
          }
          else if ((value >> 3) & 1) {
            return  2;
          }
          else {
            return  0;
          }
        },        
        min: 0,
        max: 2
      }, {
        name: 'currentStatus',
        address: 40101,
        readType: 'readUInt16BE',
        converter: function(value) {
          if ((value >> 6) & 1) {
            return  1;
          }
          else {
            return  0;
          }
        },        
        min: 0,
        max: 1
      }, {
        name: 'voltageStatus',
        address: 40101,
        readType: 'readUInt16BE',
        converter: function(value) {
          if ((value >> 7) & 1) {
            return  1;
          }
          else if ((value >> 8) & 1) {
            return  2;
          }
          else {
            return  0;
          }
        },        
        min: 0,
        max: 2
      }, {
        name: 'voltageUnbalance',
        address: 40101,
        readType: 'readUInt16BE',
        converter: function(value) {
          if ((value >> 11) & 1) {
            return  1;
          }
          else {
            return  0;
          }
        },        
        min: 0,
        max: 1
      }, {
        name: 'temperatureStatus',
        address: 40101,
        readType: 'readUInt16BE',
        converter: function(value) {
          if ((value >> 9) & 1) {
            return  1;
          }
          else if ((value >> 10) & 1) {
            return  2;
          }
          else {
            return  0;
          }
        },        
        min: 0,
        max: 2
      }, {
        name: 'temperatureUnbalance',
        address: 40101,
        readType: 'readUInt16BE',
        converter: function(value) {
          if ((value >> 12) & 1) {
            return  1;
          }
          else {
            return  0;
          }
        },        
        min: 0,
        max: 1
      }, {
        name: 'contactorStatus',
        address: 40101,
        readType: 'readUInt16BE',
        converter: function(value) {
          if ((value >> 13) & 1) {
            return  1;
          }
          else {
            return  0;
          }
        },        
        min: 0,
        max: 1
      }, {
        name: 'fuseStatus',
        address: 40101,
        readType: 'readUInt16BE',
        converter: function(value) {
          if ((value >> 14) & 1) {
            return  1;
          }
          else {
            return  0;
          }
        },        
        min: 0,
        max: 1
      }, {
        name: 'emergencyBell',
        address: 40101,
        readType: 'readUInt16BE',
        converter: function(value) {
          if ((value >> 15) & 1) {
            return  1;
          }
          else {
            return  0;
          }
        },        
        min: 0,
        max: 1
      }, {
        name: 'warningCode',
        address: 40102,
        readType: 'readUInt16BE',
        min: 0,
        max: 10,
      }, {
        name: 'errorCode',
        address: 40105,
        readType: 'readUInt16BE',
        min: 0,
        max: 10,
      }]
  };

  SmartPMSDevice.call(self, master, config);
}

util.inherits(SmartPMSDeviceBAT, SmartPMSDevice);

module.exports = SmartPMSDeviceBAT;