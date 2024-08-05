import { of as observableOf, empty as emptyObservable } from 'rxjs';

import { pubSubApi } from '@app/core/services/communication/pubsub/pubsub-api.constant';
import { InPlayLiveStreamComponent } from './inplay-live-stream.component';

describe('CDInPlayLiveStreamComponent', () => {
  let component: InPlayLiveStreamComponent;

  const testStr = 'TestString';

  let pubSubService;
  let inplayHelperService;
  let inPlayLiveStreamService;
  let inplayMainService;
  let changeDetectorRef;
  let sportsConfigService;

  beforeEach(() => {
    changeDetectorRef = {
      detectChanges: jasmine.createSpy('detectChanges')
    };

    pubSubService = {
      API: pubSubApi,
      subscribe: jasmine.createSpy('subscribe'),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      publish: jasmine.createSpy('publish')
    };

    inplayHelperService = {
      getRibbonData: jasmine.createSpy().and.returnValue(observableOf({ items: [{ categoryName: testStr }] })),
      subscribe4RibbonUpdates: () => {},
      subscribeForSportCompetitionChanges: () => {},
      unsubscribe4RibbonUpdates: () => {},
      unsubscribeForSportCompetitionChanges: () => {},
      unsubscribeForLiveUpdates: () => {},
      disconnect: jasmine.createSpy('disconnect')
    };

    inPlayLiveStreamService = {
      generateSwitchers: jasmine.createSpy(),
      getData: jasmine.createSpy().and.returnValue(observableOf({})),
      removeCompetitionFromCollection: jasmine.createSpy(),
      sendGTM: jasmine.createSpy('sendGTM'),
      prepareFooter: jasmine.createSpy('prepareFooter'),
      removeEventFromCollection: jasmine.createSpy('removeEventFromCollection')
    };

    inplayMainService = jasmine.createSpyObj(['unsubscribeForUpdates']);

    sportsConfigService = {
      getSport: jasmine.createSpy('getSport').and.returnValue(observableOf({}))
    };

    component = new InPlayLiveStreamComponent(
      pubSubService,
      inplayHelperService,
      inPlayLiveStreamService,
      inplayMainService,
      changeDetectorRef,
      sportsConfigService
    );

    component.events = [];
  });

  it('should create component instance', () => {
    expect(component).toBeTruthy();
  });

  describe('ngOnInit', () => {
    beforeEach(() => {
      spyOn(component, 'getData').and.returnValue(emptyObservable());
      pubSubService.subscribe.and.callFake((p1, p2, cb) => {
        if (p2 === pubSubService.API.SPORT_CHANGED) {
          cb({ categoryName: 'category name' });
        }
      });
    });

    it('should set categoryName', () => {
      component.ngOnInit();
      expect(component.categoryName).toEqual('category name');
    });

    it('categoryName should be in lowercase', () => {
      component.ngOnInit();
      expect(component.categoryName).toEqual(component.categoryName.toLowerCase());
    });

    it('competition should be deleted from cache and activeFilter is livenow', () => {
      const data = {
        removed: [
          '123'
        ],
        added: []
      };
      component.categoryId = 21;
      component.activeFilter = 'livenow'
      pubSubService.subscribe.and.callFake((cSyncName, method, cb) => {
        if (method === 'INPLAY_LS_COMPETITION_REMOVED') {
          cb(data);
        }
        if (method === 'RELOAD_IN_PLAY') {
          spyOn(component, 'ngOnInit');
          spyOn(component, 'ngOnDestroy');

          cb();

          expect(component.ngOnDestroy).toHaveBeenCalled();
          expect(component.ngOnInit).toHaveBeenCalled();
        }
      });

      component.ngOnInit();
      expect(pubSubService.subscribe)
        .toHaveBeenCalledWith(component.cSyncName, 'INPLAY_LS_COMPETITION_REMOVED', jasmine.any(Function));
      expect(inPlayLiveStreamService.removeCompetitionFromCollection).toHaveBeenCalledWith(component.competitions, data.removed);
      expect(component.getData).toHaveBeenCalled();
    });
    it('should delete competition from cache and activeFilter is livestream', () => {
      const data = {
        removed: [
          '123'
        ],
        added: []
      };
      component.categoryId = 21;
      component.activeFilter = 'livestream'
      pubSubService.subscribe.and.callFake((cSyncName, method, cb) => {
        if (method === 'INPLAY_LS_COMPETITION_REMOVED') {
          cb(data);
        }
        if (method === 'RELOAD_IN_PLAY') {
          spyOn(component, 'ngOnInit');
          spyOn(component, 'ngOnDestroy');

          cb();

          expect(component.ngOnDestroy).toHaveBeenCalled();
          expect(component.ngOnInit).toHaveBeenCalled();
        }
      });

      component.ngOnInit();
      expect(pubSubService.subscribe)
        .toHaveBeenCalledWith(component.cSyncName, 'INPLAY_LS_COMPETITION_REMOVED', jasmine.any(Function));
      expect(inPlayLiveStreamService.removeCompetitionFromCollection).toHaveBeenCalledWith(component.competitions, data.removed);
      expect(component.getData).toHaveBeenCalled();
    });

   it('should re-use current state when re-init',   () => {
     component.activeFilter = component.viewByFilters[1];
     component.categoryName = 'tennis';
     component.categoryId = 34;

     component.ngOnInit();

     expect(inplayHelperService.getRibbonData).toHaveBeenCalledWith(component.requestConfigLiveStream);

     component.categoryName = 'tennis';
     component.categoryId = 34;
     expect(component.categoryName).toEqual('tennis');
     expect(component.categoryId).toEqual(34);
   });
  });

  describe('updateActiveEvent', () => {
    it('update active elem', () => {
      expect(component.activeEvent).toEqual(undefined);
      component.updateActiveEvent({value: 12021982} as any);
      expect(component.activeEvent).toEqual(12021982 as any);
    });
  });

  describe('getData', () => {
    let args;

    beforeEach(() => {
      args = [123, 'name', {requestParams: {}} as any, true];
    });

    it('should set loading flag staring the load process', () => {
      component.loading = false;
      component.menuItems = [] as any;
      component.getData(args[0], args[1], args[2], args[3]);

      expect(component['changeDetectorRef'].detectChanges).toHaveBeenCalled();
      expect(component.loading).toBe(true);
      expect(inPlayLiveStreamService.getData).toHaveBeenCalledWith(args[0], args[1], args[2], jasmine.any(Array));
    });

    it('should set loading flag finishing the load process', () => {
      component.loading = false;
      component.menuItems = [] as any;
      const stream$ = component.getData(args[0], args[1], args[2], args[3]);

      expect(component.loading).toBe(true);
      expect(inPlayLiveStreamService.getData).toHaveBeenCalledWith(args[0], args[1], args[2], jasmine.any(Array));

      stream$.subscribe(() => {
        expect(component.loading).toBe(false);
        expect(component['changeDetectorRef'].detectChanges).toHaveBeenCalled();
      });
    });
  });

  it('should disconnect onDestroy', () => {
    component['sportsConfigSubscription'] = {
      unsubscribe: jasmine.createSpy('unsubscribe')
    } as any;

    component.ngOnDestroy();

    expect(inplayHelperService.disconnect).toHaveBeenCalled();
    expect(component['sportsConfigSubscription'].unsubscribe).toHaveBeenCalled();
  });
});
