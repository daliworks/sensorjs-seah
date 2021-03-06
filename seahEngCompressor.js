'use strict';

var util = require('util');
var SeAHEngDevice = require('./seahEngDevice');

function SeAHEngDeviceCompressor(master, unitId) {
  var self = this;

  var config = {
    type: 'compressor',
    unitId : unitId || 1,
    memoryZones: [
      { address: 36000, count: 36 },
      { address: 46100, count: 23 },
      { address: 16200, count: 72 },
      { address: 10080, count: 120 },
      { address: 10208, count: 3 },
      { address: 10224, count: 3 },
      { address: 10240, count: 3 },
      { address: 10256, count: 2 },
      { address: 10272, count: 1 },
      { address: 10288, count: 8 },
      { address: 10304, count: 40}
    ],
    registers : [
      SeAHEngDevice.makeRegisterDescription(16200	),
      SeAHEngDevice.makeRegisterDescription(16201	),
      SeAHEngDevice.makeRegisterDescription(16202	),
      SeAHEngDevice.makeRegisterDescription(16203	),
      SeAHEngDevice.makeRegisterDescription(16204	),
      SeAHEngDevice.makeRegisterDescription(16205	),
      SeAHEngDevice.makeRegisterDescription(16206	),
      SeAHEngDevice.makeRegisterDescription(16207	),
      SeAHEngDevice.makeRegisterDescription(16216	),
      SeAHEngDevice.makeRegisterDescription(16217	),
      SeAHEngDevice.makeRegisterDescription(16218	),
      SeAHEngDevice.makeRegisterDescription(16219	),
      SeAHEngDevice.makeRegisterDescription(16220	),
      SeAHEngDevice.makeRegisterDescription(16221	),
      SeAHEngDevice.makeRegisterDescription(16222	),
      SeAHEngDevice.makeRegisterDescription(16223	),
      SeAHEngDevice.makeRegisterDescription(16232	),
      SeAHEngDevice.makeRegisterDescription(16233	),
      SeAHEngDevice.makeRegisterDescription(16234	),
      SeAHEngDevice.makeRegisterDescription(16235	),
      SeAHEngDevice.makeRegisterDescription(16236	),
      SeAHEngDevice.makeRegisterDescription(16237	),
      SeAHEngDevice.makeRegisterDescription(16238	),
      SeAHEngDevice.makeRegisterDescription(16239	),
      SeAHEngDevice.makeRegisterDescription(16248	),
      SeAHEngDevice.makeRegisterDescription(16249	),
      SeAHEngDevice.makeRegisterDescription(16250	),
      SeAHEngDevice.makeRegisterDescription(16251	),
      SeAHEngDevice.makeRegisterDescription(16252	),
      SeAHEngDevice.makeRegisterDescription(16253	),
      SeAHEngDevice.makeRegisterDescription(16254	),
      SeAHEngDevice.makeRegisterDescription(16255	),
      SeAHEngDevice.makeRegisterDescription(16264	),
      SeAHEngDevice.makeRegisterDescription(16265	),
      SeAHEngDevice.makeRegisterDescription(16266	),
      SeAHEngDevice.makeRegisterDescription(16267	),
      SeAHEngDevice.makeRegisterDescription(16268	),
      SeAHEngDevice.makeRegisterDescription(16269	),
      SeAHEngDevice.makeRegisterDescription(16270	),
      SeAHEngDevice.makeRegisterDescription(16271	),
      SeAHEngDevice.makeRegisterDescription(10080	),
      SeAHEngDevice.makeRegisterDescription(10081	),
      SeAHEngDevice.makeRegisterDescription(10082	),
      SeAHEngDevice.makeRegisterDescription(10083	),
      SeAHEngDevice.makeRegisterDescription(10084	),
      SeAHEngDevice.makeRegisterDescription(10085	),
      SeAHEngDevice.makeRegisterDescription(10086	),
      SeAHEngDevice.makeRegisterDescription(10087	),
      SeAHEngDevice.makeRegisterDescription(10096	),
      SeAHEngDevice.makeRegisterDescription(10097	),
      SeAHEngDevice.makeRegisterDescription(10098	),
      SeAHEngDevice.makeRegisterDescription(10099	),
      SeAHEngDevice.makeRegisterDescription(10100	),
      SeAHEngDevice.makeRegisterDescription(10101	),
      SeAHEngDevice.makeRegisterDescription(10102	),
      SeAHEngDevice.makeRegisterDescription(10112	),
      SeAHEngDevice.makeRegisterDescription(10113	),
      SeAHEngDevice.makeRegisterDescription(10114	),
      SeAHEngDevice.makeRegisterDescription(10115	),
      SeAHEngDevice.makeRegisterDescription(10116	),
      SeAHEngDevice.makeRegisterDescription(10117	),
      SeAHEngDevice.makeRegisterDescription(10118	),
      SeAHEngDevice.makeRegisterDescription(10119	),
      SeAHEngDevice.makeRegisterDescription(10128	),
      SeAHEngDevice.makeRegisterDescription(10129	),
      SeAHEngDevice.makeRegisterDescription(10130	),
      SeAHEngDevice.makeRegisterDescription(10131	),
      SeAHEngDevice.makeRegisterDescription(10132	),
      SeAHEngDevice.makeRegisterDescription(10133	),
      SeAHEngDevice.makeRegisterDescription(10134	),
      SeAHEngDevice.makeRegisterDescription(10135	),
      SeAHEngDevice.makeRegisterDescription(10144	),
      SeAHEngDevice.makeRegisterDescription(10145	),
      SeAHEngDevice.makeRegisterDescription(10146	),
      SeAHEngDevice.makeRegisterDescription(10147	),
      SeAHEngDevice.makeRegisterDescription(10148	),
      SeAHEngDevice.makeRegisterDescription(10149	),
      SeAHEngDevice.makeRegisterDescription(10150	),
      SeAHEngDevice.makeRegisterDescription(10151	),
      SeAHEngDevice.makeRegisterDescription(10160	),
      SeAHEngDevice.makeRegisterDescription(10161	),
      SeAHEngDevice.makeRegisterDescription(10162	),
      SeAHEngDevice.makeRegisterDescription(10163	),
      SeAHEngDevice.makeRegisterDescription(10164	),
      SeAHEngDevice.makeRegisterDescription(10165	),
      SeAHEngDevice.makeRegisterDescription(10166	),
      SeAHEngDevice.makeRegisterDescription(10167	),
      SeAHEngDevice.makeRegisterDescription(10176	),
      SeAHEngDevice.makeRegisterDescription(10177	),
      SeAHEngDevice.makeRegisterDescription(10178	),
      SeAHEngDevice.makeRegisterDescription(10179	),
      SeAHEngDevice.makeRegisterDescription(10180	),
      SeAHEngDevice.makeRegisterDescription(10181	),
      SeAHEngDevice.makeRegisterDescription(10182	),
      SeAHEngDevice.makeRegisterDescription(10183	),
      SeAHEngDevice.makeRegisterDescription(10192	),
      SeAHEngDevice.makeRegisterDescription(10193	),
      SeAHEngDevice.makeRegisterDescription(10194	),
      SeAHEngDevice.makeRegisterDescription(10195	),
      SeAHEngDevice.makeRegisterDescription(10196	),
      SeAHEngDevice.makeRegisterDescription(10197	),
      SeAHEngDevice.makeRegisterDescription(10198	),
      SeAHEngDevice.makeRegisterDescription(10199	),
      SeAHEngDevice.makeRegisterDescription(10208	),
      SeAHEngDevice.makeRegisterDescription(10209	),
      SeAHEngDevice.makeRegisterDescription(10210	),
      SeAHEngDevice.makeRegisterDescription(10211	),
      SeAHEngDevice.makeRegisterDescription(10212	),
      SeAHEngDevice.makeRegisterDescription(10213	),
      SeAHEngDevice.makeRegisterDescription(10214	),
      SeAHEngDevice.makeRegisterDescription(10215	),
      SeAHEngDevice.makeRegisterDescription(10224	),
      SeAHEngDevice.makeRegisterDescription(10225	),
      SeAHEngDevice.makeRegisterDescription(10226	),
      SeAHEngDevice.makeRegisterDescription(10227	),
      SeAHEngDevice.makeRegisterDescription(10228	),
      SeAHEngDevice.makeRegisterDescription(10229	),
      SeAHEngDevice.makeRegisterDescription(10230	),
      SeAHEngDevice.makeRegisterDescription(10231	),
      SeAHEngDevice.makeRegisterDescription(10240	),
      SeAHEngDevice.makeRegisterDescription(10241	),
      SeAHEngDevice.makeRegisterDescription(10242	),
      SeAHEngDevice.makeRegisterDescription(10243	),
      SeAHEngDevice.makeRegisterDescription(10244	),
      SeAHEngDevice.makeRegisterDescription(10245	),
      SeAHEngDevice.makeRegisterDescription(10246	),
      SeAHEngDevice.makeRegisterDescription(10247	),
      SeAHEngDevice.makeRegisterDescription(10256	),
      SeAHEngDevice.makeRegisterDescription(10257	),
      SeAHEngDevice.makeRegisterDescription(10258	),
      SeAHEngDevice.makeRegisterDescription(10259	),
      SeAHEngDevice.makeRegisterDescription(10260	),
      SeAHEngDevice.makeRegisterDescription(10261	),
      SeAHEngDevice.makeRegisterDescription(10262	),
      SeAHEngDevice.makeRegisterDescription(10263	),
      SeAHEngDevice.makeRegisterDescription(10272	),
      SeAHEngDevice.makeRegisterDescription(10273	),
      SeAHEngDevice.makeRegisterDescription(10274	),
      SeAHEngDevice.makeRegisterDescription(10275	),
      SeAHEngDevice.makeRegisterDescription(10276	),
      SeAHEngDevice.makeRegisterDescription(10277	),
      SeAHEngDevice.makeRegisterDescription(10278	),
      SeAHEngDevice.makeRegisterDescription(10279	),
      SeAHEngDevice.makeRegisterDescription(10288	),
      SeAHEngDevice.makeRegisterDescription(10289	),
      SeAHEngDevice.makeRegisterDescription(10290	),
      SeAHEngDevice.makeRegisterDescription(10291	),
      SeAHEngDevice.makeRegisterDescription(10292	),
      SeAHEngDevice.makeRegisterDescription(10293	),
      SeAHEngDevice.makeRegisterDescription(10294	),
      SeAHEngDevice.makeRegisterDescription(10295	),
      SeAHEngDevice.makeRegisterDescription(10304	),
      SeAHEngDevice.makeRegisterDescription(10305	),
      SeAHEngDevice.makeRegisterDescription(10306	),
      SeAHEngDevice.makeRegisterDescription(10307	),
      SeAHEngDevice.makeRegisterDescription(10308	),
      SeAHEngDevice.makeRegisterDescription(10309	),
      SeAHEngDevice.makeRegisterDescription(10310	),
      SeAHEngDevice.makeRegisterDescription(10311	),
      SeAHEngDevice.makeRegisterDescription(10320	),
      SeAHEngDevice.makeRegisterDescription(10321	),
      SeAHEngDevice.makeRegisterDescription(10322	),
      SeAHEngDevice.makeRegisterDescription(10323	),
      SeAHEngDevice.makeRegisterDescription(10324	),
      SeAHEngDevice.makeRegisterDescription(10325	),
      SeAHEngDevice.makeRegisterDescription(10326	),
      SeAHEngDevice.makeRegisterDescription(10327	),
      SeAHEngDevice.makeRegisterDescription(10336	),
      SeAHEngDevice.makeRegisterDescription(10337	),
      SeAHEngDevice.makeRegisterDescription(10338	),
      SeAHEngDevice.makeRegisterDescription(10339	),
      SeAHEngDevice.makeRegisterDescription(10340	),
      SeAHEngDevice.makeRegisterDescription(10341	),
      SeAHEngDevice.makeRegisterDescription(10342	),
      SeAHEngDevice.makeRegisterDescription(10343	),
      SeAHEngDevice.makeRegisterDescription(36000, 0, 10000, 'readInt16BE', 0.01),
      SeAHEngDevice.makeRegisterDescription(36001, 0, 10000, 'readInt16BE', 0.01),
      SeAHEngDevice.makeRegisterDescription(36002, 0, 10000, 'readInt16BE', 0.01),
      SeAHEngDevice.makeRegisterDescription(36003, 0, 10000, 'readInt16BE', 0.01),
      SeAHEngDevice.makeRegisterDescription(36004, 0, 10000, 'readInt16BE', 0.01),

      SeAHEngDevice.makeRegisterDescription(36005, 0, 10000, 'readInt16BE', 0.1),
      SeAHEngDevice.makeRegisterDescription(36006, 0, 10000, 'readInt16BE', 0.1),
      SeAHEngDevice.makeRegisterDescription(36007, 0, 10000, 'readInt16BE', 0.1),
      SeAHEngDevice.makeRegisterDescription(36008, 0, 1000, 'readInt16BE', 0.1),
      SeAHEngDevice.makeRegisterDescription(36009, 0, 10000, 'readInt16BE', 0.1),
      SeAHEngDevice.makeRegisterDescription(36010, 0, 10000, 'readInt16BE', 0.1),
      SeAHEngDevice.makeRegisterDescription(36011, 0, 10000, 'readInt16BE', 0.1),
      SeAHEngDevice.makeRegisterDescription(36012, 0, 10000, 'readInt16BE', 0.1),
      SeAHEngDevice.makeRegisterDescription(36013, 0, 10000, 'readInt16BE', 0.1),
      SeAHEngDevice.makeRegisterDescription(36014, 0, 10000, 'readInt16BE', 0.1),

      SeAHEngDevice.makeRegisterDescription(36015, 0, 10000, 'readInt16BE', 0.01),
      SeAHEngDevice.makeRegisterDescription(36016, 0, 10000, 'readInt16BE', 0.01),
      SeAHEngDevice.makeRegisterDescription(36017, -1000, 5000, 'readInt16BE', 0.1),
      SeAHEngDevice.makeRegisterDescription(36018, -1000, 5000, 'readInt16BE', 0.1),
      SeAHEngDevice.makeRegisterDescription(36019, 0, 1000, 'readInt16BE', 0.1),

      SeAHEngDevice.makeRegisterDescription(36020, 0, 10000, 'readInt16BE', 0.1),
      SeAHEngDevice.makeRegisterDescription(36021, 0, 10000, 'readInt16BE', 0.1),
      SeAHEngDevice.makeRegisterDescription(36022, 0, 10000, 'readInt16BE', 0.1),
      SeAHEngDevice.makeRegisterDescription(36023, 0, 10000, 'readInt16BE', 0.1),
      SeAHEngDevice.makeRegisterDescription(36024, 0, 10000, 'readInt16BE', 0.1),

      SeAHEngDevice.makeRegisterDescription(36025, -1000, 5000, 'readInt16BE', 0.1),
      SeAHEngDevice.makeRegisterDescription(36026, -1000, 5000, 'readInt16BE', 0.1),
      SeAHEngDevice.makeRegisterDescription(36027, -1000, 5000, 'readInt16BE', 0.1),
      SeAHEngDevice.makeRegisterDescription(36028, -1000, 5000, 'readInt16BE', 0.1),
      SeAHEngDevice.makeRegisterDescription(36029, -1000, 5000, 'readInt16BE', 0.1),
      SeAHEngDevice.makeRegisterDescription(36030, -10000, 10000, 'readInt16BE', 1),
      SeAHEngDevice.makeRegisterDescription(36031, -1000, 5000, 'readInt16BE', 0.1),
      SeAHEngDevice.makeRegisterDescription(36032, -1000, 5000, 'readInt16BE', 0.1),
      SeAHEngDevice.makeRegisterDescription(36033, -1000, 5000, 'readInt16BE', 0.1),
      SeAHEngDevice.makeRegisterDescription(36034, -1000, 5000, 'readInt16BE', 0.1),
      SeAHEngDevice.makeRegisterDescription(36035, -1000, 5000, 'readInt16BE', 0.1),

      SeAHEngDevice.makeWriteRegisterDescription(320),
      SeAHEngDevice.makeWriteRegisterDescription(321),
      SeAHEngDevice.makeWriteRegisterDescription(322),
      SeAHEngDevice.makeWriteRegisterDescription(323),
      SeAHEngDevice.makeWriteRegisterDescription(324),
      SeAHEngDevice.makeWriteRegisterDescription(325),
      SeAHEngDevice.makeWriteRegisterDescription(326),

      SeAHEngDevice.makeWriteRegisterDescription(40200, 0, 10000, 'readInt16BE', 'writeInt16BE', 0.01),

      SeAHEngDevice.makeWriteRegisterDescription(40202,   0, 10000, 'readInt16BE', 'writeInt16BE', 0.01),
      SeAHEngDevice.makeWriteRegisterDescription(40203,   0, 10000, 'readInt16BE', 'writeInt16BE', 0.01),
      SeAHEngDevice.makeWriteRegisterDescription(40204,   0, 10000, 'readInt16BE', 'writeInt16BE', 0.01),
      SeAHEngDevice.makeWriteRegisterDescription(40205,   0, 10000, 'readInt16BE', 'writeInt16BE', 0.01),
      SeAHEngDevice.makeWriteRegisterDescription(40206,   -1000, 5000, 'readInt16BE', 'writeInt16BE', 0.1),
      SeAHEngDevice.makeWriteRegisterDescription(40207,   -1000, 5000, 'readInt16BE', 'writeInt16BE', 0.1),
      SeAHEngDevice.makeWriteRegisterDescription(40208,   -1000, 5000, 'readInt16BE', 'writeInt16BE', 0.1),

      SeAHEngDevice.makeWriteRegisterDescription(40210,   0, 1000, 'readInt16BE', 'writeInt16BE', 0.1),

      SeAHEngDevice.makeWriteRegisterDescription(40220,   -1000, 5000, 'readInt16BE', 'writeInt16BE', 0.1),
      SeAHEngDevice.makeWriteRegisterDescription(40221,   -1000, 5000, 'readInt16BE', 'writeInt16BE', 0.1),
      SeAHEngDevice.makeWriteRegisterDescription(40222,   -1000, 5000, 'readInt16BE', 'writeInt16BE', 0.1),
      SeAHEngDevice.makeWriteRegisterDescription(40223,   -1000, 5000, 'readInt16BE', 'writeInt16BE', 0.1),
      SeAHEngDevice.makeWriteRegisterDescription(40224,   -1000, 5000, 'readInt16BE', 'writeInt16BE', 0.1),

      SeAHEngDevice.makeWriteRegisterDescription(40226,   0, 10000, 'readInt16BE', 'writeInt16BE', 0.01),
      SeAHEngDevice.makeWriteRegisterDescription(40227,   -10000, 10000, 'readInt16BE', 'writeInt16BE', 1),

      SeAHEngDevice.makeWriteRegisterDescription(40240,   0, 10000, 'readInt16BE', 'writeInt16BE', 0.1),
      SeAHEngDevice.makeWriteRegisterDescription(40241,   0, 10000, 'readInt16BE', 'writeInt16BE', 0.1),
      SeAHEngDevice.makeWriteRegisterDescription(40242,   0, 10000, 'readInt16BE', 'writeInt16BE', 0.1),
      SeAHEngDevice.makeWriteRegisterDescription(40243,   0, 10000, 'readInt16BE', 'writeInt16BE', 0.1),

      SeAHEngDevice.makeWriteRegisterDescription(40260,   -1000, 5000, 'readInt16BE', 'writeInt16BE', 0.1),
      SeAHEngDevice.makeWriteRegisterDescription(40261,   -1000, 5000, 'readInt16BE', 'writeInt16BE', 0.1),
      SeAHEngDevice.makeWriteRegisterDescription(40262,   -1000, 5000, 'readInt16BE', 'writeInt16BE', 0.1),
      SeAHEngDevice.makeWriteRegisterDescription(40263,   -1000, 5000, 'readInt16BE', 'writeInt16BE', 0.1),

      SeAHEngDevice.makeWriteRegisterDescription(40280, 0, 65535, 'readUInt16BE', 'writeUInt16BE', 1),
      SeAHEngDevice.makeWriteRegisterDescription(40281, 0, 65535, 'readUInt16BE', 'writeUInt16BE', 1),

      SeAHEngDevice.makeWriteRegisterDescription(40300, 0, 10000, 'readInt16BE', 'writeInt16BE', 0.01),
      SeAHEngDevice.makeWriteRegisterDescription(40301, 0, 10000, 'readInt16BE', 'writeInt16BE', 0.01)

    ]
  };

  SeAHEngDevice.call(self, master, config);
}

util.inherits(SeAHEngDeviceCompressor, SeAHEngDevice);

module.exports = SeAHEngDeviceCompressor;