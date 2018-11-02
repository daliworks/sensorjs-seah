'use strict';

var util = require('util');
var sensorDriver = require('../../index');
var Network = sensorDriver.Network;

function SeahEng(options) {
  Network.call(this, 'seahEng', options);
}

util.inherits(SeahEng, Network);

SeahEng.prototype.discover = function (networkName, options, cb) {
  return cb && cb(new Error('Not supported'));
};

module.exports = new SeahEng();
