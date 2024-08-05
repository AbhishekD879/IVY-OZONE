import { of as observableOf } from 'rxjs';
import { fakeAsync, flush } from '@angular/core/testing';

import { UkToteEventComponent } from '@uktote/components/ukToteEvent/uk-tote-event.component';
import { IUkTotePoolBet } from '@uktote/models/tote-pool.model';
import { IPool, IPoolValue, IToteEvent } from '@uktote/models/tote-event.model';
import { CurrencyCalculator } from '@core/services/currencyCalculatorService/currency-calculator.class';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { UK_TOTE_CONFIG } from '@uktote/constants/uk-tote-config.contant';
import { FRACTIONAL_TO_DECIMAL_MAP } from '@core/services/constants/frac-to-dec.constant';

describe('UkToteEventComponent', () => {
  let component: UkToteEventComponent;
  let locale;
  let ukToteService;
  let ukToteLiveUpdatesService;
  let ukTotesHandleLiveServeUpdatesService;
  let betBuilderService;
  let routingHelperService;
  let location;
  let gtm;
  let storage;
  let currencyCalculatorService;
  let pubSubService;
  let fracToDecService;

  const pools = [
    {type: 'UEXA', id: 123},
    {type: 'UTRI', id: 456},
    {type: 'USW', id: 789},

    {type: 'WN', poolType: 'WN', id: 3766539},
    {type: 'PL', poolType: 'PL', id: 3766540},
    {type: 'EX', poolType: 'EX', id: 3766541}
  ] as IUkTotePoolBet[];
  const event = {
    markets: [],
  } as IToteEvent;
  const intTotePoolIds = [3766539, 3766540, 3766541];
  const poolToPoolValue = [
    {
      type: 'WN', guides: [
        {poolValue: {id: '28472071', poolId: '3766539', runnerNumber1: '5', value: '0'}},
        {poolValue: {id: '28472072', poolId: '3766539', runnerNumber1: '6', value: '2.5'}}
      ]
    },
    {
      type: 'PL', guides: [
        {poolValue: {id: '28472073', poolId: '3766540', runnerNumber1: '6', value: '5'}},
      ]
    },
    {
      type: 'EX', guides: []
    },
    {
      type: 'EX2'
    }
  ] as IPool[];
  const guides = [
    {id: '28472071', poolId: '3766539', runnerNumber1: '5', value: '0'},
    {id: '28472072', poolId: '3766539', runnerNumber1: '6', value: '2.5'},
    {id: '28472073', poolId: '3766540', runnerNumber1: '6', value: '5'}
  ] as IPoolValue[];

  const marketEntity = {
    outcomes: [
      {
        id: '5',
        name: 'someOutcomes'
      },
      {
        id: '6',
        name: 'someOutcomes6'
      },
    ]
  } as any;

  beforeEach(() => {
    locale = {
      getString: jasmine.createSpy('getString').and.returnValue('test_string')
    };
    ukToteService = {
      extendToteEventInfo: jasmine.createSpy('extendToteEventInfo'),
      getAllIdsForEvents: jasmine.createSpy('getAllIdsForEvents'),
      isMultipleLegsToteBet: jasmine.createSpy('isMultipleLegsToteBet'),
      sortOutcomes: jasmine.createSpy('sortOutcomes'),
      getGuidesData: jasmine.createSpy('getGuidesData').and.returnValue(Promise.resolve(poolToPoolValue)),
      isOutcomeSuspended: jasmine.createSpy('isOutcomeSuspended').and.returnValue(true),
      isEventSuspended: jasmine.createSpy('isEventSuspended').and.returnValue(event),
      isMarketSuspended: jasmine.createSpy('isMarketSuspended').and.returnValue(event)
    };
    ukToteLiveUpdatesService = {
      getAllChannels: jasmine.createSpy('getAllChannels'),
      updateEventWithLiveUpdate: jasmine.createSpy('updateEventWithLiveUpdate')
    };
    ukTotesHandleLiveServeUpdatesService = {
      subscribe: jasmine.createSpy('subscribe'),
      unsubscribe: jasmine.createSpy('unsubscribe')
    };
    betBuilderService = {
      clear: jasmine.createSpy('clear')
    };
    routingHelperService = {
      formEdpUrl: jasmine.createSpy('formEdpUrl'),
    };
    location = jasmine.createSpyObj('location', ['replaceState', 'go']);
    gtm = {
      push: jasmine.createSpy('push')
    };
    storage = {
      set: jasmine.createSpy('set')
    };
    currencyCalculatorService = {
      getCurrencyCalculator: jasmine.createSpy().and.returnValue(observableOf(new CurrencyCalculator([])))
    };
    pubSubService = {
      publish: jasmine.createSpy('publish'),
      API: pubSubApi
    };
    fracToDecService = {
      oddsFormat: 'frac',
      getFormattedValue: (priceNum: number, priceDen: number) => {
        if (fracToDecService.oddsFormat === 'frac') {
          return `${priceNum}/${priceDen}`;
        }
        const predefinedDecimalValue = FRACTIONAL_TO_DECIMAL_MAP[`${priceNum}/${priceDen}`];

        if (predefinedDecimalValue) {
          return predefinedDecimalValue;
        }

        return (1 + (priceNum / priceDen)).toFixed(2);
      }
    }

    component = new UkToteEventComponent(locale, ukToteService, ukToteLiveUpdatesService, ukTotesHandleLiveServeUpdatesService,
      betBuilderService, routingHelperService, location, gtm, storage, currencyCalculatorService, pubSubService, fracToDecService);

    component.pools = pools;
    component.event = event;
    component.marketEntity = marketEntity;
    component['checkboxesMap'] = {
      '111': {
        '1st': 'checked',
        '2nd': 'open'
      },
      '222': {
        '1st': 'open',
        '2nd': 'open'
      }
    } as any;
  });

  describe('ngOnInit', () => {
    beforeEach(() => {
      ['verifyPoolType', 'updateLocation'].forEach(method => {
        const bind = component[method].bind(component);
        component[method] = jasmine.createSpy(method).and.callFake(bind);
      });
      component['setBetProperties'] = jasmine.createSpy('setBetProperties');
    });

    describe('should verify selectedPoolType input parameter', () => {
      it('and should set its value to betFilter property if it is supported and is present in pool', () => {
        component.selectedPoolType = 'UTRI';
        component.ngOnInit();
        expect(component['verifyPoolType']).toHaveBeenCalledWith('UTRI');
        expect(component.betFilter).toEqual('UTRI');
      });

      describe('and should set type value of the first to betFilter property', () => {
        it('if pooltype is not provided', () => {
          component.selectedPoolType = null;
          component.ngOnInit();
          expect(component['verifyPoolType']).toHaveBeenCalledWith(null);
          expect(component.betFilter).toEqual('UEXA');
        });

        it('if provided pooltype is not supported', () => {
          component.selectedPoolType = 'USW';
          component.ngOnInit();
          expect(component['verifyPoolType']).toHaveBeenCalledWith('USW');
          expect(component.betFilter).toEqual('UEXA');
        });

        it('if provided pooltype is not present in pools', () => {
          component.selectedPoolType = 'UQDP';
          component.ngOnInit();
          expect(component['verifyPoolType']).toHaveBeenCalledWith('UQDP');
          expect(component.betFilter).toEqual('UEXA');
        });

        it('should call createPoolSwitchers', () => {
          component['createPoolSwitchers'] = jasmine.createSpy();
          component['poolSwitchers'] = [
            {
              name: 'uktote.poolType1',
              onClick: () => {},
              viewByFilters: 'poolType1'
            },
            {
              name: 'uktote.poolType2',
              onClick: () => {},
              viewByFilters: 'poolType2'
            }
          ];

          component.ngOnInit();
          expect(component['createPoolSwitchers']).toHaveBeenCalled();
        });

        it('should not call getGuidesData', () => {
          component['updateLocation'] = jasmine.createSpy('updateLocation');
          component['getPoolHeaders'] = jasmine.createSpy('getPoolHeaders').and.returnValue([]);
          component.pools = [
            {type: 'PO', poolType: 'PO', id: 3766539},
            {type: 'IU', poolType: 'IU', id: 3766540}
          ] as IUkTotePoolBet[];

          component.ngOnInit();
          expect(component['updateLocation']).toHaveBeenCalledWith(component.betFilter, true);
          expect(ukToteService.getGuidesData).not.toHaveBeenCalled();
        });
      });
    });

    describe('should update the browser location', () => {
      beforeEach(() => {
        routingHelperService.formEdpUrl.and.returnValue('edpUrl');
      });

      it('should update the browser with proper URL when "replace" argument is falsy', () => {
        component['updateLocation']('UEXA');
        expect(location.go).toHaveBeenCalledWith('edpUrl/totepool/exacta');
      });

      it('should replace the browser with proper URL when "replace" argument is true', () => {
        component['updateLocation']('UTRI', true);
        expect(location.replaceState).toHaveBeenCalledWith('edpUrl/totepool/trifecta');
      });
    });

    it('should call updateLocation', () => {
      component.doRedirect = true;
      component.betFilter = 'UEXA';
      component.ngOnInit();

      expect(component['updateLocation']).toHaveBeenCalledWith('UEXA', true);
    });

    it('should not call updateLocation', () => {
      component.doRedirect = false;
      component.ngOnInit();

      expect(component['updateLocation']).not.toHaveBeenCalled();
    });

    it('should set intTotePoolIds property', () => {
      component.ngOnInit();
      expect(component.intTotePoolIds).toEqual(intTotePoolIds);
    });

    it('should get pool guides', fakeAsync(() => {
      component.ngOnInit();
      flush();
      expect(ukToteService.getGuidesData).toHaveBeenCalledWith(
        {poolsIds: component.intTotePoolIds}
      );
      expect(component.guides).toEqual(guides);
    }));

    describe('getGuideValue', () => {
      beforeEach(() => {
        component.guides = guides;
      });

      it('should return PL pool value for PL pool', () => {
        expect(component['getGuideValue']('6', 'PL')).toEqual('5');
      });

      it('should return WN pool value for EX pool', () => {
        expect(component['getGuideValue']('6', 'EX')).toEqual('2.5');
      });

      it('should return undefined if there is no pool value for runner', () => {
        expect(component['getGuideValue']('1', 'WN')).toBeUndefined();
      });

      it('should return undefined if there is no guides', () => {
        component.guides = null;
        expect(component['getGuideValue']('1', 'WN')).toBeNull();
      });
    });

    describe('checkIsLabelsMode', () => {
      it('should return true for Win pool type', () => {
        component.betFilter = 'UWIN';
        expect(component['checkIsLabelsMode']()).toBeTruthy();
      });
      it('should return true for Place pool type', () => {
        component.betFilter = 'UPLC';
        expect(component['checkIsLabelsMode']()).toBeTruthy();
      });
      it('should return true for Win pool type', () => {
        component.betFilter = 'WN';
        expect(component['checkIsLabelsMode']()).toBeTruthy();
      });
      it('should return true for Place pool type', () => {
        component.betFilter = 'PL';
        expect(component['checkIsLabelsMode']()).toBeTruthy();
      });
      it('should return true for Execta pool type', () => {
        component.betFilter = 'EX';
        expect(component['checkIsLabelsMode']()).toBeTruthy();
      });
      it('should return true for Trifecta pool type', () => {
        component.betFilter = 'TR';
        expect(component['checkIsLabelsMode']()).toBeTruthy();
      });
      it('should return false for other pool types', () => {
        component.betFilter = 'UTRI';
        expect(component['checkIsLabelsMode']()).toBeFalsy();
      });
    });

    describe('getPoolCssClass', () => {
      it('should return Win pool type for Win pool type', () => {
        component.betFilter = 'UWIN';
        expect(component['getPoolCssClass']()).toEqual('win-pool');
      });
      it('should return Win pool type for Win pool type', () => {
        component.betFilter = 'WN';
        expect(component['getPoolCssClass']()).toEqual('win-pool');
      });
      it('should return Place pool type for Place pool type', () => {
        component.betFilter = 'UPLC';
        expect(component['getPoolCssClass']()).toEqual('place-pool');
      });
      it('should return Place pool type for Place pool type', () => {
        component.betFilter = 'PL';
        expect(component['getPoolCssClass']()).toEqual('place-pool');
      });
      it('should return Execta class for Execta pool type', () => {
        component.betFilter = 'EX';
        expect(component['getPoolCssClass']()).toEqual('execta-pool');
      });
      it('should return Trifecta class for Trifecta pool type', () => {
        component.betFilter = 'TR';
        expect(component['getPoolCssClass']()).toEqual('trifecta-pool');
      });
      it('should return empty string if not correct type', () => {
        component.betFilter = 'NTR';
        expect(component['getPoolCssClass']()).toEqual('');
      });
    });

    describe('generatePageCssClasses', () => {
      it('should add labels-mode class to classes list', () => {
        component.isLabelsMode = true;
        expect(component['generatePageCssClasses']()).toEqual({
          'uk-tote-event': true,
          'labels-mode': true,
          'checkboxes-mode': false
        });
      });
      it('should add checkboxes-mode class and pool type class', () => {
        component.isLabelsMode = false;
        component.poolCssClass = 'win-pool';
        expect(component['generatePageCssClasses']()).toEqual({
          'uk-tote-event': true,
          'labels-mode': false,
          'checkboxes-mode': true,
          'win-pool': true
        });
      });
    });

    describe('onMapUpdate method should', () => {
      it('check bet build warning message', () => {
        component.betBuilderMsg = {} as { warning: string };
        const map = {124: {'1st': 'checked'}};
        component['getBetBuilderWarning']
          = jasmine.createSpy('getBetBuilderWarning').and.returnValue('testMessage');
        component.onMapUpdate(map);
        expect(component['getBetBuilderWarning']).toHaveBeenCalledWith(map as any);
        expect(component.betBuilderMsg.warning).toEqual('testMessage');
      });
    });

    describe('getBetBuilderWarning method', () => {
      let map;

      beforeEach(() => {
        map = {
          '111': {
            '1st': 'checked',
            '2nd': 'open'
          },
          '222': {
            '1st': 'open',
            '2nd': 'open'
          }
        };
      });

      it('should return warning message if less than 2 checkboxes selected for Execta', () => {
        component.betFilter = 'EX';
        const warn = component['getBetBuilderWarning'](map);
        expect(warn.length > 0).toBeTruthy();
      });

      it('should return warning message if less than 3 checkboxes selected for Trifecta', () => {
        map = { ...map, ...{
          '333': {
            '1st': 'checked',
            '2nd': 'open'
          }
        }};
        component.betFilter = 'TR';
        const warn = component['getBetBuilderWarning'](map);
        expect(warn.length > 0).toBeTruthy();
      });

      it('should return null', () => {
        component.betFilter = 'EX';
        const warn = component['getBetBuilderWarning'](null);
        expect(warn).toBeNull();
      });
    });

    it('should get currency calculator', fakeAsync(() => {
      component.ngOnInit();

      expect(component.currencyCalculator instanceof CurrencyCalculator).toBeTruthy();

      flush();
    }));

    describe('getBetBuilderWarning method', () => {
      let map;

      beforeEach(() => {
        map = {
          '111': {
            '1st': 'checked',
            '2nd': 'open'
          },
          '222': {
            '1st': 'open',
            '2nd': 'open'
          }
        };
      });

      it('should return warning message if less than 2 checkboxes selected for Execta', () => {
        component.betFilter = 'EX';
        const warn = component['getBetBuilderWarning'](map);
        expect(warn.length > 0).toBeTruthy();
      });

      it('should return warning message if less than 3 checkboxes selected for Trifecta', () => {
        map = {...map, ...{
          '333': {
            '1st': 'checked',
            '2nd': 'open'
          }
        }};
        component.betFilter = 'TR';
        const warn = component['getBetBuilderWarning'](map);
        expect(warn.length > 0).toBeTruthy();
      });
    });

    describe('getGuides method', () => {
      it('should pluck guides from pools', () => {
        expect(component['getGuides'](poolToPoolValue)).toEqual(guides);
      });
    });

    describe('unsibscribeFromLiveUpdates method', () => {
      it('should unsibscribe from lice updates', () => {
        component.subscribedForLiveUpdates = true;
        component.channels = ['123', '456'];
        expect(component['unsibscribeFromLiveUpdates']());
        expect(component.subscribedForLiveUpdates).toBeFalsy();
        expect(component['ukTotesHandleLiveServeUpdatesService'].unsubscribe)
          .toHaveBeenCalledWith(['123', '456']);

      });

      it('shouldn\'t unsibscribe from lice updates if not subscribed yet', () => {
        component.subscribedForLiveUpdates = false;
        expect(component['unsibscribeFromLiveUpdates']());
        expect(component.subscribedForLiveUpdates).toBeFalsy();
        expect(component['ukTotesHandleLiveServeUpdatesService'].unsubscribe)
          .not.toHaveBeenCalled();

      });
    });

    describe('goToFilter method', () => {
      beforeEach(() => {
        ['verifyPoolType', 'updateLocation', 'setBetProperties'].forEach(method => {
          const bind = component[method].bind(component);
          component[method] = jasmine.createSpy(method).and.callFake(bind);
        });
        component.betFilter = 'UEXA';
        component['getPoolHeaders'] = jasmine.createSpy('getPoolHeaders').and.returnValue([]);
      });

      it('should return from method', () => {
        component['goToFilter']('UEXA');
        expect(component.betFilter).toEqual('UEXA');
        expect(component['setBetProperties']).not.toHaveBeenCalled();
        expect(component['pubSubService'].publish).not.toHaveBeenCalled();
        expect(component['gtm'].push).not.toHaveBeenCalled();
      });

      it('should update betFilter', () => {
        component['goToFilter']('USC7');
        expect(component.betFilter).toEqual('USC7');
        expect(component['setBetProperties']).toHaveBeenCalledWith(component.betFilter);
        expect(component['pubSubService'].publish)
          .toHaveBeenCalledWith('CHANGE_BET_FILTER', UK_TOTE_CONFIG.poolTypesMap[component.betFilter].path);
        expect(component['gtm'].push).toHaveBeenCalledWith('trackEvent', {
          eventCategory: 'uk tote',
          eventAction: 'tab',
          eventLabel: component['locale'].getString(`uktote.'USC7'`)
        });
      });

      it('should update betFilter(international)', () => {
        component.intTotePoolIds = <any>[{}];
        component['goToFilter']('USC7');
        expect(component.betFilter).toEqual('USC7');
        expect(component['setBetProperties']).toHaveBeenCalledWith(component.betFilter);
        expect(component['pubSubService'].publish)
        .toHaveBeenCalledWith('CHANGE_BET_FILTER', UK_TOTE_CONFIG.poolTypesMap[component.betFilter].path);
        expect(component['gtm'].push).toHaveBeenCalledWith('trackEvent', {
          eventCategory: 'international tote',
          eventAction: 'tab',
          eventLabel: component['locale'].getString(`uktote.'USC7'`)
        });
      });

      it('should call updateLocation', () => {
        component.doRedirect = true;
        component['goToFilter']('USC7');

        expect(component['updateLocation']).toHaveBeenCalledWith('USC7');
      });

      it('should not call updateLocation', () => {
        component.doRedirect = false;
        component['goToFilter']('USC7');

        expect(component['updateLocation']).not.toHaveBeenCalled();
      });
    });
  });

  describe('getMarketEntity', () => {
    it('should sort oucomes for not multiple legs pool', () => {
      component['isMultipleLegsToteBet'] = false;
      component.event = {
        markets: [
          {
            id: '1'
          } as any,
          {
            id: '2',
            outcomes: [
              {
                id: '4'
              } as any
            ]
          } as any
        ]
      } as any;
      component.chosenPoolBet = {
        marketIds: [
          '2'
        ]
      } as any;
      expect((component['getMarketEntity']('EX')).id).toEqual('2' as any);
      expect(ukToteService.sortOutcomes).toHaveBeenCalledWith([{id: '4'} as any], false);
    });
    it('should exclude unnamed favourites for Win, Place, Exacta, Trifecta', () => {
      component.event = {
        markets: [{ id: '2', outcomes: [{ id: '4' }] }]
      } as any;
      component.chosenPoolBet = { marketIds: ['2'] } as any;
      component['isMultipleLegsToteBet'] = false;
      (component as any).getMarketEntity('UEXA');
      expect(ukToteService.sortOutcomes).toHaveBeenCalledWith([{ id: '4'} as any], true);
      (component as any).getMarketEntity('UTRI');
      expect(ukToteService.sortOutcomes).toHaveBeenCalledWith([{ id: '4'} as any], true);
      (component as any).getMarketEntity('UWIN');
      expect(ukToteService.sortOutcomes).toHaveBeenCalledWith([{ id: '4'} as any], true);
      (component as any).getMarketEntity('UPLC');
      expect(ukToteService.sortOutcomes).toHaveBeenCalledWith([{ id: '4'} as any], true);
    });

    it('isMultipleLegsToteBet is true', () => {
      component['isMultipleLegsToteBet'] = true;
      expect((component['getMarketEntity']('EX'))).toBeUndefined();
    });

  });

  it('ngOnDestroy', () => {
    component['unsibscribeFromLiveUpdates'] = jasmine.createSpy('unsibscribeFromLiveUpdates');
    component.ngOnDestroy();

    expect(component['unsibscribeFromLiveUpdates']).toHaveBeenCalled();
  });

  it('trackByOutcomes should return value', () => {
    const outcome = {
      isDisplayed: true,
      id: 15,
      name: 'outcomeName',
      marketId: 5
    } as any;
    const result = component.trackByOutcomes(1, outcome);
    expect(result).toBe(`${outcome.id}_${outcome.marketId}`);
  });

  it('trackByPoolHeader should return value', () => {
    const header = 'poolHeader';
    const result = component.trackByPoolHeader(1, header);
    expect(result).toBe(`1${header}`);
  });

  it('poolHeaders should return value', () => {
    component.betFilter = 'UEXA';
    const result = component['getPoolHeaders']();
    expect(result).toEqual(['1st', '2nd', 'any']);
  });

  describe('#isSuspended', () => {
    it('should set data and return true', () => {
      const outcomeEntity = {
        id: 3
      } as any;

      component.chosenPoolBet = {
        isActive: true
      } as any;

      const result = component.isSuspended(outcomeEntity);

      expect(ukToteService.isOutcomeSuspended).toHaveBeenCalledWith(outcomeEntity);
      expect(ukToteService.isEventSuspended).toHaveBeenCalledWith(component.event);
      expect(ukToteService.isMarketSuspended).toHaveBeenCalledWith(component.event);
      expect(betBuilderService.clear).toHaveBeenCalledWith(null);
      expect(betBuilderService.clear).toHaveBeenCalledWith(outcomeEntity.id);
      expect(result).toBeTruthy();
    });

    it('should set data and return false', () => {
      const outcomeEntity = {
        nonRunner: true
      } as any;

      component.chosenPoolBet = {
        isActive: true
      } as any;

      component.event = undefined;

      ukToteService.isOutcomeSuspended = jasmine.createSpy('isOutcomeSuspended').and.returnValue(false);
      ukToteService.isEventSuspended = jasmine.createSpy('isEventSuspended').and.returnValue(component.event);
      ukToteService.isMarketSuspended = jasmine.createSpy('isMarketSuspended').and.returnValue(component.event);

      const result = component.isSuspended(outcomeEntity);

      expect(betBuilderService.clear).not.toHaveBeenCalled();
      expect(betBuilderService.clear).not.toHaveBeenCalled();
      expect(result).toBeFalsy();
    });
  });

  it('onExpand should call', () => {
    const oIndex = 1;
    component.onExpand(oIndex);
    expect(component.expandedSummary).toEqual({1: true});
  });

  it('onExpand should call when oIndex is undefined', () => {
    const oIndex = 2;
    component.expandedSummary[oIndex] = true;
    component.onExpand(oIndex);
    expect(component.expandedSummary).toEqual({2: false});
  });

  it('whatIsMessage should call', () => {
    component.betFilter = 'whatIs';

    const result = component.whatIsMessage();
    expect(locale.getString).toHaveBeenCalledWith(`uktote.${component.betFilter}`);
    expect(result).toBe('test_string');
  });

  describe('#setBetProperties', () => {
    beforeEach(() => {
      component.betFilter = 'UEXA';
      component.groupedPoolBets = {
        UEXA: {
          '1st': 'open',
          '2nd': 'open',
          any: 'open'
        }
      } as any;
    });

    it('should set data', () => {
      const betFilter = 'UEXA';
      component.chosenPoolBet = {
        marketIds: [
          '1', '2', '3'
        ]
      } as any;

      component['checkIsLabelsMode'] = jasmine.createSpy();
      component['getPoolCssClass'] = jasmine.createSpy();
      component['generatePageCssClasses'] = jasmine.createSpy();
      component['subscribeForLiveUpdates'] = jasmine.createSpy();
      component['getMarketEntity'] = jasmine.createSpy().and.returnValue({ outcomes: [] });
      component['detectSuspendedOutcomes'] = jasmine.createSpy();
      component['generateCheckboxMap'] = jasmine.createSpy();
      component['unsibscribeFromLiveUpdates'] = jasmine.createSpy();

      component['setBetProperties'](betFilter);

      expect(ukToteService.isMultipleLegsToteBet).toHaveBeenCalledWith(component.betFilter);
      expect(ukToteService.getAllIdsForEvents).toHaveBeenCalledWith([component.event]);
      expect(ukToteLiveUpdatesService.getAllChannels).toHaveBeenCalledWith(component.ids);

      expect(component.expandedSummary).toEqual({});
      expect(component['checkIsLabelsMode']).toHaveBeenCalled();
      expect(component['getPoolCssClass']).toHaveBeenCalled();
      expect(component['generatePageCssClasses']).toHaveBeenCalled();
      expect(component['getMarketEntity']).toHaveBeenCalledWith(betFilter);
      expect(component['detectSuspendedOutcomes']).toHaveBeenCalled();
      expect(component['generateCheckboxMap']).toHaveBeenCalledWith([], betFilter);
      expect(component['unsibscribeFromLiveUpdates']).toHaveBeenCalled();
      expect(component['subscribeForLiveUpdates']).toHaveBeenCalled();
      expect(betBuilderService.clear).toHaveBeenCalledWith(null);
    });

    it('should set data', () => {

      const betFilter = 'UEXA';
      ukToteService.isMultipleLegsToteBet = jasmine.createSpy().and.returnValue(true);
      component['subscribeForLiveUpdates'] = jasmine.createSpy();
      component['getMarketEntity'] = jasmine.createSpy();
      component['detectSuspendedOutcomes'] = jasmine.createSpy();
      component['generateCheckboxMap'] = jasmine.createSpy();
      component['unsibscribeFromLiveUpdates'] = jasmine.createSpy();

      component['setBetProperties'](betFilter);

      expect(ukToteService.isMultipleLegsToteBet).toHaveBeenCalledWith(component.betFilter);
      expect(ukToteService.getAllIdsForEvents).toHaveBeenCalledWith([component.event]);
      expect(ukToteLiveUpdatesService.getAllChannels).toHaveBeenCalledWith(component.ids);

      expect(component['getMarketEntity']).not.toHaveBeenCalled();
      expect(component['detectSuspendedOutcomes']).not.toHaveBeenCalled();
      expect(component['generateCheckboxMap']).not.toHaveBeenCalled();
      expect(component['unsibscribeFromLiveUpdates']).not.toHaveBeenCalled();
      expect(component['subscribeForLiveUpdates']).toHaveBeenCalled();
    });
  });

  it('detectSuspendedOutcomes should call', () => {
    component['isSuspended'] = jasmine.createSpy().and.returnValue(true);

    component['detectSuspendedOutcomes']();
    expect(component['isSuspended']).toHaveBeenCalledTimes(2);
  });

  it('detectSuspendedOutcomes should call when marketEntity is undefined', () => {
    component['isSuspended'] = jasmine.createSpy().and.returnValue(false);
    component.marketEntity = undefined;

    component['detectSuspendedOutcomes']();
    expect(component['isSuspended']).not.toHaveBeenCalledTimes(2);
  });

  it('generateCheckboxMap when poolType is empty', () => {
    const outcomes = [] as any;
    const poolType = '';

    const result = component['generateCheckboxMap'](outcomes, poolType);
    expect(result).toEqual({});
  });

  it('generateCheckboxMap when poolType is empty', () => {
    const outcomes = [
      {
        id: '1',
        name: 'someOutcomes'
      }
    ] as any;
    const poolType = 'EX';

    component['generateCheckboxMap'](outcomes, poolType);
    expect(component.outcomesMap[1]).toEqual({
      id: '1',
      name: 'someOutcomes'
    } as any);
  });

  it('should updateEvent call', () => {
    const liveUpdate = {
      id: 1,
      type: 'someType'
    } as any;
    component['detectSuspendedOutcomes'] = jasmine.createSpy();
    component['updateEvent'](liveUpdate);
    expect(ukToteLiveUpdatesService.updateEventWithLiveUpdate).toHaveBeenCalledWith(component.event, liveUpdate);
    expect(component['detectSuspendedOutcomes']).toHaveBeenCalled();
  });

  it('should subscribeForLiveUpdates call', () => {
    component['subscribeForLiveUpdates']();
    expect(storage.set).toHaveBeenCalledWith('toteLiveChannels', component.channels);
    expect(ukTotesHandleLiveServeUpdatesService.subscribe)
      .toHaveBeenCalledWith(component.channels, jasmine.any(Function));
    expect(component.subscribedForLiveUpdates).toBeTruthy();
  });

  it('should subscribeForLiveUpdates call and return undefined', () => {
    component.subscribedForLiveUpdates = true;
    const result = component['subscribeForLiveUpdates']();
    expect(storage.set).toHaveBeenCalledWith('toteLiveChannels', component.channels);
    expect(ukTotesHandleLiveServeUpdatesService.subscribe).not.toHaveBeenCalled();
    expect(result).toBeUndefined();
  });

  it('filterByPoolTypeOrder should call and order pools', () => {
    const poolsArray = ['UEXA', 'UTRI', 'TR'];
    const poolTypeOrder = ['UEXA', 'UTRI'];
    const result = component['filterByPoolTypeOrder'](poolsArray, poolTypeOrder);
    expect(result).toEqual(['UEXA', 'UTRI']);
  });

  it('filterByPoolTypeOrder should return pools without filtering', () => {
    const poolsArray = ['UEXA', 'UTRI'];
    const result = component['filterByPoolTypeOrder'](poolsArray, null);
    expect(result).toBe(poolsArray);
  });

  it('createPoolSwitchers should call', () => {
    component.poolTypes = ['poolType1', 'poolType2'];
    component['createPoolSwitchers']();
    expect(component.poolSwitchers).toEqual(
      [
        {
          name: 'uktote.poolType1',
          onClick: jasmine.any(Function),
          viewByFilters: 'poolType1'
        },
        {
          name: 'uktote.poolType2',
          onClick: jasmine.any(Function),
          viewByFilters: 'poolType2'
        },
      ]
    );
  });

  it('should call fracToDec', () => {
    fracToDecService.oddsFormat = 'frac';
    expect(component.fracToDec(9,2)).toBe('9/2');
    fracToDecService.oddsFormat = 'decimal';
    expect(component.fracToDec(9,2)).toBe('5.50');
    fracToDecService.oddsFormat = 'frac';
    expect(component.fracToDec(undefined,2)).toBe('undefined/2');
  });
});
