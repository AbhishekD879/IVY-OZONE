import environment from '@environment/oxygenEnvConfig';

export const brand = (env) => env.brand === 'bma' ? 'Coral' : 'Ladbrokes';

export const defaultModules: any[] = [ // IOutputModule
  {
    '@type': 'RacingEventsModule',
    _id: '1',
    title: 'UK and Irish Races',
    data: [],
    racingType: 'UIR'
  },
  {
    '@type': 'RacingEventsModule',
    _id: '2',
    title: 'International Races',
    racingType: 'IR',
    data: []
  },
  {
    '@type': 'RacingEventsModule',
    _id: '3',
    title: `${brand(environment)} Legends`,
    racingType: 'LVR',
    data: []
  },
  {
    '@type': 'RacingModule',
    title: 'International Tote Carousel',
    data: [
      {
        '@type': 'RacingModuleConfig',
        name: 'ITC'
      }
    ]
  },
  {
    '@type': 'VirtualRaceModule',
    title: 'Virtual Race Carousel',
    data: [
      {
        '@type': 'VirtualRaceModuleData',
        name: 'VRC'
      }
    ]
  },
];

export const enum FLAGS {
  UK = 'UK',
  VR = 'VR'
}

export const enum AREAS {
  HREDP = 'HREDP'
}

export const HRTabs = {
  MARKETS: 'markets', MYBETS: 'myBets'
};