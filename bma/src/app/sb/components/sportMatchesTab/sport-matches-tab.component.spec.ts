import { fakeAsync, tick } from '@angular/core/testing';
import { of as observableOf, throwError } from 'rxjs';

import { SportMatchesTabComponent } from './sport-matches-tab.component';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { SITECORE_PROMOTION,FANZONE_CONFIG,TEAM_COLORS, SITECORE_PROMOTION_EMPTY_TEASER } from '@app/sb/components/sportMatchesTab/mockdata/sport-matches-tab.component.mock';
import { oddsCardConstant } from '@app/shared/constants/odds-card-constant';
import environment from '@environment/oxygenEnvConfig';

describe('SportMatchesTabComponent', () => {
  let component: SportMatchesTabComponent;
  let activatedRoute;
  let marketSortService;
  let sportTabsService;
  let enhancedMultiplesService;
  let storageService;
  let pubSubService;
  let windowRef;
  let changeDetectorRef;
  let locationService;
  let gamingService;
  let favouritesService;
  let gtmService, routingHelperService, router;
  let cmsService;
  let competitionFiltersService;
  let user;
  let vanillaApiService;
  let deviceService;
  let timeService;

  const sitecorePromotion = SITECORE_PROMOTION;
  const emptySitecorePromotion = [];
  const emptyTeaserSitecore = SITECORE_PROMOTION_EMPTY_TEASER;
  const fanzoneConfig = FANZONE_CONFIG;

  const teamColors = TEAM_COLORS;
  let templateService;

  beforeEach(() => {

    activatedRoute = {
      snapshot: {
        paramMap: {
          get: jasmine.createSpy()
        }
      }
    };

    cmsService = {
      getMarketSwitcherFlagValue: jasmine.createSpy('getMarketSwitcherFlagValue').and.returnValue(observableOf(Boolean)),
      getFanzone: jasmine.createSpy('getFanzone').and.returnValue(observableOf(fanzoneConfig)),
      getTeamsColors: jasmine.createSpy('getTeamsColors').and.returnValue(observableOf(teamColors)),
      getSystemConfig: jasmine.createSpy('getSystemConfig').and.returnValue(observableOf({
        Fanzone: {
          enabled: true
        }
      }))
    };

    competitionFiltersService = {
      filterEvents: jasmine.createSpy('filterEvents').and.returnValue([]),
      filterEventsByHiddenMarkets: jasmine.createSpy('filterEventsByHiddenMarkets').and.returnValue([]),
      getSeoSchemaEvents: jasmine.createSpy('getSeoSchemaEvents').and.returnValue([{id:'1'}])
    };

    sportTabsService = {
      deleteEvent: jasmine.createSpy(),
      eventsBySections: jasmine.createSpy('eventsBySections').and.callFake((sections) => sections)
    };

    marketSortService = {
      setMarketFilterForMultipleSections: jasmine.createSpy()
    };

    enhancedMultiplesService = {
      getEnhancedMultiplesEvents: jasmine.createSpy().and.returnValue(observableOf([]))
    };

    storageService = {
      get: jasmine.createSpy()
    };

    pubSubService = {
      subscribe: jasmine.createSpy('subscribe'),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      publish: jasmine.createSpy(),
      API: pubSubApi
    };

    windowRef = {
      nativeWindow: {
        setTimeout: jasmine.createSpy().and.callFake(cb => cb()),
        setInterval: jasmine.createSpy().and.callFake(cb => cb()),
        location:{href: 'football'}
      }
    };

    changeDetectorRef = {
      detach: jasmine.createSpy(),
      detectChanges: jasmine.createSpy()
    };

    gamingService = {
      arrangeEventsBySection: jasmine.createSpy('arrangeEventsBySection'),
      filterOutFutureEvents: jasmine.createSpy('filterOutFutureEvents'),
      setMarketsAvailability: jasmine.createSpy('setMarketsAvailability')
    };

    locationService = {
      path: jasmine.createSpy().and.callFake(() => 'matches/page')
    };

    gtmService = {
      push: jasmine.createSpy()
    };

    routingHelperService = {
      formInplayUrl: jasmine.createSpy(),
      formCompetitionUrl: jasmine.createSpy().and.returnValue('football/competitions'),
      formSportUrl: jasmine.createSpy().and.returnValue(observableOf('/sport/football'))
    };

    favouritesService = {
      isFavouritesEnabled: true
    };

    router = {
      navigateByUrl: jasmine.createSpy()
    };

    user = {
      username: 'abc'
    };
    vanillaApiService = {
      get: jasmine.createSpy('get').and.returnValue(observableOf(sitecorePromotion))
    };
    templateService = {
      isListTemplate: (selectedMarket: string)=>{
       return oddsCardConstant.LIST_TEMPLATES.indexOf(selectedMarket) !== -1;
      }
    };
    deviceService = {
      isRobot: jasmine.createSpy('isRobot').and.returnValue(true)
    };
    timeService = {
      determineDay: jasmine.createSpy('isRobot')
    }

    component = new SportMatchesTabComponent(
      activatedRoute,
      cmsService,
      sportTabsService,
      marketSortService,
      enhancedMultiplesService,
      storageService,
      pubSubService,
      windowRef,
      changeDetectorRef,
      locationService,
      gtmService,
      routingHelperService,
      favouritesService,
      router,
      competitionFiltersService,
      vanillaApiService,
      user,
      templateService,
      deviceService,
      timeService
    );

    component.sport = ({
      getByTab: jasmine.createSpy().and.returnValue(observableOf([]).toPromise()),
      readonlyRequestConfig: { categoryId: 129 },
      subscribeLPForUpdates: jasmine.createSpy(),
      unSubscribeLPForUpdates: jasmine.createSpy(),
      subscribeEventChildsUpdates: jasmine.createSpy('subscribeEventChildsUpdates'),
      unsubscribeEventChildsUpdates: jasmine.createSpy('unsubscribeEventChildsUpdates'),
      filterOutFutureEvents: jasmine.createSpy('filterOutFutureEvents'),
      arrangeEventsBySection: jasmine.createSpy('arrangeEventsBySection'),
      config: {
        tier: 0
      },
      sportConfig: {
        config: {
          name: 'basketball',
          request: {
            categoryId: '1'
          }
        }
      }
    } as any);
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });

  it('should init component with proper properties', () => {
    expect(component.locationPath).toEqual('matches/page');
  });

  describe('ngOnDestroy', () => {
    it('should unsubscribe from live updates of only expanded sections', () => {
      spyOn(component as any,'removeSchemaForSportsTab');
      component.eventsBySections = [{
        subscriptionKey: 'type-1'
      }, {
        subscriptionKey: null
      }, {
        subscriptionKey: 'type-2'
      }] as any;

      component.ngOnDestroy();

      expect(component.sport.unsubscribeEventChildsUpdates).toHaveBeenCalledTimes(2);
      expect(component['removeSchemaForSportsTab']).toHaveBeenCalled();
    });

    it('should unsubscribe from connect events', () => {
      component.ngOnDestroy();

      expect(pubSubService.unsubscribe).toHaveBeenCalledWith('MatchesSportTabComponent');
    });

    it('should unsubscribe from data loader subscription', () => {
      const loadDataSubscription = jasmine.createSpyObj('loadDataSubscription', ['unsubscribe']);
      component['loadDataSubscription'] = loadDataSubscription;
      component.ngOnDestroy();

      expect(loadDataSubscription.unsubscribe).toHaveBeenCalled();
    });

    it('should unsubscribe from enhancedMultiples', () => {
      component['enhancedMultiplesSubscription'] = {
        unsubscribe: jasmine.createSpy('unsubscribe')
      } as any;
      component.ngOnDestroy();

      expect(component['enhancedMultiplesSubscription'].unsubscribe).toHaveBeenCalled();
    });

    it('should unsubscribe from marketSwitcherConfig', () => {
      component['marketSwitcherConfigSubscription'] = {
        unsubscribe: jasmine.createSpy('unsubscribe')
      } as any;
      component.ngOnDestroy();

      expect(component['marketSwitcherConfigSubscription'].unsubscribe).toHaveBeenCalled();
    });
  });

  describe('updateState', () => {
    it('should changeAccordionState', () => {
      component.isExpandedEnhanced = false;
      component.updateState(true, 'enhanced');

      expect(component.isExpandedEnhanced).toBeTruthy();

      const eventSectionMock: any = {
        isExpanded: false
      };

      component.updateState(true, 'event', eventSectionMock);
      expect(eventSectionMock.isExpanded).toBeTruthy();
    });

    it('should not section state when no section in argument and do not throw error', () => {
      expect(component.updateState(true, 'event')).toEqual(undefined);
    });

    it('should change expanded state to true if section was not expanded and subscribe to live updates', () => {
      const subscriptionKey = 'type-123';
      const section = {
        subscriptionKey: null,
        events: [{ id: 1 }],
        typeId: 442
      } as any;
      (component.sport.subscribeEventChildsUpdates as any).and.returnValue(subscriptionKey);

      component.updateState(true, 'event', section);

      expect(section.isExpanded).toBeTruthy();
      expect(component.sport.subscribeEventChildsUpdates).toHaveBeenCalledWith(section.events, section.typeId);
      expect(section.subscriptionKey).toEqual(subscriptionKey);
    });

    it('should not change expanded state if section was expanded and subscribed', () => {
      const subscriptionKey = 'type-123';
      const section = {
        subscriptionKey,
        events: [{ id: 1 }],
        typeId: 442
      } as any;
      (component.sport.subscribeEventChildsUpdates as any).and.returnValue(subscriptionKey);

      component.updateState(true, 'event', section);

      expect(section.isExpanded).toBeTruthy();
      expect(component.sport.subscribeEventChildsUpdates).not.toHaveBeenCalled();
    });

    it('should not unsubscrtibe from updates if section was not expanded', () => {
      const subscriptionKey = 'type-123';
      const section = {
        isExpanded: false,
        subscriptionKey,
        events: [{ id: 1 }],
        typeId: 442
      } as any;

      component.updateState(false, 'event', section);

      expect(section.isExpanded).toBeFalsy();
      expect(component.sport.unsubscribeEventChildsUpdates).not.toHaveBeenCalled();
    });

    it('should unsubscrtibe from updates if section was expanded', () => {
      const subscriptionKey = 'type-123';
      const section = {
        isExpanded: true,
        subscriptionKey,
        events: [{ id: 1 }],
        typeId: 442
      } as any;

      component.updateState(false, 'event', section);

      expect(section.isExpanded).toBeFalsy();
      expect(component.sport.unsubscribeEventChildsUpdates).toHaveBeenCalledWith(subscriptionKey);
    });
  });

  describe('#ngOnInit', () => {
    beforeEach(() => {
      component.sport = Object.assign(component.sport, gamingService);
    });

    it('should sync on events', () => {
      component.ngOnInit();
      expect(pubSubService.subscribe).toHaveBeenCalledTimes(3);
      expect(pubSubService.subscribe.calls.allArgs()[1]).toEqual(
        ['MatchesSportTabComponent', pubSubService.API.DELETE_EVENT_FROM_CACHE, jasmine.any(Function)]
      );
    });

    it('should be undefined', () => {
      component['activeMarketFilter'] = 'test';
      component.ngOnInit();
      expect(component['activeMarketFilter']).toBeUndefined();
    });

    it('should load data', () => {
      spyOn(component as any, 'loadMatchesData');
      component.ngOnInit();
      expect(component['loadMatchesData']).toHaveBeenCalled();
    });

    it('should re-init MarketsAvailability on DELETE_MARKET_FROM_CACHE event', () => {
      component.eventsCache = [];
      component.eventsBySections = [];
      component['activeMarketFilter'] = '';

      component['pubSubService'].subscribe = jasmine.createSpy('pubSubService.subscribe')
        .and.callFake((filename: string, eventName: string, callback: Function) => {
          if (eventName === 'DELETE_MARKET_FROM_CACHE') {
            callback();

            expect(gamingService.setMarketsAvailability).toHaveBeenCalled();
          }
        });

      component.ngOnInit();
    });

    it('should not re-init MarketsAvailability when no EventsCache', () => {
      component.eventsCache = undefined;
      component.eventsBySections = [];
      component['activeMarketFilter'] = '';

      component['pubSubService'].subscribe = jasmine.createSpy('pubSubService.subscribe')
        .and.callFake((filename: string, eventName: string, callback: Function) => {
          if (eventName === 'DELETE_MARKET_FROM_CACHE') {
            callback();

            expect(gamingService.setMarketsAvailability).not.toHaveBeenCalled();
          }
        });

      component.ngOnInit();
    });

    it('should delete event on DELETE_EVENT_FROM_CACHE event', () => {
      component.eventsCache = [];
      component.eventsBySections = [];
      component['activeMarketFilter'] = '';

      component['pubSubService'].subscribe = jasmine.createSpy('pubSubService.subscribe')
        .and.callFake((filename: string, eventName: string, callback: Function) => {
          if (eventName === 'DELETE_EVENT_FROM_CACHE') {
            callback('123');

            expect(sportTabsService.deleteEvent).toHaveBeenCalledWith('123', []);
          }
        });

      component.ngOnInit();
    });

    it('should call detect changes and fanzone enabled on fanzone data subscribe', () => {

      component['pubSubService'].subscribe = jasmine.createSpy('pubSubService.subscribe')
        .and.callFake((filename: string, eventName: string, callback: Function) => {
          if (eventName === 'FANZONE_DATA') {
            callback('123');
            expect(component.isFanzoneEnabled).toBe(true);
            expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
          }
        });

      component.ngOnInit();
    });

    describe('check for isMarketSwitcherConfigured', () => {
      it('should set isMarketSwitcherConfigured to true if cmsService getMarketSwitcherFlagValue return true', () => {
        cmsService.getMarketSwitcherFlagValue.subscribe = jasmine.createSpy('cmsService.getMarketSwitcherFlagValue')
          .and.callFake((flag) => {
            expect(cmsService.getMarketSwitcherFlagValue).toHaveBeenCalled();
            flag = true;
            expect(component.isMarketSwitcherConfigured).toBe(true);
          });
      });
      it('should set isMarketSwitcherConfigured to false if cmsService getMarketSwitcherFlagValue return false', () => {
        cmsService.getMarketSwitcherFlagValue.subscribe = jasmine.createSpy('cmsService.getMarketSwitcherFlagValue')
          .and.callFake((flag) => {
            expect(cmsService.getMarketSwitcherFlagValue).toHaveBeenCalled();
            flag = false;
            expect(component.isMarketSwitcherConfigured).toBe(false);
          });
      });
    });

    describe('should define isDisplayTutorial', () => {
      it(`as truthy if sportName equals football, there's no footballTutorial and Favourites is enabled`, () => {
        activatedRoute.snapshot.paramMap.get.and.returnValue('football');
        storageService.get.and.returnValue(undefined);

        component.ngOnInit();
        expect(component.isDisplayTutorial).toBeTruthy();
      });

      it(`as falsy if sportName does not equal football, there's no footballTutorial and Favourites is enabled`, () => {
        activatedRoute.snapshot.paramMap.get.and.returnValue('volleyball');
        storageService.get.and.returnValue(undefined);

        component.ngOnInit();
        expect(component.isDisplayTutorial).toBeFalsy();
      });

      it(`as falsy if sportName equals football but there's footballTutorial and Favourites is enabled`, () => {
        activatedRoute.snapshot.paramMap.get.and.returnValue('volleyball');
        storageService.get.and.returnValue(['footballTutorial']);

        component.ngOnInit();
        expect(component.isDisplayTutorial).toBeFalsy();
      });

      it(`as falsy if sportName equals football, there's no footballTutorial but Favourites is disabled`, () => {
        activatedRoute.snapshot.paramMap.get.and.returnValue('football');
        storageService.get.and.returnValue(undefined);
        favouritesService.isFavouritesEnabled = false;

        component.ngOnInit();
        expect(component.isDisplayTutorial).toBeFalsy();
      });

      it(`as falsy if sportName equals football but there's footballTutorial and Favourites is disabled`, () => {
        activatedRoute.snapshot.paramMap.get.and.returnValue('football');
        storageService.get.and.returnValue(['footballTutorial']);
        favouritesService.isFavouritesEnabled = false;

        component.ngOnInit();
        expect(component.isDisplayTutorial).toBeFalsy();
      });

      it(`as falsy if sportName not equals football, there's footballTutorial and Favourites is disabled`, () => {
        activatedRoute.snapshot.paramMap.get.and.returnValue('basketball');
        storageService.get.and.returnValue(['footballTutorial']);
        favouritesService.isFavouritesEnabled = false;

        component.ngOnInit();
        expect(component.isDisplayTutorial).toBeFalsy();
      });
    });

    it('should detect changes', () => {
      windowRef.nativeWindow.setInterval.and.callFake(cb => cb());
      component.ngOnInit();
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });
  });

  describe('trackEvent', () => {
    it('should track proper event click', () => {
      component.locationPath = 'home/matches';
      component.trackEvent(({
        name: 'Man Utd vs Man City',
        id: 159
      }) as any);
      expect(gtmService.push).toHaveBeenCalledWith('trackEvent', {
        event: 'trackEvent',
        eventCategory: 'upcoming module',
        eventAction: 'home/matches',
        eventName: 'Man Utd vs Man City',
        eventLabel: 'view event',
        eventID: 159
      });
    });
  });

  describe('trackByDate', () => {
    it('should track proper event click', () => {
      const trackByDateId = component.trackByDate(5, ({
        startTime: 4123412341234,
        title: '23 jun'
      }) as any);
      expect(trackByDateId).toEqual('4123412341234_23_jun_5');
    });
  });

  describe('loadMatchesData', () => {
    beforeEach(() => {
      spyOn(component as any, 'schemaForsportsTab');
    });
    it('should call events fetching method with ' +
      'tab property if it is set', () => {
        component.isFirstLoad = false;
        component.tab = 'today';
        component.sportName = 'tennis';
        spyOn(component.displayFilters, 'emit').and.callThrough();

        component['loadMatchesData']();

        expect(component.sport.getByTab).toHaveBeenCalledWith('today');
        expect(component['enhancedMultiplesService'].getEnhancedMultiplesEvents)
          .toHaveBeenCalledWith('tennis', 'today');
        expect(component.displayFilters.emit).not.toHaveBeenCalled();
        expect(component.isFirstLoad).toBeFalse();
      });

    it('should call events fetching method with ' +
      'upcoming value if tab is not set', fakeAsync(() => {
        component.sport.getByTab = jasmine.createSpy().and.returnValue(observableOf([{}, {}] as any).toPromise());
        
        component.isFirstLoad = true;
        component.sportName = 'tennis';
        component.eventsBySectionsCopy = [{ categoryId: '1' }] as any;
        spyOn(component.displayFilters, 'emit').and.callThrough();

        component['loadMatchesData']();
        tick();

        expect(component.sport.getByTab).toHaveBeenCalledWith('upcoming');
        expect(component['enhancedMultiplesService'].getEnhancedMultiplesEvents)
          .toHaveBeenCalledWith('tennis', '');
        expect(component.displayFilters.emit).toHaveBeenCalledWith(true);
        expect(component.isFirstLoad).toBeFalse();
        expect(component['schemaForsportsTab']).toHaveBeenCalledWith(component.eventsBySectionsCopy);
      }));

    it('should emit hide matches tab for all sports if no events are available', fakeAsync(() => {
      component.tab = 'matches';
      component['loadMatchesData']();
      tick();

      expect(component.sport.getByTab).toHaveBeenCalledWith('matches');
      expect(component.eventsBySectionsCopy).toEqual([]);
    }));

    it('gamingService.arrangeEventsBySection toHaveBeenCalled', fakeAsync(() => {
      component.tab = 'today';
      enhancedMultiplesService.getEnhancedMultiplesEvents.and.returnValue(observableOf([{
        id: 2,
        name: 'name',
        isLiveNowEvent: false
    }]));
      (component.sport.arrangeEventsBySection as any).and.returnValue([]);
      component['loadMatchesData']();
      tick();

      expect(component.sport.getByTab).toHaveBeenCalledWith('today');
      expect(component.sport.arrangeEventsBySection).toHaveBeenCalledWith([{ id: 2, name: 'name', isLiveNowEvent: false } as any], true);
    }));

    it('gamingService.arrangeEventsBySection not toHaveBeenCalled', fakeAsync(() => {
      component.tab = 'upcoming';
      component['filterUpcomingEvents'] = jasmine.createSpy('filterUpcomingEvents').and.returnValue([]);
      gamingService.arrangeEventsBySection.and.returnValue([]);
      component['loadMatchesData']();
      tick();

      expect(component.sport.getByTab).toHaveBeenCalledWith('upcoming');
      expect(gamingService.arrangeEventsBySection).not.toHaveBeenCalled();
    }));

    it('should not emit hide matches tab if events are available', fakeAsync(() => {
      component.sport.getByTab = jasmine.createSpy().and.returnValue(observableOf([{}, {}] as any).toPromise());
      component.tab = 'matches';
      component['loadMatchesData']();
      tick();

      expect(component.sport.getByTab).toHaveBeenCalledWith('matches');
    }));

    it('loadMatchesData error', fakeAsync(() => {
      component.sport.getByTab = jasmine.createSpy('getByTab').and.returnValue(Promise.reject('error'));
      component['loadMatchesData']();
      tick();

      expect(component.isResponseError).toBeTruthy();
    }));

    it('should unsubscribe if previous subscription is active', fakeAsync(() => {
      const loadDataSubscription = jasmine.createSpyObj('loadDataSubscription', ['unsubscribe']);
      component['loadDataSubscription'] = loadDataSubscription;

      component['loadMatchesData']();
      tick();

      expect(loadDataSubscription.unsubscribe).toHaveBeenCalled();
    }));

    it('should set isLoadedEnhanced to true', fakeAsync(() => {
      enhancedMultiplesService.getEnhancedMultiplesEvents = jasmine.createSpy('getEnhancedMultiplesEvents')
        .and.returnValue(throwError('error'));
      component['loadMatchesData']();
      tick();

      expect(component.isLoadedEnhanced).toBeTruthy();
    }));

    it('should reset cached events', () => {
      competitionFiltersService.eventsBySections = [{} as any];

      component['loadMatchesData']();

      expect(component.eventsBySectionsCopy).toEqual([]);
      expect(component.eventsBySectionsCopy.length).toEqual(0);
    });

    it('loadMatchesData with golff_matches', fakeAsync(() => {
      activatedRoute.snapshot['_routerState'] = {url: 'golf_matches'} ;
      component.sportId = 18;
      component.sport.getByTab = jasmine.createSpy().and.returnValue(observableOf([{}, {}] as any).toPromise());
      component['loadMatchesData']();
      tick();

      expect(component.isResponseError).toBeFalsy();
    }));

    it('loadMatchesData with golff_matches', fakeAsync(() => {
      activatedRoute.snapshot['_routerState'] = {url: 'match/matches'};
      component.sportId = 18;
      component.sport.getByTab = jasmine.createSpy().and.returnValue(observableOf([{}, {}] as any).toPromise());
      component['loadMatchesData']();
      tick();

      expect(component.isResponseError).toBeFalsy();
    }));

  });

  describe('checkMarketSwitcherComponent', () => {
    it('should set isMarketSwitcherComponentLoaded to true when sport is tennis and not CMS configured', () => {
      component.sport = ({ sportConfig: { config: { request: { categoryId: '34'} } } } as any);
      component.isMarketSwitcherConfigured = false;
      spyOn(component as any,'getMSDataFromCMSFeature');
      component['checkMarketSwitcherComponent']();
      expect(component.isMarketSwitcherComponentLoaded).toBe(true);
    });
    it('should set isMarketSwitcherComponentLoaded to true when sport is football and not CMS configured', () => {
      component.sport = ({ sportConfig: { config: { request: { categoryId: '16'} } } } as any);
      component.isMarketSwitcherConfigured = false;
      spyOn(component as any,'getMSDataFromCMSFeature');
      component['checkMarketSwitcherComponent']();
      expect(component.isMarketSwitcherComponentLoaded).toBe(true);
    });
    it('should set isMarketSwitcherComponentLoaded to true when sport is tennis and CMS configured', () => {
      component.sport = ({ sportConfig: { config: { request: { categoryId: '34'} } } } as any);
      component.isMarketSwitcherConfigured = true;
      component['checkMarketSwitcherComponent']();
      expect(component.isMarketSwitcherComponentLoaded).toBe(false);
    });
    it('should set isMarketSwitcherComponentLoaded to true when sport is football and CMS configured', () => {
      component.sport = ({ sportConfig: { config: { request: { categoryId: '16'} } } } as any);
      component.isMarketSwitcherConfigured = true;
      component['checkMarketSwitcherComponent']();
      expect(component.isMarketSwitcherComponentLoaded).toBe(false);
    });
  });

  describe('handleOutput', () => {
    it('should execute filterEvents when output is filterChange', () => {
      component.handleOutput({ output: 'filterChange', value: 'someFilter' });
      expect(component['activeMarketFilter']).toBe('someFilter');
    });
    it('should execute filterEvents when output is hideEnhancedSection', () => {
      component.handleOutput({ output: 'hideEnhancedSection', value: 'someFilter' });
      expect(component.isExpandedEnhanced).toBeFalsy();
    });
    it('should passby when output is other than filterChange and hideEnhancedSection', () => {
      component.handleOutput({ output: 'someoutput', value: 'someFilter' });
      expect(component['activeMarketFilter']).not.toBeDefined();
      expect(component.isExpandedEnhanced).toBeTruthy();
    });
  });

  describe('isInPlayEvent', () => {
    it('should return true if event is live', () => {
      const isEventInPlay = component['isInPlayEvent'](({
        isLiveNowEvent: true
      } as any));
      expect(isEventInPlay).toEqual(true);
    });
    it('should return true if event is started', () => {
      const isEventInPlay = component['isInPlayEvent'](({
        isStarted: true
      } as any));
      expect(isEventInPlay).toEqual(true);
    });
    it('should return false if event is not started', () => {
      const isEventInPlay = component['isInPlayEvent'](({
        isStarted: false,
        isLiveNowEvent: false
      } as any));
      expect(isEventInPlay).toEqual(false);
    });
  });

  describe('isPrimaryMarket', () => {
    it('should return true for Football primary market case', () => {
      const isPrimaryMarket = component.isPrimaryMarket(({
        defaultValue: 'Match Result'
      } as any));
      expect(isPrimaryMarket).toEqual(true);
    });
    it('should return true for not football primary market case', () => {
      const isPrimaryMarket = component.isPrimaryMarket(({} as any));
      expect(isPrimaryMarket).toEqual(true);
    });
    it('should return false for non primary market case', () => {
      const isPrimaryMarket = component.isPrimaryMarket(({
        defaultValue: 'Some other market choosen'
      } as any));
      expect(isPrimaryMarket).toEqual(false);
    });
  });

  describe('#goToCompetition', () => {
    it('should build competition URL and redirect', () => {
      routingHelperService.formCompetitionUrl.and.returnValue('some/url');
      component.goToCompetition({
        sectionTitle: 'England - Premier league'
      } as any);
      expect(routingHelperService.formCompetitionUrl).toHaveBeenCalled();
      expect(router.navigateByUrl).toHaveBeenCalledWith('some/url');
      expect(gtmService.push).toHaveBeenCalledWith('trackEvent', {
        event: 'trackEvent',
        eventCategory: 'upcoming module',
        eventAction: 'matches/page',
        eventLabel: 'see all',
        competitionName: 'England - Premier league'
      });
    });
  });

  describe('#filterUpcomingEvents', () => {
    beforeEach(() => {
      component.sport = gamingService;
    });

    it('for tier1,2 sports', () => {
      component['filterOutInplayEvents'] = jasmine.createSpy();
      component['filterUpcomingEvents']([{}] as any);
      expect(gamingService.filterOutFutureEvents).toHaveBeenCalled();
      expect(component['filterOutInplayEvents']).toHaveBeenCalled();
    });
  });

  describe('#getMSDataFromCMSFeature', () => {
    it('getMSDataFromCMSFeature for golf_competitions', fakeAsync(() => {
      component.sport = ({ sportConfig: { config: { request: { categoryId: '18'}, name: 'golf' } } } as any);
      component.currentURL = 'golf_matches';
      component['getMSDataFromCMSFeature']()
      tick();
    }));
  });

  describe('#filterEvents', () => {
    it('filter should be defined', () => {
      component.filterEvents('someFilter');
      expect(component['activeMarketFilter']).toBe('someFilter');
    });

    it('filter should not be defined', () => {
      expect(component['activeMarketFilter']).not.toBeDefined();
    });

    it('when filters are the same', () => {
      component['activeMarketFilter'] = 'someFilter';
      component.filterEvents('someFilter');
      expect(windowRef.nativeWindow.setTimeout).not.toHaveBeenCalled();
      expect(marketSortService.setMarketFilterForMultipleSections).not.toHaveBeenCalled();
    });

    it('when filters are different', () => {
      component['activeMarketFilter'] = 'someFilter';
      component.filterEvents('someOtherFilter');
      expect(windowRef.nativeWindow.setTimeout).toHaveBeenCalled();
      expect(marketSortService.setMarketFilterForMultipleSections).toHaveBeenCalled();
      expect(component['activeMarketFilter']).toBe('someOtherFilter');
    });

    it('when filter not defined', () => {
      component.filterEvents('someOtherFilter');
      expect(windowRef.nativeWindow.setTimeout).toHaveBeenCalled();
      expect(marketSortService.setMarketFilterForMultipleSections).toHaveBeenCalled();
      expect(component['activeMarketFilter']).toBe('someOtherFilter');
    });

    it('when filters are available', () => {
      component.isSportEventFiltersEnabled = true;
      component.filterEvents('someOtherFilter');
      expect(marketSortService.setMarketFilterForMultipleSections).toHaveBeenCalledTimes(2);
      expect(component['activeMarketFilter']).toBe('someOtherFilter');
      expect(competitionFiltersService.filterEvents).toHaveBeenCalledWith(undefined, undefined, []);
      expect(competitionFiltersService.selectedMarket).toEqual('someOtherFilter');
    });
  });

  describe('updateDynamicProperties', () => {
    describe('isMarketSelectorActive', () => {
      it(`should equal True if  sportName equal football and eventsBySections.length > 0`, () => {
        component.sportName = 'football';
        component.eventsBySections = [{ categoryId: '1' }] as any;
        component.eventsBySectionsCopy = [{ categoryId: '1' }] as any;
        component.isMarketSelectorActive = false;

        component.updateDynamicProperties();

        expect(component.isMarketSelectorActive).toBeTruthy();
      });

      describe('should equal False', () => {
        it(`if sportName Not equal football`, () => {
          component.sportName = 'tennis';
          component.isMarketSelectorActive = true;
        });
        it(`if sportName is equal football and eventsBySections.length = 0`, () => {
          component.sportName = 'football';
          component.eventsBySections = [] as any;
          component.eventsBySectionsCopy = [] as any;
          component.isMarketSelectorActive = true;
        });

        afterEach(() => {
          component.updateDynamicProperties();

          expect(component.isMarketSelectorActive).toBeFalsy();
        });
      });
    });

    describe('showEventsBySections', () => {
      beforeEach(() => {
        component.eventsBySections = [{ categoryId: '1' }] as any;
        component.eventsBySectionsCopy = [{ categoryId: '1' }] as any;
      });

      describe('should equal True if eventsBySections.length and ', () => {
        it(`isMarketSelectorActive equal False and eventsBySections[0] has defaultValue`, () => {
          component.isMarketSelectorActive = true;
          component.eventsBySections[0].defaultValue = 'something';
        });


        afterEach(() => {
          component.updateDynamicProperties();

          expect(component.showEventsBySections).toBeTruthy();
        });
      });

      describe('should equal False if', () => {
        it(`No eventsBySections`, () => {
          component.eventsBySections = [];
        });


        it(`isMarketSelectorActive equal True and eventsBySections[0] Has Not defaultValue`, () => {
          component.sportName = 'football';
          component.eventsBySections[0].defaultValue = null;
        });

        afterEach(() => {
          component.updateDynamicProperties();

          expect(component.showEventsBySections).toBeFalsy();
        });
      });

    });
  });

  describe('initMarketSelector', () => {
    it(`should check IsMarketSelectorActive`, fakeAsync(() => {
      spyOn(component as any, 'updateDynamicProperties');

      component['initMarketSelector']('');

      tick();

      expect(component.updateDynamicProperties).toHaveBeenCalledTimes(1);
    }));
  });

  describe('loadMatchesData', () => {
    it(`should check IsMarketSelectorActive`, fakeAsync(() => {
      spyOn(component as any, 'updateDynamicProperties');

      component['loadMatchesData']();

      tick();

      expect(component.updateDynamicProperties).toHaveBeenCalledTimes(1);
    }));
  });

  it('should detect tabs changing ngOnChanges and reset applied filter', () => {
    component.ngOnInit();

    component['activeMarketFilter'] = 'test';

    component.ngOnChanges({
      tab: {
        currentValue: 'newTab',
        previousValue: 'oldTab'
      }
    } as any);

    expect(component['activeMarketFilter']).toBeUndefined();
  });

  it('should reset filters on ngOnChanges when tab is different from `today`', () => {
    component.ngOnInit();
    spyOn(component as any,'removeSchemaForSportsTab')
    component.leagueFilter = {} as any;
    component.timeFilter = {} as any;

    component.ngOnChanges({
      tab: {
        currentValue: 'tomorrow',
        previousValue: 'today'
      }
    } as any);

    expect(component.leagueFilter).toBeNull();
    expect(component.timeFilter).toBeNull();
    expect(component['removeSchemaForSportsTab']).toHaveBeenCalled();
  });

  it('should not reset filters on ngOnChanges when tab is `today`', () => {
    component.ngOnInit();

    component.leagueFilter = {} as any;
    component.timeFilter = {} as any;

    component.ngOnChanges({
      tab: {
        currentValue: 'today',
        previousValue: 'today'
      }
    } as any);

    expect(component.leagueFilter).toEqual({} as any);
    expect(component.timeFilter).toEqual({} as any);
  });

  it('should update time filter if it`s different from current and filter events', () => {
    component.eventsBySectionsCopy = [];

    component.ngOnChanges({ timeFilter: { currentValue: {} },tab: undefined } as any);

    expect(component.timeFilter).toEqual({} as any);
    expect(competitionFiltersService.filterEvents).toHaveBeenCalledWith(undefined, {} as any, []);
    expect(component.eventsBySections).toEqual([]);
  });

  it('should not update time filter if it`s different from current neither filter events', () => {
    component.eventsBySections = [];
    component.ngOnChanges({ timeFilter: { currentValue: undefined, previousValue: undefined },tab: {currentValue: undefined}  } as any);

    expect(component.timeFilter).toBeUndefined();
    expect(competitionFiltersService.filterEvents).not.toHaveBeenCalled();
    expect(component.eventsBySections).toEqual([]);
  });

  it('should update league filter if it`s different from current and filter events', () => {
    component.ngOnChanges({ leagueFilter: { currentValue: {} }  } as any);

    expect(component.leagueFilter).toEqual({} as any);
    expect(competitionFiltersService.filterEvents).toHaveBeenCalledWith({} as any, undefined, []);
    expect(component.eventsBySections).toEqual([]);
  });

  it('should not update league filter if it`s different from current neither filter events', () => {
    component.eventsBySections = [];
    component.ngOnChanges({ leagueFilter: { currentValue: undefined, previousValue: undefined },tab: {currentValue: 'today'}  } as any);

    expect(component.leagueFilter).toBeUndefined();
    expect(competitionFiltersService.filterEvents).not.toHaveBeenCalled();
    expect(component.eventsBySections).toEqual([]);
  });

  it('should detect tabs changing ngOnChanges and reset applied filter', () => {
    component.ngOnInit();

    component['activeMarketFilter'] = 'test';

    component.ngOnChanges({
      tab: {
        currentValue: 'today',
        previousValue: 'oldTab'
      }
    } as any);

    expect(component['currentTabName']).toEqual('today');
  });

  it('should change or not change sport according to values in changes', () => {
    component.ngOnChanges({
      sport: {
        currentValue: 'currentValue',
        previousValue: 'previousValue'
      }
    } as any);
    expect(component.sport as any).toEqual('currentValue');

    // no changes
    (component.sport as any) = 'previousValue';
    component.ngOnChanges({
      sport: {
        currentValue: 'previousValue',
        previousValue: 'previousValue'
      }
    } as any);
    expect(component.sport as any).toEqual('previousValue');
  });

  it('should change or not change featuredEventsCount according to values in changes', () => {
    component.ngOnChanges({
      featuredEventsCount: {
        currentValue: 1,
        previousValue: 0
      }
    } as any);
    expect(component.featuredEventsCount).toEqual(1);

    // no changes
    component.ngOnChanges({
      sport: {
        currentValue: 2,
        previousValue: 2
      }
    } as any);
    expect(component.featuredEventsCount).toEqual(1);
  });

  it('should not reset applied filter when tab was not changed', () => {
    component.ngOnInit();

    component['activeMarketFilter'] = 'test';

    component.ngOnChanges({
      tab: {
        currentValue: 'newTab',
        previousValue: undefined
      }
    } as any);

    expect(component['activeMarketFilter']).toEqual('test');
  });

  it('should not reset applied filter when tab was not changed', () => {
    component.ngOnInit();

    component['activeMarketFilter'] = 'test';

    component.ngOnChanges({
      tab: {
        currentValue: undefined,
        previousValue: 'oldTab'
      }
    } as any);

    expect(component['activeMarketFilter']).toEqual('test');
  });

  it('should not reset applied filter when not tab update', () => {
    component.ngOnInit();

    component['activeMarketFilter'] = 'test';

    component.ngOnChanges({
      notATab: {}
    } as any);

    expect(component['activeMarketFilter']).toEqual('test');
  });

  describe('prepeareAccordions', () => {
    it('should sort sections by sectionTitle and classDisplayOrder', () => {
      const sections = [
        {
          categoryName: 'American Football',
          classDisplayOrder: 0,
          className: 'American Football USA',
          events: [],
          groupedByDate: [],
          isExpanded: true,
          sectionTitle: 'American Football - NFL',
          typeDisplayOrder: -500,
          typeId: 4,
          typeName: 'NFL'
        },
        {
          categoryName: 'American Football',
          classDisplayOrder: -1,
          className: 'American Football Canada',
          events: [],
          groupedByDate: [],
          isExpanded: true,
          sectionTitle: 'American Football - CFL',
          typeDisplayOrder: -500,
          typeId: 4,
          typeName: 'NFL'
        },
        {
          categoryName: 'American Football',
          classDisplayOrder: -1,
          className: 'American Football Auto Test',
          events: [],
          groupedByDate: [],
          isExpanded: true,
          sectionTitle: 'American Football - Auto Test League',
          typeDisplayOrder: -500,
          typeId: 4,
          typeName: 'NFL'
        },
        {
          categoryName: 'American Football',
          classDisplayOrder: 100500,
          className: 'American Football Auto Test',
          events: [],
          groupedByDate: [],
          isExpanded: true,
          sectionTitle: 'American Football - Auto Test League #2',
          typeDisplayOrder: -500,
          typeId: 4,
          typeName: 'NFL'
        },
      ];

      component.ngOnInit();

      const sortedSections = component['prepeareAccordions'](sections as any);

      expect(sortedSections[0].isExpanded).toBeTruthy();
    });

    it('should set isExpanded = true max to first 3 sections', () => {
      const sections = [
        {
          categoryName: 'American Football',
          classDisplayOrder: 0,
          className: 'American Football USA',
          events: [],
          groupedByDate: [],
          sectionTitle: 'American Football - NFL',
          typeDisplayOrder: -500,
          typeId: 1,
          typeName: 'NFL'
        },
        {
          categoryName: 'American Football2',
          classDisplayOrder: -1,
          className: 'American Football Canada',
          events: [],
          groupedByDate: [],
          sectionTitle: 'American Football - CFL',
          typeDisplayOrder: -500,
          typeId: 2,
          typeName: 'NFL'
        },
        {
          categoryName: 'American Football3',
          classDisplayOrder: -1,
          className: 'American Football Auto Test3',
          events: [],
          groupedByDate: [],
          sectionTitle: 'American Football - Auto Test League',
          typeDisplayOrder: -500,
          typeId: 3,
          typeName: 'NFL'
        },
        {
          categoryName: 'American Football4',
          classDisplayOrder: 100500,
          className: 'American Football Auto Test4',
          events: [],
          groupedByDate: [],
          sectionTitle: 'American Football - Auto Test League #2',
          typeDisplayOrder: -500,
          typeId: 4,
          typeName: 'NFL'
        },
        {
          categoryName: 'American Football5',
          classDisplayOrder: 100500,
          className: 'American Football Auto Test5',
          events: [],
          isExpanded: true,
          groupedByDate: [],
          sectionTitle: 'American Football - Auto Test League #2',
          typeDisplayOrder: -500,
          typeId: 5,
          typeName: 'NFL'
        }
      ];

      component.ngOnInit();

      const sortedSections = component['prepeareAccordions'](sections as any);

      expect(sortedSections[0].isExpanded).toBeTruthy();
      expect(sortedSections[1].isExpanded).toBeTruthy();
      expect(sortedSections[2].isExpanded).toBeTruthy();
      expect(sortedSections[3].isExpanded).toBeFalsy();
      expect(sortedSections[4].isExpanded).toBeTruthy();
    });
  });

  describe('subscribeForSectionUpdates', () => {
    it('should not unsubscribe for updates if there is no section', () => {
      component['subscribeForSectionUpdates'](null);

      expect(component.sport.subscribeEventChildsUpdates).not.toHaveBeenCalled();
    });

    it('should not subscribe for updates if section has subscriptionKey', () => {
      const subscriptionKey = 'type-123';
      const section = { subscriptionKey } as any;
      component['subscribeForSectionUpdates'](section);

      expect(component.sport.subscribeEventChildsUpdates).not.toHaveBeenCalled();
    });

    it('should subscribe for updates and set subscriptionKey', () => {
      const subscriptionKey = 'type-123';
      const section = {
        subscriptionKey: null,
        events: [{ id: 1 }],
        typeId: 442
      } as any;
      (component.sport.subscribeEventChildsUpdates as any).and.returnValue(subscriptionKey);
      component['subscribeForSectionUpdates'](section);

      expect(component.sport.subscribeEventChildsUpdates).toHaveBeenCalledWith(section.events, section.typeId);
      expect(section.subscriptionKey).toEqual(subscriptionKey);
    });
  });

  describe('unsubscribeFromSectionUpdates', () => {
    it('should not unsubscribe from updates if there is no section', () => {
      component['unsubscribeFromSectionUpdates'](null);

      expect(component.sport.unsubscribeEventChildsUpdates).not.toHaveBeenCalled();
    });

    it('should not unsubscribe from updates if section has no subscriptionKey', () => {
      const section = {} as any;
      component['unsubscribeFromSectionUpdates'](section);

      expect(component.sport.unsubscribeEventChildsUpdates).not.toHaveBeenCalled();
    });

    it('should unsubscribe from updates and clear subscriptionKey', () => {
      const subscriptionKey = 'type-123';
      const section = { subscriptionKey } as any;
      component['unsubscribeFromSectionUpdates'](section);

      expect(component.sport.unsubscribeEventChildsUpdates).toHaveBeenCalledWith(subscriptionKey);
      expect(section.subscriptionKey).toBeNull();
    });
  });

  describe('#selectedMarket', () => {
    let eventsBySection;

    beforeEach(() => {
      eventsBySection = {
        defaultValue: 'defaultValue',
        events: [{
          markets: [{
            templateMarketName: 'Market name'
          }]
        }]
      };
    });

    it('should return default value', () => {
      const result = component.selectedMarket(eventsBySection);

      expect(result).toBeUndefined();
    });
    it('should return default value with env data', () => {
      component.sportId = 36;
      const envData = JSON.stringify(environment.CATEGORIES_DATA);
      environment.CATEGORIES_DATA = {
        "defaultMarkets":[{"sportIds":["16","10","32","13","31","30","36"],"name":"Match Result"}]
      } as any;
      eventsBySection.defaultValue = "";
      const result = component.selectedMarket(eventsBySection);
      environment.CATEGORIES_DATA = JSON.parse(envData);
      expect(result).toEqual('Match Result');
    });
  });

  it('#trackByTypeId should return custom type id', () => {
    const sportSection = {
      isExpanded: true,
      typeId: 123,
      deactivated: false
    };

    expect(component.trackByTypeId(123, sportSection as any))
      .toEqual(`${sportSection.typeId}_${sportSection.deactivated}`);
  });

  it('#trackById should return sport event id', () => {
    expect(component.trackById(123, { id: 456 } as any)).toEqual(456);
  });

  it('#hideEnhancedSection should hide enhanced section', () => {
    component.hideEnhancedSection();

    expect(component.isExpandedEnhanced).toBeFalsy();
  });

  describe('#reinitHeader', () => {
    it('should assign changed Market', () => {
      const changedMarket = {
        id: '1',
        cashoutAvail: 'cashoutAvail',
        correctPriceTypeCode: 'correctPriceTypeCode',
        dispSortName: 'dispSortName',
      };

      component.reinitHeader(changedMarket as any);

      expect(component.undisplayedMarket).toEqual(changedMarket as any);
    });
  });

  it('#hideLoading should detect changes and emit data', fakeAsync(() => {
    spyOn(component.isLoadedEvent, 'emit');
    component['hideLoading']();

    tick();
    expect(component.isLoaded).toBeTruthy();
    expect(component['changeDetectorRef'].detectChanges).toHaveBeenCalled();
    expect(component.isLoadedEvent.emit).toHaveBeenCalledWith({ output: 'isLoadedEvent', value: component.isLoaded });
  }));
  describe('schemaForsportsTab', () => {
    it('should get schemadata and publish the data with sport schemaUrl with today', () => {
      component.tab = 'today';
      timeService.determineDay.and.returnValue('today');
      cmsService.getSystemConfig.and.returnValue(observableOf({
        SeoSchemaConfig: {
          schemaConfig: ['today']
        }
      }));
      const matches = [{ events: [{ id: '1', correctedDayValue: 'sb.today',startTime : 100 }], sport: 'football', typeName: 'premier-league', className: 'team', groupedByDate: [{ events: [{ id: '1', }] }] } as any];
      component['schemaForsportsTab'](matches);
      expect(routingHelperService.formSportUrl).toHaveBeenCalled();
      expect(component['sportSchemaUrl']).toEqual('/sport/football');
      expect(competitionFiltersService.getSeoSchemaEvents).toHaveBeenCalled();
      expect(pubSubService.publish).toHaveBeenCalledWith('SCHEMA_DATA_UPDATED', [[{ id: '1' }], '/sport/football'])
    });
    it('should get schemadata and publish the data with sport schemaUr with tommorrow', () => {
      component.tab = 'today';
      timeService.determineDay.and.returnValue('tomorrow');
      cmsService.getSystemConfig.and.returnValue(observableOf({
        SeoSchemaConfig: {
          schemaConfig: ['tomorrow']
        }
      }));
      const matches = [{ events: [{ id: '1', correctedDayValue: 'sb.today', startTime: 100 }], sport: 'football', typeName: 'premier-league', className: 'team', groupedByDate: [{ events: [{ id: '1', }] }] } as any];
      component['schemaForsportsTab'](matches);
      expect(routingHelperService.formSportUrl).toHaveBeenCalled();
      expect(component['sportSchemaUrl']).toEqual('/sport/football');
      expect(competitionFiltersService.getSeoSchemaEvents).toHaveBeenCalled();
      expect(pubSubService.publish).toHaveBeenCalledWith('SCHEMA_DATA_UPDATED', [[{ id: '1' }], '/sport/football']);
    });
    it('should get schemadata and publish the data with sport schemaUrl with both today and tomorrow', () => {
      component.tab = 'today';
      timeService.determineDay.and.returnValue('tomorrow');
      cmsService.getSystemConfig.and.returnValue(observableOf({
        SeoSchemaConfig: {
          schemaConfig: ['today', 'tomorrow']
        }
      }));
      const matches = [{ events: [{ id: '1', correctedDayValue: 'sb.today', startTime: 100 }], sport: 'football', typeName: 'premier-league', className: 'team', groupedByDate: [{ events: [{ id: '1', }] }] } as any];
      component['schemaForsportsTab'](matches);
      expect(routingHelperService.formSportUrl).toHaveBeenCalled();
      expect(component['sportSchemaUrl']).toEqual('/sport/football');
      expect(competitionFiltersService.getSeoSchemaEvents).toHaveBeenCalled();
      expect(pubSubService.publish).toHaveBeenCalledWith('SCHEMA_DATA_UPDATED', [[{ id: '1' }], '/sport/football']);
    });
    it('should get schemadata and publish the data with sport schemaUrl', () => {
      component.tab = 'today';
      timeService.determineDay.and.returnValue('tomorrow');
      cmsService.getSystemConfig.and.returnValue(observableOf({
        SeoSchemaConfig: {
          schemaConfig: null
        }
      }));
      const matches = [{ events: [{ id: '1', correctedDayValue: 'sb.today', startTime: 100 }], sport: 'football', typeName: 'premier-league', className: 'team', groupedByDate: [{ events: [{ id: '1', }] }] } as any];
      component['schemaForsportsTab'](matches);
      expect(component['sportSchemaUrl']).toEqual('/sport/football');
      expect(competitionFiltersService.getSeoSchemaEvents).not.toHaveBeenCalled();
      expect(pubSubService.publish).not.toHaveBeenCalledWith('SCHEMA_DATA_UPDATED', [[{ id: '1' }], '/sport/football']);
    });
    it('should get schemadata and not publish the data with sport schemaUrl with schemaConfig is null', () => {
      component.tab = 'today';
      timeService.determineDay.and.returnValue('tomorrow');
      cmsService.getSystemConfig.and.returnValue(observableOf({
        SeoSchemaConfig: null
      }));
      const matches = [{ events: [{ id: '1', correctedDayValue: 'sb.today', startTime: 100 }], sport: 'football', typeName: 'premier-league', className: 'team', groupedByDate: [{ events: [{ id: '1', }] }] } as any];
      component['schemaForsportsTab'](matches);
      expect(component['sportSchemaUrl']).toEqual('/sport/football');
      expect(competitionFiltersService.getSeoSchemaEvents).not.toHaveBeenCalled();
      expect(pubSubService.publish).not.toHaveBeenCalledWith('SCHEMA_DATA_UPDATED', [[{ id: '1' }], '/sport/football']);
    });
    it('should get schemadata and not publish the data with sport schemaUrl with both SeoSchemaConfig is null', () => {
      component.tab = 'today';
      timeService.determineDay.and.returnValue('tomorrow');
      cmsService.getSystemConfig.and.returnValue(observableOf(null));
      const matches = [{ events: [{ id: '1', correctedDayValue: 'sb.today', startTime: 100 }], sport: 'football', typeName: 'premier-league', className: 'team', groupedByDate: [{ events: [{ id: '1', }] }] } as any];
      component['schemaForsportsTab'](matches);
      expect(component['sportSchemaUrl']).toEqual('/sport/football');
      expect(competitionFiltersService.getSeoSchemaEvents).not.toHaveBeenCalled();
      expect(pubSubService.publish).not.toHaveBeenCalledWith('SCHEMA_DATA_UPDATED', [[{ id: '1' }], '/sport/football']);
    });
    it('should get schemadata and not publish the data with sport schemaUrl', () => {
      component.tab = 'today';
      const matches = [{ events: [null], sport: 'football', typeName: 'premier-league', className: 'team', groupedByDate: [{ events: [{ id: '1', }] }] } as any];
      component['schemaForsportsTab'](matches);
      expect(routingHelperService.formSportUrl).toHaveBeenCalled();
      expect(component['sportSchemaUrl']).toEqual('/sport/football');
      expect(competitionFiltersService.getSeoSchemaEvents).not.toHaveBeenCalled();
      expect(pubSubService.publish).not.toHaveBeenCalledWith('SCHEMA_DATA_UPDATED', [[{ id: '1' }], '/sport/football'])
    });
    it('should get not schemadata and not publish the data with sport schemaUrl', () => {
      component.tab = 'today';
      const matches = [null];
      component['schemaForsportsTab'](matches);
      expect(routingHelperService.formSportUrl).toHaveBeenCalled();
      expect(component['sportSchemaUrl']).toEqual('/sport/football');
      expect(competitionFiltersService.getSeoSchemaEvents).not.toHaveBeenCalled();
      expect(pubSubService.publish).not.toHaveBeenCalledWith('SCHEMA_DATA_UPDATED', [[{ id: '1' }], '/sport/football'])
    });
    it('should get not schemadata and not publish the data with sport schemaUrl', () => {
      component.tab = 'today';
      const matches = [{ sport: 'football', typeName: 'premier-league', className: 'team', groupedByDate: [{ events: [{ id: '1', }] }] } as any];
      component['schemaForsportsTab'](matches);
      expect(routingHelperService.formSportUrl).toHaveBeenCalled();
      expect(component['sportSchemaUrl']).toEqual('/sport/football');
      expect(competitionFiltersService.getSeoSchemaEvents).not.toHaveBeenCalled();
      expect(pubSubService.publish).not.toHaveBeenCalledWith('SCHEMA_DATA_UPDATED', [[{ id: '1' }], '/sport/football'])
    });
  });
  describe('removeSchemaForSportsTab', () => {
    it('should publish schema_removed with url', () => {
      component['sportSchemaUrl'] = '/sport/football';
      component['removeSchemaForSportsTab']();
      expect(pubSubService.publish).toHaveBeenCalledWith(pubSubApi.SCHEMA_DATA_REMOVED, '/sport/football');
    });
    it('should not publish schema_removed with url', () => {
      component['competitionUrl'] = null;
      component['removeSchemaForSportsTab']();
      expect(pubSubService.publish).not.toHaveBeenCalledWith(pubSubApi.SCHEMA_DATA_REMOVED, '/sport/football');
    });
  });


  describe('activeIndex', () => {
    it('should call activeIndex', () => {
      component.eventsBySections = [{deactivated: false}, {deactivated: true}] as any;
      const retVal = component.activeIndex(2);
      expect(retVal).toBe(1);
    });
  });
})
 
  

 
