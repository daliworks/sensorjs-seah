'use strict';

var util = require('util');
var SensorLib = require('..');
var Sensor = SensorLib.Sensor;
var logger = Sensor.getLogger('Sensor');
var SeAHEng= require('../seahEng');

function SeAHEngSensor(sensorInfo, options) {
  var self = this;
  var tokens;

  Sensor.call(self, sensorInfo, options);

  tokens = self.id.split('-');

  self.deviceType = tokens[1];
  self.deviceId = tokens[2];
  self.field = tokens[3];

  self.device = SeAHEng.getDevice(self.deviceType, self.deviceId);

  self.lastData = { value: 0, time: 0};
  self.dataArray = [];
  
  if (sensorInfo.model) {
    self.model = sensorInfo.model;
  }

  try {
    self.onChange = SeAHEngSensor.properties.dataTypes[self.model];
    self.dataType = SeAHEngSensor.properties.dataTypes[self.model][0];
  }
  catch(e) {
    logger.error('Model :', self.model);
  }

  self.device.activeField(self.field);
  self.device.on(self.field, function(data) {
    self.lastData.value = data.value;
    self.lastData.time = data.time;
    logger.trace('Trace :', self.lastData);

    if (self.onChange) {
      var result = {
        status: 'on',
        id: self.id,
        result: {},
        time: {}
      };

      result.result[self.dataType] = data.value;
      result.time[self.dataType] = self.lastTime = data.time;

      self.emit('change', result);
    }
    else {
      self.dataArray.push(self.lastData);
    }
  });

}
util.inherits(SeAHEngSensor, Sensor);

SeAHEngSensor.properties = {
  supportedNetworks: ['seahEng'],
  dataTypes: {
    'seahEngTurboCompressorCount' : ['count'],
    'seahEngTurboCompressorCurrent' : ['current'],
    'seahEngTurboCompressorFrequency' : ['frequency'] ,
    'seahEngTurboCompressorNumber' : ['number'],
    'seahEngTurboCompressorOnoff' : ['onoff'],
    'seahEngTurboCompressorPercent' : ['percent'],
    'seahEngTurboCompressorPressureMMH2O' : ['pressure'],
    'seahEngTurboCompressorPressure' : ['pressure'],
    'seahEngTurboCompressorTemperature' : ['temperature'],
    'seahEngTurboCompressorVibration' : ['vibration'],
    'seahEngTurboCompressorVolume' : ['volume']
  },
  discoverable: false,
  addressable: true,
  recommendedInterval: 60000,
  maxInstances: 32,
  maxRetries: 8,
  idTemplate: '{gatewayId}-{deviceAddress}-{sequence}',
  onChange: {
    'seahEngTurboCompressorCount' : false,
    'seahEngTurboCompressorCurrent' : false,
    'seahEngTurboCompressorFrequency' : false,
    'seahEngTurboCompressorNumber' : false,
    'seahEngTurboCompressorOnoff' : true,
    'seahEngTurboCompressorPercent' : false,
    'seahEngTurboCompressorPressure' : false,
    'seahEngTurboCompressorPressureMMH2O' : false,
    'seahEngTurboCompressorTemperature' : false,
    'seahEngTurboCompressorVibration' : false,
    'seahEngTurboCompressorVolume' : false
  },
  models: [
    'seahEngTurboCompressorCount',
    'seahEngTurboCompressorCurrent',
    'seahEngTurboCompressorFrequency',
    'seahEngTurboCompressorNumber',
    'seahEngTurboCompressorOnoff',
    'seahEngTurboCompressorPercent',
    'seahEngTurboCompressorPressure',
    'seahEngTurboCompressorPressureMMH2O',
    'seahEngTurboCompressorTemperature',
    'seahEngTurboCompressorVibration',
    'seahEngTurboCompressorVolume'
  ],
  category: 'sensor'
};


SeAHEngSensor.prototype._get = function () {
  var self = this;
  var result = {
    status: 'off',
    id: self.id,
    result: {},
    time: {}
  };

  logger.debug('Called _get():', self.id);

  //if (self.device.updateSimulation) {
    //self.device.updateSimulation();
  //}

  if (self.onChange) {
    var elapsedTime = new Date().getTime() - self.lastData.time;
  
    if (elapsedTime <= self.device.getConnectionTimeout()){
      logger.trace(self.id, 'The last data[', self.lastData.value, '] transmission time interval - [', elapsedTime, 'ms ]') ;
      result.status = 'on';
      result.result[self.dataType] = self.lastData.value;
      result.time[self.dataType] = self.lastData.time;
      self.emit('data', result); 
    }
  }
  else{
    result.status = 'on';

    if (self.dataArray.length){
      result.result[self.dataType] = self.lastData.value;
      result.time[self.dataType] = self.lastData.time;
      self.dataArray = [];
    }

    self.emit('data', result); 
  }

  if (result.status === 'off') {
    logger.info(self.id, 'The device did not respond.') ;
  }
};

SeAHEngSensor.prototype._enableChange = function () {};

SeAHEngSensor.prototype._clear = function () {};

module.exports = SeAHEngSensor;
