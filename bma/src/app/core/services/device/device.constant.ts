export const sumsungVersion = {
    S7: [ 'SM-G93' ],
    S6: [ 'SM-G92' ],
    S5: [ 'SM-G90', 'SCL23', 'SC-04F', 'SM-G80', 'SM-G87' ],
    S4: [ 'GT-I95', 'GT-I9190', 'SM-C101', 'SHV-E300', 'SGH-M919', 'SCH-I545', 'SPH-L720', 'SGH-I337',
        'SC-04E', 'GT-I9192' ],
    S3: [ 'GT-I93', 'GT-I8200', 'GT-I8190', 'SHV-E210', 'SGH-T999', 'SGH-I747', 'SGH-N064', 'SGH-N035',
        'SCH-J021', 'SCH-R530', 'SCH-I535', 'SCH-S960', 'SCH-S968', 'SCH-I939' ],
    S2: [ 'GT-I910', 'GT-I921', 'SGH-I757', 'SGH-I727', 'SGH-I927', 'SGH-T989', 'SCH-i919', 'GT-i910',
        'SC-02C', 'SHW-M250', 'SGH-I777', 'SPH-D710', 'SCH-R760', 'ISW11SC' ],
    S1: [ 'GT-I90', 'GT-S75', 'GT-G316' ],
    Note: [ 'GT-N700', 'SHV-E160', 'SC-05D', 'SGH-N054', 'SGH-i717', 'SGH-T879', 'GT-i922', 'SCH-I889' ],
    'Note 2': [ 'GT-N710', 'SCH-i605', 'SCH-R950', 'SGH-i317', 'SGH-T889', 'SPH-L900', 'SCH-N719',
        'SGH-N025', 'SC-02E', 'SHV-E250' ],
    'Note 3': [ 'SM-N900' ],
    'Note 8.0': [ 'GT-N511', 'GT-N510' ],
    'Tab 2 7.0': [ 'GT-P310', 'GT-P311' ],
    'Tab 3 7.0': [ 'GT-P322', 'SM-T217', 'GT-P320', 'SM-T211', 'GT-P321', 'SM-T210' ],
    'Tab 3 8.0': [ 'SM-T310', 'SM-T311', 'SM-T315' ],
    'Tab 10.1': [ 'GT-P710', 'SC-01D', 'GT-P751' ],
    'Tab 2 10.1': [ 'GT-P510', 'GT-P511' ],
    'Tab 3 10.1': [ 'GT-P520', 'GT-P521', 'GT-P522', 'SM-T530', 'SM-T531', 'SM-T535' ]
};

export const samsungPrefixes = ['SM', 'SCL23', 'SC', 'GT', 'SHV', 'SGH', 'SCH', 'SHW', 'SPH', 'ISW11SC'];
export const samsungPrefixesRegexp = new RegExp(`^${samsungPrefixes.join('|')}`);
export const uaRegexp = /\((Linux;[^)]+)\)/;
export const uaSamsungRegexp = /^\s+|samsung-?\s*|\/\w+|\s*build\/.+/gi;
