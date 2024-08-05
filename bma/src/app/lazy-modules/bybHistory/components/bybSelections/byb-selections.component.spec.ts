import { of, Subject, Subscription } from 'rxjs';

import { BybSelectionsComponent } from './byb-selections.component';
import { ISportEvent } from '@core/models/sport-event.model';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { IScoreboardStatsUpdate } from '@bybHistoryModule/models/scoreboards-stats-update.model';
import { IBybSelection } from '@bybHistoryModule/models/byb-selection.model';

describe('BybSelectionsComponent', () => {
  let component: BybSelectionsComponent;
  let bybSelectionsService;
  let handleScoreboardsStatsUpdatesService;
  let betTrackingService;
  let changeDetectorRef;
  let pubSubService;
  let coreToolsService;

  let callbackHandler;
  let initBetTrackerHandler;

  beforeEach(() => {
    callbackHandler = (ctrlName: string, eventName: string, callback) => {
      if (eventName === 'EVENT_STARTED') {
        initBetTrackerHandler = callback;
      }
    };

    bybSelectionsService = {
      getSortedSelections: jasmine.createSpy('getSortedSelections'),
      replaceStoredSelection: jasmine.createSpy('replaceStoredSelection'),
      hideTooltipTriggerSub: {
        subscribe: jasmine.createSpy('subscribe'),
        unsubscribe: jasmine.createSpy('unsubscribe'),
      },
    };
    handleScoreboardsStatsUpdatesService = {
      subscribeForUpdates: jasmine.createSpy('subscribeForUpdates'),
      unsubscribe: jasmine.createSpy('unsubscribe')
    };
    betTrackingService = {
      isTrackingEnabled: jasmine.createSpy('isTrackingEnabled').and.returnValue(of(true)),
      updateProgress: jasmine.createSpy('updateProgress'),
      extendSelectionsWithTrackingConfig: jasmine.createSpy('extendSelectionsWithTrackingConfig')
    };
    changeDetectorRef = {
      markForCheck: jasmine.createSpy('markForCheck'),
      detectChanges: jasmine.createSpy('detectChanges')
    };
    pubSubService = {
      subscribe: jasmine.createSpy('subscribe').and.callFake(callbackHandler),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      publishSync: jasmine.createSpy('publishSync'),
      publish: jasmine.createSpy('publish'),
      API: pubSubApi
    };
    coreToolsService = {
      uuid: jasmine.createSpy('uuid').and.returnValue('1111')
    };

    component = new BybSelectionsComponent(
      bybSelectionsService,
      handleScoreboardsStatsUpdatesService,
      betTrackingService,
      changeDetectorRef,
      pubSubService,
      coreToolsService
    );
    component.leg = {
      eventEntity: { name: 'event name', id: '123456' },
      backupEventEntity: { name: 'backup event name', id: '123456' },
      part: [{ description: 'event', eventMarketDesc: 'event' }]
    } as any;

    component.bet = {} as any;
  });

  describe('ngOnInit', () => {
    beforeEach(() => {
      component.bet = {
        event: ['123456'],
        id: '123'
      } as any;
    });

    it('should prepare selections', () => {
      component.ngOnInit();

      expect(bybSelectionsService.getSortedSelections).toHaveBeenCalledWith(component.leg);
      expect(component['subscriptionName']).toEqual('BybSelectionsComponent123-1111');
      expect(pubSubService.subscribe).toHaveBeenCalledTimes(3);
      expect(pubSubService.subscribe).toHaveBeenCalledWith('BybSelectionsComponent123-1111', 'UPDATE_BYB_BET', jasmine.any(Function));
      expect(pubSubService.subscribe).toHaveBeenCalledWith('BybSelectionsComponent123-1111', 'CLOSE_TOOLTIPS', jasmine.any(Function));
      expect(bybSelectionsService.hideTooltipTriggerSub.subscribe).toHaveBeenCalled();
    });

    it('should publish each stake height', () => {
      component.isLastBet = true; 
      component.ngOnInit();     
      expect(pubSubService.publish).toHaveBeenCalledWith('UPDATE_ITEM_HEIGHT');
    });

    it('should betTrackingEnabled to be true', () => {
      component.leg.eventEntity = {
        isStarted: true,
        id: 1234
      } as ISportEvent;
      component.ngOnInit();

      expect(betTrackingService.isTrackingEnabled).toHaveBeenCalled();
      expect(betTrackingService.extendSelectionsWithTrackingConfig).toHaveBeenCalled();
      expect(handleScoreboardsStatsUpdatesService.subscribeForUpdates).toHaveBeenCalledWith('1234');
      expect(changeDetectorRef.markForCheck).toHaveBeenCalled();
      expect(component.betTrackingEnabled).toBeTruthy();
    });

    it('should betTrackingEnabled to be true when bet is settled', () => {
      component.leg.eventEntity = {
        isStarted: true,
        id: 1234
      } as ISportEvent;

      component.ngOnInit();

      expect(betTrackingService.isTrackingEnabled).toHaveBeenCalled();
      expect(betTrackingService.extendSelectionsWithTrackingConfig).toHaveBeenCalled();
      expect(handleScoreboardsStatsUpdatesService.subscribeForUpdates).toHaveBeenCalledWith('1234');
      expect(changeDetectorRef.markForCheck).toHaveBeenCalled();
      expect(component.betTrackingEnabled).toBeTruthy();
    });

    it('should betTrackingEnabled to be false when bet is not settled and event is not started', () => {
      component.leg.eventEntity = {
        isStarted: false,
        id: 1234
      } as ISportEvent;

      component.ngOnInit();

      expect(betTrackingService.isTrackingEnabled).toHaveBeenCalled();
      expect(betTrackingService.extendSelectionsWithTrackingConfig).not.toHaveBeenCalled();
      expect(handleScoreboardsStatsUpdatesService.subscribeForUpdates).not.toHaveBeenCalledWith('1234');
      expect(changeDetectorRef.markForCheck).not.toHaveBeenCalled();
      expect(component.betTrackingEnabled).toBeFalsy();
    });

    it('should betTrackingEnabled to be false', () => {
      betTrackingService.isTrackingEnabled = jasmine.createSpy('isTrackingEnabled').and.returnValue(of(false));
      component.ngOnInit();

      expect(betTrackingService.isTrackingEnabled).toHaveBeenCalled();
      expect(component.betTrackingEnabled).toBeFalsy();
    });

    it('should create event entity from leg backupEventEntity ', () => {
      delete component.leg.eventEntity;
      component.ngOnInit();

      expect(component.eventEntity).toEqual({ name: 'backup event name', id: '123456' } as any);
    });

    it('should init bet tracking on subscription', () => {
      component['initBetTracking'] = jasmine.createSpy('initBetTracking');
      component['setIsVoided'] = jasmine.createSpy('setIsVoided');
      component.bet = {
        event: ['123456']
      } as any;
      component.ngOnInit();

      initBetTrackerHandler('123456');

      expect(component['initBetTracking']).toHaveBeenCalledTimes(2);
      expect(component.eventEntity.isStarted).toBeTruthy();
      expect(component['setIsVoided']).toHaveBeenCalled();
    });

    it('should not init bet tracking on subscription', () => {
      component['initBetTracking'] = jasmine.createSpy('initBetTracking');
      component.bet = {
        event: ['123456']
      } as any;
      component.ngOnInit();

      initBetTrackerHandler('654321');

      expect(component['initBetTracking']).toHaveBeenCalledTimes(1);
    });
  });

  describe('ngOnDestroy', () => {
    beforeEach(() => {
      component.eventEntity = { name: 'event name', id: '123456' } as any;
    });

    it('should unsubscribe from hideTooltipSubjSubscription', () => {
      component['hideTooltipSubjSubscription'] = new Subscription();
      component['hideTooltipSubjSubscription'].unsubscribe = jasmine.createSpy();
      component.ngOnDestroy();
      expect(component['hideTooltipSubjSubscription'].unsubscribe).toHaveBeenCalled();
    });

    it('should unsubscribe from betTrackingEnabled', () => {
      component['betTrackingEnabledSubscription'] = new Subscription();
      component['betTrackingEnabledSubscription'].unsubscribe = jasmine.createSpy();

      component.ngOnDestroy();

      expect(component['betTrackingEnabledSubscription'].unsubscribe).toHaveBeenCalled();
    });

    it('should not unsubscribe from betTrackingEnabled', () => {
      component['betTrackingEnabledSubscription'] = undefined;

      component.ngOnDestroy();

      expect(component['betTrackingEnabledSubscription']).not.toBeDefined();
    });

    it('should unsubscribe from betTrackingEnabled', () => {
      component.ngOnDestroy();

      expect(pubSubService.unsubscribe).toHaveBeenCalled();
    });

    it('should unsubscribe from scoreboards live updates', () => {
      component.betTrackingEnabled = true;
      component.ngOnDestroy();

      expect(handleScoreboardsStatsUpdatesService.unsubscribe).toHaveBeenCalledWith('123456');
    });

    it('should Not unsubscribe from scoreboards live updates when subscription not found', () => {
      component.betTrackingEnabled = false;
      component.ngOnDestroy();
      expect(handleScoreboardsStatsUpdatesService.unsubscribe).not.toHaveBeenCalled();
    });
  });

  it('should trackBySelectionId', () => {
    const selection = {
      part: {
        outcome: {
          id: '123456'
        }
      }
    } as any;

    expect(component.trackBySelectionId(1, selection)).toEqual('123456');
  });

  it('should updateTrackingParameters', () => {
    component.selections = {
      part: {
        outcome: {
          id: '123456'
        }
      }
    } as any;
    component.bet = {} as any;
    component['updateTrackingParameters']({} as any);

    expect(betTrackingService.updateProgress).toHaveBeenCalledWith(component.selections, component.bet, {});
  });

  describe('onLiveUpdateHandler', () => {
    it('should handle update', () => {
      component['eventEntity'] = { id: 123 } as any;
      component['onLiveUpdateHandler']({ obEventId: '123' } as IScoreboardStatsUpdate);

      expect(betTrackingService.updateProgress).toHaveBeenCalled();
      expect(changeDetectorRef.markForCheck).toHaveBeenCalled();
    });

    it('should not handle update when id is not from current event', () => {
      component['eventEntity'] = { id: 123 } as any;
      component['onLiveUpdateHandler']({ obEventId: '123123' } as IScoreboardStatsUpdate);

      expect(betTrackingService.updateProgress).not.toHaveBeenCalled();
      expect(changeDetectorRef.markForCheck).not.toHaveBeenCalled();
    });

    it('should not handle update', () => {
      component['onLiveUpdateHandler'](null);

      expect(betTrackingService.updateProgress).not.toHaveBeenCalled();
      expect(changeDetectorRef.markForCheck).not.toHaveBeenCalled();
    });
  });

  describe('toggleTooltip', () => {
    it('should show tooltip', () => {
      const event = {
        stopPropagation: jasmine.createSpy('stopPropagation'),
        target: {
          getBoundingClientRect: jasmine.createSpy('getBoundingClientRect').and.returnValue({ left: 50 })
        }
      } as any;
      const selection = { showTooltip: false, title: 'Positive' } as IBybSelection;
      component.selections = [];

      component.toggleTooltip(event, selection);

      expect(selection.showTooltip).toBeTruthy();
      expect(pubSubService.publish).toHaveBeenCalledWith('BET_TRACKER_TOOLTIP', true);
      expect(changeDetectorRef.markForCheck).toHaveBeenCalled();
    });

    it('should Get Left Margin Space', () => {
      const event = {
        stopPropagation: jasmine.createSpy('stopPropagation'),
        target: {
          getBoundingClientRect: jasmine.createSpy('getBoundingClientRect').and.returnValue({ left: 50 })
        }
      } as any;
      const selection = { showTooltip: false, title: 'Positive' } as IBybSelection;
      component.selections = [];

      component.toggleTooltip(event, selection);

      expect(selection.showTooltip).toBeTruthy();
      expect(pubSubService.publish).toHaveBeenCalledWith('BET_TRACKER_TOOLTIP', true);
      expect(changeDetectorRef.markForCheck).toHaveBeenCalled();
    });

    it('should Get Right Margin Space', () => {
      const event = {
        stopPropagation: jasmine.createSpy('stopPropagation'),
        target: {
          getBoundingClientRect: jasmine.createSpy('getBoundingClientRect').and.returnValue({ left: 50 })
        }
      } as any;
      const selection = { showTooltip: false, title: 'Title length larger then fixed check length' } as IBybSelection;
      component.selections = [];

      component.toggleTooltip(event, selection);

      expect(selection.showTooltip).toBeTruthy();
      expect(pubSubService.publish).toHaveBeenCalledWith('BET_TRACKER_TOOLTIP', true);
      expect(changeDetectorRef.markForCheck).toHaveBeenCalled();
    });

    it('should close all other tooltips and show tooltip which has been clicked', () => {
      const event = {
        stopPropagation: jasmine.createSpy('stopPropagation'),
        target: {
          getBoundingClientRect: jasmine.createSpy('getBoundingClientRect').and.returnValue({ left: 50 })
        }
      } as any;
      const selection = { showTooltip: false, title: 'Positive' } as IBybSelection;
      component.selections = [];

      component.toggleTooltip(event, selection);

      expect(selection.showTooltip).toBeTruthy();
      expect(pubSubService.publish).toHaveBeenCalledWith('BET_TRACKER_TOOLTIP', true);
      expect(changeDetectorRef.markForCheck).toHaveBeenCalled();
    });

    it('should close the tooltip', () => {
      const event = {
        stopPropagation: jasmine.createSpy('stopPropagation'),
        target: {
          getBoundingClientRect: jasmine.createSpy('getBoundingClientRect').and.returnValue({ left: 50 })
        }
      } as any;
      const selection = { showTooltip: true, title: 'Positive' } as IBybSelection;

      component.toggleTooltip(event, selection);

      expect(pubSubService.publish).toHaveBeenCalledWith('CLOSE_TOOLTIPS');
    });

    it('should Not show tooltip when event is not found', () => {
      const event = undefined;
      const selection = { showTooltip: false } as IBybSelection;

      component.toggleTooltip(event, selection);

      expect(selection.showTooltip).toBeFalsy();
    });
  });

  describe('closeSelectionsTooltips', () => {
    it('should close all selections tooltips when user tap away from tooltip', () => {
      component.selections = [{showTooltip: true} as IBybSelection];
      component['closeSelectionsTooltips']();

      expect(component.selections[0].showTooltip).toBeFalsy();
      expect(changeDetectorRef.markForCheck).toHaveBeenCalled();
    });
  });

  describe('ngOnInit', () => {

    it('should prepare selections', () => {
      component.selections = [{
        part: {
          outcomeId: '491727391'
        }
      },
      {
       part: {
        outcomeId: '491727390'
       }
     },
     {
       part: {
        outcomeId: '491727392'
       }
     },
     {
       part: {
        outcomeId: '491861050'
       }
     },
     {
       part: {
        outcomeId: '491624066'
       }
     }
   ]as IBybSelection[];
      component.betSettled = true;
      component.isFiveASideBet = true;
      component.voidBet = true;
      component.betBuilder = true;
      component.bet = {
        settled: 'Y',
        event: ['123456'],
        id: '123',
        leg: [{
          part: [{
            outcomeId: '491727391',
            'outcome': [{
              'result': { 'confirmed': 'Y', 'value': 'V' },
            }],
          },
          {
            outcomeId: '491727390',
            'outcome': [{
              'result': { 'confirmed': 'Y', 'value': 'V' },
            }],
          },
          {
            outcomeId: '491727392',
            'outcome': [{
              'result': { 'confirmed': 'Y', 'value': 'V' },
            }],
          },
          {
            outcomeId: '491861050',
            'outcome': [{
              'result': { 'confirmed': 'Y', 'value': 'V' },
            }],
          },
          {
            outcomeId: '491624066',
            'outcome': [{
              'result': { 'confirmed': 'Y', 'value': 'W' },
            }],
          },
          ]
        }]
      } as any;
        component['setIsVoided']();
       expect(component.betSettled).toBeTruthy();
       expect(component.isFiveASideBet).toBeTruthy();
       expect(component.betBuilder).toBeTruthy();
       expect(component.voidBet).toBeTruthy();
       expect(component.selections[0].isVoided).toBeTruthy();
       expect(component.selections[1].isVoided).toBeTruthy();
       expect(component.selections[2].isVoided).toBeTruthy();
       expect(component.selections[3].isVoided).toBeTruthy();
       expect(component.selections[4].isVoided).toBeFalsy();
  });
  });
  describe('should set voidedBet flag', () => {
    it('should set voidedBet, case1', () => {
      component.bet = { numLinesVoid: '1', totalStatus: 'void' } as any;
      component.ngOnInit();
      expect(component.voidedBet).toBe(true);
    });
    it('should set voidedBet, case2', () => {
      component.bet = { numLinesVoid: '0', totalStatus: 'void' } as any;
      component.ngOnInit();
      expect(component.voidedBet).toBe(false);
    });
    it('should set voidedBet, case 3', () => {
      component.bet = { numLinesVoid: '1', totalStatus: 'won' } as any;
      component.ngOnInit();
      expect(component.voidedBet).toBe(false);
    });
    it('should set voidedBet, case4', () => {
      component.bet = { numLinesVoid: '0', totalStatus: 'won' } as any;
      component.ngOnInit();
      expect(component.betSettled).toBe(false);
    });

    it('should call replaceStoredSelection', () => {
      const event = {
        stopPropagation: jasmine.createSpy('stopPropagation'),
        target: {
          getBoundingClientRect: jasmine.createSpy('getBoundingClientRect').and.returnValue({ left: 50 })
        }
      } as any;
      const selection = { showTooltip: false, title: 'Positive' } as IBybSelection;
      spyOn(component as any, 'closeSelectionsTooltips');
      component.toggleTooltip(event, selection);
      expect(bybSelectionsService.replaceStoredSelection).toHaveBeenCalledWith(selection);
    });

    it('should detectChanges must be called when triggered', () => {
      const selections = { showTooltip: true, desc: 'Result in 30mins', title: 'Positive' };
      const storedselections = { showTooltip: true, desc: 'Result in 30mins', title: 'Positive' };

      bybSelectionsService.getSortedSelections = jasmine.createSpy('getSortedSelections').and.returnValue(of(selections));
      bybSelectionsService.hideTooltipTriggerSub = new Subject();
      component.ngOnInit();
      bybSelectionsService.hideTooltipTriggerSub.next(storedselections);
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });

    it('should detectChanges must NOT be called when triggered', () => {
      const selections = { showTooltip: false, desc: 'Result in 30mins', title: 'Positive' };
      const storedselections = { showTooltip: true, desc: 'Result in 30mins', title: 'Positive' };

      bybSelectionsService.getSortedSelections = jasmine.createSpy('getSortedSelections').and.returnValue(of(selections));
      bybSelectionsService.hideTooltipTriggerSub = new Subject();
      component.ngOnInit();
      bybSelectionsService.hideTooltipTriggerSub.next(storedselections);
      expect(changeDetectorRef.detectChanges).not.toHaveBeenCalled();
    });


  });
});
