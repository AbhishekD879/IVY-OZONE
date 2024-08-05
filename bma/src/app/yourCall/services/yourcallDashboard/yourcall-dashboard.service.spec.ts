import { YourcallDashboardService } from '@yourcall/services/yourcallDashboard/yourcall-dashboard.service';
import { fakeAsync, tick } from '@angular/core/testing';

describe('YourcallDashboardService -', () => {
  let
    service: YourcallDashboardService,
    userService,
    fracToDecService,
    pubsubService,
    yourcallValidationService,
    yourcallProviderService,
    localeService,
    gtmService,
    awsService,
    bybSelectedSelectionsService;

  beforeEach(() =>  {
    userService = {
      status: true,
      oddsFormat: 'frac'
    };
    fracToDecService = {
      fracToDec: jasmine.createSpy('fracToDec'),
      decToFrac: jasmine.createSpy('decToFrac').and.returnValue(123),
      getDecimal: jasmine.createSpy('getDecimal')
    };
    pubsubService = {
      publish: jasmine.createSpy('publish'),
      API: {
        YC_DASHBOARD_DISPLAYING_CHANGED: 'YC_DASHBOARD_DISPLAYING_CHANGED'
      }
    };
    yourcallValidationService = {
      validate: jasmine.createSpy('validate').and.returnValue(true),
      isValidSelectionCount: jasmine.createSpy('isValidSelectionCount').and.returnValue(true)
    };
    yourcallProviderService = {
      calculateAccumulatorOdds: jasmine.createSpy('calculateAccumulatorOdds').and.returnValues(Promise.resolve({})),
      helper: {
        buildOddsParams: jasmine.createSpy('buildOddsParams').and.returnValue({
          obEventId: '12',
          selectionIds: '123',
          outcomeIds: '124',
          selectionType: '125'
        }),
        parseOddsValue: jasmine.createSpy('parseOddsValue'),
        parseOddsError: jasmine.createSpy('parseOddsError').and.returnValue('error')
      },
      isValidResponse: jasmine.createSpy('isValidResponse').and.returnValue(true)
    };
    localeService = {
      getString: jasmine.createSpy('getString').and.returnValue('yc.error')
    };
    gtmService = jasmine.createSpyObj(['push']);
    awsService = jasmine.createSpyObj(['addAction']);
    bybSelectedSelectionsService = {
        callGTM: jasmine.createSpy('callGTM').and.callFake(({}, {})=> false),
        duplicateIdd : new Set()
    };
    service = new YourcallDashboardService(
      userService,
      fracToDecService,
      pubsubService,
      yourcallValidationService,
      yourcallProviderService,
      localeService,
      gtmService,
      awsService,
      bybSelectedSelectionsService
    );

    service['_odds'] = {
      dec: '1000',
      frac: '1/100'
    };

    service.game = {
      obTypeId: 442
    } as any;

    service.eventObj = {
      id: 11
    } as any;

    service['dashboardItemsUpdate$'] = {
      next: jasmine.createSpy('next'),
      asObservable: jasmine.createSpy('asObservable')
    } as any;
  });

  it('constructor', () => {
    expect(service).toBeTruthy();
  });

  it('get dashboardItems$', () => {
    const dashboardItems$ = {} as any;
    service['dashboardItemsUpdate$']['asObservable']
      = jasmine.createSpy('asObservable').and.returnValue(dashboardItems$);
    const result = service.dashboardItems$;
    expect(service['dashboardItemsUpdate$']['asObservable']).toHaveBeenCalled();
    expect(result).toBe(dashboardItems$);
  });

  describe('@trackAddToQuickBetSlip', () => {
    it('should track to GA and NR', () => {
      service.trackAddToQuickBetSlip('foo', true);

      expect(gtmService.push).toHaveBeenCalledWith(
        'trackEvent',
        {
          eventCategory: 'your call',
          eventAction: 'foo',
          eventLabel: jasmine.any(Number)
        }
      );
      expect(awsService.addAction).toHaveBeenCalledWith(
        'yourcallDashboard=>placeBet (add to quickbet)',
        { isLoggedIn: true }
      );
    });

    it('should track to GA for add selection to qb', () => {
      service.trackAddToQuickBetSlip('foo', true);

      expect(gtmService.push).toHaveBeenCalledWith(
        'trackEvent', {
          event: 'trackEvent',
          eventCategory: 'quickbet',
          eventAction: 'add to quickbet',
          eventLabel: 'success',
          ecommerce: {
            add: {
              products: [{
                name: undefined,
                category: '16',
                variant: '442',
                brand: 'Bet Builder',
                metric1: 0,
                dimension60: '11',
                dimension62: 0,
                dimension63: 1,
                dimension64: 'EDP',
                dimension65: 'Bet Builder',
                dimension86: 0,
                dimension87: 0,
                dimension89: undefined,
                quantity: 1
              }]
            }
          }
        }
      );
    });
  });

  describe('#odds', () => {
    it('get odds dec format', () => {
      userService.oddsFormat = 'dec';
      const result = service.odds;

      expect(result).toEqual('1000.00');
    });

    it('get odds frac format', () => {
      const result = service.odds;

      expect(result).toEqual('1/100');
    });

    it('set odds no odds', () => {
      const result = service.odds = undefined;

      expect(result).toEqual(undefined);
    });

    it('set odds dec odds', () => {
      const result = service.odds = '1000';

      expect(result).toEqual('1000');
    });

    it('set odds frac odds', () => {
      const result = service.odds = '1/10';

      expect(result).toEqual('1/10');
    });
  });

  describe('#isButtonAvailable', () => {
    it('get isButtonAvailable', () => {
      service.items = [{
        selection: {
          disable: false
        }
      }, {
        selection: {
          disable: true
        }
      }] as any;
      const result = service.isButtonAvailable;

      expect(result).toEqual(true);
    });
  });

  describe('#isEditSection', () => {
    it('get isEditSection', () => {
      service.items = [{
        selection: {
          edit: false
        }
      }, {
        selection: {
          edit: true
        }
      }] as any;
      const result = service.isEditSection;

      expect(result).toEqual(true);
    });
  });

  describe('#add', () => {

    it('skip inside with null', () => {
      service.items = [{
        market: { }
      }] as any;
      spyOn(service, 'callGTM');
      bybSelectedSelectionsService.duplicateIdd.add(1);
      service.add({} as any, null, false);
      expect(service['dashboardItemsUpdate$']['next']).toHaveBeenCalled();
    });

    it('skip inside', () => {
      service.items = [{
        market: { }
      }] as any;
      spyOn(service, 'callGTM');
      bybSelectedSelectionsService.duplicateIdd.add(1)
      service.add({} as any, {idd : 1} as any, false);

      expect(pubsubService.publish).toHaveBeenCalledWith('YC_DASHBOARD_DISPLAYING_CHANGED', true);
      expect(yourcallValidationService.validate).toHaveBeenCalled();
      expect(yourcallValidationService.isValidSelectionCount).toHaveBeenCalled();
      expect(service['dashboardItemsUpdate$']['next']).toHaveBeenCalled();
    });

    it('should add selection to dashboard', () => {
      service.items = [{
        market: { }
      }] as any;
      spyOn(service, 'callGTM');
      service.add({} as any, {} as any, false);

      expect(pubsubService.publish).toHaveBeenCalledWith('YC_DASHBOARD_DISPLAYING_CHANGED', true);
      expect(yourcallValidationService.validate).toHaveBeenCalled();
      expect(yourcallValidationService.isValidSelectionCount).toHaveBeenCalled();
      expect(service['dashboardItemsUpdate$']['next']).toHaveBeenCalled();
    });

    it('should add selection to dashboard if market multi', () => {
      service.items = [{
        market: {
          id: '13',
          multi: true
        },
        selection: {
          id: '12'
        }
      }] as any;
      spyOn(service, 'callGTM');
      service.add(service.items[0].market as any, service.items[0].selection as any, false);

      expect(pubsubService.publish).toHaveBeenCalledWith('YC_DASHBOARD_DISPLAYING_CHANGED', true);
      expect(yourcallValidationService.validate).toHaveBeenCalled();
      expect(yourcallValidationService.isValidSelectionCount).toHaveBeenCalled();
    });

    it('should add selection to dashboard if market not multi', () => {
      service.items = [{
        market: {
          id: '13'
        },
        selection: {
          id: '12'
        }
      }] as any;
      spyOn(service, 'callGTM');
      service.add(service.items[0].market as any, service.items[0].selection as any, false);

      expect(pubsubService.publish).toHaveBeenCalledWith('YC_DASHBOARD_DISPLAYING_CHANGED', true);
      expect(yourcallValidationService.validate).toHaveBeenCalled();
      expect(yourcallValidationService.isValidSelectionCount).toHaveBeenCalled();
    });
  });

  describe('#callGTM', () => {
    it('should call callGTM', () => {
      service.items = [
        {
          id: '1212',
          getTitle: () => 'title1',
          getMarketTitle: () => 'marketTitle1',
          getSelectionTitle: () => 'selectionTitle1',
        }
      ] as any,
      service.callGTM();
      expect(bybSelectedSelectionsService.callGTM).toHaveBeenCalled();
    });

    it('should call callGTM', () => {
      service.items = [
      ] as any,
      service.callGTM();
      expect(bybSelectedSelectionsService.callGTM).not.toHaveBeenCalled();
    });
  });

  describe('#finishBatchAdd', () => {
    it('should call finishBatchAdd method', () => {
      service.finishBatchAdd();

      expect(pubsubService.publish).toHaveBeenCalledWith('YC_DASHBOARD_DISPLAYING_CHANGED', [true, true]);
    });
  });

  describe('#edit', () => {
    it('should call edit method', () => {
      service.items = [{
        market: {
          id: '13'
        },
        selection: {
          id: '12'
        }
      }] as any;
      service.edit(service.items[0].market as any, service.items[0].selection as any, {} as any);

      expect(yourcallValidationService.validate).toHaveBeenCalled();
      expect(service.showOdds).toEqual(true);
      expect(service['dashboardItemsUpdate$']['next']).toHaveBeenCalled();
    });
  });

  describe('#remove', () => {

    it('should call remove method if market multi', () => {
      service.items = [{
        market: {
          id: '13',
          multi: false
        },
        selection: {
          id: '12',
          idd: '1-2-1'
        }
      }] as any;
      bybSelectedSelectionsService.duplicateIdd.add('1-2-1');
      service.remove(service.items[0].market as any, null as any);

      expect(yourcallValidationService.validate).toHaveBeenCalled();
      expect(service.items).toEqual([]);
    });

    it('should call remove method if market multi', () => {
      service.items = [{
        market: {
          id: '13',
          multi: true
        },
        selection: {
          id: '12',
          idd: '1-2-1'
        }
      }] as any;
      bybSelectedSelectionsService.duplicateIdd.add('1-2-1')
      service.remove(service.items[0].market as any, service.items[0].selection as any);

      expect(yourcallValidationService.validate).toHaveBeenCalled();
      expect(service.items).toEqual([]);
    });

    it('should call remove method if market multi', () => {
      service.items = [{
        market: {
          id: '132',
          multi: true
        },
        selection: {
          id: '212',
          idd: '1-2-1'
        }
      }] as any;
      bybSelectedSelectionsService.duplicateIdd.add('1-2-1')
      service.remove({marketType: 'Player Bet'} as any, {} as any);

      expect(yourcallValidationService.validate).toHaveBeenCalled();
      expect(service.items.length).toBeGreaterThan(0)
    });

    it('should call remove method if market multi sel undefined', () => {
      service.items = [{
        market: {
          id: '132',
          multi: true
        },
        selection: {
          id: '212',
        }
      }] as any;
      bybSelectedSelectionsService.duplicateIdd.add('1-2-1')
      service.remove({marketType: 'Player Bet'} as any, {} as any);

      expect(yourcallValidationService.validate).toHaveBeenCalled();
      expect(service.items.length).toBeGreaterThan(0)
    });

    it('should call remove method', () => {
      service.items = [{
        market: {
          id: '13'
        },
        selection: {
          id: '12'
        }
      }] as any;
      service.remove(service.items[0].market as any, service.items[0].selection as any);

      expect(yourcallValidationService.validate).toHaveBeenCalled();
      expect(service.items).toEqual([]);
      expect(service['dashboardItemsUpdate$']['next']).toHaveBeenCalled();
    });

    it('should call remove method if market multi', () => {
      service.items = [{
        market: {
          id: '13',
          multi: true
        },
        selection: {
          id: '12'
        }
      }] as any;
      service.remove(service.items[0].market as any, service.items[0].selection as any);

      expect(yourcallValidationService.validate).toHaveBeenCalled();
      expect(service.items).toEqual([]);
    });

    it('should call remove method if market not multi and ids not eqal', () => {
      service.items = [{
        market: {
          id: '13',
          multi: true
        },
        selection: {
          id: '12'
        }
      }] as any;

      service.remove(service.items[0].market as any, {
        id: '11'
      } as any);

      expect(yourcallValidationService.validate).toHaveBeenCalled();
      expect(service.items).toEqual([{
        market: {
          id: '13',
          multi: true
        },
        selection: {
          id: '12'
        }
      }] as any);
    });
  });

  describe('#convertOdds', () => {
    it('should call convertOdds method', () => {
      service.convertOdds('1/2');

      expect(fracToDecService.getDecimal).toHaveBeenCalledWith(1, 2);
    });

    it('should call convertOdds method without /', () => {
      const result = service.convertOdds('12');

      expect(result).toEqual('12');
    });

    it('should call convertOdds method number odds', () => {
      const result = service.convertOdds(12);

      expect(result).toEqual(12);
    });
  });

  describe('#clear', () => {
    it('should call clear method', () => {
      service.valid = false;
      service.error = true;

      service.clear();

      expect(service.items).toEqual([]);
      expect(service.valid).toEqual(true);
      expect(service.error).toEqual(false);
      expect(service['dashboardItemsUpdate$']['next']).toHaveBeenCalled();
    });
  });

  describe('#validSelectionCount', () => {
    it('should call validSelectionCount method', () => {
      service.items = [{}] as any;
      service.validSelectionCount();

      expect(yourcallValidationService.dashboard).toEqual([{}]);
      expect(yourcallValidationService.isValidSelectionCount).toHaveBeenCalled();
    });
  });

  describe('#canPlaceBet', () => {
    it('should call canPlaceBet method', () => {
      const result = service.canPlaceBet();

      expect(result).toEqual(true);
    });

    it('should call canPlaceBet method not with validSelectionCount', () => {
      yourcallValidationService.isValidSelectionCount.and.returnValue(false);
      const result = service.canPlaceBet();

      expect(result).toEqual(false);
    });
  });

  describe('#calculateOdds', () => {
    it('should call calculateOdds method', fakeAsync(() => {
      service.items = [{}] as any;
      service.calculateOdds();

      tick();

      expect(yourcallProviderService.calculateAccumulatorOdds).toHaveBeenCalledWith({
        obEventId: '12',
        selectionIds: '123',
        outcomeIds: '124',
        selectionType: '125'
      });
    }));

    it('should call calculateOdds method with no items', () => {
      service.errorMessage = 'errorMessage';
      service.calculateOdds();

      expect(service.errorMessage).toEqual(undefined);
    });

    it('should call calculateOdds with error', fakeAsync(() => {
      yourcallProviderService.helper.parseOddsValue.and.returnValue(Promise.reject('error'));
      service.items = [{}] as any;
      service.calculateOdds();

      tick(100);

      expect(yourcallProviderService.isValidResponse).toHaveBeenCalledWith('error', 'calculateAccumulatorOdds');
    }));
  });

  describe('#trackEditingPlayerBet', () => {
    it('should call trackEditingPlayerBet method for statVal', () => {
      service.trackEditingPlayerBet('statVal', {
        player: {
          name: 'Player name'
        },
        stat: {
          title: 'title'
        },
        statVal: 'statVal'
      } as any);

      expect(gtmService.push).toHaveBeenCalledWith('trackEvent', {
        eventCategory: 'your call',
        eventAction: 'build bet',
        eventLabel: 'update statistic',
        playerName: 'Player name',
        playerStat: 'title',
        playerStatNum: 'statVal'
      });
    });

    it('should call trackEditingPlayerBet method for statistic', () => {
      service.trackEditingPlayerBet('statistic', {
        player: {
          name: 'Player name'
        },
        stat: {
          title: 'title'
        },
        statVal: 'statVal'
      } as any);

      expect(gtmService.push).toHaveBeenCalledWith('trackEvent', {
        eventCategory: 'your call',
        eventAction: 'build bet',
        eventLabel: 'select player bet',
        playerName: 'Player name',
        playerStat: 'title',
        playerStatNum: 'statVal'
      });
    });

    it('should call trackEditingPlayerBet method for unknown field', () => {
      service.trackEditingPlayerBet('', {
        player: {
          name: 'Player name'
        },
        stat: {
          title: 'title'
        },
        statVal: 'statVal'
      } as any);

      expect(gtmService.push).not.toHaveBeenCalled();
    });
  });

  describe('#trackBoardRemovingSelection', () => {
    it('should call trackBoardRemovingSelection method', () => {
      service.trackBoardRemovingSelection('marketTitle');

      expect(gtmService.push).toHaveBeenCalledWith('trackEvent', {
        eventCategory: 'your call',
        eventAction: 'dashboard',
        eventLabel: 'remove selection',
        market: 'marketTitle'
      });
    });
  });

  describe('#validate', () => {
    it('should call validate method', () => {
      service.items = [{}] as any;
      service['validate']();

      expect(yourcallValidationService.dashboard).toEqual([{}]);
      expect(yourcallValidationService.validate).toHaveBeenCalled();
    });
  });

  describe('#trackAddingSelection', () => {
    it('should call trackAddingSelection method', () => {
      service.eventObj = {
        id: 11,
        name: 'name'
      } as any;
      service['trackAddingSelection']();

      expect(gtmService.push).toHaveBeenCalledWith('trackEvent', {
        eventCategory: 'your call',
        eventAction: 'match bet',
        sportName: 'Football',
        eventName: 'name',
        eventID: 11
      });
    });
  });

  describe('#handleOddsError', () => {
    it('should call handleOddsError method', () => {
      service['handleOddsError']('error');

      expect(yourcallProviderService.isValidResponse).toHaveBeenCalledWith('error', 'calculateAccumulatorOdds');
      expect(service.loading).toEqual(false);
      expect(service.error).toEqual(true);
      expect(service.errorMessage).toEqual('error');
    });

    it('should call handleOddsError method when helper cannot parse odds error', () => {
      yourcallProviderService.helper.parseOddsError.and.returnValue(undefined);
      service['handleOddsError']('error');

      expect(yourcallProviderService.isValidResponse).toHaveBeenCalledWith('error', 'calculateAccumulatorOdds');
      expect(service.loading).toEqual(false);
      expect(service.error).toEqual(true);
      expect(service.errorMessage).toEqual('yc.error');
    });

    it('should call handleOddsError method when isValidResponse = false', () => {
      yourcallProviderService.isValidResponse.and.returnValue(false);
      service['handleOddsError']('error');

      expect(yourcallProviderService.isValidResponse).toHaveBeenCalledWith('error', 'calculateAccumulatorOdds');
      expect(yourcallProviderService.helper.parseOddsError).not.toHaveBeenCalled();
      expect(localeService.getString).not.toHaveBeenCalled();
    });
  });
});
