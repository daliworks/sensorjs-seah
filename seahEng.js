'use strict';

var _ = require('lodash');
var util = require('util');
var logger = require('.').Sensor.getLogger('Sensor');
var ModbusMaster = require('./modbusRTUMaster');
var SeAHEngBlower = require('./seahEngBlower');
var SeAHEngCompressor = require('./seahEngCompressor');

function SeAHEng(config) {
  var   self = this;

  ModbusMaster.call(self, config);

  self.log('trace', 'Create new SeAHEng :', config);
}

util.inherits(SeAHEng, ModbusMaster);

var seahEngs = [];

function getSeAHEng(config){
  var host = config.host;
  var port = (config.port && parseInt(config.port)) || 502;
  var unitId = (config.unitId && parseInt(config.unitId)) || 1;

  var seahEng = _.find(seahEngs, function(seahEng) {
    return  (seahEng.host === host) && (seahEng.port === port);
  });

  if (!seahEng) {
    seahEng = new SeAHEng(config);
    seahEngs.push(seahEng);
    seahEng.start();
  }

  return  seahEng;
}

module.exports = {
  get: getSeAHEng,
  getDevice: function(type, deviceId){
    try {
      if (deviceId.split(':').length > 3) {
        logger.error('Invalid device ID :', deviceId);
        return undefined;
      }

      var config  = {
        host : deviceId.split(':')[0],
        port : deviceId.split(':')[1]
      };

      var unitId = (deviceId.split(':')[2] && parseInt(deviceId.split(':')[2])) || 1;

      var seahEng = getSeAHEng(config);
      if (_.isUndefined(seahEng[type])) {
        switch (type) {
        case 'blower':
          logger.info('Create blower');
          seahEng.blower = new SeAHEngBlower(seahEng, unitId);
          seahEng.devices.push(seahEng.blower);
          break;
        case 'compressor':
          logger.info('Create compressor');
          seahEng.compressor = new SeAHEngCompressor(seahEng, unitId);
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