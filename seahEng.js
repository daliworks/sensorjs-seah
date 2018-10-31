'use strict';

var _ = require('lodash');
var util = require('util');
var logger = require('.').Sensor.getLogger('Sensor');
var ModbusMaster = require('./modbusRTUMaster');
var SeAHEngBlower = require('./seahEngBlower');
var SeAHEngCompressor = require('./seahEngCompressor');

function SeAHEng(address) {
  var   self = this;

  ModbusMaster.call(self, address, 502);

  self.log('trace', 'Create :', address);
}

util.inherits(SeAHEng, ModbusMaster);

var seahEngs = [];

function getSeAHEng(address){
  var seahEng = _.find(seahEngs, function(seahEng) {
    return  (seahEng.address === parseInt(address));
  });

  if (!seahEng) {
    seahEng = new SeAHEng(address);
    seahEngs.push(seahEng);
    seahEng.start();
  }

  return  seahEng;
}

module.exports = {
  get: getSeAHEng,
  getDevice: function(type, address){
    try {
      var seahEng = getSeAHEng(address);

      switch(type) {
      case  'blower':
        seahEng.EMS = new SeAHEngBlower(seahEng);
        seahEng.devices.push(seahEng.EMS);
        break;
      case 'compressor':
        seahEng.PMS = new SeAHEngCompressor(seahEng);
        seahEng.devices.push(seahEng.PMS);
        break;
      }
      
      return  seahEng[type];
    }
    catch(err) {
      logger.error('Device not found :', type, address);
      return  undefined;
    }
  }
};