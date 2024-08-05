export const activeMatrixFormation = [{
  rowIndex: 1,
  collIndex: 6,
  position: 'Hacker',
  stat: 'To Concede',
  statId: 14,
  roleId: 'position1'
}, {
  rowIndex: 1,
  collIndex: 7,
  position: 'Cruncher',
  stat: 'Tackles',
  statId: 2,
  roleId: 'position2'
}, {
  rowIndex: 2,
  collIndex: 1,
  position: 'Baller',
  stat: 'Assists',
  statId: 6,
  roleId: 'position3'
}, {
  rowIndex: 3,
  collIndex: 6,
  position: 'Sniper',
  stat: 'Shots',
  statId: 3,
  roleId: 'position4'
}, {
  rowIndex: 3,
  collIndex: 7,
  position: 'FInisher',
  stat: 'Goals',
  statId: 12,
  roleId: 'position5'
}];

export const activeItemMock = {
  rowIndex: 2,
  collIndex: 7,
  position: 'Sharpshooter',
  stat: 'Shots On Target',
  statId: 4,
  selected: true
} as any;

export const playerMock = {
  id: 18,
  name: 'J. Gbamin',
  teamName: 'EVERTON',
  teamColors: {
    primaryColour: '#777777',
    secondaryColour: '#ccc',
  },
  appearances: 2,
  cleanSheets: 0,
  tackles: 2,
  passes: 35,
  crosses: 35,
  assists: 0,
  shots: 0,
  shotsOnTarget: 0,
  shotsOutsideTheBox: 0,
  goals: 0,
  goalsInsideTheBox: 0,
  goalsOutsideTheBox: 0,
  cards: 0,
  cardsRed: 0,
  cardsYellow: 0,
  position: {
    long: 'Midfielder',
    short: 'MF'
  },
  penaltySaves: 5,
  conceeded: 3,
  saves: null,
  isGK: false
};

export const eventEntityMock = {
  id: 8,
  name: 'Leg event'
} as any;
