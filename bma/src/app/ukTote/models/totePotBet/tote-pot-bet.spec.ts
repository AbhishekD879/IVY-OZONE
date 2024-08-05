import { TotePotBet } from '@uktote/models/totePotBet/tote-pot-bet';
import { UK_TOTE_CONFIG } from '../../constants/uk-tote-config.contant';

describe('TotePotBet', () => {
  let ukToteService;
  let pool;
  let events;
  let totePotBet;

  function fillAllLegs() {
    totePotBet.legs[3].selectOutcome('sel_12');
    totePotBet.legs[0].selectOutcome('sel_42');
    totePotBet.legs[1].selectOutcome('sel_22');
    totePotBet.legs[2].selectOutcome('sel_32');
  }

  beforeEach(() => {
    pool = {
      id: '123456',
      type: 'UQDP',
      isActive: true,
      marketIds: ['mkt_4', 'mkt_2', 'mkt_3', 'mkt_1']
    };
    events = [
      {
        eventStatusCode: 'A',
        markets: [
          {
            id: 'mkt_1',
            linkedMarketId: 'linkedMarketId_1',
            outcomes: [
              { id: 'sel_11' },
              { id: 'sel_12' }
            ]
          }
        ]
      },
      {
        eventStatusCode: 'A',
        markets: [
          {
            id: 'mkt_2',
            linkedMarketId: 'linkedMarketId_2',
            outcomes: [
              { id: 'sel_21' },
              { id: 'sel_22' }
            ]
          }
        ]
      },
      {
        eventStatusCode: 'A',
        markets: [
          {
            id: 'mkt_3',
            linkedMarketId: 'linkedMarketId_3',
            outcomes: [
              { id: 'sel_31' },
              { id: 'sel_32' }
            ]
          }
        ]
      },
      {
        eventStatusCode: 'A',
        markets: [
          {
            id: 'mkt_4',
            linkedMarketId: 'linkedMarketId_4',
            outcomes: [
              { id: 'sel_41' },
              { id: 'sel_42' },
              { id: 'sel_43' },
              { id: 'sel_44' },
              { id: 'sel_45' }
            ]
          }
        ]
      }
    ];

    ukToteService = {
      sortOutcomes: jasmine.createSpy().and.callFake(x => x),
      getRaceTitle: jasmine.createSpy().and.returnValue('race title'),
      isOutcomeSuspended: jasmine.createSpy().and.returnValue(false)
    };

    totePotBet = new TotePotBet(pool, events, UK_TOTE_CONFIG, ukToteService);
  });

  it('should init component', () => {
    expect(totePotBet).toBeTruthy();
    const sortedLegsIds = totePotBet.legs.map(x => x.linkedMarketId).join(',');
    expect(sortedLegsIds).toEqual('linkedMarketId_4,linkedMarketId_2,linkedMarketId_3,linkedMarketId_1');
  });

  describe('numberOfLines', () => {
    it('should return 1 if nothing selected', () => {
      expect(totePotBet.numberOfLines).toEqual(1);
    });
    it('should return correct number of lines for selected Outcomes', () => {
      totePotBet.legs[0].selectOutcome('sel_41');
      totePotBet.legs[0].selectOutcome('sel_42');
      totePotBet.legs[0].selectOutcome('sel_43');
      totePotBet.legs[3].selectOutcome('sel_11');
      totePotBet.legs[3].selectOutcome('sel_12');
      expect(totePotBet.numberOfLines).toEqual(6);
    });
  });

  describe('updateBetStatus', () => {
    it('should set isSuspended to false if pool is not suspended and all ' +
      'legs aren`t suspended', () => {
      totePotBet.legs[0].isSuspended = true;
      totePotBet.updateBetStatus();
      expect(totePotBet.isSuspended).toBeFalsy();
    });
    it('should set isSuspended to true if pool is suspended', () => {
      totePotBet.pool.isActive = false;
      totePotBet.updateBetStatus();
      expect(totePotBet.isSuspended).toBeTruthy();
    });
    it('should set isSuspended to true if pool is active but all legs are suspended', () => {
      totePotBet.legs.forEach(leg => leg.isSuspended = true);
      totePotBet.updateBetStatus();
      expect(totePotBet.isSuspended).toBeTruthy();
    });
  });

  describe('checkIfSomeLegFilled', () => {
    it('should false if no legs filled', () => {
      expect(totePotBet.checkIfSomeLegFilled()).toBeFalsy();
    });
    it('should return true if at least one leg filled', () => {
      totePotBet.legs[3].selectOutcome('sel_12');
      expect(totePotBet.checkIfSomeLegFilled()).toBeTruthy();
    });
  });

  describe('checkIfAllLegsFilled', () => {
    it('should false if not all legs filled', () => {
      totePotBet.legs[3].selectOutcome('sel_12');
      expect(totePotBet.checkIfAllLegsFilled()).toBeFalsy();
    });
    it('should should true if not all legs filled', () => {
      fillAllLegs();
      expect(totePotBet.checkIfAllLegsFilled()).toBeTruthy();
    });
  });

  it('clear should deselect all outcomes', () => {
    fillAllLegs();
    expect(totePotBet.checkIfAllLegsFilled()).toBeTruthy();
    totePotBet.clear();
    expect(totePotBet.checkIfSomeLegFilled()).toBeFalsy();
  });

  it('getBetObject should return bet object to pass into Bet Placement API', () => {
    fillAllLegs();

    expect(totePotBet.getBetObject(12.4)).toEqual({
      poolType: 'UQDP',
      stakePerLine: 12.4,
      betNo: 159,
      poolItem: [
        {
          outcome: 'sel_42',
          poolId: '123456'
        },
        {
          outcome: 'sel_22',
          poolId: '123456'
        },
        {
          outcome: 'sel_32',
          poolId: '123456'
        },
        {
          outcome: 'sel_12',
          poolId: '123456'
        }
      ]
    } as any);
  });

  it('generateToteBetDetails should generate bet object to be used on Betslip', () => {
    fillAllLegs();
    expect(totePotBet.generateToteBetDetails('some restrictions' as any)).toEqual({
      poolName: 'Quadpot Totepool',
      numberOfLines: 1,
      stakeRestrictions: 'some restrictions',
      orderedLegs: [
        {
          name: 'Leg 1',
          eventTitle: 'race title',
          outcomes: [
            {
              id: 'sel_42'
            }
          ],
          event: {
            eventStatusCode: 'A',
            markets: [
              {
                id: 'mkt_4',
                linkedMarketId: 'linkedMarketId_4',
                outcomes: [
                  {
                    id: 'sel_41'
                  },
                  {
                    id: 'sel_42'
                  },
                  {
                    id: 'sel_43'
                  },
                  {
                    id: 'sel_44'
                  },
                  {
                    id: 'sel_45'
                  }
                ]
              }
            ]
          }
        },
        {
          name: 'Leg 2',
          eventTitle: 'race title',
          outcomes: [
            {
              id: 'sel_22'
            }
          ],
          event: {
            eventStatusCode: 'A',
            markets: [
              {
                id: 'mkt_2',
                linkedMarketId: 'linkedMarketId_2',
                outcomes: [
                  {
                    id: 'sel_21'
                  },
                  {
                    id: 'sel_22'
                  }
                ]
              }
            ]
          }
        },
        {
          name: 'Leg 3',
          eventTitle: 'race title',
          outcomes: [
            {
              id: 'sel_32'
            }
          ],
          event: {
            eventStatusCode: 'A',
            markets: [
              {
                id: 'mkt_3',
                linkedMarketId: 'linkedMarketId_3',
                outcomes: [
                  {
                    id: 'sel_31'
                  },
                  {
                    id: 'sel_32'
                  }
                ]
              }
            ]
          }
        },
        {
          name: 'Leg 4',
          eventTitle: 'race title',
          outcomes: [
            {
              id: 'sel_12'
            }
          ],
          event: {
            eventStatusCode: 'A',
            markets: [
              {
                id: 'mkt_1',
                linkedMarketId: 'linkedMarketId_1',
                outcomes: [
                  {
                    id: 'sel_11'
                  },
                  {
                    id: 'sel_12'
                  }
                ]
              }
            ]
          }
        }
      ]
    });
  });

  it('getOutcomeLinkedLeg should return leg addicted to provided selection', () => {
    const linkedLeg = totePotBet.getOutcomeLinkedLeg({ id: 'sel_11' } as any);
    expect(linkedLeg.name).toEqual('Leg 4');
    expect(linkedLeg.linkedMarketId).toEqual('linkedMarketId_1');
    expect(linkedLeg.marketId).toEqual('mkt_1');
  });
});
