'use strict';

export const sportsConfig = {
  racing: {
    horseracing: { name: 'horseracing', path: 'horse-racing', id: '21', specialsClassIds: '227' },
    greyhound: { name: 'greyhoundracing', path: 'greyhound-racing', id: '19', specialsClassIds: '201' },
    virtualMotorsports: { id: '39', specialsClassIds: '288' },
    virtualCycling: { id: '39', specialsClassIds: '290' },
    virtualHorseRacing: { id: '39', specialsClassIds: '285' },
    virtualGreyhound: { id: '39', specialsClassIds: '286' }
  },
  virtuals: [{ path: 'virtual-sport', id: '39' }],
  currentMatches: [
    { name: 'International', id: '115' },
    { name: 'UEFA Club Comps', id: '165' },
    { name: 'England', id: '97' },
    { name: 'Scotland', id: '158' },
    { name: 'Spain', id: '166' },
    { name: 'Italy', id: '120' },
    { name: 'Germany', id: '105' },
    { name: 'France', id: '102' },
    { name: 'Netherlands', id: '140' },
    { name: 'USA', id: '176' },
    { name: 'A-Z', id: 'ALL' }
  ],
  footballCoupons: {
    idsToIntersect: [206, 268, 240, 192, 249, 223, 193, 212],
    typeIds: '442,25230,25231,25232,696,678,435,440,441,437,434,438,971,975,967,472,468,734,728,735,500,501,504,929,927,930,928,823,1024'
  },
  footballId: '16',
  categoryIds: ['1', '9', '32', '10', '13', '22', '6', '31', '30', '18', '5', '16', '36', '34'],
  tierOne: ['34', '16', '6'],
  unhandledSportsForMTA: ['16', '18', '34', '39'],
  sortCodesForMTA: ['HL', 'WH', 'MH'],
  golfSport: 'golf',
  golfId: '18',
  currentSetMarketNames: ['Current Set Winner', 'Set X Winner'],
  defaultMarkets: [
    { sportIds: ['16', '10', '32', '13', '31', '30', '36', '34'], name: 'Match Result'},
    { sportIds: ['1', '5', '6', '22'], name: 'Money Line'},
    { sportIds: ['9'], name: 'Fight Betting'},
    { sportIds: ['18'], name: '2 Ball Betting'}
  ],
  specialMarkets: ['#Yourcall', '#GetAPrice Specials', 'Smart Boosts', 'Price Boost', 'Player Specials'],
  specialTagCode: 'EVFLAG_SP'
};
