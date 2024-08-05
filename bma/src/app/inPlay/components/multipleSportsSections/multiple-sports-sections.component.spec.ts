import { of, throwError } from 'rxjs';
import { fakeAsync, flush, tick } from '@angular/core/testing';

import { MultipleSportsSectionsComponent } from '@app/inPlay/components/multipleSportsSections/multiple-sports-sections.component';
import { inplayConfig } from '@app/inPlay/constants/config';
import { EVENTS } from '@core/constants/websocket-events.constant';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';

describe('#MultipleSportsSectionsComponent', () => {
  let component: MultipleSportsSectionsComponent;
  let inPlayMainService,
    inPlayConnectionService,
    routingHelperService,
    stickyVirtualScrollerService,
    cmsService,
    getSportDataErrorCase,
    awsService,
    pubsubService,
    changeDetectorRef;

  beforeEach(() => {
    cmsService = {
      getSystemConfig: jasmine.createSpy('getSystemConfig').and.returnValue(of({
        'VirtualScrollConfig': {
          enabled: true
        }
      }))
    };

    inPlayConnectionService = {
      status: jasmine.createSpy('status'),
      setConnectionErrorState: jasmine.createSpy('setConnectionErrorState'),
    };

    inPlayMainService = {
      generateSwitchers: jasmine.createSpy('generateSwitchers'),
      getSportData: jasmine.createSpy('getSportData').and.callFake(() => {
        switch (getSportDataErrorCase) {
          case 1: return of(null);
          case 2: return of({});
          case 3: return of({
            error: 'error'
          });
        }
      }),
      getRibbonData: jasmine.createSpy().and.returnValue(of([])),
      getTopLevelTypeParameter: jasmine.createSpy(),
      getLevelIndex: jasmine.createSpy().and.returnValue(0),
      unsubscribeForSportCompetitionUpdates: jasmine.createSpy(),
      unsubscribeForEventsUpdates: jasmine.createSpy(),
      getSportConfigSafe: jasmine.createSpy().and.returnValue(of({
        config: {
          tier: 1
        }
      })),
      getSportName: jasmine.createSpy().and.returnValue('football'),
      extendSectionWithSportInstance: jasmine.createSpy()
    };

    routingHelperService = {
      formInplayUrl: jasmine.createSpy('formInplayUrl'),
      formSportCompetitionsUrl: jasmine.createSpy()
    };

    stickyVirtualScrollerService = {
      stick: jasmine.createSpy('stick'),
      destroyEvents: jasmine.createSpy('destroyEvents'),
      updateScrollVisibility: jasmine.createSpy('updateScrollVisibility'),
    };

    awsService = {
      addAction: jasmine.createSpy()
    };

    pubsubService = {
      subscribe: jasmine.createSpy('subscribe'),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      publish: jasmine.createSpy('publish'),
      API: pubSubApi
    };
    changeDetectorRef = jasmine.createSpyObj('changeDetectorRef', ['detectChanges']);

    component = new MultipleSportsSectionsComponent(
      stickyVirtualScrollerService,
      inPlayMainService,
      inPlayConnectionService,
      routingHelperService,
      cmsService,
      awsService,
      pubsubService,
      changeDetectorRef
    );

    component.viewByFilters = [
      'livenow',
      'upcoming'
    ];
    component.skeletonShow = { 'livenow': [true], 'upcoming': [true], 'someFilter': [false] };
  });

  it('#ngOnInit', fakeAsync(() => {
    component['initAccordions'] = jasmine.createSpy();
    component.ngOnInit();
    flush();
    expect(component['initAccordions']).toHaveBeenCalled();
  }));

  it('Should fetch event by sports EVENT_BY_SPORTS_SUBSCRIBE gets triggered', () => {
    pubsubService.subscribe.and.callFake((subscriber, method, handler) => {
      if (method === `${pubSubApi.EVENT_BY_SPORTS_CHANNEL}_MULTIPLE`) {
        handler({livenow: {} , upcoming: {} } as any);
      }
    }),
    component.ngOnInit();
    expect(pubsubService.subscribe).toHaveBeenCalledWith('EVENT_BY_SPORTS_SUBSCRIBE',
    `${pubSubApi.EVENT_BY_SPORTS_CHANNEL}_MULTIPLE`,jasmine.any(Function));
    expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
  });

  it('virtualScrollEnabled is false', fakeAsync(() => {
    cmsService.getSystemConfig.and.returnValue(of({
      'VirtualScrollConfig': {
        enabled: false
      }
    }));

    component.ngOnInit();
    expect(cmsService.getSystemConfig).toHaveBeenCalled();
    expect(component.isVirtualScrollEnabled).toBeFalsy();
  }));

  it('should use OnPush strategy', () => {
    expect(MultipleSportsSectionsComponent['__annotations__'][0].changeDetection).toBe(0);
  });

  it('virtualScrollEnabled is true', fakeAsync(() => {
    cmsService.getSystemConfig.and.returnValue(of({
      'VirtualScrollConfig': {
        enabled: true
      }
    }));

    component.ngOnInit();
    expect(cmsService.getSystemConfig).toHaveBeenCalled();
    expect(component.isVirtualScrollEnabled).toBeTruthy();
  }));

  it('ngOnDestroy', () => {
    component.ngOnDestroy();

    expect(stickyVirtualScrollerService.destroyEvents).toHaveBeenCalled();
  });

  describe('#goToInplaySportPage', () => {
    it('should navigate to inplay page', () => {
      component.goToSportCompetitionsPage({
        sportUri: 'sport/someString'
      } as any);
      expect(routingHelperService.formSportCompetitionsUrl).toHaveBeenCalledWith('sport/someString');
    });
  });

  describe('#isLiveNowFilter', () => {
    it('should be true', () => {
      component.viewByFilters = ['livenow'];
      expect(component.isLiveNowFilter('livenow')).toBeTruthy();
    });
    it('should be false', () => {
      component.viewByFilters = ['someOtherFilter'];
      expect(component.isLiveNowFilter('someFilter')).toBeFalsy();
    });
  });

  it('#trackById', () => {
    expect(component.trackById(1, 'someFilter')).toBe('1_someFilter');
  });

  describe('#initAccordions', () => {
    it('should call #getSportData', () => {
      component.expandedSportsCount = 2;
      component.viewByFilters = ['someFilter'];
      component.expandedKey = 'expandedKey';
      component.eventsByGroups = {
        someFilter: {
          eventsBySports: [
            {
              categoryId: 1,
              categoryCode: 'FOOTBALL'
            },
            {
              categoryId: 2,
              categoryCode: 'TENNIS'
            }
          ]
        }
      } as any;
      component['getSportData'] = jasmine.createSpy().and.returnValue(of({}));
      expect(component.isDataReady).toBeFalsy();
      component['initAccordions']();
      expect(component['getSportData']).toHaveBeenCalledTimes(2);
      expect(component.isDataReady).toBeTruthy();
    });

    it('should not set true for isDataReady if no eventsByGroups', () => {
      component.viewByFilters = [];
      component.eventsByGroups = undefined;
      component.isDataReady = false;

      component['initAccordions']();
      expect(component.isDataReady).toEqual(false);
    });

    it('should not set true for isDataReady eventsByGroups has no fields from filter', () => {
      component.viewByFilters = ['someFilter'];
      component.eventsByGroups = {};
      component.isDataReady = false;

      component['initAccordions']();
      expect(component.isDataReady).toEqual(false);
    });
    it('should behave correctly in error case', fakeAsync(() => {
      component.viewByFilters = ['someFilter'];
      component.eventsByGroups = {
        someFilter: {
          eventsBySports: [{}]
        }
      };
      component.skeletonShow = { 'livenow': [true], 'upcoming': [true], 'someFilter': [false] };
      component.isDataReady = false;
      component.expandedSportsCount = 10;
      component['getSportData'] = jasmine.createSpy().and.returnValue(throwError({} as any));
      component['handleEventsLoaded'] = jasmine.createSpy('handleEventsLoaded');

      spyOn(console, 'warn');

      component['initAccordions']();

      flush();

      expect(console.warn).toHaveBeenCalledWith({});
      expect(component['handleEventsLoaded']).toHaveBeenCalled();
    }));
  });

  describe('#getSportData', () => {
    it('should call #applySingleSportData', () => {
      inPlayMainService.getSportData.and.returnValue(of({ someData: 'someData' }));
      component['applySingleSportData'] = jasmine.createSpy();
      component['getSportData'](1, 'someFilter', 'football').subscribe();
      expect(component['applySingleSportData']).toHaveBeenCalled();
    });
  });

  describe('#applySingleSportData', () => {
    it('should call inPlayMainService.extendSectionWithSportInstance', () => {
      component.eventsByGroups = {
        someFilter: {
          eventsBySports: [{
            id: 1
          }]
        }
      };
      component['applySingleSportData']({
        eventsByTypeName: [{
          id: 1
        }]
      } as any, 1, 'someFilter', { config: {} } as any);
      expect(inPlayMainService.extendSectionWithSportInstance).toHaveBeenCalled();
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });
    it('should not call inPlayMainService.extendSectionWithSportInstance', () => {
      inPlayMainService.getLevelIndex.and.returnValue({});
      component.eventsByGroups = {
        someFilter: {
          eventsBySports: [{
            id: 1
          }]
        }
      };
      component['applySingleSportData']({
        eventsByTypeName: [{
          id: 1
        }]
      } as any, 1, 'someFilter', { config: {} } as any);
      expect(inPlayMainService.extendSectionWithSportInstance).not.toHaveBeenCalled();
    });
    it('should not call inPlayMainService.extendSectionWithSportInstance', () => {
      inPlayMainService.getLevelIndex.and.returnValue({});
      component.eventsByGroups = {
        someFilter: {
          eventsBySports: [{
            id: 1
          }]
        }
      };
      component['applySingleSportData']({} as any, 1, 'someFilter', { config: {} } as any);
      expect(inPlayMainService.extendSectionWithSportInstance).not.toHaveBeenCalled();
    });
  });

  describe('#toggleSport', () => {
    beforeEach(() => {
      component.isVirtualScrollEnabled = true;
      component.skeletonShow = { 'live': [false] ,'upcoming': [false] ,'someFilter':[false] };
    });
    it('when expanded', () => {
      const isExpanded = true;
      component['getSportData'] = jasmine.createSpy().and.returnValue(of({}));
      component.toggleSport(isExpanded, {
        categoryId: 123,
        categoryCode: 'TENNIS',
        'expanded-sports-tab': false
      } as any, 'someFilter', 0);
      expect(component['getSportData']).toHaveBeenCalled();
      expect(changeDetectorRef.detectChanges).toHaveBeenCalledTimes(2);
    });
    it('when expanded with getSportData throwing Error', () => {
      const isExpanded = true;
      component['getSportData'] = jasmine.createSpy().and.returnValue(throwError(''));
      component.toggleSport(isExpanded, {
        categoryId: 123,
        categoryCode: 'TENNIS',
        'expanded-sports-tab': false
      } as any, 'someFilter', 0);
      expect(component.skeletonShow['someFilter'][0]).toBe(false);
    });
    it('when collapsed', () => {
      const isExpanded = false;
      const sport = {
        categoryId: 123,
        categoryCode: 'TENNIS',
        'expanded-sports-tab': true
      };
      component.eventsByGroups = {
        someFilter: {
          eventsBySports: [
            sport
          ]
        }
      };
      component.toggleSport(isExpanded, sport as any, 'someFilter',0);
      expect(inPlayMainService.unsubscribeForSportCompetitionUpdates).toHaveBeenCalled();
      expect(inPlayMainService.unsubscribeForEventsUpdates).toHaveBeenCalled();
      expect(changeDetectorRef.detectChanges).toHaveBeenCalledTimes(2);
    });
    it('when collapsed after expand', () => {
      const isExpanded = false;
      const sport = {
        categoryId: 123,
        categoryCode: 'TENNIS',
        'expanded-sports-tab': true
      };
      component.eventsByGroups = {
        someFilter: {
          eventsBySports: [
            sport
          ]
        }
      };
      component.skeletonShow = { 'livenow': [true], 'upcoming': [true], 'someFilter': [false] };
      component['getSportData'] = jasmine.createSpy().and.callFake(() => {
        sport['expanded-sports-tab'] = isExpanded;
        return of({});
      });
      cmsService.getSystemConfig.and.returnValue(of({
        'VirtualScrollConfig': {
          enabled: false
        }
      }));
      component.toggleSport(isExpanded, sport as any, 'someFilter',0);
      expect(inPlayMainService.unsubscribeForSportCompetitionUpdates).toHaveBeenCalled();
      expect(inPlayMainService.unsubscribeForEventsUpdates).toHaveBeenCalled();
      expect(component.skeletonShow['someFilter'][0]).toBe(true);
    });
  });

  describe('getSportData', () => {
    it('should correctly handle error case 1', fakeAsync(() => {
      getSportDataErrorCase = 1;
      component['getSportData'](1, '12', 'football').subscribe();
      tick();
      expect(inPlayConnectionService.setConnectionErrorState).toHaveBeenCalled();
    }));
    it('should correctly handle error case 2', fakeAsync(() => {
      getSportDataErrorCase = 2;
      component['getSportData'](1, '12', 'football').subscribe();
      tick();
      expect(inPlayConnectionService.setConnectionErrorState).toHaveBeenCalled();
    }));
    it('should correctly handle error case 3', fakeAsync(() => {
      getSportDataErrorCase = 3;
      component['getSportData'](1, '12', 'football').subscribe(() => { });
      tick();
      expect(inPlayConnectionService.setConnectionErrorState).toHaveBeenCalled();
    }));
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

    describe('eventsByGroups changes', () => {
      let changes;

      beforeEach(() => {
        component['initAccordions'] = jasmine.createSpy('initAccordions');
      });

      it('should not call initAccordions if not changes for eventsByGroups', () => {
        changes = {} as any;
        component.isDataReady = false;
        component.ngOnChanges(changes);

        component.ngOnChanges(changes);

        expect(component['initAccordions']).not.toHaveBeenCalled();
      });

      it('should not call initAccordions if it is first change for eventsByGroups', () => {
        changes = {
          eventsByGroups: {
            isFirstChange: () => true
          }
        } as any;
        component.isDataReady = false;
        component.ngOnChanges(changes);

        expect(component['initAccordions']).not.toHaveBeenCalled();
      });

      it('should not call initAccordions if isDataReady', () => {
        changes = {
          eventsByGroups: {
            isFirstChange: () => false
          }
        } as any;
        component.isDataReady = true;
        component.ngOnChanges(changes);

        expect(component['initAccordions']).not.toHaveBeenCalled();
      });

      it('should call initAccordions', () => {
        changes = {
          eventsByGroups: {
            isFirstChange: () => false
          }
        } as any;
        component.isDataReady = false;
        component.ngOnChanges(changes);

        expect(component['initAccordions']).toHaveBeenCalled();
      });
    });

  });

  describe('socket reconnect error handler', () => {
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

  describe('ngOnChanges', () => {
    it('should not track page action if changes not ssError', () => {
      const changes = {
        isWatchLive: {
          currentValue: true
        }
      } as any;

      component.ngOnChanges(changes);

      expect(awsService.addAction).not.toHaveBeenCalled();
    });

    it('should not track page action if changes of ssError have not current value', () => {
      const changes = {
        ssError: {
          currentValue: false
        }
      } as any;

      component.ngOnChanges(changes);

      expect(awsService.addAction).not.toHaveBeenCalled();
    });

    it('should track page action if changes of ssError have current value', () => {
      const changes = {
        ssError: {
          currentValue: true
        }
      } as any;

      component.ngOnChanges(changes);

      expect(awsService.addAction).toHaveBeenCalledWith('inplay=>UI_Message=>Unavailable=>ssError');
    });
  });

  describe('handleEventsLoaded', () => {
    it('should return false if eventsByGroups is undefined', () => {
      expect(component.contentReady).toBeFalsy();
      component['eventsByGroups'] = undefined as any;
      component['handleEventsLoaded']();
      expect(component.contentReady).toBeFalsy();
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });
    it('if no data wit such filter', () => {
      expect(component.contentReady).toBeFalsy();
      component['eventsByGroups'] = {
      } as any;
      component['handleEventsLoaded']();
      expect(component.contentReady).toBeFalsy();
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });
    it('if no events are for this filter', () => {
      expect(component.contentReady).toBeFalsy();
      component['eventsByGroups'] = {
        livenow: {}
      } as any;
      component['handleEventsLoaded']();
      expect(component.contentReady).toBeTruthy();
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });
    it('should return false if opened sections not initialized yet', () => {
      component.eventsByGroups = {
        livenow: {
          eventsBySports: [
            {
              initiallyExpanded: true,
              eventsLoaded: false
            },
            {
              initiallyExpanded: false,
              eventsLoaded: false
            }
          ]
        }
      } as any;
      component['handleEventsLoaded']();
      expect(component['contentReady']).toBeFalsy();
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });
    it('should return true if opened sections already initialized', () => {
      component.eventsByGroups = {
        livenow: {
          eventsBySports: [
            {
              initiallyExpanded: true,
              eventsLoaded: true
            },
            {
              initiallyExpanded: false,
              eventsLoaded: false
            }
          ]
        }
      } as any;
      component['handleEventsLoaded']();
      expect(component['contentReady']).toBeTruthy();
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });
  });
  describe('isErrorState', () => {
    it('should return true in case of ssError', () => {
      component['ssError'] = {} as any;
      expect(component.isErrorState).toBeTruthy();
    });
    it('should return true in case of reconnect error', () => {
      component['ssError'] = undefined as any;
      component['wsError']['reconnectFailed'] = true as any;
      expect(component.isErrorState).toBeTruthy();
    });
    it('should return false in case of no errors', () => {
      component['ssError'] = undefined as any;
      component['wsError']['reconnectFailed'] = false as any;
      expect(component.isErrorState).toBeFalsy();
    });
  });

  describe('#reloadComponent()', () => {
    it('should reload component', () => {
      component.ngOnDestroy = jasmine.createSpy('ngOnDestroy');
      component.ngOnInit = jasmine.createSpy('ngOnInit');
      component.reloadComponent();
      expect(component.ssError).toBe(false);
      expect(component.ngOnDestroy).toHaveBeenCalled();
      expect(component.ngOnInit).toHaveBeenCalled();
    });
  });

  describe('#showNoEventsSection', () => {
    it('should return false if error', () => {
      component['ssError'] = true;
      component['eventsByGroups'] = {
        filter: {}
      };
      expect(component.showNoEventsSection('filter')).toBe(false);
    });
    it('should return false if error and empty object', () => {
      component['ssError'] = true;
      component['eventsByGroups'] = {};
      expect(component.showNoEventsSection('filter')).toBe(false);
    });
    it('should return false if empty object', () => {
      component['ssError'] = false;
      component['eventsByGroups'] = {};
      expect(component.showNoEventsSection('filter')).toBe(false);
    });
    it('should return true', () => {
      component['ssError'] = false;
      component['eventsByGroups'] = {
        filter: {
          eventsIds: [1, 2]
        }
      };
      expect(component.showNoEventsSection('filter')).toBe(false);
    });

  });

  describe('#getSportTrackingId()', () => {
    it('should return result', () => {
      const eventsBySports = {
        categoryId: '123',
        topLevelType: '321'
      };
      const result = '123-321';
      expect(component.getSportTrackingId(1, eventsBySports)).toEqual(result);
    });
  });

  describe('#isUpcomingFilter()', () => {
    it('should return false', () => {
      const filter = '';
      expect(component.isUpcomingFilter(filter)).toBe(false);
    });
    it('should return true if upcomingLiveStream', () => {
      const filter = 'upcomingLiveStream';
      expect(component.isUpcomingFilter(filter)).toBe(true);
    });
    it('should return true if upcoming', () => {
      const filter = 'upcoming';
      expect(component.isUpcomingFilter(filter)).toBe(true);
    });
  });

  describe('getNoEventsMessage', () => {
    it('should return live events message', () => {
      expect(component.getNoEventsMessage('livenow')).toBe('inplay.noLiveEventsFound');
    });
    it('should return upcoming events message', () => {
      expect(component.getNoEventsMessage('upcoming')).toBe('inplay.noUpcomingEventsFound');
    });
  });
});
