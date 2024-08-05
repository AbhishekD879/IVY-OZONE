import { RacingPostTipService } from '@lazy-modules/racingPostTip/service/racing-post-tip.service';
import { mostRacingTipsMock } from '@lazy-modules/racingPostTip/mock/racing-pot-tip-mock';
import { pubSubApi } from '@app/core/services/communication/pubsub/pubsub-api.constant';

describe('RacingPostApiService', () => {
  let service: RacingPostTipService;
 let pubSubService;

  const mock = {
    location: 'Bet Receipt',
    module: 'RP Tip',
    dimension86: 0,
    dimension87: 0,
    dimension88: null
  } as any;
  beforeEach(() => {
    pubSubService = {
      publish: jasmine.createSpy('publish'),
      publishSync: jasmine.createSpy('publishSync'),
      subscribe: jasmine.createSpy('subscribe'),
      API: pubSubApi
    };
    service = new RacingPostTipService(pubSubService);
  });

  it('get racingPostGTM', () => {
    service['_racingPostGTM'] = mock;
    expect(service.racingPostGTM).toEqual(mock);
  });

  it('set racingPostGTM', () => {
    service.racingPostGTM = mock as any;
    expect(service['_racingPostGTM']).toBe(mock);
  });

  it('set raceData', () => {
    const data = [];
    service.updateRaceData(data);
    expect(service.raceData).toEqual([]);
  });

  describe('#getMostTipThroughMainBet', () => {
    it('should getMostTipThroughMainBet filterd races', () => {
      service['categoryId'] = '21';
      const showReceipt = true;
      const mainBetReceipt = true;
      const mainBetReceipts =  [
        {
          betId: '123',
          eventMarket: 'Match Result',
          leg: [
            {
              part: [{ event: { id: 1, categoryId: '21' }, marketId: '123123' }],
              odds: {
                frac: '5/2',
                dec: '3.50',
              }
            }
          ]
        }
      ] as any;

      const events = [
        {
          name: 'horse race',
          id: 1,
          categoryId: '21',
          horses: [
            {horseName:'a', isMostTipped: true, runnerNumber: '1' },
            { horseName:'b', isMostTipped: false, runnerNumber: '2' },
          ],
        },
        {
          name: 'horse race',
          id: 2,
          categoryId: '21',
          horses: [
            {horseName:'a', isMostTipped: true, runnerNumber: '1' },
            {horseName:'b', isMostTipped: false, runnerNumber: '2' },
          ],
        },
      ] as any;
      service['getOutComeAndTip'] = jasmine.createSpy('getOutComeAndTip');
      service.getMostTipThroughMainBet(events, mainBetReceipts, showReceipt, mainBetReceipt);
      expect(service['categoryId']).toEqual(mainBetReceipts[0].leg[0].part[0].event.categoryId);
     });
  });

  describe('#getMostTipThroughMainBet inner else condition', () => {
    it('should getMostTipThroughMainBet filterd races else', () => {
      service['categoryId'] = '16';
      const showReceipt = true;
      const mainBetReceipt = true;
      const mainBetReceipts =  [
        {
          betId: '123',
          eventMarket: 'Match Result',
          leg: [
            {
              part: [{ event: { id: 1, categoryId: '99' }, marketId: '123123' }],
              odds: {
                frac: '5/2',
                dec: '3.50',
              }
            }
          ]
        }
      ] as any;

      const events = [
        {
          name: 'horse race',
          id: 1,
          categoryId: '21',
          horses: [
            {horseName:'a', isMostTipped: true, runnerNumber: '1' },
            { horseName:'b', isMostTipped: false, runnerNumber: '2' },
          ],
        },
        {
          name: 'horse race',
          id: 2,
          categoryId: '21',
          horses: [
            { horseName:'a',isMostTipped: true, runnerNumber: '1' },
            { horseName:'b', isMostTipped: false, runnerNumber: '2' },
          ],
        },
      ] as any;
      service['getOutComeAndTip'] = jasmine.createSpy('getOutComeAndTip');
      service.getMostTipThroughMainBet(events, mainBetReceipts, showReceipt, mainBetReceipt);
      expect(service['categoryId']).not.toEqual(mainBetReceipts[0].leg[0].part[0].event.categoryId);
     });
  });


  describe('#getMostTipThroughQuickBet', () => {
    it('should getMostTipThroughQuickBet filterd races if', () => {
      service['categoryId'] = '21';
      const showReceipt = true;
      const showquickBetReceipt = true;
      const quickBetReceipt = {
         categoryId:'21',
         eventId:1
        }as any;

      const events = [
        {
          name: 'horse race',
          id: 1,
          categoryId: '21',
          horses: [
            { isMostTipped: true, runnerNumber: '1' },
            { isMostTipped: false, runnerNumber: '2' },
          ],
        },
        {
          name: 'horse race',
          id: 2,
          categoryId: '21',
          horses: [
            {horseName:'a', isMostTipped: true, runnerNumber: '1' },
            {horseName:'b', isMostTipped: false, runnerNumber: '2' },
          ],
        },
      ] as any;
      service['getOutComeAndTip'] = jasmine.createSpy('getOutComeAndTip');
      service.getMostTipThroughQuickBet(events, quickBetReceipt, showReceipt, showquickBetReceipt);
      expect(service['categoryId']).toEqual(quickBetReceipt.categoryId);
     });
  });

  describe('#getMostTipThroughQuickBet', () => {
    it('should getMostTipThroughQuickBet filterd races else', () => {
      service['categoryId'] = '21';
      const showReceipt = true;
      const showquickBetReceipt = true;
      const quickBetReceipt = {
         categoryId:'23',
         eventId:1
        } as any;

      const events = [
        {
          name: 'horse race',
          id: 1,
          categoryId: '21',
          horses: [
            {horseName:'a', isMostTipped: true, runnerNumber: '1' },
            {horseName:'b', isMostTipped: false, runnerNumber: '2' },
          ],
        },
        {
          name: 'horse race',
          id: 2,
          categoryId: '21',
          horses: [
            { horseName:'a', isMostTipped: true, runnerNumber: '1' },
            { horseName:'b', isMostTipped: false, runnerNumber: '2' },
          ],
        },
      ] as any;
      service['getOutComeAndTip'] = jasmine.createSpy('getOutComeAndTip');
      service.getMostTipThroughQuickBet(events, quickBetReceipt, showReceipt, showquickBetReceipt);
      expect(service['categoryId']).not.toEqual(quickBetReceipt.categoryId);
     });
  });

  describe('setFilteredRaceEvents', () => {
    it('when horses array is present', () => {
      const showReceipt = true;
      const isReciptPresent = true;
      service['getOutComeAndTip'] = jasmine.createSpy('getOutComeAndTip');
      const events = [
        {
          name: 'horse race',
          id: 1,
          categoryId: '21',
          horses: [
            {horseName:'a', isMostTipped: true, runnerNumber: '1' },
            { horseName:'b', isMostTipped: false, runnerNumber: '2' },
          ],
        },
        {
          name: 'horse race',
          id: 2,
          categoryId: '21',
          horses: [
            {horseName:'a', isMostTipped: true, runnerNumber: '1' },
            {horseName:'b', isMostTipped: false, runnerNumber: '2' },
          ],
        },
      ] as any;
      service['setFilteredRaceEvents'](events, 1, showReceipt, isReciptPresent);
      expect(pubSubService.publish).not.toHaveBeenCalled();
    });
    it('when horses array is not present', () => {
      const showReceipt = true;
      const isReciptPresent = true;
      const events = [
        {
          name: 'horse race',
          id: 1,
          categoryId: '21',
          horses: [],
        },
        {
          name: 'horse race',
          id: 2,
          categoryId: '21',
          horses: [],
        },
      ] as any;
      service['getOutComeAndTip'] = jasmine.createSpy('getOutComeAndTip');
      service['setFilteredRaceEvents'](events, 1, showReceipt, isReciptPresent);
      expect(pubSubService.publish).toHaveBeenCalled();
    });
    it('when horses array is present but showReceipt is false', () => {
      const showReceipt = false;
      const isReciptPresent = true;
      service['getOutComeAndTip'] = jasmine.createSpy('getOutComeAndTip');
      service['setFilteredRaceEvents'](mostRacingTipsMock as any, 1, showReceipt, isReciptPresent);
      expect(pubSubService.publish).toHaveBeenCalled();
    });
    it('when horses array is present but recipt is false', () => {
      const showReceipt = false;
      const isReciptPresent = false;
      service['getOutComeAndTip'] = jasmine.createSpy('getOutComeAndTip');
      service['setFilteredRaceEvents'](mostRacingTipsMock as any, 1, showReceipt, isReciptPresent);
      expect(pubSubService.publish).toHaveBeenCalled();
    });
    it('when horses array is present but isReciptPresent is false', () => {
      const showReceipt = true;
      const isReciptPresent = false;
      service['getOutComeAndTip'] = jasmine.createSpy('getOutComeAndTip');
      service['setFilteredRaceEvents'](mostRacingTipsMock as any, 1, showReceipt, isReciptPresent);
      expect(pubSubService.publish).toHaveBeenCalled();
    });
  });
  describe('#getOutComeAndTip ', () => {
    it('should push horses if mosttipped is true', () => {
      service['mostTippedHorseEvents'] = [];
      service['getRunner'] = jasmine.createSpy('getRunner');
      const race = mostRacingTipsMock[0] as any;
      service['getOutComeAndTip'](race);
      expect(service['mostTippedHorseEvents'].length).not.toBe(0);
    });
    it('should check the scenario for false case', () => {
      service['mostTippedHorseEvents'] = [];
      const race = {
        horses: []
      } as any;
      service['getOutComeAndTip'](race);
      service['getRunner'] = jasmine.createSpy('getRunner');
      expect(service['mostTippedHorseEvents'].length).toBe(0);
    });
    it('Inner else power horse', () => {
      service['mostTippedHorseEvents'] = [];
      service['getRunner'] = jasmine.createSpy('getRunner');
      const race = {
        horses: [{isMostTipped: false}]
      } as any;
      service['getOutComeAndTip'](race);
      expect(service['mostTippedHorseEvents'].length).toBe(0);
    });
    it('More than one horses power', () => {
      service['getRunner'] = jasmine.createSpy('getRunner');
      service['mostTippedHorseEvents'] = [];
      const race = {
        markets: [{
          children: [
            {
              outcome: {
                displayOrder: 1,
                icon: false,
                id: '125825053',
                name: 'a',
                runnerNumber: '2',
                silkName: '123.png',
                prices: [{
                  priceNum: '9',
                  priceDen: '2'
                }
                ]
              }
            },
            {
              outcome: {
                displayOrder: 1,
                icon: false,
                id: '125825053',
                name: 'b',
                silkName: '123.png',
                runnerNumber: '5',
                prices: [{
                  priceNum: '9',
                  priceDen: '2'
                }
                ]
              }
            },
            {
              outcome: {
                displayOrder: 3,
                icon: false,
                id: '125825053',
                name: 'c',
                silkName: '123.png',
                runnerNumber: '1',
                prices: [{
                  priceNum: '9',
                  priceDen: '2'
                }
                ]
              }
            }
          ],
        }],
        horses: [{ horseName: 'a', isMostTipped: true, runnerNumber: '' }, { horseName: 'b', isMostTipped: true, runnerNumber: '' },
        { horseName: 'c', isMostTipped: true, runnerNumber: '' }]
      } as any;
      service['getOutComeAndTip'](race);
      expect(service['getRunner']).toHaveBeenCalled();
      expect(service['mostTippedHorseEvents'].length).not.toBe(0);
    });
  });

  it('getRunner', () => {
    const horse = {
      horseName: 'a'
    } as any;
    const race = [
      {
        outcome: {
          displayOrder: 1,
          icon: false,
          id: '125825053',
          name: 'a',
          runnerNumber: '2',
          silkName: '123.png',
          prices: [{
            priceNum: '9',
            priceDen: '2'
          }
          ]
        }
      },
      {
        outcome: {
          displayOrder: 1,
          icon: false,
          id: '125825053',
          name: 'b',
          silkName: '123.png',
          runnerNumber: '5',
          prices: [{
            priceNum: '9',
            priceDen: '2'
          }
          ]
        }
      },
      {
        outcome: {
          displayOrder: 3,
          icon: false,
          id: '125825053',
          name: 'c',
          silkName: '123.png',
          runnerNumber: '1',
          prices: [{
            priceNum: '9',
            priceDen: '2'
          }]
        }
      }
     ] as any;
    expect(service['getRunner'](horse, race)).toBeDefined();
  });

  it('#getRunner when horse name not matches', () => {
    const horse = {
      horseName: 'b'
    } as any;
    const race = [];
    expect(service['getRunner'](horse, race)).toBe('');
  });
});
