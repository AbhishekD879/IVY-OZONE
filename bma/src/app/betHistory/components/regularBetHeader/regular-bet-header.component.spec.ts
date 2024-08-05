import { RegularBetHeaderComponent } from './regular-bet-header.component';

describe('RegularBetHeaderComponent', () => {
  let component: RegularBetHeaderComponent;
  let locale;
  let editMyAccaService;
  let timeService;
  let serviceClosureService;
  let casinoMyBetsIntegratedService;

  beforeEach(() => {
    timeService = {
      formatByPattern: jasmine.createSpy('formatByPattern').and.returnValue('formatted time')
    };
    locale = {
      getString: jasmine.createSpy()
    };
    editMyAccaService = {
      EMAEnabled: true,
      isBetOpen: jasmine.createSpy('isBetOpen').and.returnValue(true),
      canEditBet: jasmine.createSpy('canEditBet').and.returnValue(true),
    };

    serviceClosureService = {
      userServiceClosureOrPlayBreak: false
    };

    casinoMyBetsIntegratedService = {};

    component = new RegularBetHeaderComponent(
      locale,
      editMyAccaService,
      timeService,
      serviceClosureService,
      casinoMyBetsIntegratedService
    );
  });

  it('constructor', () => {
    expect(component).toBeTruthy();
  });

  describe('ngOnInit', () => {
    it(`should define fullBetType`, () => {
      locale.getString.and.returnValue('localeString');
      component.bet = {
        eventSource: {
          betType: 'betType',
          betTags :{
            betTag:[
              {
                "tagName": "LDIPx",
                "tagValue": ""
            
            }]
          }
        }
      };

      component.ngOnInit();

      expect(component.fullBetType).toEqual('localeString');
    });

    it('should set acca time to empty string', () => {
      expect(component.accaTime).toEqual('');
      component.bet = {
        eventSource: {
          betTags :{
            betTag:[
              {
                "tagName": "LDIPx",
                "tagValue": ""
            
            }]
          }
        }
      };
      component.ngOnInit();
      expect(component.accaTime).toEqual('');
    });

    it('should set acca time', () => {
      component.bet = {
        eventSource: {
          accaHistory: {
            time: ''
          },betType: 'betType',
          betTags :{
            betTag:[
              {
                "tagName": "LDIPx",
                "tagValue": ""
            
            }]
          }
        }
      };
      component.ngOnInit();
      expect(component.accaTime).toEqual('formatted time');
    });
  });

  describe('isLdipBetTag', () =>{
    it('should return value if LDIP tag is available', () =>{
      const bet = { eventSource: { betTags:{ betTag: [{tagName: 'LDIP'}]} }};
      const result = component.isLdipBetTag(bet);
      expect(result).toBeTruthy();
    });
    it('should return value if LDIP tag is not available', () =>{
      const bet = { eventSource: {}};
      const result = component.isLdipBetTag(bet);
      expect(result).toBeFalsy();
    });
    it('should return value if eventSource tag is not available', () =>{
      const bet = {};
      const result = component.isLdipBetTag(bet);
      expect(result).toBeFalsy();
    });
  })

  describe('getFullBetType', () => {
    it('should return bybType', () => {
      component.bet = { eventSource: { bybType: 'Build Your Bet' } ,  betTags :{
        betTag:[
          {
            "tagName": "LDIPx",
            "tagValue": ""
        
        }]
      }};
      expect(component.getFullBetType()).toEqual(component.bet.eventSource.bybType);
    });

    it('should get string by betType code', () => {
      component.bet = { eventSource: { betType: 'SGL' } ,
      betTags :{
        betTag:[
          {
            "tagName": "xxx",
            "tagValue": ""
        
        }]
      }};
      component.getFullBetType();
      expect(locale.getString).toHaveBeenCalledWith(`bethistory.betTypes.${component.bet.eventSource.betType}`);
    });

    it('should return bet type as luckydip', () => {
      component.bet = { eventSource: { betType: 'Luckydip', betTags :{
        betTag:[
          {
            "tagName": "LDIP",
            "tagValue": ""
        }]
      }}};
      component.getFullBetType();
      expect(locale.getString).toHaveBeenCalledWith('lucky Dip');
    });
  });

  it('isEMAEnabled', () => {
    expect(component.isEMAEnabled).toEqual(true);
  });

  it('showEditAccaButton', () => {
    editMyAccaService.canEditBet = () => true;
    component.betHistoryHeader = false;
    component.bet = {
      eventSource: {
        isPartialActive: false,
        isConfirmInProgress: false,
        inProgress: false,
        cashoutValue: '1'
      }
    };
    expect(component.showEditAccaButton()).toBeTruthy();
  });

  it('showEditAccaButton (canEditBet = false)', () => {
    editMyAccaService.canEditBet.and.returnValue(false);
    component.betHistoryHeader = false;
    component.bet = {
      eventSource: {
        isPartialActive: false,
        isConfirmInProgress: false,
        inProgress: false,
        cashoutValue: '1'
      }
    };
    expect(component.showEditAccaButton()).toBeFalsy();
  });

  it('showEditAccaButton when cashout value is not number', () => {
    editMyAccaService.canEditBet = () => true;
    component.betHistoryHeader = false;
    component.bet = {
      eventSource: {
        isPartialActive: false,
        isConfirmInProgress: false,
        inProgress: false,
        cashoutValue: 'fa'
      }
    };
    expect(component.showEditAccaButton()).toBeTruthy();
  });

  it('showEditAccaButton when cashout value is CASHOUT_SELN_NO_CASHOUT', () => {
    editMyAccaService.canEditBet = () => true;
    component.bet = {
      eventSource: {
        isPartialActive: false,
        isConfirmInProgress: false,
        inProgress: false,
        cashoutValue: 'CASHOUT_SELN_NO_CASHOUT'
      }
    };
    expect(component.showEditAccaButton()).toBeFalsy();
  });

  it('showEditAccaButton(partial cashout in progress)', () => {
    editMyAccaService.canEditBet = () => true;
    component.bet = {
      eventSource: {
        isPartialActive: true,
        isConfirmInProgress: true,
        inProgress: false
      }
    };
    expect(component.showEditAccaButton()).toBeTruthy();
  });

  it('showEditAccaButton(partial cashout in progress leg and part)', () => {
    editMyAccaService.canEditBet = () => true;
    component.bet = {
      eventSource: {
        isPartialActive: true,
        isConfirmInProgress: false,
        inProgress: false,
        leg:[{eventEntity:{categoryId :'16'},part:[{eventMarketDesc:'test'}]}]
      }
    };
    expect(component.showEditAccaButton()).toBeTruthy();
  });

  it('showEditAccaButton(cashout in progress)', () => {
    editMyAccaService.canEditBet = () => true;
    component.bet = {
      eventSource: {
        isPartialActive: false,
        isConfirmInProgress: true,
        inProgress: true
      }
    };
    expect(component.showEditAccaButton()).toBeFalsy();
  });

  it('showEditAccaButton(bet not defined)', () => {
    editMyAccaService.canEditBet = () => true;
    component.bet = undefined;
    expect(component.showEditAccaButton()).toBeFalsy();
  });

  it('showEditAccaButton(serviceclosure returns true)', () => {
    spyOn<any>(component, 'availabilityPerCashOutValue').and.returnValue(true);
    component.bet = {eventSource: {isCashOutedBetSuccess: true, isConfirmInProgress: true, isPartialActive: true,inProgress: true,
      isAccaEdit: true}};
    component.betHistoryHeader = true;
    serviceClosureService.userServiceClosureOrPlayBreak = false;
    const retVal = component.showEditAccaButton();
    expect(retVal).toBeTruthy();
  });

  describe('showStatus', () => {
    it('should return false if bet is open', () => {
      component.bet = {
        eventSource: {
          totalStatus: 'open'
        }
      };
      expect(component.showStatus).toEqual(false);
    });
    it('should return true if bet is pending', () => {
      component.bet = {
        eventSource: {
          totalStatus: 'pending'
        }
      };
      expect(component.showStatus).toEqual(false);
    });
    it('should return true if bet is not pending and open', () => {
      component.bet = {
        eventSource: {
          totalStatus: 'cashed out'
        }
      };
      expect(component.showStatus).toEqual(true);
    });
  });

  describe('showFiveASideStatus', () => {
    it('should return false if bet is void', () => {
      component.bet = {
        eventSource: {
          totalStatus: 'void'
        }
      };
      expect(component.showFiveASideStatus).toEqual(false);
    });
    it('should return true if bet is lost', () => {
      component.bet = {
        eventSource: {
          totalStatus: 'lost'
        }
      };
      expect(component.showFiveASideStatus).toEqual(true);
    });
    it('should return true  if bet is won', () => {
      component.bet = {
        eventSource: {
          totalStatus: 'won'
        }
      };
      expect(component.showFiveASideStatus).toEqual(true);
    });
  });

  describe('#hasFiveASideWidget', () => {
    it('should return false, if 1st condition is false', () => {
      component.hasLeaderboardWidget = false;
      expect(component.hasFiveASideWidget).toBe(false);
    });
    it('should return false, if 2nd condition is false', () => {
      component.hasLeaderboardWidget = true;
      component.bet = {
        eventSource: {
          source: 'A'
        }
      } as any;
      expect(component.hasFiveASideWidget).toBe(false);
    });
    it('should return false, if 3rd condition is false', () => {
      component.hasLeaderboardWidget = true;
      component.bet = {
        eventSource: {
          totalStatus: 'void',
          source: 'f'
        }
      } as any;
      expect(component.hasFiveASideWidget).toBe(false);
    });
    it('should return true, if all conditions satisfies', () => {
      component.hasLeaderboardWidget = true;
      component.bet = {
        eventSource: {
          totalStatus: 'open',
          source: 'f'
        }
      } as any;
      expect(component.hasFiveASideWidget).toBe(true);
    });
    it('should return true, if fullbet type is fiveaside won', () => {
      component.hasLeaderboardWidget = true;
      component.bet = {
        eventSource: {
          totalStatus: 'won',
          source: 'f'
        }
      } as any;
      component.fullBetType = '5-A-Side';
      expect(component.hasFiveASideWidget).toBe(true);
    });
    it('should return true, if fullbet type is fiveaside lost', () => {
      component.hasLeaderboardWidget = true;
      component.bet = {
        eventSource: {
          totalStatus: 'lost',
          source: 'f'
        }
      } as any;
      component.fullBetType = '5-A-Side';
      expect(component.hasFiveASideWidget).toBe(true);
    });
    it('should return false, if fullbet type is fiveaside void', () => {
      component.hasLeaderboardWidget = true;
      component.bet = {
        eventSource: {
          totalStatus: 'void',
          source: 'f'
        }
      } as any;
      component.fullBetType = '5-A-Side';
      expect(component.hasFiveASideWidget).toBe(false);
    });
    it('should return false, if hasLeaderboardWidget is false & fullbet type is fiveaside won', () => {
      component.hasLeaderboardWidget = false;
      component.bet = {
        eventSource: {
          totalStatus: 'won',
          source: 'f'
        }
      } as any;
      component.fullBetType = '5-A-Side';
      expect(component.hasFiveASideWidget).toBe(false);
    });
    it('should return true, if hasLeaderboardWidget is false & fullbet type is fiveaside lost', () => {
      component.hasLeaderboardWidget = false;
      component.bet = {
        eventSource: {
          totalStatus: 'lost',
          source: 'f'
        }
      } as any;
      component.fullBetType = '5-A-Side';
      expect(component.hasFiveASideWidget).toBe(false);
    });
    it('should return false, if hasLeaderboardWidget is false & fullbet type is fiveaside void', () => {
      component.hasLeaderboardWidget = false;
      component.bet = {
        eventSource: {
          totalStatus: 'void',
          source: 'f'
        }
      } as any;
      component.fullBetType = '5-A-Side';
      expect(component.hasFiveASideWidget).toBe(false);
    });
  });

  describe("#reuse", () => {
    beforeEach(() => {
      component.reuseBet.emit = jasmine.createSpy('emit');
    });
    it('should emit reuse event on click', () => {
      component.reuse();
      expect(component.reuseBet.emit).toHaveBeenCalled();
    });
  });

  describe("#checkIfAnyEventActive", () => {
    it('should return true if event not confirmed', () => {
      component.bet = {
        eventSource: {
          leg: [{
            part: [{
              outcome: [{
                result: {
                  confirmed: 'N'
                }
              }]
            }],
            status: 'open'
          }]
        }
      } as any;
      const res = component.checkIfAnyEventActive();
      expect(res).toEqual(true);
    });
    it('should return false if event confirmed', () => {
      component.bet = {
        eventSource: {
          leg: [{
            part: [{
              outcome: [{
                result: {
                  confirmed: 'Y'
                }
              }]
            }],
            status: 'open'
          }]
        }
      } as any;
      const res = component.checkIfAnyEventActive();
      expect(res).toEqual(false);
    });
  });

  describe("#checkEdpPage", () => {
    it('should return true if reuseLocation not HREDP', () => {
      component.reuseLocation = undefined;
      const res = component.checkEdpPage();
      expect(res).toEqual(true);
    });
    it('should return false if reuseLocation is HREDP', () => {
      component.reuseLocation = 'HREDP';
      const res = component.checkEdpPage();
      expect(res).toEqual(false);
    });
    it('should return false if reuseLocation is EDP', () => {
      component.reuseLocation = 'EDP';
      const res = component.checkEdpPage();
      expect(res).toEqual(false);
    });
  });

  describe("#checkIfAnyEventDisplayed", () => {
    it('should return true if event not confirmed', () => {
      component.bet = {
        eventSource: {
          leg: [{
            part: [{
              outcome: [{
                result: {
                  confirmed: 'N'
                }
              }]
            }],
            status: 'open'
          }],
          events: {}
        }
      } as any;
      const res = component.checkIfAnyEventDisplayed();
      expect(res).toEqual(true);
    });
    it('should return true if event confirmed and displayed SGL', () => {
      component.bet = {
        eventSource: {
          betType: 'SGL',
          leg: [{
            part: [{
              outcome: [{
                result: {
                  confirmed: 'N'
                }
              }]
            }],
            status: 'open'
          }],
          events: {12345 : {displayed: "Y"}},
          markets: {12345 : {displayed: "Y"}},
          outcomes: {12345 : {displayed: "Y"}}
        }
      } as any;
      const res = component.checkIfAnyEventDisplayed();
      expect(res).toEqual(true);
    });
    it('should return true if event confirmed and displayed MUL', () => {
      component.bet = {
        eventSource: {
          betType: 'MUL',
          leg: [{
            part: [{
              outcome: [{
                result: {
                  confirmed: 'N'
                }
              }]
            }],
            status: 'open'
          }],
          events: {12345 : {displayed: "Y"}},
          markets: {12345 : {displayed: "Y"}},
          outcomes: {12345 : {displayed: "Y"}}
        }
      } as any;
      const res = component.checkIfAnyEventDisplayed();
      expect(res).toEqual(true);
    });
    it('should return false if event confirmed and not displayed SGL', () => {
      component.bet = {
        eventSource: {
          betType: 'SGL',
          leg: [{
            part: [{
              outcome: [{
                result: {
                  confirmed: 'N'
                }
              }]
            }],
            status: 'open'
          }],
          events: {12345 : {displayed: "N"}},
          markets: {12345 : {displayed: "N"}},
          outcomes: {12345 : {displayed: "N"}}
        }
      } as any;
      const res = component.checkIfAnyEventDisplayed();
      expect(res).toEqual(false);
    });
    it('should return false if event confirmed and not displayed MUL', () => {
      component.bet = {
        eventSource: {
          betType: 'MUL',
          leg: [{
            part: [{
              outcome: [{
                result: {
                  confirmed: 'N'
                }
              }]
            }],
            status: 'open'
          }],
          events: {12345 : {displayed: "N"}},
          markets: {12345 : {displayed: "N"}},
          outcomes: {12345 : {displayed: "N"}}
        }
      } as any;
      const res = component.checkIfAnyEventDisplayed();
      expect(res).toEqual(false);
    });
  });
});
