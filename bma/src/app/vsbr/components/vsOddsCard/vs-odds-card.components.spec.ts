import { fakeAsync, tick } from '@angular/core/testing';
import { of as observableOf } from 'rxjs';

import { VsOddsCardComponent } from '@app/vsbr/components/vsOddsCard/vs-odds-card.component';
import { IVirtualSportEventEntity } from '@app/vsbr/models/virtual-sports-event-entity.model';

describe('VsOddsCardComponent', () => {
  let component: VsOddsCardComponent;

  const event = {
    stopPropagation: jasmine.createSpy('stopPropagation')
  } as any;

  const filter = {
    orderBy: jasmine.createSpy('orderBy'),
    groupBy: jasmine.createSpy()
  } as any;
  const cms = {
    getSystemConfig: jasmine.createSpy().and.returnValue(observableOf({ Betslip: 'Betslip' }))
  } as any;
  const user = {} as any;
  const pubsub = {
    publish: jasmine.createSpy(),
    API: {
      ADD_TO_BETSLIP_BY_SELECTION: 'ADD_TO_BETSLIP_BY_SELECTION',
      LAST_MADE_BET: 'LAST_MADE_BET'
    }
  } as any;
  const betSlipSelectionsData = {
    count: jasmine.createSpy(),
    getSelectionsByOutcomeId: jasmine.createSpy()
  } as any;
  const priceOddsButtonService = {
    animate: jasmine.createSpy()
  } as any;
  const gtmTrackingService = {
    detectVirtualSportTracking: jasmine.createSpy()
  } as any;
  const commandService = {
    API: {IS_ADDTOBETSLIP_IN_PROCESS: 'IS_ADDTOBETSLIP_IN_PROCESS'},
    executeAsync: jasmine.createSpy('executeAsync').and.returnValue(Promise.resolve(false))
  } as any;

  beforeEach(fakeAsync(() => {
    component = new VsOddsCardComponent(
      filter,
      cms,
      user,
      pubsub,
      betSlipSelectionsData,
      priceOddsButtonService,
      gtmTrackingService,
      commandService
    );

    component.currentEvent = {
      event: {
        className: 'Virtual Grand National',
        name: 'Race of Champions'
      }
    } as IVirtualSportEventEntity;

    component.templateMarketName = 'Test';
  }));

  it('should create VsOddsCardComponent instance', () => {
    expect(component).toBeTruthy();
  });

  describe('@ngOnInit', () => {
    it('ngOnInit', () => {
      component.ngOnInit();

      expect(cms.getSystemConfig).toHaveBeenCalled();
    });

    it('should not set max bets amount', () => {
      cms.getSystemConfig.and.returnValue(observableOf({}));
      component.ngOnInit();
      expect(component['maxBetsAmount']).not.toBeDefined();
    });
  });

  describe('@onPriceOddsButtonClick', () => {
    const outcome = {
      children: [{
        price: {}
      }]
    } as any;

    it('should execute async check', () => {
      component['addToBetSlip'] = jasmine.createSpy('addToBetSlip');
      component.onPriceOddsButtonClick(event, outcome);

      expect(event.stopPropagation).toHaveBeenCalled();
      expect(commandService.executeAsync).toHaveBeenCalledWith('IS_ADDTOBETSLIP_IN_PROCESS');
    });

    it('after check should add to betslip if not in progress', fakeAsync(() => {
      component['addToBetSlip'] = jasmine.createSpy('addToBetSlip');
      component.onPriceOddsButtonClick(event, outcome);
      tick();

      expect(component['addToBetSlip']).toHaveBeenCalledWith(event, outcome);
    }));

    it('after check should not add to betslip if still in progress', fakeAsync(() => {
      component['addToBetSlip'] = jasmine.createSpy('addToBetSlip');
      commandService.executeAsync.and.returnValue(Promise.resolve(true));
      component.onPriceOddsButtonClick(event, outcome);
      tick();

      expect(component['addToBetSlip']).not.toHaveBeenCalledWith(event, outcome);
    }));
  });

  describe('addToBetSlip', () => {
    let event1;
    let outcome;
    let pubSubPublishResult;

    beforeEach(() => {
      event1 = {};
      pubSubPublishResult = {};
      outcome = {
        children: [{
          price: {}
        }]
      };
      component.gtmModuleTitle = 'gtmModuleTitle';
      component.currentEvent = {
        event: {
          categoryId: '1',
          typeId: '1',
          id: '1'
        }
      } as any;

      priceOddsButtonService.animate.and.returnValue(Promise.resolve());
      gtmTrackingService.detectVirtualSportTracking.and.returnValue({});
      pubsub.publish.and.callFake((chanel: string, data: any) => {
        if (chanel === 'ADD_TO_BETSLIP_BY_SELECTION') {
          pubSubPublishResult = data;
        }
      });
    });

    it('should detecting GTM origin', () => {
      component.addToBetSlip(event1 as any, outcome as any);

      expect(gtmTrackingService.detectVirtualSportTracking).toHaveBeenCalledWith('virtual edp', component.currentEvent);
    });

    it('should publish to ADD_TO_BETSLIP_BY_SELECTION with betData and tracking props', fakeAsync(() => {
      component.addToBetSlip(event1 as any, outcome as any);

      expect(pubsub.publish).toHaveBeenCalledWith('ADD_TO_BETSLIP_BY_SELECTION', jasmine.any(Object));
      tick();
      expect(pubSubPublishResult.GTMObject &&
        pubSubPublishResult.GTMObject.tracking &&
        pubSubPublishResult.GTMObject.betData).toBeTruthy();
    }));

    it('should publish to ADD_TO_BETSLIP_BY_SELECTION without betData and tracking props', fakeAsync(() => {
      gtmTrackingService.detectVirtualSportTracking.and.returnValue(null);
      component.addToBetSlip(event as any, outcome as any);

      expect(pubsub.publish).toHaveBeenCalledWith('ADD_TO_BETSLIP_BY_SELECTION', jasmine.any(Object));
      tick();
      expect(pubSubPublishResult.GTMObject && pubSubPublishResult.GTMObject.tracking).toBeFalsy();
    }));

    it('should publish bet with in-play to ADD_TO_BETSLIP_BY_SELECTION', fakeAsync(() => {
      component.currentEvent.event.eventIsLive = true;

      component.addToBetSlip(event as any, outcome as any);

      expect(pubsub.publish).toHaveBeenCalledWith('ADD_TO_BETSLIP_BY_SELECTION', jasmine.any(Object));
      tick();
      expect(pubSubPublishResult.GTMObject &&
        pubSubPublishResult.GTMObject.betData.dimension62 === 1).toBeTruthy();
    }));

    it('should publish bet with BYB to ADD_TO_BETSLIP_BY_SELECTION', fakeAsync(() => {
      component['env'].BYB_CONFIG.HR_YC_EVENT_TYPE_ID = 1;

      component.addToBetSlip(event as any, outcome as any);

      expect(pubsub.publish).toHaveBeenCalledWith('ADD_TO_BETSLIP_BY_SELECTION', jasmine.any(Object));
      tick();
      expect(pubSubPublishResult.GTMObject &&
        pubSubPublishResult.GTMObject.betData.dimension63 === 1).toBeTruthy();
    }));

    it('should not add to betslip', fakeAsync(() => {
      pubsub.publish.calls.reset();
      component.currentEvent = null;
      component.addToBetSlip({} as any, {} as any);
      tick();
      expect(pubsub.publish).not.toHaveBeenCalledWith('ADD_TO_BETSLIP_BY_SELECTION', jasmine.any(Object));
    }));

    it('dimesion180 with virtual', () => {
      component.currentEvent.event.categoryId = '39';
      component.addToBetSlip(event1 as any, outcome as any);

      expect(gtmTrackingService.detectVirtualSportTracking).toHaveBeenCalledWith('virtual edp', component.currentEvent);
    });
  });

  describe('@getEventData', () => {
    beforeEach(() => {
      component.eventOutcomes = [{
        outcome: {
          name: 'H',
          outcomeMeaningMinorCode: 1,
          displayOrder: 1,
          children: [{
            price: { priceDec: 2 }
          }]
        }
      }, {
        outcome: {
          name: 'D',
          outcomeMeaningMinorCode: 2,
          displayOrder: 2,
          children: [{
            price: { priceDec: 2 }
          }]
        }
      }, {
        outcome: {
          name: 'A',
          outcomeMeaningMinorCode: 3,
          displayOrder: 3,
          children: [{
            price: { priceDec: 1 }
          }]
        }
      }] as any;
    });

    it('it should sort outcomes for WinEw template', () => {
      const result = [{
        outcome: {
          name: 'A',
          outcomeMeaningMinorCode: 3,
          displayOrder: 3,
          children: [{
            price: { priceDec: 1 }
          }]
        }
      }, {
        outcome: {
          name: 'D',
          outcomeMeaningMinorCode: 2,
          displayOrder: 2,
          children: [{
            price: { priceDec: 2 }
          }]
        }
      }, {
        outcome: {
          name: 'H',
          outcomeMeaningMinorCode: 1,
          displayOrder: 1,
          children: [{
            price: { priceDec: 2 }
          }]
        }
      }] as any;

      component.template = 'WinEw';
      expect(component['getEventData']()).toEqual(result);
    });

    it('it should sort outcomes for Column template', () => {
      const result = [{
        outcome: {
          name: 'H',
          outcomeMeaningMinorCode: 1,
          displayOrder: 1,
          children: [{
            price: { priceDec: 2 }
          }]
        }
      }, {
        outcome: {
          name: 'D',
          outcomeMeaningMinorCode: 2,
          displayOrder: 2,
          children: [{
            price: { priceDec: 2 }
          }]
        }
      }, {
        outcome: {
          name: 'A',
          outcomeMeaningMinorCode: 3,
          displayOrder: 3,
          children: [{
            price: { priceDec: 1 }
          }]
        }
      }] as any;

      component.template = 'Column';
      expect(component['getEventData']()).toEqual(result);
    });

    it('it should sort outcomes for Horizontal template', () => {
      const result = [{
        outcome: {
          name: 'H',
          outcomeMeaningMinorCode: 1,
          displayOrder: 1,
          children: [{
            price: { priceDec: 2 }
          }]
        }
      }, {
        outcome: {
          name: 'D',
          outcomeMeaningMinorCode: 2,
          displayOrder: 2,
          children: [{
            price: { priceDec: 2 }
          }]
        }
      }, {
        outcome: {
          name: 'A',
          outcomeMeaningMinorCode: 3,
          displayOrder: 3,
          children: [{
            price: { priceDec: 1 }
          }]
        }
      }] as any;

      component.template = 'Horizontal';
      expect(component['getEventData']()).toEqual(result);
    });

    it('it should sort outcomes for Vertical template', () => {
      const result = [{
        outcome: {
          name: 'A',
          outcomeMeaningMinorCode: 3,
          displayOrder: 3,
          children: [{
            price: { priceDec: 1 }
          }]
        }
      }, {
        outcome: {
          name: 'H',
          outcomeMeaningMinorCode: 1,
          displayOrder: 1,
          children: [{
            price: { priceDec: 2 }
          }]
        }
      }, {
        outcome: {
          name: 'D',
          outcomeMeaningMinorCode: 2,
          displayOrder: 2,
          children: [{
            price: { priceDec: 2 }
          }]
        }
      }] as any;

      component.template = 'Vertical';
      expect(component['getEventData']()).toEqual(result);
    });

    it('it should sort outcomes by price and group by name', () => {
      component.templateMarketName = 'Correct Score (game)';
      component.eventOutcomes = [{
        outcome: {
          name: 'H 1-0',
          outcomeMeaningMinorCode: 1,
          displayOrder: 1,
          children: [{
            price: { priceDec: 2 }
          }]
        }
      }, {
        outcome: {
          name: 'H 1-1',
          outcomeMeaningMinorCode: 1,
          displayOrder: 1,
          children: [{
            price: { priceDec: 1 }
          }]
        }
      }, {
        outcome: {
          name: 'A 1-0',
          outcomeMeaningMinorCode: 3,
          displayOrder: 3,
          children: [{
            price: { priceDec: 2 }
          }]
        }
      }, {
        outcome: {
          name: 'A 1-1',
          outcomeMeaningMinorCode: 3,
          displayOrder: 3,
          children: [{
            price: { priceDec: 1 }
          }]
        }
      }] as any;

      const result = [
        {
          outcome: {
            name: 'A 1-1',
            outcomeMeaningMinorCode: 3,
            displayOrder: 3,
            children: [{
              price: { priceDec: 1 }
            }]
          }
        }, {
          outcome: {
            name: 'A 1-0',
            outcomeMeaningMinorCode: 3,
            displayOrder: 3,
            children: [{
              price: { priceDec: 2 }
            }]
          }
        }, {
          outcome: {
            name: 'H 1-1',
            outcomeMeaningMinorCode: 1,
            displayOrder: 1,
            children: [{
              price: { priceDec: 1 }
            }]
          }
        }, {
          outcome: {
            name: 'H 1-0',
            outcomeMeaningMinorCode: 1,
            displayOrder: 1,
            children: [{
              price: { priceDec: 2 }
            }]
          }
        }] as any;

      component.template = 'Vertical';
      component.templateMarketName = 'Correct score (Game)';
      expect(component['getEventData']()).toEqual(result);
    });
  });

  it('trackOutcomeById', () => {
    expect(
      component.trackOutcomeById(0, { outcome: { id: 1 } } as any)
    ).toBe('0_1');
  });

  it('trackGroupedOutcomes', () => {
    const outcomes: any[] = [
      { outcome: { id: 1 } },
      { outcome: { id: 2 } },
    ];
    expect(component.trackGroupedOutcomes(0, outcomes)).toEqual('0_1_2');
  });

  it('getGroupedEventsData', () => {
    filter.groupBy.and.returnValue({
      'outcome3': { outcomeMeaningMinorCode: 3 },
      'outcome1': { outcomeMeaningMinorCode: 1 },
      'outcome2': { outcomeMeaningMinorCode: 2 }
    });
    expect(
      component.getGroupedEventsData()
    ).toEqual([
      { outcomeMeaningMinorCode: 1 },
      { outcomeMeaningMinorCode: 2 },
      { outcomeMeaningMinorCode: 3 }
    ] as any);
  });

  describe('outputPrice', () => {
    it('should return fractional price', () => {
      user.oddsFormat = 'frac';
      expect(component.outputPrice({ priceNum: 1, priceDen: 2 })).toBe('1/2');
    });

    it('should return decimal price', () => {
      user.oddsFormat = 'dec';
      expect(component.outputPrice({ priceDec: 1.1 } as any)).toBe('1.10');
    });
  });

  describe('isActiveClass', () => {
    it('should return true', () => {
      betSlipSelectionsData.count.and.returnValue(2);
      betSlipSelectionsData.getSelectionsByOutcomeId.and.returnValue([
        { price: { priceType: 'SP' } }, { price: { priceType: 'LP' }}
      ]);
      component['maxBetsAmount'] = 10;
      expect(component.isActiveClass('1', 'LP')).toBeTruthy();
    });

    it('should return false', () => {
      betSlipSelectionsData.count.and.returnValue(2);
      component['maxBetsAmount'] = 1;
      expect(component.isActiveClass('1', 'LP')).toBeFalsy();
    });
  });

  describe('getOutcomeHandicap', () => {
    it('shoud return hendicap', () => {
      const outcome: any = {
        outcomeMeaningMajorCode: 'HW',
        children: [{
          price: { rawHandicapValue: '1.5', handicapValueDec: '1.5,' }
        }]
      };
      expect(component['getOutcomeHandicap'](outcome)).toEqual({ type: 'HW', raw: '1.5' });
    });

    it('shoud not return hendicap', () => {
      const outcome: any = { children: [{ price: {} }] };
      expect(component['getOutcomeHandicap'](outcome)).toBeUndefined();
    });
  });
});
