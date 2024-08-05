import { YourCallMarketGroupItem } from '@app/yourCall/models/markets/yourcall-market-group-item';
import { IYourcallSelection, IYourcallSeletionBase } from '@app/yourCall/models/selection.model';
import { YourCallMarketGroup } from '@app/yourCall/models/markets/yourcall-market-group';

export const groupedMarkets = ['Total Goals', 'Total Corners', 'Teams to Score', 'Match Booking Points'];
export const totalGoals = [{ 'bothTeams-fullTime': 'Total Goals' },
{ 'teamA-fullTime': 'Home Total Goals' },
{ 'teamB-fullTime': 'Away Total Goals' }
];
export const totalCorners = [{ 'bothTeams-fullTime': 'Total Corners' },
{ 'teamA-fullTime': 'Home Total Corners' },
{ 'teamB-fullTime': 'Away Total Corners' }
];

export const matchBooking = [{ 'bothTeams-fullTime': 'Match Booking Points' },
{ 'teamA-fullTime': 'Away Booking Points' },
{ 'teamB-fullTime': 'Home Booking Points' }
];

export const teamsToScore = [{ 'bothTeams-fullTime': 'Both Teams To Score In First Half' },
{ 'teamA-fullTime': 'Both Teams To Score In Second Half' },
{ 'teamB-fullTime': 'Both Teams To Score In Both Halves' }
];

export const result = [{ 'bothTeams-fullTime': 'Match Betting' },
];

export const groups = {
  'Total Goals': 'Total Goals',
  'Home Total Goals': 'Total Goals',
  'Away Total Goals': 'Total Goals',
  'Total Corners': 'Total Corners',
  'Home Total Corners': 'Total Corners',
  'Away Total Corners': 'Total Corners',
  'Match Betting': 'Match Betting',
  'FIRST HALF BETTING': 'Match Betting',
  'SECOND HALF BETTING': 'Match Betting',
  'Match Booking Points': 'Match Booking Points',
  'Away Booking Points': 'Match Booking Points',
  'Home Booking Points': 'Match Booking Points'
};

export const customMarkets = {
  'Both Teams To Score': [
    {
      key: 'Both',
      isGroup: true,
      name: 'Select Team',
      groupName: 'Both Teams To Score',
      'val': [{ key: '90 Minutes', '90 Minutes': 'BOTH TEAMS TO SCORE', isGroup: false, name: 'Time Period' },
      { key: '1st Half', '1st Half': 'BOTH TEAMS TO SCORE IN 1ST HALF', isGroup: false },
      { key: '2nd Half', '2nd Half': 'BOTH TEAMS TO SCORE IN 2ND HALF', isGroup: false },
      { key: 'Both Halves', 'Both Halves': 'BOTH TEAMS TO SCORE IN BOTH HALVES', isGroup: false }]
    },
    {
      key: 'Home',
      isGroup: true,
      'val': [{ key: 'Both Halves', 'Both Halves': 'TEAM TO SCORE IN BOTH HALVES', isGroup: false, name: 'Time Period' }],
    }, {
      key: 'Away',
      isGroup: true,
      'val': [{ key: 'Both Halves', 'Both Halves': 'TEAM TO SCORE IN BOTH HALVES', isGroup: false, name: 'Time Period' }]
    }
  ],


  'Match Betting': [
    {
      key: 'HOME',
      isGroup: true,
      name: 'Select Team',
      groupName: 'Match Betting',
      'val': [{ key: '90 Minutes', '90 Minutes': 'MATCH BETTING', isGroup: false, name: 'Time Period' },
      { key: '1st Half', '1st Half': 'FIRST HALF BETTING', isGroup: false, name: 'Time Period' },
      { key: '2nd Half', '2nd Half': 'SECOND HALF BETTING', isGroup: false, name: 'Time Period' }
      ],
    },
    {
      key: 'DRAW',
      isGroup: true,
      'val': [{ key: '90 Minutes', '90 Minutes': 'MATCH BETTING', isGroup: false, name: 'Time Period' },
      { key: '1st Half', '1st Half': 'FIRST HALF BETTING', isGroup: false, name: 'Time Period' },
      { key: '2nd Half', '2nd Half': 'SECOND HALF BETTING', isGroup: false, name: 'Time Period' }
      ],
    }, {
      key: 'AWAY',
      isGroup: true,
      'val': [{ key: '90 Minutes', '90 Minutes': 'MATCH BETTING', isGroup: false, name: 'Time Period' },
      { key: '1st Half', '1st Half': 'FIRST HALF BETTING', isGroup: false, name: 'Time Period' },
      { key: '2nd Half', '2nd Half': 'SECOND HALF BETTING', isGroup: false, name: 'Time Period' }
      ],
    }
  ]
};
export const newMarketsArr = [
  'Total Goals',
  'Participant_1 Total Goals',
  'Participant_2 Total Goals',
  'Exact Total Goals',
  '1st Half Participant_1 Total Goals',
  '2nd Half Participant_1 Total Goals',
  '1st Half Participant_2 Total Goals',
  '2nd Half Participant_2 Total Goals',
  'Participant_1 To Score 2+ Goals',
  'Participant_1 To Score 3+ Goals',
  'Participant_1 To Score 4+ Goals',
  'Participant_1 To Score 5+ Goals',
  'Participant_2 To Score 2+ Goals',
  'Participant_2 To Score 3+ Goals',
  'Participant_2 To Score 4+ Goals',
  'Participant_2 To Score 5+ Goals',

  'Match Betting',

  'Total Corners',
  'Participant_1 Total corners',
  'Participant_2 Total corners',

  'Both Teams To Score',
  'Both Teams To Score In First Half',
  'Both Teams To Score In Second Half',
  'Both Teams To Score In Both Halves',
  'Team To Score In Both Halves',

  'Booking points',
  'Match Booking Points',
  'Participant_1 Booking points',
  'Participant_2 Booking points',

  'Player Bets',
  // 'To Be Shown A Card',
  // 'First Goalscorer',
  // 'Last Goalscorer',
  // 'Anytime Goalscorer'
];

export const goalsMarketCheck = [
  'Total Goals',
  'Participant_1 Total Goals',
  'Participant_2 Total Goals',
  'Exact Total Goals',
  '1st Half Participant_1 Total Goals',
  '2nd Half Participant_1 Total Goals',
  '1st Half Participant_2 Total Goals',
  '2nd Half Participant_2 Total Goals',
  'Participant_1 To Score 2+ Goals',
  'Participant_1 To Score 3+ Goals',
  'Participant_1 To Score 4+ Goals',
  'Participant_1 To Score 5+ Goals',
  'Participant_2 To Score 2+ Goals',
  'Participant_2 To Score 3+ Goals',
  'Participant_2 To Score 4+ Goals',
  'Participant_2 To Score 5+ Goals'
];

export const cornersMarketCheck = [
  'Total Corners',
  'Participant_1 Total corners',
  'Participant_2 Total corners'
]

export const bothTeamsToScoreMarketCheck = [
  'Both Teams To Score',
  'Both Teams To Score In First Half',
  'Both Teams To Score In Second Half',
  'Both Teams To Score In Both Halves',
  'Team To Score In Both Halves'
];
export const MatchBookingPointsMarketCheck = [
  'Match Booking Points',
  'Booking points',
  'Participant_1 Booking points',
  'Participant_2 Booking points',
];


export const AddTo = 'ADD TO BET BUILDER';
export const Added = 'ADDED';

export const MarketNames = {
  'Popular Markets': 'Popular Market',
  'Player Bets': 'Player Bet',
  'Team Bets': 'Team Bet'
};
export interface IEnableSwitchers {
  'All Markets'?: boolean;
  'Popular Markets'?: boolean;
  'Team Bets'?: boolean;
  'Player Bets'?: boolean;
}


export const CustomDefaultGroup: ICustomMarket = {
  'Both Teams To Score': [{
    key: '',
    isGroup: false,
    name: '',
    groupName: '',
    '90 Minutes': '',
    '1st Half': '',
    '2nd Half': '',
    'Both Halves': '',
    'val': {}
  }],
  'Match Betting': [{
    key: '',
    isGroup: false,
    name: '',
    groupName: '',
    '90 Minutes': '',
    '1st Half': '',
    '2nd Half': '',
    'Both Halves': '',
    'val': {}
  }]
};

export const Goals = {
  'Total Goals': 'Goals',
  'Total Corners': 'Corners',
  'Match Booking Points': 'Points'
};


export interface IExpandCollapseMap {
  [key: number]: boolean;
}

export interface ISwitcher {
  name: string;
}

export interface ICustomMarket {
  [key: string]: ICustomMarketType[];
}

export interface ICustomMarketType {
  key: string;
  isGroup: boolean;
  name: string;
  groupName: string;
  '90 Minutes'?: string;
  '1st Half'?: string;
  '2nd Half'?: string;
  'Both Halves'?: string;
  'val' : any;
}

export interface ITabEvent {
  market: string;
}

export interface ISelectedMarketSelection {
  market: YourCallMarketGroupItem;
  selection: IYourcallSelection;
}

export interface IMapMarket {
  'market': YourCallMarketGroup | YourCallMarketGroupItem;
  'selection': IYourcallSeletionBase;
}