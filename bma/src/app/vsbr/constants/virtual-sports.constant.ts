import { IMarketsConfig, IMarketsTemplateMap } from './../models/virtual-sports-config.model';

export const FIRST_CATEGORY: number = 0;
export const VIRTUAL_ROUTE_NAME: string = 'virtual-sports';
export const SPORTS_ROUTE_NAME: string = 'sports';

export const marketsTemplateMap: IMarketsTemplateMap = {
  WinEw: ['To Win', 'To-Win', 'Win/EachWay', 'Win or each way', 'Win or Each Way', 'Meeting Winner', 'WIN',
    'Win & Each Way Places 1,2,3,4,5'],
  Horizontal: ['Match Betting', 'Match Result', 'Match Results', 'First Team to Score', 'Both Teams to Score',
    'Match Result & Both Teams To Score','Score from Penalty', 'Win/Draw/Win', 'Double Chance', 'Head/Head (winner)', 'Leg Winner',
    '180 in the leg', 'Winning Checkout', 'Winning Double Colour', 'Nine dart finish'],
  Vertical: ['Total Number of Goals', 'Under/Over 2.5', 'Correct Score (Game)', 'Total Number of Points',
    'Seconds Survived', 'Seconds Survived (Under/Over)40', 'Seconds Survived (Under/Over)50', 'Seconds Survived (Under/Over)60',
    'Seconds Survived (Under/Over)70', 'Seconds Survived (3 way)', 'Fight Outcome', 'Seconds Survived and Outcome',
    'Winner, Checkout and Double', 'Winning Double', 'Player 1 first three darts', 'Player 2 first three darts']
};

export const verticalTemplateName: string = 'Vertical';
export const winEwTemplateName: string = 'WinEw';

export const winEwFilter: string = 'winew';
export const forecastFilter: string = 'forecast';
export const tricastFilter: string = 'tricast';

export const MARKETS_CONFIG: IMarketsConfig = {
  [winEwFilter]: 'Win/Each Way',
  [forecastFilter]: 'Forecast',
  [tricastFilter]: 'Tricast',
  'place': 'Place',
  'show': 'Show',
};
