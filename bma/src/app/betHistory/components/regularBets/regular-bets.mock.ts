export const regularBets = {
    config: {
        enabled: true,
        infoText: 'your bet has been void as one or more players were not selected.Please go to 5-A-Side to place your bet again',
        gotoFiveASideText: 'Please go to your 5-A-Side to update your bet'
      },

      config1: {
        enabled: true,
        infoText: 'welcome',
        gotoFiveASideText: 'Please'
    },
    config2: {
      enabled: true,
      infoText: `Look below to find out what other markets are available Look below to find out what other markets hie
       Look below to find out what other markets hie Look below to find out what other markets hie Look below to
       find out what other markets hie`,
      gotoFiveASideText: 'Please go to your 5-A-Side to update your bet. Please go to your 5-A-Side to update your bet'
    },

  eventStartTime: {
    eventSource: {
      leg: [{
        part: [{
          outcome: [{
            event: {
              startTime: new Date().getTime() + (11 * 60 * 1000)
            }
          }]
        }]
      }]
    }
  },

  eventStartTime2: {
    eventSource: {
      leg: [{
        part: [{
          outcome: [{
            event: { startTime: '2020-12-21T17:30:00' }
          }]
        }]
      }]
    }
  }
};

export const contestBets = [{
  eventSource: {
    event: ['123456'],
    betId: '2379097305',
    source: 'f',
    contestId: '60eb075772149d6475386619',
    leg: [{ part: [{ outcome: [{}] }] }]
  },
  footballAlertsVisible: false,
  optaDisclaimerAvailable: true
},
{
  eventSource: {
    event: ['12345655464'],
    betId: '2379096729',
    source: 'f',
    contestId: 'NA',
    leg: [{ part: [{ outcome: [{}] }] }],
  },
  footballAlertsVisible: false
}];

export const initialBets = [
  {
    eventSource: {
      event: ['123456'],
      betId: '2379097305',
      source: 'f',
      leg: [{ part: [{ outcome: [{}] }] }]
    }
  },
  {
    eventSource: {
      event: ['12345655464'],
      betId: '2379096729',
      source: 'f',
      leg: [{ part: [{ outcome: [{}] }] }]
    }
  }
];
