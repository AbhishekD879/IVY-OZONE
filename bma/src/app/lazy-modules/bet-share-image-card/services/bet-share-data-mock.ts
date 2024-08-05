export const POOLS_DATA = {
  betData: {
    leg: [{
      orderedOutcomes: [{ name: 'test', isFavourite: true, runnerNumber: 'race1' }]
    }],
    legs:[{adjustedResult: 'test'}],
    getRaceTitle:()=>{return 'test'},
    toteMarketTitle: 'Placepot7',
    status: 'lost',
    totalStake: '$11',
    totalReturns: '$1',
    date: '12-11-2023',
    betTitle: 'pools',
    id:'123',
    settled: 'Y'
  }
};

export const SHARE_DATA = [{
  selectionName: 'test selection', marketName: 'test market', odds: '2/3', eventStartTime: '12 Jan2022',
  eventName: 'test event', lotteryDrawResults: [{}]
}];
SHARE_DATA['betType'] = 'BUILD YOUR BET';
SHARE_DATA['stake'] = '$0.1';
SHARE_DATA['returns'] = '$0.111';
SHARE_DATA['betFullDate'] = 'Jan2018,19';

export const EVENT_SOURCE = {    
  bybType: 'regular',
  leg: [{
    backupEventEntity: { id: '123' },
    part: [{ outcome: '123' }],
    cashoutId: '12345'
  }],
  id: '123',
  raceNumberTitle: 'race1',
  toteMarketTitle: 'Placepot',
  totalStatus: 'won',
  status: 'won',
  stake: '$11',
  potentialPayout: '$1',
  date: '12-11-2023',
  settled: 'Y',
  betId: '123'
}

export const REGULAR_BET_DATA = {
    eventSource: EVENT_SOURCE,
    id: '123',
    bets: {id:'123'}
};

export const REGULAR_SHARE_DATA = {
  betData:{
  eventSource: {...EVENT_SOURCE},
    id: '123'
  },
  bets: [{eventSource:{...EVENT_SOURCE} }],
  sportType: 'regularBets'
  };

  export const REGULAR_BET_CATEGORY_ID = {
    betData:{
      bybType:'',
      eventSource: {    
        bybType: 'regular',
        leg: [{
          backupEventEntity: { id: '123' },
          part: [{ outcome: {eventCategory:{id:'21',name:'test'}}}],
          cashoutId: '12345'
        }],
        id: '123',
        raceNumberTitle: 'race1',
        toteMarketTitle: 'Placepot',
        totalStatus: 'won',
        status: 'won',
        stake: '$11',
        potentialPayout: '$1',
        date: '12-11-2023',
        settled: 'Y',
        betId: '123'
      },
        id: '123'
      },
      bets: [{eventSource:{    
        leg: [{
          backupEventEntity: { id: '123' },
          part: [{ outcome: '123' }],
          cashoutId: '12345'
        }],
        id: '123',
        raceNumberTitle: 'race1',
        toteMarketTitle: 'Placepot',
        totalStatus: 'won',
        status: 'won',
        stake: '$11',
        potentialPayout: 'N/A',
        date: '12-11-2023',
        settled: 'Y',
        betId: '123',
        betType: 'pools'
      } }],
      sportType: 'regularBets'
  }

  export const REGULAR_SHARE_5ASIDE_CATEGORY = {
    betData:{
      bybType:'5-A-Side',
      eventSource: {    
        bybType: 'regular',
        leg: [{
          backupEventEntity: { id: '123' },
          part: [{ outcome: {eventCategory:{id:'55555',name:'test'}}}],
          cashoutId: '12345'
        }],
        id: '123',
        raceNumberTitle: 'race1',
        toteMarketTitle: 'Placepot',
        totalStatus: 'won',
        status: 'won',
        stake: '$11',
        potentialPayout: '$1',
        date: '12-11-2023',
        settled: 'Y',
        betId: '123'
      },
        id: '123'
      },
      bets: [{eventSource:{    
        bybType: 'regular',
        leg: [{
          backupEventEntity: { id: '123' },
          part: [{ outcome: '123' }],
          cashoutId: '12345'
        }],
        id: '123',
        raceNumberTitle: 'race1',
        toteMarketTitle: 'Placepot',
        totalStatus: 'won',
        status: 'won',
        stake: '$11',
        potentialPayout: '$1',
        date: '12-11-2023',
        settled: 'Y',
        betId: '123'
      } }],
      sportType: 'regularBets'
  }

  export const REGULAR_SHARE_CATEGORY_DATA = {
    betData:{
      bybType:'',
      eventSource: {    
        bybType: 'regular',
        leg: [{
          backupEventEntity: { id: '123' },
          part: [{ outcome: { id: '123'}}],
          cashoutId: '12345'
        }],
        id: '123',
        raceNumberTitle: 'race1',
        toteMarketTitle: 'Placepot',
        totalStatus: 'won',
        status: 'won',
        stake: '$11',
        potentialPayout: '$1',
        date: '12-11-2023',
        settled: 'Y',
        betId: '123'
      },
        id: '123'
      },
      bets: [{eventSource:{    
        bybType: 'regular',
        leg: [{
          backupEventEntity: { id: '123' },
          part: [{ outcome: '123' }],
          cashoutId: '12345'
        }],
        id: '123',
        raceNumberTitle: 'race1',
        toteMarketTitle: 'Placepot',
        totalStatus: 'won',
        status: 'won',
        stake: '$11',
        potentialPayout: '$1',
        date: '12-11-2023',
        settled: 'Y',
        betId: '123'
      } }],
      sportType: 'regularBets'
  }

export const LOTTO_BET_DATA = {
  betData: {
    balls: [{ ballNo: '11' }], drawName: 'test draw',
    lotteryResults: [{ drawAt: '12-3-2023' }],
    name: 'test name', status: 'settled', betDate: '1-11-2020',
    stake: '$12', totalReturns: '$1',isSettled: 'N'
  }
}

export const imgObject = new Image();
imgObject.crossOrigin="anonymous";
imgObject.src ="https://scmedia.itsfogo.com/$-$/5539b5e8d1cc4b6595ea27657d46ce3f.jpg";

export const BET_SHARE_IMG_DATA = [{line1:'test',line2:'test data',
line3:'test line',eventName:'test event',selectionName:'test selection',selectionOutcomes:['test slection outcomes']
,marketName:'BUILD YOUR BET',selectionHeaderName:'jackPot',lotteryDrawResults: [{drawLineName:'test line'}]}];

BET_SHARE_IMG_DATA['betFullDate'] = '12-11-2023';
BET_SHARE_IMG_DATA['betFullDateTime'] = '1-2-13';
BET_SHARE_IMG_DATA['stake'] = '$22';
BET_SHARE_IMG_DATA['returns'] = '$33';
BET_SHARE_IMG_DATA['betType'] = 'Bet Builder';
BET_SHARE_IMG_DATA['imageObj'] = imgObject;
BET_SHARE_IMG_DATA['betId'] = '12345';

export const USER_PREF_FLAGS = {
  oddsFlag:true,
  stakeFlag: true,
  returnsFlag: true,
  selectionNameFlag: true,
  eventNameFlag: true,
  dateFlag: true
}

export const USER_PREFERENCES = [{"name":"Total Returns","isSelected":false},
{"name":"Stake","isSelected":true},
{"name":"Odds","isSelected":true},
{"name":"Selection Name","isSelected":true},
{"name":"Event Name","isSelected":true},
{"name":"Bet Placed Date","isSelected":true}]


export const CMS_DATA ={  popUpDesc:'test desc',
                          genericSharingLink:'https://sports.coral.co.uk',
                          horseRacingUrl:"https://scmedia.itsfogo.com/$-$/5539b5e8d1cc4b6595ea27657d46ce3f.jpg",
                          footBallUrl:"https://scmedia.itsfogo.com/$-$/5539b5e8d1cc4b6595ea27657d46ce3f.jpg",
                          openBetsGenericUrl:"https://scmedia.itsfogo.com/$-$/5539b5e8d1cc4b6595ea27657d46ce3f.jpg",
                          url5ASide:'https://scmedia.itsfogo.com/$-$/5539b5e8d1cc4b6595ea27657d46ce3f.jpg',
                          settledBetsGenericUrl:"https://scmedia.itsfogo.com/$-$/5539b5e8d1cc4b6595ea27657d46ce3f.jpg",
                           extensionUrl:"https://scmedia.itsfogo.com/$-$/5539b5e8d1cc4b6595ea27657d46ce3f.jpg",
                          beGambleAwareLogoUrl:"https://scmedia.itsfogo.com/$-$/9ec4377d22a7465e952b051023d79fa2.jpg",
                           brandLogoUrl:"https://scmedia.itsfogo.com/$-$/7f10c18c8ae340a9b08219809b3ccd21.svg",
                          cashedOutBetControl: USER_PREFERENCES, wonBetControl:USER_PREFERENCES,
                          lostBetControl: USER_PREFERENCES, openBetControl: USER_PREFERENCES,
                          cashedOutBetsShareCardMessage: 'CHECK ${BetType}',
                          wonBetShareCardMessage: 'Won ${TPR} on ${BetType}', lostBetsShareCardMessage:'Lost ${TPR} on ${BetType}',
                          openBetShareCardMessage: 'CHECK ${BetType}', openBetShareCardSecondMessage: 'CHECK SHARE'

}
