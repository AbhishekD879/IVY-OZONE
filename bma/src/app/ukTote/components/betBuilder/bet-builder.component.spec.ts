import { BetBuilderComponent } from '@uktote/components/betBuilder/bet-builder.component';
import { LocaleService } from '@core/services/locale/locale.service';
import { eventEntityMock } from '@uktote/components/betBuilder/bet-builder.component.mock';
import * as uktote from '@localeModule/translations/en-US/uktote.lang';
import { of as observableOf, of, Subject } from 'rxjs';
import { CoreToolsService } from '@core/services/coreTools/core-tools.service';
import { fakeAsync, tick } from '@angular/core/testing';

describe('BetBuilderComponent', () => {
  let component: BetBuilderComponent;
  let commandService,
    deviceService,
    ukToteBetBuilderService,
    pubsubService,
    stakeValidatorService,
    localeService,
    filtersService,
    gtmService,
    timeService,
    ukToteService,
    windowRefService,
    elementRef,
    ukToteLiveUpdatesService,
    rendererService,
    domToolsService, currencyCalculator,
    userService, currencyCalculatorService,
    cms;
  const coreToolsService = new CoreToolsService();
  const isMultipleLegsBetSubject$ = new Subject<boolean>();

  beforeEach(() => {
    commandService = {
      execute: jasmine.createSpy(),
      API: {
        SHOW_HIDE_FOOTER_MENU: 'SHOW_HIDE_FOOTER_MENU'
      }
    };
    deviceService = {
      isMobile: true,
      isMobileOrigin: true,
      isTablet: false
    };
    ukToteBetBuilderService = {
      items: {
        any: 'testany'
      },
      betName: 'testBetNameMock',
      betModel: {
        events: [],
        legs: [],
        isSuspended: false,
        getBetObject: jasmine.createSpy().and.returnValue({
          betNo: 1,
          poolType: 'poolType'
        }),
        pool: {
          currencyCode: '$',
          id: 14
        },
        checkIfAllLegsFilled: jasmine.createSpy().and.returnValue(true),
      },
      isMultipleLegsBet: false,
      poolType: 'UEXA',
      poolId: 123456,
      checkIfShouldShow: jasmine.createSpy().and.returnValue(true),
      getTotalStake: jasmine.createSpy(),
      clear: jasmine.createSpy('clear'),
      isMultipleLegsBetSubject$,
      isMultipleLegsBet$: isMultipleLegsBetSubject$.asObservable()
    };
    pubsubService = {
      publish: jasmine.createSpy(),
      subscribe: jasmine.createSpy().and.callFake((a, b, cb) => cb && cb()),
      unsubscribe: jasmine.createSpy(),
      API: {
        ADD_TO_BETSLIP_BY_SELECTION: 'ADD_TO_BETSLIP_BY_SELECTION',
        BETBUILDER_UPDATED: 'BETBUILDER_UPDATED',
        RELOAD_COMPONENTS: 'RELOAD_COMPONENTS',
        RELOCATE_BET_BUILDER: 'RELOCATE_BET_BUILDER',
        CLEAR_BET_BUILDER: 'CLEAR_BET_BUILDER',
        SUCCESSFUL_LOGIN: 'SUCCESSFUL_LOGIN',
        SESSION_LOGOUT: 'SESSION_LOGOUT'
      }
    };
    stakeValidatorService = {
      getValidationState: jasmine.createSpy().and.returnValue({
        minStakePerLine: true,
        maxStakePerLine: true
      })
    };
    localeService = new LocaleService(coreToolsService);
    localeService.setLangData(uktote);
    filtersService = {
      numberWithCurrency: jasmine.createSpy().and.returnValue('£')
    };
    gtmService = {
      push: jasmine.createSpy()
    };
    timeService = {
      getCorrectDay: jasmine.createSpy().and.returnValue('dayMock')
    };
    ukToteService = {
      getAllIdsForEvents: jasmine.createSpy().and.returnValue({
        outcome: []
      }),
      getRaceTitle: jasmine.createSpy().and.returnValue('mockTitle')
    };
    windowRefService = {
      nativeWindow: {
        clearTimeout: jasmine.createSpy(),
        setTimeout: jasmine.createSpy().and.callFake(cb => cb && cb()),
      }
    };
    cms={
      getQuickStakes:jasmine.createSpy('getQuickStakes').and.returnValue(of(['10'])),
    }
    elementRef = {
      nativeElement: {
        querySelector: jasmine.createSpy('querySelector').and.returnValue({})
      }
    };
    ukToteLiveUpdatesService = {
      getAllChannels: jasmine.createSpy().and.returnValue([])
    };
    rendererService = {
      renderer: {
        listen: jasmine.createSpy().and.callFake((a, b, cb) => cb && cb())
      }
    };
    domToolsService = {
      getOffset: jasmine.createSpy().and.returnValue({
        left: 10,
        top: 10
      }),
      getHeight: jasmine.createSpy().and.returnValue(10),
      getWidth: jasmine.createSpy().and.returnValue(10),
      css: jasmine.createSpy().and.returnValue('color: red;')
    };
    currencyCalculator = {
      currencyExchange: jasmine.createSpy().and.callFake(() => 1.59)
    };
    userService = {
      currency: 'USD',
      currencySymbol: '$'
    };
    currencyCalculatorService = {
      getCurrencyCalculator: jasmine.createSpy().and.callFake(() => observableOf(currencyCalculator))
    };

    component = new BetBuilderComponent(commandService, deviceService, ukToteBetBuilderService, pubsubService, stakeValidatorService,
      localeService, filtersService, gtmService, timeService, ukToteService, windowRefService, elementRef, ukToteLiveUpdatesService,
      rendererService, domToolsService, userService, currencyCalculatorService,cms);

    component.eventEntity = eventEntityMock;
    component.currentPool = {
      currencyCode: 'GBP'
    } as any;
  });

  it('should init component properties', () => {
    expect(component.userCurrencyCode).toEqual('USD');
    expect(component.userCurrencySymbol).toEqual('$');
  });

  describe('getBetObject', () => {
    it('should create Exacta bet model', () => {
      component.betName = '1 EXACTA BET';
      component['ukToteBetBuilderService'] = ({
        items: {
          '1st': {
            id: '123'
          },
          '2nd': {
            id: '234'
          }
        },
        poolType: 'UEXA',
        poolId: 123456
      } as any);
      const validToteExactaBet = {
        poolType: 'UEXA',
        betNo: 134,
        poolItem: [
          {
            position: '1',
            poolId: 123456,
            outcome: '123'
          },
          {
            position: '2',
            poolId: 123456,
            outcome: '234'
          },
        ]
      };
      const betObject = component.getBetObject();

      expect(betObject).toEqual(validToteExactaBet);
    });

    it('should create TRIFECTA bet model', () => {
      component.betName = '1 TRIFECTA BET';
      component['ukToteBetBuilderService'] = ({
        betName: 'testBetNameMock',
        items: {
          '1st': {
            id: '123'
          },
          '2nd': {
            id: '234'
          },
          '3rd': {
            id: '345'
          }
        },
        poolType: 'UTRI',
        poolId: 123456
      } as any);
      const validToteTrifectaBet = {
        poolType: 'UTRI',
        betNo: 134,
        poolItem: [
          {
            position: '1',
            poolId: 123456,
            outcome: '123'
          },
          {
            position: '2',
            poolId: 123456,
            outcome: '234'
          },
          {
            position: '3',
            poolId: 123456,
            outcome: '345'
          },
        ]
      };
      const betObject = component.getBetObject();
      expect(betObject).toEqual(validToteTrifectaBet);
    });

    it('should create Combination bet model for other cases', () => {
      component.betName = '5 COMBINATION EXACTA BETS';
      component['ukToteBetBuilderService'] = ({
        items: {
          any: [
            {
              id: '123'
            },
            {
              id: '235'
            }
          ]
        },
        poolType: 'UEXA',
        poolId: 123456
      } as any);
      const validToteCombinationBet = {
        poolType: 'UEXA',
        betNo: 134,
        poolItem: [
          {
            poolId: 123456,
            outcome: '123'
          },
          {
            poolId: 123456,
            outcome: '235'
          }
        ]
      };
      const betObject = component.getBetObject();
      expect(betObject).toEqual(validToteCombinationBet);
    });

    it('should create Combination bet model when isMultipleLegsBet is true', () => {
      const validToteCombinationBet = {
        betNo: 1,
        poolType: 'poolType'
      } as any;
      component['isMultipleLegsBet'] = true;

      const betObject = component.getBetObject();
      expect(betObject).toEqual(validToteCombinationBet);
    });
  });

  it('get isManySelections', () => {
    component['ukToteBetBuilderService'] = ({
      items: {
        any: [
          {
            id: '123'
          },
          {
            id: '235'
          }
        ]
      },
      poolType: 'UEXA',
      poolId: 123456
    } as any);

    expect(component.isManySelections).toEqual('Clear Selections');
  });


  it('should initialise component and subscribe for global events', () => {
    deviceService.isMobileOrigin = false;
    deviceService.isTablet = true;
    spyOn(component as any, 'relocateAfter');
    spyOn(component as any, 'init');
    spyOn(component as any, 'setVisibility');
    spyOn(component as any, 'resetState');
    spyOn(component as any, 'updateSwitchersState');

    component.ngOnInit();

    expect(pubsubService.subscribe).toHaveBeenCalledTimes(5);

    expect(component['setVisibility']).toHaveBeenCalledTimes(2);
    expect(component['setVisibility']).toHaveBeenCalledWith(false, true);
    expect(component['relocateAfter']).toHaveBeenCalledTimes(2);
    expect(component['relocateAfter']).toHaveBeenCalled();
    expect(ukToteBetBuilderService.clear).toHaveBeenCalled();
    expect(component['resetState']).toHaveBeenCalled();
    expect(component['updateSwitchersState']).toHaveBeenCalled();
    expect(component['init']).toHaveBeenCalledTimes(2);
    expect(component['init']).toHaveBeenCalledWith(true);

    expect(rendererService.renderer.listen).toHaveBeenCalled();
    expect(rendererService.renderer.listen).toHaveBeenCalledTimes(2);

    expect(component.betModel).toEqual(ukToteBetBuilderService.betModel);
    expect(component.isMultipleLegsBet).toBeFalsy();
  });

  it('ngOnInit when isTablet is true', () => {
    deviceService.isMobileOrigin = true;
    deviceService.isTablet = true;
    component.ngOnInit();
    expect(rendererService.renderer.listen).toHaveBeenCalled();
    expect(rendererService.renderer.listen).toHaveBeenCalledTimes(2);
  });

  it('ngOnInit should handle isMultipleLegsBet update', () => {
    component['isMultipleLegsBet'] = false;
    component.ngOnInit();
    component['ukToteBetBuilderService']['isMultipleLegsBetSubject$'].next(true);
    expect(component['isMultipleLegsBet']).toBeTruthy();
  });

  it('should reset State', () => {
    component.resetState();

    expect(component.expanded).toEqual(false);
    expect(component.stakePerLine).toBeUndefined();
    expect(component.messageClosed).toEqual(false);
    expect(component.errorField).toBeUndefined();
  });

  it('should init base state with bettypeChanged false', () => {
    component['ukToteBetBuilderService'] = ({
      items: {
        '1st': {
          id: '123'
        },
        '2nd': {
          id: '234'
        }
      },
      betName: 'testBetNameMock',
      betModel: {
        events: [],
        legs: [],
        isSuspended: false
      },
      isMultipleLegsBet: false,
      poolType: 'UEXA',
      poolId: 123456,
      checkIfShouldShow: jasmine.createSpy().and.returnValue(true),
      getTotalStake: jasmine.createSpy()
    } as any);

    spyOn(component, 'resetState');
    spyOn(component, 'setStake');

    component.init(false);

    expect(component.resetState).not.toHaveBeenCalled();
    expect(component.setStake).toHaveBeenCalled();
    expect(component.betName).toEqual(ukToteBetBuilderService.betName);
    expect(component.isBetReadyForBetslip).toBeTruthy();
  });

  it("should replace stakePerLine", () => {
    component.stakePerLine = "1,0";
    component.setStake();
    expect(component.stakePerLine).toEqual("1.0");
  })

  it("should replace comma stakePerLine", () => {
    component.stakePerLine = "1.2";
    component.setStake();
    expect(component.stakePerLine).toEqual("1.2");
  })

  it('should init base state with checkIfShouldShow false', () => {
    component['setVisibility'] = jasmine.createSpy();
    ukToteBetBuilderService.betName = undefined;
    ukToteBetBuilderService.checkIfShouldShow = jasmine.createSpy().and.returnValue(false);

    component.init(true);
    expect(component['setVisibility']).toHaveBeenCalledWith(false, true);
  });

  it('should init base state with bettypeChanged true', () => {
    spyOn(component, 'resetState');

    component.init(true);

    expect(component.resetState).toHaveBeenCalled();
  });

  describe('relocate', () => {
    beforeEach(() => {
      domToolsService.getHeight = jasmine.createSpy().and.returnValue(0);
      domToolsService.getOffset = jasmine.createSpy().and.returnValue({
        left: 0,
        top: 0
      });
    });

    it('Recalculate betbuilder CSS position and dimensions', () => {
      deviceService.isMobileOrigin = false;
      domToolsService.getOffset = jasmine.createSpy().and.returnValue({
        left: 10,
        top: 0
      });

      component.relocate();

      expect(domToolsService.css).toHaveBeenCalledWith({}, { position: 'fixed', left: 10, bottom: 0, width: 10 });
      expect(domToolsService.getOffset).toHaveBeenCalled();
      expect(domToolsService.getWidth).toHaveBeenCalled();
    });

    it('Recalculate betbuilder CSS position and dimensions', () => {
      component['BETBUILDER_MIN_HEIGHT'] = 0;
      component['TABLET_BOTTOM_MENU_HEIGHT'] = 0;
      deviceService.isTablet = false;
      deviceService.isMobile = false;

      component.relocate();

      expect(domToolsService.css).not.toHaveBeenCalledWith({}, { position: 'fixed', left: 10, bottom: 0, width: 10 });
      expect(domToolsService.getOffset).not.toHaveBeenCalled();
      expect(domToolsService.getWidth).not.toHaveBeenCalled();
    });

    it('relocate should return undefined', () => {
      elementRef.nativeElement.querySelector = jasmine.createSpy().and.returnValue('div');
      expect(component.relocate()).toBeUndefined();
    });

    it('should set bottom value to specific value if device is recognized as tablet and not as a desktop', () => {
      deviceService.isMobileOrigin = false;
      deviceService.isTablet = true;
      deviceService.isDesktop = false;
      component['BETBUILDER_MIN_HEIGHT'] = 0;
      component['TABLET_BOTTOM_MENU_HEIGHT'] = 52;

      component.relocate();

      expect(domToolsService.css).toHaveBeenCalledWith({}, { position: 'fixed', left: 0, bottom: 52, width: 10 });
    });

    it('should set bottom value to 0 if device is recognized as desktop and not as a tablet', () => {
      deviceService.isMobileOrigin = false;
      deviceService.isTablet = false;
      deviceService.isDesktop = true;
      component['BETBUILDER_MIN_HEIGHT'] = 0;
      component['TABLET_BOTTOM_MENU_HEIGHT'] = 52;

      component.relocate();

      expect(domToolsService.css).toHaveBeenCalledWith({}, { position: 'fixed', left: 0, bottom: 0, width: 10 });
    });
  });

  it('generateToteBetDetails', () => {
    component.stakeRestrictions = {} as any;

    const result = component.generateToteBetDetails();

    const hasProperties = result.betName && result.poolName && result.eventTitle &&
      result.correctedDay && result.orderedOutcomes && result.stakeRestrictions;

    expect(hasProperties).toBeTruthy();
  });

  it('should add bet To Betslip', () => {
    component['ukToteBetBuilderService'] = ({
      items: {
        any: 'testany',
        '1st': {
          id: '123'
        },
        '2nd': {
          id: '234'
        }
      },
      betName: 'testBetNameMock',
      poolType: 'UEXA',
      poolId: 123456,
      checkIfShouldShow: jasmine.createSpy().and.returnValue(true),
      getTotalStake: jasmine.createSpy()
    } as any);

    component.stakeRestrictions = {} as any;
    component.currentPool = {
      minStakePerLine: 3,
      maxStakePerLine: 3,
      stakeIncrementFactor: 3,
      minTotalStake: 3,
      maxTotalStake: 3
    } as any;

    spyOn(component, 'getOrderedOutcomes').and.returnValue([]);

    component.addToBetslip();

    expect(pubsubService.publish).toHaveBeenCalledWith(pubsubService.API.ADD_TO_BETSLIP_BY_SELECTION, jasmine.any(Object));
  });

  it('should add bet To Betslip when isMultipleLegsBet is true', () => {
    ukToteBetBuilderService.isMultipleLegsBet = true;
    component['ukToteBetBuilderService'] = ({
      items: {
        any: 'testany',
        '1st': {
          id: '123'
        },
        '2nd': {
          id: '234'
        }
      },
      betName: 'testBetNameMock',
      poolType: 'UEXA',
      poolId: 123456,
      checkIfShouldShow: jasmine.createSpy().and.returnValue(true),
      getTotalStake: jasmine.createSpy(),
      selectedOutcomes: jasmine.createSpy().and.returnValue([]),
      generateToteBetDetails: jasmine.createSpy().and.returnValue({
        poolName: 'poolName',
        numberOfLines: 4
      }),
    } as any);

    component.stakeRestrictions = {} as any;
    component.currentPool = {} as any;
    spyOn(component, 'getOrderedOutcomes').and.returnValue([]);

    component.addToBetslip();

    expect(pubsubService.publish).toHaveBeenCalledWith(pubsubService.API.ADD_TO_BETSLIP_BY_SELECTION, jasmine.any(Object));
  });

  describe('getter alertMsg', () => {
    it('should show warning msg', () => {
      component.msg = {
        warning: 'testWarning'
      };
      expect(component.alertMsg).toEqual('testWarning');
    });

    it('should show error translate if no warning msg', () => {
      component.msg = null;
      spyOn<any>(component, 'getErrorTranslate').and.returnValue('errorMsg');
      expect(component.alertMsg).toEqual('errorMsg');
    });
  });

  describe('getter showAlert', () => {
    it('should alert if warning msg', () => {
      component.msg = {
        warning: 'testWarning'
      };
      expect(component.showAlert).toEqual(true);
    });

    it('should alert if no message but bet model and error message and message not closed', () => {
      component.msg = null;
      component.errorField = 'error';
      component.messageClosed = false;
      expect(component.showAlert).toEqual(true);
    });
  });

  describe('stakeInputClasses', () => {
    it('set dark class if stake per line is filled', () => {
      component.stakePerLine = '10';
      expect(component.stakeInputClasses).toEqual({
        dark: true
      });
    });
    it('shouldn\'t set dark class if stake per line is filled', () => {
      component.stakePerLine = undefined;
      expect(component.stakeInputClasses).toEqual({
        dark: false
      });
    });
  });

  it('addListeners should update currency when user logs in/logs out', () => {
    component['addListeners']();

    expect(pubsubService.subscribe).toHaveBeenCalledWith('BetBuilderController', ['SUCCESSFUL_LOGIN', 'SESSION_LOGOUT'],
      jasmine.any(Function));
  });

  describe('getTotalStakeInUserCurrency', () => {
    it('shouldn`t convert currency if it matches', () => {
      component.poolCurrencyCode = 'USD';
      expect(component.getTotalStakeInUserCurrency(1.23)).toEqual('1.23');
      expect(currencyCalculator.currencyExchange).not.toHaveBeenCalled();
    });

    it('shouldn`t convert currency if currencyCalculator is not set', () => {
      component.currencyCalculator = null;
      expect(component.getTotalStakeInUserCurrency(1.23)).toEqual(null);
      expect(currencyCalculator.currencyExchange).not.toHaveBeenCalled();
    });

    it('shouldn`t convert currency if money value is zero', () => {
      expect(component.getTotalStakeInUserCurrency(0)).toEqual(null);
      expect(currencyCalculator.currencyExchange).not.toHaveBeenCalled();
    });

    it('should convert currency if it not matches for Pot bet', () => {
      component.userCurrencyCode = 'USD';
      component.poolCurrencyCode = 'GBP';
      expect(component.getTotalStakeInUserCurrency(1.23)).toEqual('1.59');
      expect(currencyCalculator.currencyExchange).toHaveBeenCalledWith('GBP', 'USD', 1.23);
    });
  });

  it('clearSelections', () => {
    component.clearSelections();
    expect(gtmService.push).toHaveBeenCalledWith('trackEvent', jasmine.objectContaining({
      eventCategory: 'uk tote',
      eventAction: 'dashboard',
      eventLabel: 'clear selection'
    }));
    expect(ukToteBetBuilderService.clear).toHaveBeenCalled();
  });

  describe('getToteType', () => {
    it('getToteType(international)', () => {
      component.currentPool.type = 'PL';
      expect(component['getToteType']()).toEqual('international tote');
    });

    it('getToteType(uk)', () => {
      component.currentPool.type = 'UPLC';
      expect(component['getToteType']()).toEqual('uk tote');
    });
  });

  describe('ngOnDestroy', () => {
    beforeEach(() => {
      component['isMultipleLegsBetSubscription'] = {
        unsubscribe: jasmine.createSpy('unsubscribe')
      } as any;
    });
    it('should resetState', () => {
      component.expanded = null;
      component.stakePerLine = null;
      component.messageClosed = null;
      component.errorField = null;

      component.ngOnDestroy();

      expect(component.expanded).toBe(false);
      expect(component.stakePerLine).toBe(undefined);
      expect(component.messageClosed).toBe(false);
      expect(component.errorField).toBe(undefined);
      expect(component['isMultipleLegsBetSubscription']['unsubscribe']).toHaveBeenCalled();
    });

    it('should setFooterVisibility', () => {
      component.ngOnDestroy();
      expect(commandService.execute).toHaveBeenCalledWith(commandService.API.SHOW_HIDE_FOOTER_MENU, [true], []);
      expect(component['isMultipleLegsBetSubscription']['unsubscribe']).toHaveBeenCalled();
    });

    it('should unsubscribe listeners', () => {
      component.scrollListener = jasmine.createSpy('scrollListener');
      component.resiseListener = jasmine.createSpy('resiseListener');

      component.ngOnDestroy();

      expect(component.scrollListener).toHaveBeenCalled();
      expect(component.resiseListener).toHaveBeenCalled();
      expect(component['isMultipleLegsBetSubscription']['unsubscribe']).toHaveBeenCalled();
    });

    it('should unsubscribe pubsub BetBuilderController', () => {
      component.ngOnDestroy();

      expect(pubsubService.unsubscribe).toHaveBeenCalledWith('BetBuilderController');
      expect(component['isMultipleLegsBetSubscription']['unsubscribe']).toHaveBeenCalled();
    });
  });

  describe('getOrderedOutcomes', () => {
    it('ukToteBetBuilderService items length = 3', () => {
      expect(component.getOrderedOutcomes()).toBe('testany' as any);
    });
    it('ukToteBetBuilderService items length = 2', () => {
      ukToteBetBuilderService.items = {
          '1st': '1st',
          '2nd': '2nd'
      };
      expect(component.getOrderedOutcomes()).toEqual(['1st', '2nd'] as any);
    });

    it('ukToteBetBuilderService items length = 3', () => {
      ukToteBetBuilderService.items = {
        '1st': '1st',
        '2nd': '2nd',
        '3rd': '3rd',
      };
      expect(component.getOrderedOutcomes()).toEqual(['1st', '2nd', '3rd'] as any);
    });
  });

  it('toggleSummary', () => {
    component.toggleSummary();
    expect(component.expanded).toBeTruthy();
  });

  it('getErrorTranslate', () => {
    localeService.getString = jasmine.createSpy().and.returnValue('errorCode');
    component.errorField = 'error';

    component.getErrorTranslate();
    expect(localeService.getString).toHaveBeenCalledWith('uktote.error', { value: '£'});
  });

  it('setStake should return undefined', () => {
    ukToteBetBuilderService.betModel = undefined;
    expect(component.setStake()).toBeUndefined();
  });

  it('closeMessage', () => {
    component.closeMessage();
    expect(component.messageClosed).toBeTruthy();
    expect(component.msg).toBeNull();
  });

  it('totalStakeWithCurrency', () => {
    expect(component.totalStakeWithCurrency).toBe('£');
  });

  it('isManySelections', () => {
    localeService.getString = jasmine.createSpy().and.returnValue('clearSelection');
    ukToteBetBuilderService.items = {
      '1st': {
        id: '123'
      },
      '2nd': {
        id: '234'
      }
    };

    const result = component.isManySelections;
    expect(localeService.getString).not.toHaveBeenCalledWith('uktote.clearSelections');
    expect(localeService.getString).toHaveBeenCalledWith('uktote.clearSelection');
    expect(result).toBe('clearSelection');
  });

  it('checkIfBetReadyForBetSlip when isMultipleLegsBet is true', () => {
    component['isMultipleLegsBet'] = true;
    component.stakePerLine = '10';
    component.errorField = null;

    const result = component['checkIfBetReadyForBetSlip']();
    expect(ukToteBetBuilderService.betModel.checkIfAllLegsFilled).toHaveBeenCalled();
    expect(result).toBeTruthy();
  });

  it('checkIfBetReadyForBetSlip when isMultipleLegsBet is false', () => {
    ukToteBetBuilderService.isMultipleLegsBet = false;
    component.betName = 'testBetNameMock';

    const result = component['checkIfBetReadyForBetSlip']();
    expect(ukToteBetBuilderService.betModel.checkIfAllLegsFilled).not.toHaveBeenCalled();
    expect(result).toBeTruthy();
  });

  it('relocateAfter', () => {
    component.relocate = jasmine.createSpy();
    component['relocateAfter'](200);
    expect(windowRefService.nativeWindow.clearTimeout).toHaveBeenCalledWith(component.relocateAfterJob);
    expect(windowRefService.nativeWindow.setTimeout).toHaveBeenCalled();
    expect(component.relocate).toHaveBeenCalled();
  });

  it('updateSwitchersState when isMultipleLegsBet is true', () => {
    component['isMultipleLegsBet'] = true;
    ukToteBetBuilderService.betModel.legs = [
      {
        name: 'leg1',
        linkedMarketId: 1
      },
      {
        name: 'leg2',
        linkedMarketId: 2
      },
    ];

    component['updateSwitchersState']();
    expect(pubsubService.publish).toHaveBeenCalledTimes(2);
  });

  it('updateSwitchersState when isMultipleLegsBet is false', () => {
    expect(component['updateSwitchersState']()).toBeUndefined();
  });

  it('getChannelIds', () => {
    const events = [
      { sportId: '11' } as any
    ];
    const selectedOutcomes = [
      { linkedOutcomeId: '123' } as any
    ];
    const result = component['getChannelIds'](events, selectedOutcomes);
    expect(ukToteService.getAllIdsForEvents).toHaveBeenCalledWith(events);
    expect(ukToteLiveUpdatesService.getAllChannels).toHaveBeenCalledWith({ outcome: [ '123' ] });
    expect(result).toEqual([]);
  });

  it('getValidationError', () => {
    const validationState = {
      minStakePerLine: false,
      maxStakePerLine: true,
      stakeIncrementFactor: true,
      minTotalStake: true,
      maxTotalStake: false
    } as any;

    const result = component['getValidationError'](validationState);
    expect(result).toEqual('maxStakePerLine');
  });

  it('getValidationError should return undefined', () => {
    const validationState = undefined;
    expect(component['getValidationError'](validationState)).toBeUndefined();
  });

  it('validateStake', () => {
    component.stakePerLine = '25';
    component['getValidationError'] = jasmine.createSpy().and.returnValue('error');
    const options = {};

    const result = component['validateStake'](options);
    expect(stakeValidatorService.getValidationState).toHaveBeenCalledWith(options);
    expect(component['getValidationError']).toHaveBeenCalledWith({ minStakePerLine: true, maxStakePerLine: true });

    expect(result).toEqual('error');
  });

  it('validateStake should return undefined', () => {
    component.stakePerLine = undefined;
    expect(component['validateStake']({})).toBeUndefined();
  });

  describe('ngOninit',() => {
    it('ngonintit getquickstakes', fakeAsync(() => {
        component.ngOnInit();
        tick(1000)
        expect(component.quickStakeItems.length).toBe(1)
    }))
  })

  describe('formatTotepoolStakes' , () => {
    it('more than 2 decimal', () => {
      component.formatTotepoolStakes(['10.223']);
      expect(component.quickStakeItems.length).toBe(1)
    })
    it('less than 2 decimal', () => {
      component.formatTotepoolStakes(['10'])
      expect(component.quickStakeItems.length).toBe(1)
    })
  })

  describe('onKeyboardToggle' , () => {
    it('expanded is true', () => {
      component.expanded = true;
      component.onKeyboardToggle(false);
      expect(component.expanded).toBeFalsy();
    })
    it('expanded is false', () => {
      component.expanded = false;
      component.onKeyboardToggle(true);
      expect(component.expanded).toBeFalsy();
    })
  })

});
