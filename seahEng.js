'use strict';

var _ = require('lodash');
var util = require('util');
var logger = require('.').Sensor.getLogger('Sensor');
var ModbusMaster = require('./modbusRTUMaster');
var SeAHEngBlower = require('./seahEngBlower');
var SeAHEngCompressor = require('./seahEngCompressor');

function SeAHEng(host) {
  var   self = this;

  ModbusMaster.call(self, host, 502);

  self.log('trace', 'Create :', host);
}

util.inherits(SeAHEng, ModbusMaster);

var seahEngs = [];

function getSeAHEng(host){
  var seahEng = _.find(seahEngs, function(seahEng) {
    return  (seahEng.host === host);
  });

  if (!seahEng) {
    logger.info('Create new SeAHEng');
    seahEng = new SeAHEng(host);
    seahEngs.push(seahEng);
    seahEng.start();
  }

  return  seahEng;
}

module.exports = {
  get: getSeAHEng,
  getDevice: function(type, host){
    try {
      var seahEng = getSeAHEng(host);
      if (_.isUndefined(seahEng[type])) {
        switch (type) {
        case 'blower':
          logger.info('Create blower');
          seahEng.blower = new SeAHEngBlower(seahEng);
          seahEng.devices.push(seahEng.blower);
          break;
        case 'compressor':
          logger.info('Create compressor');
          seahEng.compressor = new SeAHEngCompressor(seahEng);
          seahEng.devices.push(seahEng.compressor);
          break;

        default:
          logger.error('Not supported device type :', type);
        }
      }

      return seahEng[type];
    }
    catch (err) {
      logger.error('error :', err.message);
      return undefined;
    }
  }
};