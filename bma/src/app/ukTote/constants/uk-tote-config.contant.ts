export const UK_TOTE_CONFIG = {
  intTotePoolTypes: ['WN', 'PL', 'EX', 'TR'],
  displayOrder: [
    // UK Tote
    'UWIN', 'UPLC', 'UEXA', 'UTRI', 'UQDP', 'UPLP', 'UJKP', 'UPP7','USC6',
    // International Tote
    'WN', 'PL', 'EX', 'TR'
  ],
  marketPath: 'totepool',
  allowedPools: [
    // UK Tote
    'UWIN', 'UPLC', 'UEXA', 'UTRI', 'UQDP', 'UPLP', 'UJKP', 'UPP7','USC6',
    // International Tote
    'WN', 'PL', 'EX', 'TR'
  ],
  poolTypesMap: {
    // UK Tote
    UWIN: { name: 'Win Totepool', path: 'win' },
    UPLC: { name: 'Place Totepool', path: 'place' },
    UEXA: { name: 'Exacta Totepool', path: 'exacta' },
    UTRI: { name: 'Trifecta Totepool', path: 'trifecta' },
    UJKP: { name: 'Jackpot Totepool', path: 'jackpot' },
    UPLP: { name: 'Placepot Totepool', path: 'placepot' },
    UQDP: { name: 'Quadpot Totepool', path: 'quadpot' },
    USC6: { name: 'Scoop6 Totepool', path: 'scoop6' },
    UPP7: { name: 'ITV7 Placepot Totepool', path: 'itv7-placepot' },
    USC7: { name: 'super7', path: 'super7' },
    USW: { name: 'swinger', path: 'swinger' },
    UTD: { name: 'double', path: 'double' },
    UTT: { name: 'treble', path: 'treble' },

    // International Tote
    WN: { name: 'Win Totepool', path: 'win' },
    PL: { name: 'Place Totepool', path: 'place' },
    EX: { name: 'Exacta Totepool', path: 'exacta' },
    TR: { name: 'Trifecta Totepool', path: 'trifecta' },
    P3: { name: 'Placepot Totepool', path: 'placepot' },
    P6: { name: 'Quadpot Totepool', path: 'quadpot' }
  },
  MULTIPLE_LEGS_TOTE_BETS: [
    'UPLP', // Placepot (UK)
    'UQDP', // Quadpot (UK)
    'USC6', // Scoop6 (UK)
    'UJKP', // Jackpot (UK)
    'P3', // Placepot (INT)
    'P6', // Quadpot (INT)
    'UPP7', //ITV7Placepot
  ],
  toteBetsToExcludeFavourites: [
    'UEXA',
    'UTRI',
    'UWIN',
    'UPLC'
  ],
  SUSPENDED_STATUS_CODE: 'S',
  channelName: {
    event: 'sEVENT',
    market: 'sEVMKT',
    selection: 'sSELCN'
  },
  scoopSixPoolType: 'USC6',
  scoopSevenPoolType: 'UPP7'
};
