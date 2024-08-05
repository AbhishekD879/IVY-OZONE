import { fakeAsync, tick } from '@angular/core/testing';
import { YourcallService } from '@yourcall/services/yourcallService/yourcall.service';
import { of, Observable, throwError } from 'rxjs';
import {
  ILeagueResponse
} from '@yourcall/models/leagues.model';
import { map } from 'rxjs/operators';
import { YourCallLeague } from '@yourcall/models/yourcall-league';

describe('YourcallService', () => {
  let service;
  let eventsWithYCFlag;
  let eventsWithoutYCFlag;
  let pubsubService;
  let cmsService;
  let yourcallProviderService;
  let routingHelperService;
  let siteServerService;
  let gtmService;
  let mockedConfig;
  let localeService;

  beforeEach(() => {
    eventsWithYCFlag = [
      { drilldownTagNames: 'EVFLAG_ABC,EVFLAG_YC,' },
      { drilldownTagNames: 'EVFLAG_ABC,' }
    ];
    eventsWithoutYCFlag = [
      { drilldownTagNames: 'EVFLAG_ABC,' },
      { drilldownTagNames: 'EVFLAG_ABC,' }
    ];
    mockedConfig = [
      { typeId: 1 },
      { typeId: 2 }
    ];
    pubsubService = {
      subscribe: jasmine.createSpy('subscribe'),
      API: {
        SYSTEM_CONFIG_UPDATED: 'SYSTEM_CONFIG_UPDATED'
      }
    };
    cmsService = {
      getSystemConfig: jasmine.createSpy('getSystemConfig').and.returnValue(of({})),
      getCmsYourCallLeaguesConfig: jasmine.createSpy('getCmsYourCallLeaguesConfig').and.returnValue(of(mockedConfig)),
      getYourCallStaticBlock: jasmine.createSpy('getYourCallStaticBlock'),
    };
    yourcallProviderService = {
      useOnce: jasmine.createSpy().and.returnValue({
        getLeagues: () => of([]),
        getLeagueEventsWithoutPeriod: () => new Observable<boolean>()
      })
    };
    routingHelperService = {
      formEdpUrl: jasmine.createSpy('formEdpUrl').and.returnValue('event/12345')
    };
    siteServerService = {
      getClassToSubTypeForTypeByPortions: jasmine.createSpy('getClassToSubTypeForTypeByPortions')
    };
    gtmService = {
      push: jasmine.createSpy('push')
    };
    localeService = {
      getString: jasmine.createSpy('getString').and.returnValue('build-your-bet')
    };

    service = new YourcallService(
      pubsubService,
      cmsService,
      yourcallProviderService,
      routingHelperService,
      siteServerService,
      gtmService,
      localeService
    );
  });

  describe('$onInit', () => {
    it('should onInit', () => {
      const config = {
        YourCallIconsAndTabs: {
          enableTab: true,
          enableIcon: true
        },
        YourCallPage: {
          enable: true
        }
      };
      pubsubService.subscribe.and.callFake((p1, p2, cb) => cb(config));
      service.$onInit();

      expect(service.isEnabledYCTab).toEqual(true);
      expect(service.isEnabledYCIcon).toEqual(true);
      expect(service.isEnabledYCPage).toEqual(true);
    });
  });

  describe('getStaticBlocks(', () => {
    it('should get static blocks', () => {
      const data = [{
        title: 'title'
      }];
      cmsService.getYourCallStaticBlock.and.returnValue(of(data));
      service.getStaticBlocks();

      expect(service.staticBlock).toEqual( {
        title: {
          title: 'title'
        }
      });
    });
  });

  describe('isBYBIconAvailable', () => {
    it('should return correct ByB icon status', () => {
      const spy = spyOn(service, 'isAvailableForCompetition');
      spy.and.returnValue(true);
      expect(service.isBYBIconAvailable(111)).toBeTruthy();

      spy.and.returnValue(false);
      expect(service.isBYBIconAvailable(111)).toBeFalsy();
    });
  });

  describe('isBYBIconAvailableForEvents', () => {
    it('should return correct ByB icon status', () => {
      service.isEventsAvailableForCompetition = jasmine.createSpy('isEventsAvailableForCompetition').and.returnValue(false);

      service.isBYBIconAvailableForEvents(123);
      expect(service['isEventsAvailableForCompetition']).toHaveBeenCalledWith(123);
      expect(service.isBYBIconAvailableForEvents(123)).toBeFalsy();
    });
  });

  describe('#isFiveASideAvailableForCompetition', () => {
    it('when ruleToCheck false', () => {
      const result = service.isFiveASideAvailableForCompetition(1, false);

      expect(result).toEqual(false);
    });

    it('when ruleToCheck true, leaguesConfigMap false', () => {
      service.leaguesIndexMap[1] = 1;
      service.leagues = ['Test league', 'Premier League'];
      const result = service.isFiveASideAvailableForCompetition(1, true);

      expect(result).toEqual(undefined);
    });

    it('when ruleToCheck true, leaguesConfigMap.activeFor5aSide false', () => {
      service.leaguesIndexMap[1] = 1;
      service.leagues = ['Test league', 'Premier League'];
      service.leaguesConfigMap[1] = {
        activeFor5aSide: false
      };
      const result = service.isFiveASideAvailableForCompetition(1, true);

      expect(result).toEqual(false);
    });

    it('when ruleToCheck true, leaguesConfigMap.activeFor5aSide true', () => {
      service.leaguesIndexMap[1] = 1;
      service.leagues = ['Test league', 'Premier League'];
      service.leaguesConfigMap[1] = {
        activeFor5aSide: true
      };
      const result = service.isFiveASideAvailableForCompetition(1, true);

      expect(result).toEqual(true);
    });
  });

  describe('#isAvailableForCompetition', () => {
    it('when ruleToCheck false', () => {
      const result = service.isAvailableForCompetition(1, false);

      expect(result).toEqual(false);
    });

    it('when ruleToCheck true, leaguesConfigMap false', () => {
      service.leaguesIndexMap[1] = 1;
      service.leagues = ['Test league', 'Premier League'];
      const result = service.isAvailableForCompetition(1, true);

      expect(result).toEqual(undefined);
    });

    it('when ruleToCheck true, leaguesConfigMap.enabled false', () => {
      service.leaguesIndexMap[1] = 1;
      service.leagues = ['Test league', 'Premier League'];
      service.leaguesConfigMap[1] = {
        enabled: false
      };
      const result = service.isAvailableForCompetition(1, true);

      expect(result).toEqual(false);
    });

    it('when ruleToCheck true, leaguesConfigMap.enabled true', () => {
      service.leaguesIndexMap[1] = 1;
      service.leagues = ['Test league', 'Premier League'];
      service.leaguesConfigMap[1] = {
        enabled: true
      };
      const result = service.isAvailableForCompetition(1, true);

      expect(result).toEqual(true);
    });
  });

  describe('isEventsAvailableForCompetition', () => {
    it('should return false', () => {
      const result = service.isEventsAvailableForCompetition(123);

      expect(result).toBe(false);
    });

    it('should return true', () => {
      service.eventsData = [
        {
          data: [{ obEventId: 222 }, { obEventId: 123 }]
        }
      ];
      const result = service.isEventsAvailableForCompetition(123);

      expect(result).toBe(true);
    });
  });

  describe('isYCIconAvailable', () => {
    it('should return correct YC icon status', () => {
      expect(service.isYCIconAvailable(eventsWithYCFlag as any)).toBeTruthy();
      expect(service.isYCIconAvailable(eventsWithoutYCFlag as any)).toBeFalsy();
    });
  });

  describe('isYCAvailableForEventByOBFlag', () => {
    it('should check if any event has YC flag', () => {
      expect(service.isYCAvailableForEventByOBFlag(eventsWithYCFlag[0] as any)).toBeTruthy();
      expect(service.isYCAvailableForEventByOBFlag(eventsWithoutYCFlag[1] as any)).toBeFalsy();
    });

    it('should check if any event has YC flag case without drilldownTagNames', () => {
     const eventsWithYCFlag1 = [ {}, {} ],
       eventsWithoutYCFlag1 = [ {}, {} ];

      expect(service.isYCAvailableForEventByOBFlag(eventsWithYCFlag1[0] as any)).toBeFalsy();
      expect(service.isYCAvailableForEventByOBFlag(eventsWithoutYCFlag1[1] as any)).toBeFalsy();
    });
  });

  describe('sendGTM', () => {
    beforeEach(() => {
      spyOn<any>(service, 'sendGTM');
      spyOn<any>(service, 'changeToggleState');
    });

    it('should not send toggle events', () => {
      const data = {};
      service.isFirstTimeClicked = [{ collapsed: true, expanded: true }];
      service.sendToggleGTM(data, 0, true);

      expect(service['sendGTM']).not.toHaveBeenCalled();
      expect(service['changeToggleState']).not.toHaveBeenCalled();
    });

    it('should send expand event', () => {
      const data = {};
      service.isFirstTimeClicked = [{ collapsed: false, expanded: false }];
      service.sendToggleGTM(data, 0, true);

      expect(service['sendGTM']).toHaveBeenCalledWith(data, 'expand market accordion');
      expect(service['changeToggleState']).toHaveBeenCalledWith(0, 'expanded');
    });

    it('should send collapse event', () => {
      const data = {};
      service.isFirstTimeClicked = [{ collapsed: false, expanded: false }];
      service.sendToggleGTM(data, 0, false);

      expect(service['sendGTM']).toHaveBeenCalledWith(data, 'collapse market accordion');
      expect(service['changeToggleState']).toHaveBeenCalledWith(0, 'collapsed');
    });
  });

  describe('sendGTM', () => {
    const action = 'expand market accordion';

    it('should track league for events', () => {
      const data = {
        events: {},
        title: 'league title'
      } as any;

      service['sendGTM'](data, action);

      expect(gtmService.push).toHaveBeenCalledWith('trackEvent', {
        eventAction: 'league',
        eventCategory: 'your call',
        eventLabel: action,
        league: data.title
      });
    });

    it('should track league for isSpecials', () => {
      const data = {
        isSpecials: true,
        title: 'special market title'
      } as any;

      service['sendGTM'](data, action);

      expect(gtmService.push).toHaveBeenCalledWith('trackEvent', {
        eventAction: 'league',
        eventCategory: 'your call',
        eventLabel: action,
        league: data.title
      });
    });

    it('should track Player Bets', () => {
      const data = {
        type: 'playerBets',
        provider: 'BYB'
      } as any;

      service['sendGTM'](data, action);

      expect(gtmService.push).toHaveBeenCalledWith('trackEvent', {
        eventAction: 'build bet',
        eventCategory: 'your call',
        eventLabel: action
      });
    });

    it('should track BYB markets', () => {
      const data = {
        markets: {}
      } as any;

      service['sendGTM'](data, action);

      expect(gtmService.push).toHaveBeenCalledWith('trackEvent', {
        eventAction: 'build bet',
        eventCategory: 'your call',
        eventLabel: action
      });
    });

    it('should track market accordions', () => {
      const data = {
        dsMarket: {},
        provider: 'BYB'
      } as any;

      service['sendGTM'](data, action);

      expect(gtmService.push).toHaveBeenCalledWith('trackEvent', {
        eventAction: 'build bet',
        eventCategory: 'your call',
        eventLabel: action
      });
    });

    it('should track market accordions', () => {
      const data = {
        dsMarket: {},
        provider: 'build bet'
      } as any;

      service['sendGTM'](data, action);

      expect(gtmService.push).toHaveBeenCalledWith('trackEvent', {
        eventAction: false,
        eventCategory: 'your call',
        eventLabel: action
      });
    });
  });

  describe('getLeaguesAndCache', () => {
    it('shouldn\'t make call for Leagues if they are cached', fakeAsync(() => {
      const obs1 = service['getLeaguesAndCache'](true);
      obs1.subscribe();
      tick();
      const obs2 = service['getLeaguesAndCache'](true);
      tick();
      const obs3 = service['getLeaguesAndCache'](true);
      tick();

      expect(obs1).not.toEqual(obs2);
      expect(obs1).not.toEqual(obs3);
    }));

    it('should make call for Leagues if they are not cached', (done) => {
      const arr = [1, 2, 3];
      service['leaguesAndCache$'] = of(arr);
      const obs = service['getLeaguesAndCache']();

      obs.subscribe((result) => {
        expect(result).toBe(arr);
        done();
      });
    });

    it('should return empty of', () => {

      service.leaguesData= [{'data':[{'id':1,'className':'test'}]}] as ILeagueResponse[];
            const obs = service['getLeaguesAndCache'](true);
            obs.pipe(map((res) => {
              expect(res).toEqual(of());
           }));
    });
  });

  describe('getEventsAndCache', () => {
    it('shouldn\'t make call for Events if they are cached', fakeAsync(() => {
      yourcallProviderService.useOnce = jasmine.createSpy().and.returnValue({
        getLeagues: () => of([]),
        getLeagueEventsWithoutPeriod: jasmine.createSpy('getLeagueEventsWithoutPeriod').and.returnValue(of([1, 2, 3]))
      });
      service = new YourcallService(
        pubsubService,
        cmsService,
        yourcallProviderService,
        routingHelperService,
        siteServerService,
        gtmService,
        localeService
      );
      const obs1 = service['getEventsAndCache'](true);
      obs1.subscribe();
      tick();
      const obs2 = service['getEventsAndCache'](true);
      tick();
      const obs3 = service['getEventsAndCache'](true);
      tick();

      expect(obs1).not.toBe(obs2);
      expect(obs1).not.toBe(obs3);
    }));

    it('Should error', (done) => {
      yourcallProviderService.useOnce = jasmine.createSpy().and.returnValue({
        getLeagues: () => of([]),
        getLeagueEventsWithoutPeriod: jasmine.createSpy('getLeagueEventsWithoutPeriod').and.returnValue(Promise.reject())
      });

      service = new YourcallService(
        pubsubService,
        cmsService,
        yourcallProviderService,
        routingHelperService,
        siteServerService,
        gtmService,
        localeService
      );
      service['getEventsAndCache'](true).subscribe((val) => {
        expect(yourcallProviderService.useOnce).toHaveBeenCalled();
      }, () => {
        done();
      });
    });

    it('should call for events if default param was used', () => {
      service['getEventsAndCache']();
      expect(yourcallProviderService.useOnce).toHaveBeenCalled();
    });
  });

  describe('whenYCReady', () => {
    it('should call for events', ((done) => {
      service['yourCallSwitchers$'] = of([]);
      service['init'] = jasmine.createSpy('init').and.returnValue(of([]));
      service['getEventsAndCache'] = jasmine.createSpy('getEventsAndCache').and.returnValue(of([]));
      service['ruleToCheck'] = true;

      service.whenYCReady('ruleToCheck').subscribe(() => {
        expect(yourcallProviderService.useOnce).toHaveBeenCalled();
        expect(service['init']).toHaveBeenCalled();
        done();
      });
    }));

    it('should NOT call for events', ((done) => {
      service['yourCallSwitchers$'] = of([]);
      service['whenReadyPromise'] = false;
      service['init'] = jasmine.createSpy('init').and.returnValue(of([]));

      service.whenYCReady(false).subscribe(result => {
        expect(service['init']).not.toHaveBeenCalled();
        expect(result).toBe(true);
        done();
      });
    }));

    it('should call for events with use cache', ((done) => {
      service['yourCallSwitchers$'] = of([]);
      service['init'] = jasmine.createSpy('init').and.returnValue(of([]));
      service['getEventsAndCache'] = jasmine.createSpy('getEventsAndCache').and.returnValue(of([]));
      service['ruleToCheck'] = true;

      service.whenYCReady('ruleToCheck', true).subscribe(() => {
        expect(yourcallProviderService.useOnce).toHaveBeenCalled();
        expect(service['init']).toHaveBeenCalled();
        done();
      });
    }));
  });

  describe('init', () => {
    it('should set leagues, leaguesIndexMap and return true', (done) => {
      service['config$'] = of([]);
      service['getAvailableLeagues'] = jasmine.createSpy('getAvailableLeagues').and.returnValue(of([]));
      service['sortLeagues'] = jasmine.createSpy('sortLeagues');
      service['mapLeagues'] = jasmine.createSpy('mapLeagues');

      service.init().subscribe(() => {
        expect(service['sortLeagues']).toHaveBeenCalled();
        expect(service['mapLeagues']).toHaveBeenCalled();
        done();
      });
    });

    it('should return false in case of error', (done) => {
      service['config$'] = throwError({});

      service.init().subscribe(result => {
        expect(result).toBe(false);
        done();
      });
    });
  });

  describe('getConfig', () => {
    it('should set proper leagues properties', () => {
      service['getConfig']().subscribe();

      expect(cmsService.getCmsYourCallLeaguesConfig).toHaveBeenCalled();
      expect(service['leaguesOrdering']).toEqual([2, 1]);
      expect(service['leaguesConfigMap']).toEqual({1: mockedConfig[0], 2: mockedConfig[1]});
    });
    it('should call error callback', () => {
      cmsService.getCmsYourCallLeaguesConfig = jasmine.createSpy('getCmsYourCallLeaguesConfig').and.returnValue(throwError([]));
      service = new YourcallService(
        pubsubService,
        cmsService,
        yourcallProviderService,
        routingHelperService,
        siteServerService,
        gtmService,
        localeService
      );
      service['getConfig']().subscribe(result => {
        expect(result).toEqual([]);
      });
    });
  });

  describe('getAvailableLeagues', () => {
    it('should set leagues', (done) => {
      const arr = [3, 2, 1];
      yourcallProviderService = {
        useOnce: jasmine.createSpy().and.returnValue({
          getLeagues: () => Promise.resolve({
            data: [{
              id: 2
            }]
          }),
          getLeagueEventsWithoutPeriod: () => new Observable<boolean>()
        }),
      };
      service = new YourcallService(
        pubsubService,
        cmsService,
        yourcallProviderService,
        routingHelperService,
        siteServerService,
        gtmService,
        localeService
      );

      service['mergeLeagues'] = jasmine.createSpy('mergeLeagues').and.returnValue(arr);

      service['getAvailableLeagues']().subscribe(() => {
        expect(service.leagues).toBe(arr);
        done();
      });
    });

    it('should call error callback', () => {
      service.getLeaguesAndCache = jasmine.createSpy('getLeaguesAndCache').and.returnValue(throwError([]));

      service['getAvailableLeagues']().subscribe(result => {
        expect(result).toEqual([]);
      });
    });
  });

  describe('yourCallSwitchers', () => {
    it('should call setConfigs', () => {
      service['setConfigs'] = jasmine.createSpy();
      service['yourCallSwitchers'].subscribe();
      expect(cmsService.getSystemConfig).toHaveBeenCalled();
      expect(service['setConfigs']).toHaveBeenCalledWith({});
    });
    it('should call error callback', () => {
      cmsService.getSystemConfig = jasmine.createSpy('getSystemConfig').and.returnValue(throwError([]));
      service = new YourcallService(
        pubsubService,
        cmsService,
        yourcallProviderService,
        routingHelperService,
        siteServerService,
        gtmService,
        localeService
      );
      service['yourCallSwitchers'].subscribe(result => {
        expect(result).toEqual([]);
      });
    });
  });

  describe('#getYCTab', () => {
    it('should call getYCTab method and return tab', () => {
      const result = service.getYCTab({} as any);

      expect(result).toEqual({
        name: 'build-your-bet',
        marketName: 'build-your-bet',
        url: `/event/12345/build-your-bet`,
        markets: []
      });
    });
  });

  describe('#get5ASideTab', () => {
    it('should call get5ASideTab method and return tab', () => {
      const result = service.get5ASideTab({} as any);

      expect(result).toEqual({
        name: '5-A-Side',
        marketName: '5-a-side',
        url: `/event/12345/5-a-side`,
        markets: []
      });
    });
  });

  describe('#sendToggleGTM', () => {
    beforeEach(() => {
      service.sendGTM = jasmine.createSpy('sendGTM');
      service.changeToggleState = jasmine.createSpy('changeToggleState');
    });

    it('should send Toggle GTM', () => {
      const data = {
        title: 'new'
      } as any;
      service.isFirstTimeClicked = [{ collapsed: false, expanded: false }];
      service.sendToggleGTM(data, 0, true);

      expect(service.sendGTM).toHaveBeenCalledWith({ title: 'new' }, 'expand market accordion');
      expect(service.changeToggleState).toHaveBeenCalledWith(0, 'expanded');
    });

    it('should send Toggle GTM', () => {
      const data = {
        title: 'new'
      } as any;
      service.isFirstTimeClicked = [{ collapsed: false, expanded: false }];
      service.sendToggleGTM(data, 0, false);

      expect(service.sendGTM).toHaveBeenCalledWith({ title: 'new' }, 'collapse market accordion');
      expect(service.changeToggleState).toHaveBeenCalledWith(0, 'collapsed');
    });

    it('should send Toggle GTM', () => {
      const data = {
        title: 'new'
      } as any;
      service.isFirstTimeClicked = [{ collapsed: true, expanded: true }];
      service.sendToggleGTM(data, 0, false);

      expect(service.sendGTM).not.toHaveBeenCalled();
      expect(service.changeToggleState).not.toHaveBeenCalled();
    });
  });

  describe('#changeToggleState', () => {
    it('should change Toggle State', () => {
      service.isFirstTimeClicked = [{ collapsed: false, expanded: false }];
      service.changeToggleState(0, 'expanded');
    });
  });

  describe('#getStaticBlock', () => {
    it('should get static block and return key', () => {
      service.staticBlock = {
        key: '3'
      };
      const res = service.getStaticBlock('key');

      expect(res).toEqual('3');
    });

    it('should get static block and return null', () => {
      service.staticBlock = {
        key: '3'
      };
      const res = service.getStaticBlock('key1');

      expect(res).toEqual(null);
    });
  });

  describe('#prepareMarkets', () => {
    it('should prepare Markets', () => {
      const data = [
        { markets: [{
            showLimit: 4,
            sAllShown: false
          }],
          event: [{
            markets: [{
              showLimit: 3,
              isAllShown: false
            }]
          }]
        }] as any;

      service.prepareMarkets(data);

      expect(data[0].markets[0].showLimit).toEqual(3);
      expect(data[0].markets[0].sAllShown).toEqual(false);
    });
  });

  describe('#accordionsStateInit', () => {
    it('should Set initial collapse/expand states', () => {
      service['accordionsStateInit'](3);

      expect(service.isFirstTimeClicked).toEqual([
        { collapsed: false, expanded: false },
        { collapsed: false, expanded: false },
        { collapsed: false, expanded: false },
      ]);
    });
  });

  describe('#mapLeagues', () => {
    it('should map Leagues', () => {
      const leagues =[
        {obTypeId: 123},
        {obTypeId: 345}
      ] as any;
      const res = service['mapLeagues'](leagues);

      expect(res).toEqual({123: 0, 345:1}) ;
    });

    it('should map Leagues case Empty league', () => {
      const leagues =[ {}, {} ] as any;
      const res = service['mapLeagues'](leagues);

      expect(res).toEqual({}) ;
    });
  });

  describe('#getClassData', () => {
    it('should Get class data per typeIds from OB', () => {
      const ids = [ 124, 567, 124, 45 ] as any;
      siteServerService.getClassToSubTypeForTypeByPortions.and.returnValue([124, 567, 45]);
      const res = service.getClassData(ids);

      expect(res).toEqual([124, 567, 45]);
    });

    it('should Get class data per typeIds from OB', fakeAsync( () => {
      const ids = [] as any;
      siteServerService.getClassToSubTypeForTypeByPortions.and.returnValue([]);
      service.getClassData(ids).then(data => {
        expect(data).toEqual([]);
      });
      tick();
    }));
  });

  describe('#sortLeagues', () => {
    it('should sort Leagues', () => {
      const leagues = [{
        obTypeId: 123,
        title: 'l1',
        id: 1,
        status: 3,
        byb: true }, {
        obTypeId: 345,
        title: 'l2',
        id: 2,
        status: 3,
        byb: true
      }] as any;
      service['sortLeagues'](leagues);

      expect(service.leaguesOrdering).toEqual([]);
    });
  });

  describe('#isDisabled', () => {
    it('should return true', () => {
      const league = {
        obTypeId: 5678
      } as any;
      service['leaguesConfigMap'][league.obTypeId] = { enabled: false };
      const res = service.isDisabled(league);

      expect(res).toEqual(true);
    });

    it('should return false', () => {
      const league = {
        obTypeId: 5678
      } as any;
      service['leaguesConfigMap'][league.obTypeId] = { enabled: true };
      const res = service.isDisabled(league);

      expect(res).toEqual(false);
    });

    it('should return false', () => {
      const league = {
        obTypeId: 5678
      } as any;
      const res = service.isDisabled(league);

      expect(res).toEqual(false);
    });
  });

  describe('#mergeLeagues', () => {
    it('should merge Leagues', () => {
      const bybData = [
        { obTypeId: 987,
          tittle: 'title',
          categoryId: '16',
          categoryName: 'football',
          status:  3,
          normilized: false
        }] as any;

      const res = service.mergeLeagues(bybData);
      expect(res).toEqual([new YourCallLeague(987, undefined, 3, { byb: true, id: undefined }) as any]);
    });
  });

  describe('#setConfigs', () => {
    it('should ger data from config and set properties', () => {
      const config = {
        YourCallIconsAndTabs: {
          enableIcon: true,
          enableTab: true
        },
        YourCallPage: {
          enabled: true
        },
        FiveASide: {
          enabled: true,
          newIcon: true
        }
      } as any;
      service.setConfigs(config);

      expect(service.isEnabledYCTab).toEqual(true);
      expect(service.isEnabledYCIcon).toEqual(true);
      expect(service.isEnabledYCPage).toEqual(false);
      expect(service.isFiveASideNewIconAvailable).toEqual(true);
      expect(service.isFiveASideAvailable).toEqual(true);
    });

    it('should ger data from config and set properties', () => {
      const config = {
        YourCallIconsAndTabs: {},
        YourCallPage: {},
        FiveASide: {}
      } as any;
      service.setConfigs(config);

      expect(service.isEnabledYCTab).toEqual(false);
      expect(service.isEnabledYCIcon).toEqual(false);
      expect(service.isEnabledYCPage).toEqual(false);
      expect(service.isFiveASideNewIconAvailable).toEqual(false);
      expect(service.isFiveASideAvailable).toEqual(false);
    });
  });
});
