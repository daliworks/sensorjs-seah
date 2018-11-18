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

function SeAHEngDeviceCompressor(master, unitId) {
  var self = this;

  var config = {
    type: 'compressor',
    unitId : unitId || 1,
    memoryZones: [
      { address: 30025, count: 18 },
      { address: 30100, count: 90 },
      { address: 40200, count: 44 },
      { address: 40260, count: 4 },
      { address: 40280, count: 2 },
      { address: 40300, count: 2 }
    ],
    registers : [
      makeWriteOnlyRegisterDescription('Comp. Start Cmd', 320,undefined,undefined),
      makeWriteOnlyRegisterDescription('Comp. Stop Cmd', 321,undefined,undefined),
      makeWriteOnlyRegisterDescription('Alarm Reset Cmd', 322,undefined,undefined),
      makeWriteOnlyRegisterDescription('Load Select Cmd', 323,undefined,undefined),
      makeWriteOnlyRegisterDescription('Unload Select Cmd', 324,undefined,undefined),
      makeWriteOnlyRegisterDescription('Aux. Oil Pump Start Cmd', 325,undefined,undefined),
      makeWriteOnlyRegisterDescription('Aux. Oil Pump Stop Cmd', 326,undefined,undefined),
      makeRegisterDescription('Common Trip', 30025,0 ,undefined),
      makeRegisterDescription('Common Alarm', 30025,1 ,undefined),
      makeRegisterDescription('Common Sensor Fault', 30025,2 ,undefined),
      makeRegisterDescription('Alarm Resetting', 30025,3 ,undefined),
      makeRegisterDescription('Comp. Ready', 30026,0 ,undefined),
      makeRegisterDescription('Oil Temp Ready', 30026,1 ,undefined),
      makeRegisterDescription('Oil Pres. Ready', 30026,2 ,undefined),
      makeRegisterDescription('Not Ready Alarm', 30026,3 ,undefined),
      makeRegisterDescription('Comp. Restart Time', 30026,4 ,undefined),
      makeRegisterDescription('Comp. Run', 30027,0 ,undefined),
      makeRegisterDescription('Comp. Stop', 30027,1 ,undefined),
      makeRegisterDescription('Comp. Trip Stop', 30027,2 ,undefined),
      makeRegisterDescription('Comp. Starting', 30027,3 ,undefined),
      makeRegisterDescription('Comp. Stopping', 30027,4 ,undefined),
      makeRegisterDescription('Local / Remote Select', 30028,0 ,undefined),
      makeRegisterDescription('Load / Unload Select', 30028,1 ,undefined),
      makeRegisterDescription('Load Mode', 30028,2 ,undefined),
      makeRegisterDescription('Modulation Mode', 30028,3 ,undefined),
      makeRegisterDescription('Force Unloading', 30028,4 ,undefined),
      makeRegisterDescription('Aux. Oil Pump Run / Stop', 30029,0 ,undefined),
      makeRegisterDescription('Aux. Oil Pump Stopping', 30029,1 ,undefined),
      makeRegisterDescription('Ejector (Exh. Fan) Run / Stop', 30029,2 ,undefined),
      makeRegisterDescription('Oil Heater On / Off', 30029,3 ,undefined),
      makeRegisterDescription('PLC Rebooting', 30030,0 ,undefined),
      makeRegisterDescription('Comp. Emergency Stop', 30030,1 ,undefined),
      makeRegisterDescription('Comp. Starter Panel trip', 30030,2 ,undefined),
      makeRegisterDescription('Aux. Oil Pump EOCR Trip', 30030,3 ,undefined),
      makeRegisterDescription('Exhaust Fan EOCR Trip', 30030,4 ,undefined),
      makeRegisterDescription('Oil Exchange Time Alarm', 30030,5 ,undefined),
      makeRegisterDescription('PLC BAT Voltage Low Alarm', 30030,6 ,undefined),
      makeRegisterDescription('PLC BAT Exchange Time Alarm', 30030,7 ,undefined),
      makeRegisterDescription('Surge Unload', 30031,0 ,undefined),
      makeRegisterDescription('Surge Half Unload', 30031,1 ,undefined),
      makeRegisterDescription('Surge Count 1', 30031,2 ,undefined),
      makeRegisterDescription('Surge Count 2', 30031,3 ,undefined),
      makeRegisterDescription('Surge Count 3', 30031,4 ,undefined),
      makeRegisterDescription('Surge Count 4', 30031,5 ,undefined),
      makeRegisterDescription('Surge Count 5', 30031,6 ,undefined),
      makeRegisterDescription('2nd Inlet TFault', 30032,0 ,undefined),
      makeRegisterDescription('2nd Inlet Temp High Alarm', 30032,1 ,undefined),
      makeRegisterDescription('3rd Inlet Temp High Trip', 30032,10,undefined),
      makeRegisterDescription('2nd Inlet Temp High Trip', 30032,2 ,undefined),
      makeRegisterDescription('3rd Inlet TFault', 30032,8 ,undefined),
      makeRegisterDescription('3rd Inlet Temp High Alarm', 30032,9 ,undefined),
      makeRegisterDescription('Oil TFault', 30033,0 ,undefined),
      makeRegisterDescription('Oil Temp High Alarm', 30033,1 ,undefined),
      makeRegisterDescription('Oil Temp High Trip', 30033,2 ,undefined),
      makeRegisterDescription('Oil Temp Low Alarm', 30033,3 ,undefined),
      makeRegisterDescription('Cool Supply TFault', 30033,8 ,undefined),
      makeRegisterDescription('Cool Supply Temp High Alarm', 30033,9 ,undefined),
      makeRegisterDescription('1st Intercooler Return TFault', 30034,0 ,undefined),
      makeRegisterDescription('2nd Intercooler Return TFault', 30034,8 ,undefined),
      makeRegisterDescription('Oil Intercooler Return TFault', 30035,0 ,undefined),
      makeRegisterDescription('MBearing (DE) Temp High Trip', 30035,10,undefined),
      makeRegisterDescription('MBearing (DE) TSensor Faullt', 30035,8 ,undefined),
      makeRegisterDescription('MBearing (DE) Temp High Alarm', 30035,9 ,undefined),
      makeRegisterDescription('MBearing (NDE) TSensor Faullt', 30036,0 ,undefined),
      makeRegisterDescription('MBearing (NDE) Temp High Alarm', 30036,1 ,undefined),
      makeRegisterDescription('MWinding (R) Temp High Trip', 30036,10,undefined),
      makeRegisterDescription('MBearing (NDE) Temp High Trip', 30036,2 ,undefined),
      makeRegisterDescription('MWinding (R) TFault', 30036,8 ,undefined),
      makeRegisterDescription('MWinding (R) Temp High Alarm', 30036,9 ,undefined),
      makeRegisterDescription('MWinding (S) TFault', 30037,0 ,undefined),
      makeRegisterDescription('MWinding (S) Temp High Alarm', 30037,1 ,undefined),
      makeRegisterDescription('MWinding (T) Temp High Trip', 30037,10,undefined),
      makeRegisterDescription('MWinding (S) Temp High Trip', 30037,2 ,undefined),
      makeRegisterDescription('MWinding (T) TFault', 30037,8 ,undefined),
      makeRegisterDescription('MWinding (T) Temp High Alarm', 30037,9 ,undefined),
      makeRegisterDescription('Comp. Dis. Pres. Sensor Fault', 30038,0 ,undefined),
      makeRegisterDescription('Comp. Dis. Pres. Low Alarm', 30038,1 ,undefined),
      makeRegisterDescription('Motor Current Low Trip', 30038,10,undefined),
      makeRegisterDescription('Motor Current Abnormal Trip', 30038,11,undefined),
      makeRegisterDescription('Motor Current Sensor Fault', 30038,8 ,undefined),
      makeRegisterDescription('Oil Pres. Sensor Fault', 30039,0 ,undefined),
      makeRegisterDescription('Oil Pres. High Alarm', 30039,1 ,undefined),
      makeRegisterDescription('Oil Fltr DPres. High Trip', 30039,10,undefined),
      makeRegisterDescription('Oil Pres. Low Alarm', 30039,3 ,undefined),
      makeRegisterDescription('Oil Pres. Low Trip', 30039,4 ,undefined),
      makeRegisterDescription('Oil Pres. Low Trip (Start)', 30039,5 ,undefined),
      makeRegisterDescription('Oil Fltr DPres. Sensor Fault', 30039,8 ,undefined),
      makeRegisterDescription('Oil Fltr DPres. High Alarm', 30039,9 ,undefined),
      makeRegisterDescription('1st Vib Sensor Fault', 30040,0 ,undefined),
      makeRegisterDescription('1st Vib High Alarm (Start)', 30040,1 ,undefined),
      makeRegisterDescription('2nd Vib High Trip (Start)', 30040,10,undefined),
      makeRegisterDescription('2nd Vib High Alarm (Run)', 30040,11,undefined),
      makeRegisterDescription('2nd Vib High Trip (Run)', 30040,12,undefined),
      makeRegisterDescription('2nd Vib Abnormal Trip', 30040,13,undefined),
      makeRegisterDescription('2nd Vib Average A Alarm', 30040,14,undefined),
      makeRegisterDescription('2nd Vib Average B Alarm', 30040,15,undefined),
      makeRegisterDescription('1st Vib High Trip (Start)', 30040,2 ,undefined),
      makeRegisterDescription('1st Vib High Alarm (Run)', 30040,3 ,undefined),
      makeRegisterDescription('1st Vib High Trip (Run)', 30040,4 ,undefined),
      makeRegisterDescription('1st Vib Abnormal Trip', 30040,5 ,undefined),
      makeRegisterDescription('1st Vib Average A Alarm', 30040,6 ,undefined),
      makeRegisterDescription('1st Vib Average B Alarm', 30040,7 ,undefined),
      makeRegisterDescription('2nd Vib Sensor Fault', 30040,8 ,undefined),
      makeRegisterDescription('2nd Vib High Alarm (Start)', 30040,9 ,undefined),
      makeRegisterDescription('3rd Vib Sensor Fault', 30041,0 ,undefined),
      makeRegisterDescription('3rd Vib High Alarm (Start)', 30041,1 ,undefined),
      makeRegisterDescription('Comp. Dis. TFault', 30041,12,undefined),
      makeRegisterDescription('3rd Vib High Trip (Start)', 30041,2 ,undefined),
      makeRegisterDescription('3rd Vib High Alarm (Run)', 30041,3 ,undefined),
      makeRegisterDescription('3rd Vib High Trip (Run)', 30041,4 ,undefined),
      makeRegisterDescription('3rd Vib Abnormal Trip', 30041,5 ,undefined),
      makeRegisterDescription('3rd Vib Average A Alarm', 30041,6 ,undefined),
      makeRegisterDescription('3rd Vib Average B Alarm', 30041,7 ,undefined),
      makeRegisterDescription('After Cooler Return TFault', 30041,8 ,undefined),
      makeRegisterDescription('Oil Tank TFault', 30042,0 ,undefined),
      makeRegisterDescription('Oil Tank Level Sensor Fault', 30042,12,undefined),
      makeRegisterDescription('Oil Tank Level Low Alarm', 30042,13,undefined),
      makeRegisterDescription('System TFault', 30042,4 ,undefined),
      makeRegisterDescription('SFilter DPres. Sensor Fault', 30042,8 ,undefined),
      makeRegisterDescription('SFilter DPres. High Alarm', 30042,9 ,undefined),
      makeRegisterDescription('Dis. Pres.', 30100,undefined,0.01),
      makeRegisterDescription('Dis. Set Pres.', 30101,undefined,0.01),
      makeRegisterDescription('Reload Pres.', 30102,undefined,0.01),
      makeRegisterDescription('Unload Pres.', 30103,undefined,0.01),
      makeRegisterDescription('Motor Current', 30105,undefined,0.1),
      makeRegisterDescription('Max. Current', 30106,undefined,0.1),
      makeRegisterDescription('Min. Current', 30107,undefined,0.1),
      makeRegisterDescription('Comp. Load Ratio', 30108,undefined,0.1),
      makeRegisterDescription('Load Current', 30109,undefined,0.1),
      makeRegisterDescription('Serge Prevent Current', 30110,undefined,0.1),
      makeRegisterDescription('Modulation Current', 30111,undefined,0.1),
      makeRegisterDescription('Oil Pres.', 30115,undefined,0.01),
      makeRegisterDescription('Oil DPres.', 30116,undefined,0.01),
      makeRegisterDescription('Oil Supply Temp', 30117,undefined,0.1),
      makeRegisterDescription('Oil Tank Temp', 30118,undefined,0.1),
      makeRegisterDescription('Oil Tank Level', 30119,undefined,0.1),
      makeRegisterDescription('1st Vib', 30120,undefined,0.1),
      makeRegisterDescription('2nd Vib', 30121,undefined,0.1),
      makeRegisterDescription('3rd Vib', 30122,undefined,0.1),
      makeRegisterDescription('MBearing (DE) Temp', 30125,undefined,0.1),
      makeRegisterDescription('MBearing (NDE) Temp', 30126,undefined,0.1),
      makeRegisterDescription('MWinding (R) Temp', 30127,undefined,0.1),
      makeRegisterDescription('MWinding (S) Temp', 30128,undefined,0.1),
      makeRegisterDescription('MWinding (T) Temp', 30129,undefined,0.1),
      makeRegisterDescription('Suction Fltr DPres.', 30130,undefined,1),
      makeRegisterDescription('2nd Inlet Temp', 30131,undefined,0.1),
      makeRegisterDescription('3rd Inlet Temp', 30132,undefined,0.1),
      makeRegisterDescription('Cool Supply temp', 30135,undefined,0.1),
      makeRegisterDescription('Oil Cooler Return Temp', 30136,undefined,0.1),
      makeRegisterDescription('1st Intercooler Return Temp', 30137,undefined,0.1),
      makeRegisterDescription('2nd Intercooler Return Temp', 30138,undefined,0.1),
      makeRegisterDescription('After Cooler Return Temp', 30139,undefined,0.1),
      makeRegisterDescription('Dis. Temp', 30140,undefined,0.1),
      makeRegisterDescription('System Temp', 30141,undefined,0.1),
      makeRegisterDescription('BOV Open Output', 30145,undefined,0.1),
      makeRegisterDescription('BOV Open Feedback', 30146,undefined,0.1),
      makeRegisterDescription('IGV Open Output', 30147,undefined,0.1),
      makeRegisterDescription('IGV Open Feedback', 30148,undefined,0.1),
      makeRegisterDescription('Comp. Run Time (Day)', 30180,undefined,1),
      makeRegisterDescription('Comp. Run Time (Hour)', 30181,undefined,1),
      makeRegisterDescription('Comp. Run Count (10000)', 30182,undefined,1),
      makeRegisterDescription('Comp. Run Count (1)', 30183,undefined,1),
      makeRegisterDescription('Load Run Time (Day)', 30184,undefined,1),
      makeRegisterDescription('Load Run Time (Hour)', 30185,undefined,1),
      makeRegisterDescription('Load Run Count (10000)', 30186,undefined,1),
      makeRegisterDescription('Load Run Count (1)', 30187,undefined,1),
      makeRegisterDescription('PLC Run Time (Day)', 30188,undefined,1),
      makeRegisterDescription('PLC Run Time (Hour)', 30189,undefined,1),
      makeRegisterDescription('Oil Supply Pres. High Alarm', 40200,undefined,0.01),
      makeRegisterDescription('Oil Supply Pres. Low Alarm', 40202,undefined,0.01),
      makeRegisterDescription('Oil Supply Pres. Low Trip', 40203,undefined,0.01),
      makeRegisterDescription('Oil Fltr DPres. High Alarm', 40204,undefined,0.01),
      makeRegisterDescription('Oil Fltr DPres. High Trip', 40205,undefined,0.01),
      makeRegisterDescription('Oil Supply Temp High Alarm', 40206,undefined,0.1),
      makeRegisterDescription('Oil Supply Temp High Trip', 40207,undefined,0.1),
      makeRegisterDescription('Oil Supply Temp Low Alarm', 40208,undefined,0.1),
      makeRegisterDescription('Oil Tank Level Low Alarm', 40210,undefined,0.1),
      makeRegisterDescription('2nd Inlet Temp High Alarm', 40220,undefined,0.1),
      makeRegisterDescription('2nd Inlet Temp High Trip', 40221,undefined,0.1),
      makeRegisterDescription('3rd Inlet Temp High Alarm', 40222,undefined,0.1),
      makeRegisterDescription('3rd Inlet Temp High Trip', 40223,undefined,0.1),
      makeRegisterDescription('Cool Supply Temp High Alarm', 40224,undefined,0.1),
      makeRegisterDescription('Comp. Dis. Pres. Low Alarm', 40226,undefined,0.01),
      makeRegisterDescription('Suction Fltr DPres. High Alarm', 40227,undefined,1),
      makeRegisterDescription('Vib (Starting) High Alarm', 40240,undefined,0.1),
      makeRegisterDescription('Vib (Starting) High Trip', 40241,undefined,0.1),
      makeRegisterDescription('Vib (Runing) High Alarm', 40242,undefined,0.1),
      makeRegisterDescription('Vib (Runing) High Trip', 40243,undefined,0.1),
      makeRegisterDescription('MBearing Temp High Alarm', 40260,undefined,0.1),
      makeRegisterDescription('MBearing Temp High Trip', 40261,undefined,0.1),
      makeRegisterDescription('MWinding Temp High Alarm', 40262,undefined,0.1),
      makeRegisterDescription('MWinding Temp High Trip', 40263,undefined,0.1),
      makeRegisterDescription('Oil Exchange Time', 40280,undefined,1),
      makeRegisterDescription('PLC BAT Exchange Time', 40281,undefined,1),
      makeRegisterDescription('Dis. Pres.', 40300,undefined,0.01),
      makeRegisterDescription('Reload Pres.', 40301,undefined,0.01)
    ]
  };

  SeAHEngDevice.call(self, master, config);
}

util.inherits(SeAHEngDeviceCompressor, SeAHEngDevice);

module.exports = SeAHEngDeviceCompressor;