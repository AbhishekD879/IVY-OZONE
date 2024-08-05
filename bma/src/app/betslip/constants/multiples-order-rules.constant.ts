/**
 * Multiples weight generation rules
 * key: betSlip sigles count
 * patterns: array of static names or reg_exp expressions of multiples which should be updated
 * other: default value for for multiple, which has no rule
 * @type {{2: {patterns: [null], other: number}, 3: {patterns: [null], other: number},
 * 4: {patterns: [null], other: number}, 5: {patterns: [null], other: number},
 * 6: {patterns: [null], other: number}, 7: {patterns: [null], other: number},
 * 8: {patterns: [null], other: number}, 9: {patterns: [null], other: number},
 * 10: {patterns: [null], other: number}, 11: {patterns: [null], other: number},
 * 12: {patterns: [null], other: number}, 13: {patterns: [null], other: number},
 * 14: {patterns: [null], other: number}, 15: {patterns: [null], other: number},
 * 16: {patterns: [null], other: number}, 17: {patterns: [null], other: number},
 * 18: {patterns: [null], other: number}, 19: {patterns: [null], other: number},
 * 20: {patterns: [null], other: number}, 21: {patterns: [null], other: number},
 * 22: {patterns: [null], other: number}, 23: {patterns: [null], other: number},
 * 24: {patterns: [null], other: number}, 25: {patterns: [null], other: number},
 * more: {patterns: [null,null], other: number}}}
 */

export const multiplesOrderRules = {
  2: { patterns: [ [ 'DBL', 'strict', -1 ] ], other: 1 },
  3: { patterns: [ [ 'TBL', 'strict', -1 ] ], other: 1 },
  4: { patterns: [ [ 'ACC4', 'strict', -1 ] ], other: 1 },
  5: { patterns: [ [ 'ACC5', 'strict', -1 ] ], other: 1 },
  6: { patterns: [ [ 'ACC6', 'strict', -1 ] ], other: 1 },
  7: { patterns: [ [ 'ACC7', 'strict', -1 ] ], other: 1 },
  8: { patterns: [ [ 'ACC8', 'strict', -1 ] ], other: 1 },
  9: { patterns: [ [ 'ACC9', 'strict', -1 ] ], other: 1 },
  10: { patterns: [ [ 'AC10', 'strict', -1 ] ], other: 1 },
  11: { patterns: [ [ 'AC11', 'strict', -1 ] ], other: 1 },
  12: { patterns: [ [ 'AC12', 'strict', -1 ] ], other: 1 },
  13: { patterns: [ [ 'AC13', 'strict', -1 ] ], other: 1 },
  14: { patterns: [ [ 'AC14', 'strict', -1 ] ], other: 1 },
  15: { patterns: [ [ 'AC15', 'strict', -1 ] ], other: 1 },
  16: { patterns: [ [ 'AC16', 'strict', -1 ] ], other: 1 },
  17: { patterns: [ [ 'AC17', 'strict', -1 ] ], other: 1 },
  18: { patterns: [ [ 'AC18', 'strict', -1 ] ], other: 1 },
  19: { patterns: [ [ 'AC19', 'strict', -1 ] ], other: 1 },
  20: { patterns: [ [ 'AC20', 'strict', -1 ] ], other: 1 },
  21: { patterns: [ [ 'AC21', 'strict', -1 ] ], other: 1 },
  22: { patterns: [ [ 'AC22', 'strict', -1 ] ], other: 1 },
  23: { patterns: [ [ 'AC23', 'strict', -1 ] ], other: 1 },
  24: { patterns: [ [ 'AC24', 'strict', -1 ] ], other: 1 },
  25: { patterns: [ [ 'AC25', 'strict', -1 ] ], other: 1 },
  more: {
    patterns: [
      [ '(ACC([0-9]+))', 'r_exp', -1 ],
      [ '(AC([0-9]+))', 'r_exp', 0 ]
    ],
    other: 1
  }
};
