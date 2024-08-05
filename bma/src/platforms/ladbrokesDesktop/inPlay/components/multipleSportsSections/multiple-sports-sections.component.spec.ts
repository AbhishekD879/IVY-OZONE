import { of as observableOf, BehaviorSubject } from 'rxjs';
import { async } from '@angular/core/testing';
import { MultipleSportsSectionsComponent
} from '@ladbrokesDesktop/inPlay/components/multipleSportsSections/multiple-sports-sections.component';
import { inplayConfig } from '@app/inPlay/constants/config';
import { EVENTS } from '@core/constants/websocket-events.constant';

describe('MultipleSportsSectionsComponent', () => {
  let component: MultipleSportsSectionsComponent;
  let pubsubService;
  let inPlayMainService;
  let inPlayConnectionService;
  let awsService;
  let changeDetectorRef;

  beforeEach( async(() => {
    pubsubService = {
      publish: jasmine.createSpy(),
      subscribe: jasmine.createSpy(),
      unsubscribe: jasmine.createSpy(),
      API: {
        PUSH_TO_GTM: 'PUSH_TO_SPORT'
      }
    };

    inPlayConnectionService = {
      status: jasmine.createSpy(),
      setConnectionErrorState: jasmine.createSpy(),
    };

    inPlayMainService = {
      generateSwitchers: jasmine.createSpy(),
      getRibbonData: jasmine.createSpy().and.returnValue(observableOf([])),
      unsubscribeForSportCompetitionUpdates: jasmine.createSpy(),
      unsubscribeForEventsUpdates: jasmine.createSpy()
    };

    awsService = {
      addAction: jasmine.createSpy()
    };

    changeDetectorRef = {
      markForCheck: jasmine.createSpy('markForCheck'),
      detectChanges: jasmine.createSpy('detectChanges')
    };

    component = new MultipleSportsSectionsComponent(
      pubsubService,
      inPlayMainService,
      inPlayConnectionService,
      awsService,
      changeDetectorRef
    );
    component.viewByFilters = [
      'livenow',
      'upcoming'
    ];
  }));

  describe('#setDefaultFilter', () => {
    it('pubsubService should be called with upcoming', () => {
      component.showNoEventsSection = jasmine.createSpy().and.returnValue(true);
      component.goToFilter = jasmine.createSpy();

      component['setDefaultFilter']();

      expect(component.goToFilter).toHaveBeenCalledWith('upcoming');
      expect(changeDetectorRef.markForCheck).toHaveBeenCalled();
      expect(pubsubService.publish).toHaveBeenCalledWith(pubsubService.API.EVENT_COUNT, 'upcoming');
    });

    it('pubsubService should be called with livenow', () => {
      component.showNoEventsSection = jasmine.createSpy().and.returnValue(false);
      component['setFilter'] = jasmine.createSpy();

      component['setDefaultFilter']();

      expect(component['setFilter']).toHaveBeenCalledWith('livenow');
      expect(changeDetectorRef.markForCheck).toHaveBeenCalled();
      expect(pubsubService.publish).toHaveBeenCalledWith(pubsubService.API.EVENT_COUNT, 'livenow');
    });
  });

  it('ngOnDestroy', () => {
    component.ngOnDestroy();
    expect(pubsubService.unsubscribe).toHaveBeenCalledWith(component.moduleName);
  });

  it('should use OnPush strategy', () => {
    expect(MultipleSportsSectionsComponent['__annotations__'][0].changeDetection).toBe(0);
  });

  it(`should unsubscribe from 'getRibbonData' stream`, () => {
    const secondData = { data: [{ targetUriCopy: 'SubjectUriCopy' }] }as any;
    const ribbonData = { data: [{ targetUriCopy: 'UriCopy' }] } as any;
    const stream$ = new BehaviorSubject(ribbonData);
    inPlayMainService.getRibbonData.and.returnValue(stream$ as any);
    spyOn(component as any, 'getSwitchers');
    spyOn(component as any, 'setDefaultFilter');

    component.ngOnInit();


    expect(component['getSwitchers']).toHaveBeenCalledWith(ribbonData.data);

    component.ngOnDestroy();
    stream$.next(secondData);

    expect(component['getSwitchers']).toHaveBeenCalledTimes(1);
    expect(component['unsubscribe'].isStopped).toBeTruthy();
  });

  it('Should prepare showMore link from categoryName', () => {
    let result;
    result = component.getShowMoreLink('sport/football');
    expect(result).toEqual('/in-play/football');

    result = component.getShowMoreLink('sport/horse-racing');
    expect(result).toEqual('/in-play/horse-racing');
  });

  it('Should prepare showMore title from categoryName', () => {
    let result;
    result = component.getShowMoreTitle('football');
    expect(result).toEqual('view all football in-play events');

    result = component.getShowMoreTitle('FOOTBALL');
    expect(result).toEqual('view all FOOTBALL in-play events');

    result = component.getShowMoreTitle('FoOTBaLL');
    expect(result).toEqual('view all FoOTBaLL in-play events');

    result = component.getShowMoreTitle('Horse racing');
    expect(result).toEqual('view all Horse racing in-play events');

    result = component.getShowMoreTitle('Ho-rse racing');
    expect(result).toEqual('view all Ho-rse racing in-play events');
  });

  describe('ngOnChanges', () => {
    it('shoulnd not track ssError', () => {
      let changes = {};

      component.ngOnChanges(changes as any);
      expect(awsService.addAction).not.toHaveBeenCalled();

      changes = { ssError: false };
      component.ngOnChanges(changes as any);
      expect(awsService.addAction).not.toHaveBeenCalled();
    });

    it('shoulnd not track ssError', () => {
      const changes = { ssError: true };
      component.ngOnChanges(changes as any);

      expect(awsService.addAction).not.toHaveBeenCalledWith('inplay=>UI_Message=>Unavailable=>ssError');
    });
  });

  describe('#toggleSport', () => {
    it('when expanded', () => {
      const isExpanded = true;
      component['getSportData'] = jasmine.createSpy().and.returnValue(observableOf({}));
      component.toggleSport(isExpanded, {
        categoryId: 123,
        categoryCode: 'TENNIS',
        'expanded-sports-tab': false
      } as any);
      expect(component['getSportData']).toHaveBeenCalled();
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });
    it('when collapsed', () => {
      const isExpanded = false;
      const sport = {
        categoryId: 123,
        categoryCode: 'TENNIS',
        'expanded-sports-tab': true
      };
      component.filter = 'someFilter';
      component.eventsByGroups = {
        someFilter: {
          eventsBySports: [
            sport
          ]
        }
      };
      component.toggleSport(isExpanded, sport as any);
      expect(inPlayMainService.unsubscribeForSportCompetitionUpdates).toHaveBeenCalled();
      expect(inPlayMainService.unsubscribeForEventsUpdates).toHaveBeenCalled();
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });
    it('when collapsed after expand', () => {
      const isExpanded = false;
      const sport = {
        categoryId: 123,
        categoryCode: 'TENNIS',
        'expanded-sports-tab': true
      };
      component.filter = 'someFilter';
      component.eventsByGroups = {
        someFilter: {
          eventsBySports: [
            sport
          ]
        }
      };
      component['getSportData'] = jasmine.createSpy().and.callFake(() => {
        sport['expanded-sports-tab'] = isExpanded;
        return observableOf({});
      });
      component.toggleSport(isExpanded, sport as any);
      expect(inPlayMainService.unsubscribeForSportCompetitionUpdates).toHaveBeenCalled();
      expect(inPlayMainService.unsubscribeForEventsUpdates).toHaveBeenCalled();
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });
  });

  describe('socket reconnect error handler', () => {
    beforeEach(() => {
      spyOn<any>(component, 'setDefaultFilter');
      spyOn<any>(component, 'initEventsListeners');
    });


    it('should subscirbe on SOCKET_RECONNECT_ERROR', () => {
      component.ngOnInit();

      expect(pubsubService.subscribe).toHaveBeenCalledWith(component.moduleName,
        `${inplayConfig.moduleName}.${EVENTS.SOCKET_RECONNECT_ERROR}`, jasmine.any(Function));
    });

    it('should track error on SOCKET_RECONNECT_ERROR', () => {
      component['pubsubService'].subscribe = jasmine.createSpy().and.callFake((a, b, fn) => { fn(); });
      component.ngOnInit();

      expect(awsService.addAction).toHaveBeenCalledWith('inplay=>UI_Message=>Unavailable=>wsError');
    });
  });

  describe('should check ssError on init and', () => {
    beforeEach(() => {
      spyOn<any>(component, 'setDefaultFilter');
      spyOn<any>(component, 'initEventsListeners');
    });

    it('should not track error if ssError is not true', () => {
      component.ssError = false;
      component.ngOnInit();

      expect(awsService.addAction).not.toHaveBeenCalled();
    });

    it('should track error if ssError is true', () => {
      component.ssError = true;
      component.ngOnInit();

      expect(awsService.addAction).toHaveBeenCalledWith('inplay=>UI_Message=>Unavailable=>ssError');
    });
  });

  it('@reloadComponent', () => {
    spyOn(component, 'ngOnInit');
    component.reloadComponent();

    expect(component.ssError).toBe(false);
    expect(pubsubService.unsubscribe).toHaveBeenCalled();
    expect(component.ngOnInit).toHaveBeenCalled();
  });
});
