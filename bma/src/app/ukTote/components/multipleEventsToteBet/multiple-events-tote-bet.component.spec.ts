import { fakeAsync, tick } from '@angular/core/testing';
import { of } from 'rxjs';

import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { MultipleEventsToteBetComponent } from './multiple-events-tote-bet.component';

describe('MultipleEventsToteBetComponent', () => {
  let ukTotesHandleLiveServeUpdatesService;
  let ukToteLiveUpdatesService;
  let ukToteBetBuilderService;
  let multipleEventsToteBetService;
  let ukToteService;
  let storageService;
  let pubSubService;
  let component: MultipleEventsToteBetComponent;

  beforeEach(() => {
    ukTotesHandleLiveServeUpdatesService = {
      subscribe: jasmine.createSpy('subscribe'),
      unsubscribe: jasmine.createSpy('unsubscribe')
    };
    ukToteLiveUpdatesService = {
      getAllChannels: jasmine.createSpy('getAllChannels')
    };
    ukToteBetBuilderService = {
      add: jasmine.createSpy('add')
    };
    multipleEventsToteBetService = {
      setRacingForm: jasmine.createSpy('setRacingForm').and.returnValue(of([])),
      changeLegsWithLiveUpdate: jasmine.createSpy('changeLegsWithLiveUpdate')
    };
    ukToteService = {
      loadEventsByMarketIds: jasmine.createSpy('loadEventsByMarketIds').and.returnValue(Promise.resolve([])),
      extendToteEvents: jasmine.createSpy('extendToteEvents').and.returnValue(of([])),
      getAllIdsForEvents: jasmine.createSpy('getAllIdsForEvents')
    };
    storageService = {
      set: jasmine.createSpy('set')
    };
    pubSubService = {
      API: pubSubApi,
      subscribe: jasmine.createSpy('subscribe'),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      publishSync: jasmine.createSpy('publishSync'),
      publish: jasmine.createSpy('publish')
    };

    component = new MultipleEventsToteBetComponent(
      ukTotesHandleLiveServeUpdatesService,
      ukToteLiveUpdatesService,
      ukToteBetBuilderService,
      multipleEventsToteBetService,
      ukToteService,
      storageService,
      pubSubService
    );

    component.potBet = {
      isSuspended: false,
      legs: [
        {
          name: 'oneLeg',
          linkedMarketId: 11,
          index: 1,
          filled: false,
          isSuspended: false
        }
      ],
      pool: {
        id: 3,
        type: 'poolType'
      }
    } as any;

    component.legFilter = 1;

    component.legSwitchers = [
      {
        viewByFilters: '1',
        name: 'swither1',
        filled: true,
        suspended: false,
        onClick: () => {},
      },
      {
        viewByFilters: '2',
        name: 'swither2',
        filled: true,
        onClick: () => {}
      } as any
    ];

    component.poolBetVal = {
      marketIds: ['1']
    } as any;
  });

  it('ngOnInit', fakeAsync(() => {
    component.ngOnInit();
    tick();
    expect(ukToteService.loadEventsByMarketIds).toHaveBeenCalledTimes(1);
    expect(ukToteService.extendToteEvents).toHaveBeenCalledTimes(1);
    expect(multipleEventsToteBetService.setRacingForm).toHaveBeenCalledTimes(1);
    expect(pubSubService.subscribe).toHaveBeenCalledTimes(1);
    expect(pubSubService.publishSync).toHaveBeenCalledTimes(1);
  }));

  it('ngOnInit (error)', fakeAsync(() => {
    ukToteService.loadEventsByMarketIds.and.returnValue(Promise.reject(null));
    component.ngOnInit();
    tick();
    expect(ukToteService.extendToteEvents).not.toHaveBeenCalled();
    expect(component.loading).toBeFalsy();
    expect(component.requestFailed).toBeTruthy();
  }));

  it('ngOnChanges', () => {
    component.ngOnInit = jasmine.createSpy();

    component.ngOnChanges({
      poolBetVal: {
        currentValue: 'newValue',
        previousValue: 'oldValue'
      }
    } as any);
    expect(component.ngOnInit).toHaveBeenCalled();
  });


  it('ngOnChanges currentValue is empty', () => {
    component.ngOnInit = jasmine.createSpy();

    component.ngOnChanges({
      poolBetVal: {
        currentValue: '',
        previousValue: 'oldValue'
      }
    } as any);
    expect(component.ngOnInit).not.toHaveBeenCalled();
  });

  it('ngOnDestroy ', () => {
    component['unsubscribeFromLiveUpdates'] = jasmine.createSpy();

    component.ngOnDestroy();
    expect(component['unsubscribeFromLiveUpdates']).toHaveBeenCalled();
    expect(pubSubService.unsubscribe).toHaveBeenCalledWith('multipleEventsToteBet');
  });

  it('chosenPoolLeg', () => {
    const result = component.chosenPoolLeg;
    expect(result).toEqual(component.potBet.legs[0]);
  });

  it('updateSwitcher', () => {
    component['triggerBetBuilder'] = jasmine.createSpy();
    const leg = {
      name: 'someLeg',
      index: '1',
      filled: false,
    } as any;

    component.updateSwitcher(leg);
    expect(component['triggerBetBuilder']).toHaveBeenCalled();
  });

  it('createLegsSwitchers', () => {
    component['goToFilter'] = jasmine.createSpy();
    component['createLegsSwitchers']();

    expect(component.legSwitchers).toEqual([
      {
        viewByFilters: 1,
        name: 'oneLeg',
        filled: false,
        suspended: false,
        onClick: jasmine.any(Function)
      } as any
    ]);
    component.legSwitchers[0].onClick();
    expect(component['goToFilter']).toHaveBeenCalledWith(component.potBet.legs[0].index);
  });

  it('triggerBetBuilder', ()  => {
    component['triggerBetBuilder']();

    expect(ukToteBetBuilderService.add).toHaveBeenCalledWith({
      betModel: component.potBet,
      poolType: component.potBet.pool.type
    });
  });

  it('updateLeg', () => {
    component['setBetStatus'] = jasmine.createSpy();
    const liveUpdate = {
      id: 7,
      type: 'type'
    } as any;

    component['updateLeg'](liveUpdate);
    expect(multipleEventsToteBetService.changeLegsWithLiveUpdate)
      .toHaveBeenCalledWith(component.potBet.legs, liveUpdate);
    expect(component['setBetStatus']).toHaveBeenCalled();
  });

  it('unsubscribeFromLiveUpdates', () => {
    component['unsubscribeFromLiveUpdates']();
    expect(ukTotesHandleLiveServeUpdatesService.unsubscribe).toHaveBeenCalledWith(component['channels']);
  });

  it('goToFilter when this.legFilter === legFilter', () => {
    const legFilter = 1;

    const result = component['goToFilter'](legFilter);
    expect(pubSubService.publish).not.toHaveBeenCalled();
    expect(result).toBeUndefined();
  });

  it('goToFilter  when this.legFilter !== legFilter', () => {
    const legFilter = 3;

    component['goToFilter'](legFilter);
    expect(component.legFilter).toBe(legFilter);
    expect(pubSubService.publish).toHaveBeenCalledWith(pubSubService.API.RELOCATE_BET_BUILDER);
  });
  describe('reloadComponent', () => {
    it('should call onDestroy and onInit', () => {
      spyOn(component as any, 'ngOnInit');
      spyOn(component as any, 'ngOnDestroy');
      component.reloadComponent();
      expect(component.ngOnDestroy).toHaveBeenCalled();
      expect(component.ngOnInit).toHaveBeenCalled();
    });
  });
});
