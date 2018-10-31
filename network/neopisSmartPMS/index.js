'use strict';

var util = require('util');
var sensorDriver = require('../../index');
var Network = sensorDriver.Network;

function NeopisSmartPMS(options) {
  Network.call(this, 'neopisSmartPMS', options);
}

util.inherits(NeopisSmartPMS, Network);

NeopisSmartPMS.prototype.discover = function (networkName, options, cb) {
  return cb && cb(new Error('Not supported'));
};

module.exports = new NeopisSmartPMS();
