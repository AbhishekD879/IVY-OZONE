import { ElementRef } from '@angular/core';
import { fakeAsync, tick, discardPeriodicTasks } from '@angular/core/testing';
import { of as observableOf, throwError } from 'rxjs';

import {
  CompetitionsPageComponent
} from '@lazy-modules/competitionsSportTab/components/competitionsPage/competitions-page.component';
import { COMPETITIONS_TABS } from '@lazy-modules/competitionsSportTab/contstants/competitions.constant';
import { ICompetitionCategory } from '@lazy-modules/competitionsSportTab/components/competitionsSportTab/competitions.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import environment from '@environment/oxygenEnvConfig';

describe('CompetitionsPageComponent', () => {
  let component: CompetitionsPageComponent;
  let currentMatchesService;
  let cmsService;
  let storageService;
  let windowRefService;
  let filterService;
  let commandService;
  let activatedRoute;
  let router;
  let renderer;
  let pubsubService;
  let cmsCompetitionsData;
  let ssCompetitionsData;
  let typeEventsByClassNameData;
  let updateEventService;
  let changeDetectorRef;
  let domToolsService;
  let sportsConfigService;
  let sportConfig;
  let competitionFiltersService;
  let deviceService;
  let routingHelperService;

  beforeEach(() => {
    environment.brand = 'ladbrokes';
    environment.CURRENT_PLATFORM = 'mobile';
    cmsCompetitionsData = { 'A-ZClassIDs': '11,12', InitialClassIDs: '21,22' };
    ssCompetitionsData = [{
      class: {
        categoryCode: 'Football',
        categoryDisplayOrder: '-9998',
        categoryId: '16',
        categoryName: 'Football',
        classSortCode: 'ST',
        classStatusCode: 'A',
        displayOrder: '0',
        hasNext24HourEvent: 'true',
        hasOpenEvent: 'true',
        id: '609',
        isActive: 'true',
        name: 'Football World Club Competitions',
        originalName: 'Football World Club Competitions',
        responseCreationTime: '2019-01-30T09:44:06.550Z',
        siteChannels: 'P,Q,C,I,M,'
      },
      loading: true,
      type: {
        cashoutAvail: 'Y',
        classId: '609',
        displayOrder: -1270,
        hasNext24HourEvent: 'true',
        hasOpenEvent: 'true',
        id: '27194',
        isActive: 'true',
        name: 'ASEAN League',
        siteChannels: 'P,Q,C,I,M,',
        typeFlagCodes: 'IVA,',
        typeStatusCode: 'A'
      }
    }];
    typeEventsByClassNameData = {
      outrights: [{ name: 'outright event' }],
      data: {
        events: [{ name: 'eventName' }],
        type: {
          id: 'typeId',
          name: 'typeName',
          classId: 'classId'
        }
      }
    };
    windowRefService = {
      nativeWindow: {
        setInterval: jasmine.createSpy('setInterval').and.callFake(cb => cb()),
        clearInterval: jasmine.createSpy('clearInterval')
      },
      document: {
        documentElement: { scrollTop: 0 },
        body: {
          clientHeight: 500,
          scrollTop: 0
        },
        getElementById: jasmine.createSpy('getElementById').and.returnValue({
          classList: {
            add: jasmine.createSpy().and.returnValue('fav-icon-active'),
            remove: jasmine.createSpy().and.returnValue('fav-icon-inactive')
          }
        }),
        querySelector: jasmine.createSpy('querySelector').and.returnValue({ offsetHeight: 400 })
      }
    };
    filterService = {
      orderBy: jasmine.createSpy('orderBy').and.callFake(data => data)
    };
    renderer = {
      listen: jasmine.createSpy('listen'),
      setStyle: jasmine.createSpy('setStyle')
    };
    activatedRoute = {
      snapshot: {
        params: ['football'],
        paramMap: { get: jasmine.createSpy('get').and.returnValue('football') }
      },
      params: observableOf({ typeName: 'typeName', className: 'className' })
    };
    commandService = {
      executeAsync: jasmine.createSpy('executeAsync').and.returnValue(Promise.resolve({ id: 451 })),
      API: { GET_SEASON: 'GET_SEASON' }
    };
    router = {
      navigateByUrl: jasmine.createSpy('navigateByUrl').and.returnValue(true)
    };
    currentMatchesService = {
      getFootballClasses: jasmine.createSpy('getFootballClasses').and.returnValue(Promise.resolve(ssCompetitionsData)),
      getTypeEventsByClassName: jasmine.createSpy('getTypeEventsByClassName').and.returnValue(Promise.resolve(typeEventsByClassNameData)),
      subscribeForUpdates: jasmine.createSpy('subscribeForUpdates'),
      unSubscribeForUpdates: jasmine.createSpy('unSubscribeForUpdates'),
      getTypesForClasses: jasmine.createSpy('getTypesForClasses').and.returnValue(Promise.resolve(ssCompetitionsData)),
      getOtherClasses: jasmine.createSpy('getOtherClasses').and.returnValue(Promise.resolve(ssCompetitionsData))
    };
    pubsubService = {
      subscribe: jasmine.createSpy('subscribe'),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      publish: jasmine.createSpy('publish'),
      API: pubSubApi
    };
    cmsService = {
      getCompetitions: jasmine.createSpy('getCompetitions').and.returnValue(observableOf(cmsCompetitionsData)),
      getItemSvg: jasmine.createSpy('getItemSvg').and.returnValue(observableOf({
        svg: 'svg',
        svgId: 'svgId'
      })),
      getSportTabs: jasmine.createSpy('getSportTabs').and.returnValue(observableOf({tabs: []}))
    };
    storageService = {
      get: jasmine.createSpy('get').and.callFake(key =>
        key === 'competitionsMainClasses_football' ? [{ class: { id: 'c1' } }] :
          key === 'competitionsAZClasses_football' ? ['1', '2', '3'] :
            null)
    };
    updateEventService = {};
    changeDetectorRef = {
      detach: jasmine.createSpy('detach'),
      detectChanges: jasmine.createSpy('detectChanges')
    };
    domToolsService = {
      getElementBottomPosition: jasmine.createSpy('getElementBottomPosition')
    };
    sportsConfigService = {
      getSport: jasmine.createSpy('getSport').and.returnValue(observableOf({ sportConfig: sportConfig }))
    };
    sportConfig = {
      config: {
        request: { categoryId: '16' },
        tier: 1
      },
      tabs: []
    };
    competitionFiltersService = {
      formTimeFilters: jasmine.createSpy('formTimeFilters').and.returnValue([]),
      filterEvents: jasmine.createSpy('filterEvents').and.returnValue([{}]),
      getSportEventFiltersAvailability: jasmine.createSpy('getSportEventFiltersAvailability').and.returnValue(observableOf(true)),
      getSeoSchemaEvents: jasmine.createSpy('getSeoSchemaEvents').and.returnValue([{id:'1'}])
    };
    deviceService = {
      isRobot: jasmine.createSpy('isRobot').and.returnValue(true)
    };
    routingHelperService = {
      formCompetitionUrl: jasmine.createSpy().and.returnValue('/football/premier-league')
    };
    component = new CompetitionsPageComponent(
      activatedRoute,
      currentMatchesService,
      filterService,
      commandService,
      windowRefService,
      cmsService,
      renderer,
      storageService,
      router,
      changeDetectorRef,
      pubsubService,
      domToolsService,
      sportsConfigService,
      competitionFiltersService,
      routingHelperService,
      deviceService,
      updateEventService);

    component.sportId = '16';
    component.competitionsList = { nativeElement: '<competitionsList>' } as ElementRef;
    component.sport = {
      arrangeEventsBySection: jasmine.createSpy('arrangeEventsBySection').and.returnValue([{
        groupedByDate: [{ events: [{ id: '1' }] }, { events: [{ id: '2' }] }]
      }])
    } as any;
    spyOn(console, 'warn');
  });

  it('should call favIconDown', () => {
    component.favIconDown();
    expect(windowRefService.document.getElementById).toHaveBeenCalledWith('fav-icon');
  })
  it('should call favIconUp', () => {
    component.favIconUp();
    expect(windowRefService.document.getElementById).toHaveBeenCalledWith('fav-icon');
  })

  it('should create component instance', () => {
    expect(component).toBeTruthy();
    expect(component.sportName).toEqual('football');
    expect(component.isOnHomePage).toEqual(false);
    expect(component.sportDefaultPath).toEqual('sport/football/competitions');
    expect(component.sportId).toEqual('16');
    expect(component.mainCategories).toEqual([{ class: { id: 'c1' } } as ICompetitionCategory]);
    expect(component.allCategoriesClasses).toEqual(['1', '2', '3']);
    expect(storageService.get.calls.allArgs()).toEqual([['competitionsMainClasses_football'], ['competitionsAZClasses_football']]);
  });

  describe('#ngOnInit', () => {
    beforeEach(() => {
      spyOn(component, 'loadAllCompetitions');
      spyOn(component, 'loadCompetitionsData');
      spyOn(component, 'showCompetitionsList');
      spyOn(component, 'goToPage');
    });

    it('should redirect to sport name competitions if it is olympics', () => {
      component.sportId = '';
      component.ngOnInit();
      expect(changeDetectorRef.detach).toHaveBeenCalled();
      expect(pubsubService.subscribe).toHaveBeenCalled();
    });

    it('should delete event by id', () => {
      pubsubService.subscribe.and.callFake((name, channel, cb) => channel === 'DELETE_EVENT_FROM_CACHE' && cb(1));
      spyOn(component as any, 'deleteEvent');
      component.ngOnInit();
      expect(pubsubService.subscribe).toHaveBeenCalledWith(
        'competitionsPage', pubsubService.API.DELETE_EVENT_FROM_CACHE, jasmine.any(Function)
      );
      expect(component['deleteEvent']).toHaveBeenCalledWith(1 as any);
    });

    it('error case', () => {
      component['showError'] = jasmine.createSpy();
      sportsConfigService.getSport = jasmine.createSpy().and.returnValue(throwError('error'));
      component.ngOnInit();
      expect(console.warn).toHaveBeenCalled();
    });

    it('should toggle competition list on subscription to pubsub event CHANGE_STATE_CHANGE_COMPETITIONS', () => {
      let cb = data => {};
      spyOn(component as any,'removeSchemaForCompetitions');
      pubsubService.subscribe.and.callFake((name, api, fn) => { cb = fn; });

      component.ngOnInit();
      expect(pubsubService.subscribe).toHaveBeenCalledWith('competitionsPage', 'CHANGE_STATE_CHANGE_COMPETITIONS', jasmine.any(Function));
      cb('state');
      expect(component.showCompetitionsList).toHaveBeenCalledWith('state' as any);
      expect(component['removeSchemaForCompetitions']).toHaveBeenCalled();
    });

    it('should loadAllCompetitions when mainCategories are available', () => {
      component.ngOnInit();
      expect(component.loadAllCompetitions).toHaveBeenCalledWith('football');
    });

    it('should update state and load competitions data on route params change', () => {
      component.ngOnInit();
      expect(component.seasonId).toEqual('');
      expect(component.isLoaded).toEqual(false);
      expect(component.state).toEqual({ error: false, loading: true });
      expect(component.loadCompetitionsData).toHaveBeenCalledWith('typeName', 'className', sportConfig);
    });

    it('should get competition filters', () => {
      component.ngOnInit();
      expect(competitionFiltersService.formTimeFilters).toHaveBeenCalledWith('competitions', []);
      expect(component.competitionFilters).toEqual([]);
    });

    it('should get Sport Event Filters availability', () => {
      component.ngOnInit();

      expect(component.isSportEventFiltersEnabled).toBeTruthy();
      expect(competitionFiltersService.getSportEventFiltersAvailability).toHaveBeenCalled();
    });

    it('should call cms service getSportTabs', fakeAsync(() => {
      sportsConfigService.getSport.and.returnValue(observableOf({
        sportConfig: {
          config: {
            tier: 1,
            request: {
              categoryId: '16'
            }
          }
        }
      }));
      component.ngOnInit();
      tick();

      expect(cmsService.getSportTabs).toHaveBeenCalledWith('16');
      expect(component.sportId).toEqual('16');
    }));

    describe('when mainCategories are not available', () => {
      beforeEach(() => {
        spyOn(component, 'getClasses').and.returnValue(observableOf([{ class: { id: 'c2' } }]));
        component.mainCategories = null;
        component.sportName = 'football';
        component.ngOnInit();
      });

      it('should get competitions config from cms, get classes and then load all competitions data', () => {
        expect(cmsService.getCompetitions).toHaveBeenCalledWith('football');
        expect(component.allCategoriesClasses).toEqual(['11', '12']);
        expect(component.getClasses).toHaveBeenCalledWith(['21', '22'], 'football');
        expect(component.mainCategories).toEqual([{ class: { id: 'c2' } } as ICompetitionCategory]);
        expect(component.loadAllCompetitions).toHaveBeenCalledWith('football');
      });
    });
  });

  it('#ngOnInit when error from sportsConfigService', fakeAsync(() => {
    sportsConfigService.getSport.and.returnValue(throwError('error'));
    component.allCategories = [{id: '1'}] as any;
    component.ngOnInit();
    tick(500);
    expect(currentMatchesService.getFootballClasses).not.toHaveBeenCalled();
    expect(currentMatchesService.getOtherClasses).not.toHaveBeenCalled();
    discardPeriodicTasks();
  }));

  it('#ngOnDestroy', () => {
    component['resizeListener'] = jasmine.createSpy('resizeListener');
    component['getDataSubscription'] = {
      unsubscribe: jasmine.createSpy('unsubscribe')
    } as any;
    component['sportsConfigSubscription'] = {
      unsubscribe: jasmine.createSpy('sportsConfigSubscription')
    } as any;
    component['cmsConfigSubscription'] = {
      unsubscribe: jasmine.createSpy('cmsConfigSubscription')
    } as any;
    spyOn(component as any,'removeSchemaForCompetitions');
    component.ngOnDestroy();

    expect(component['resizeListener']).toHaveBeenCalledTimes(1);
    expect(component['getDataSubscription'].unsubscribe).toHaveBeenCalled();
    expect(component['sportsConfigSubscription'].unsubscribe).toHaveBeenCalled();
    expect(component['cmsConfigSubscription'].unsubscribe).toHaveBeenCalled();
    expect(currentMatchesService.unSubscribeForUpdates).toHaveBeenCalled();
    expect(pubsubService.unsubscribe).toHaveBeenCalledWith('competitionsPage');
    expect(component['removeSchemaForCompetitions']).toHaveBeenCalled();
  });

  it('#ngOnDestroy is no data subscription, no error', () => {
    component.ngOnDestroy();

    expect(currentMatchesService.unSubscribeForUpdates).toHaveBeenCalled();
  });

  describe('loadAllCompetitions', () => {
    it('should set the loading property of the first of all-categories list to "false" if latter exists', () => {
      component.allCategories = [{}, {}] as ICompetitionCategory[];
      component.loadAllCompetitions('football');
      expect(component.allCategories).toEqual([{ loading: false }, {}] as ICompetitionCategory[]);
    });

    it('should get the allCategories value by calling getClasses method if it is empty', () => {
      spyOn(component, 'getClasses').and.callThrough();
      currentMatchesService.getFootballClasses.and.returnValue(observableOf([
        { class: { name: 'b' } }, { class: { name: 'C' } }, { class: { name: 'A' } }
      ] as ICompetitionCategory[]));
      component.loadAllCompetitions('football');
      expect(component.getClasses).toHaveBeenCalledWith(['1', '2', '3'], 'football');
      expect(component.allCategories).toEqual([
        { class: { name: 'A' }, loading: false }, { class: { name: 'b' } }, { class: { name: 'C' } }
      ] as ICompetitionCategory[]);
    });

    it('should set allCategories fallback value if getClasses returns empty result', () => {
      component.getClasses =  () => observableOf([]);
      component.loadAllCompetitions('football');
      expect(component.allCategories).toEqual([{ loading: false }] as any);
    });

    it('should set the allCategories fallback value if getClasses method thrown an error', () => {
      spyOn(component, 'getClasses').and.callThrough();
      currentMatchesService.getFootballClasses.and.returnValue(throwError('error'));
      component.loadAllCompetitions('football');
      expect(component.getClasses).toHaveBeenCalledWith(['1', '2', '3'], 'football');
      expect(component.allCategories).toEqual([{ loading: false }] as ICompetitionCategory[]);
    });
  });

  describe('getClasses', () => {
    it('should return observable for football sport', () => {
      component.getClasses(['1', '2'], 'football');
      expect(currentMatchesService.getFootballClasses).toHaveBeenCalledWith(['1', '2']);
    });
    it('should return observable for non-football sport', () => {
      component.getClasses(['1', '2'], 'non-football');
      expect(currentMatchesService.getOtherClasses).toHaveBeenCalledWith(['1', '2'], '16');
    });
  });

  describe('#isTennis', () => {
    it('should return true if current sport is Tennis', () => {
      component.sportName = 'tennis';
      expect(component.isTennis()).toEqual(true);
    });
    it('should return false if current sport is Football', () => {
      component.sportName = 'football';
      expect(component.isTennis()).toEqual(false);
    });
  });

  describe('handleCompetitionFilterOutput', () => {
    it('should not update filter if no output', () => {
      component.timeFilter = null;

      component.handleCompetitionFilterOutput({} as any);

      expect(component.timeFilter).toBeNull();
    });

    it('should update filter', () => {
      const timeFilter = { id: 1, name: '1h', type: 'TIME', value: 1, active: true } as any;
      const expected = { ...timeFilter, active: false };

      component.timeFilter = timeFilter;
      component['eventsByCategoryCopy'] = {} as any;

      component.handleCompetitionFilterOutput({ output: 'filterChange', value: { ...timeFilter, active: false } });

      expect(component.timeFilter).toEqual(expected);
      expect(component.eventsByCategory).toEqual({} as any);
      expect(competitionFiltersService.filterEvents).toHaveBeenCalledWith(null, expected, [{} as any]);
    });
  });

  describe('#loadCompetitionsData', () => {
    beforeEach(()=>{
     spyOn(component as any,'schemaForCompetitions');
    });
    it('should update component porperties from matches service response', fakeAsync(() => {
      component.loadCompetitionsData('typeName', 'className', sportConfig);
      tick();
      expect(currentMatchesService.getTypeEventsByClassName).toHaveBeenCalledWith('typeName', 'className', sportConfig);
      expect(component.typeName).toEqual('typeName');
      expect(component.typeId).toEqual('typeId');
      expect(component.classId).toEqual('classId');
      expect(component.displayFilters).toBeTrue();
      expect(component.sport.arrangeEventsBySection).toHaveBeenCalledWith([{ name: 'eventName' }] as any, true);
      expect(component.eventsByCategory).toEqual({ groupedByDate: [{ events: [{ id: '1' }] }, { events: [{ id: '2' }] }] } as any);
      expect(component['eventsByCategoryCopy']).toEqual({ groupedByDate: [{ events: [{ id: '1' }] }, { events: [{ id: '2' }] }] } as any);
      expect(component.outrights).toEqual([{ name: 'outright event' } as ISportEvent]);
      expect(filterService.orderBy.calls.allArgs()).toEqual([
        [[{ name: 'outright event' }], ['startTime', 'displayOrder', 'name']],
      ]);
      expect(currentMatchesService.unSubscribeForUpdates).toHaveBeenCalled();
      expect(currentMatchesService.subscribeForUpdates).toHaveBeenCalledWith([{ name: 'eventName' }]);
      expect(component.isLoaded).toEqual(true);
      expect(component.state.loading).toEqual(false);
      expect(cmsService.getItemSvg).not.toHaveBeenCalled();
    }));

    it('should return display filters false', fakeAsync(() => {
      (component.sport.arrangeEventsBySection as any).and.returnValue([undefined]);
      component.loadCompetitionsData('typeName', 'className', sportConfig);
      tick();

      expect(component.displayFilters).toBeFalse();
    }));

    it('Should call loadCompetitionsData method with categories', fakeAsync(() => {
      (component.sport.arrangeEventsBySection as any).and.returnValue([{
        id: '1',
        categoryName: 'categoryName'
      }]);
      component.loadCompetitionsData('typeName', 'className', sportConfig);
      tick();
      expect(cmsService.getItemSvg).toHaveBeenCalledWith('categoryName');
      expect(component.titleIconSvg).toEqual('svg');
      expect(component.titleIconSvgId).toEqual('svgId');
    }));

    it('should handle errors', fakeAsync(() => {
      spyOn(component, 'hideSpinner');

      currentMatchesService.getTypeEventsByClassName.and.returnValue(throwError('error'));

      component.loadCompetitionsData('typeName', 'className', sportConfig);

      tick();

      expect(currentMatchesService.subscribeForUpdates).not.toHaveBeenCalled();
      expect(component.isLoaded).toBeTruthy();
      expect(component.hideSpinner).toHaveBeenCalled();
    }));


    it('should handle errors', fakeAsync(() => {
      spyOn(component, 'showError');
      currentMatchesService.getTypeEventsByClassName.and.returnValue(throwError({ noEventsFound: true }));
      component.loadCompetitionsData('typeName', 'className', sportConfig);
      tick();
      expect(component.isLoaded).toBeTruthy();
      expect(component.showError).not.toHaveBeenCalled();
    }));

    describe('generating switcher tabs and selecting first available', () => {
      beforeEach(() => {
        commandService.executeAsync.and.returnValue(Promise.resolve({})); // no seasonId so results/standings tabs are not added
      });

      it('should add matches and outrights tab if data is available and show switchers', fakeAsync(() => {
        component.loadCompetitionsData('typeName', 'className', sportConfig);
        tick();
        expect(component.competitionTabs).toEqual([COMPETITIONS_TABS[0], COMPETITIONS_TABS[1]]);
        expect(component.showSwitchers).toEqual(true);
        expect(component.activeTab).toEqual({ id: 'tab-competition-matches', name: 'matches' });
      }));

      it('should add matches tab only if outrights data is empty', fakeAsync(() => {
        typeEventsByClassNameData.outrights = null;
        component.loadCompetitionsData('typeName', 'className', sportConfig);
        tick();
        expect(component.competitionTabs).toEqual([COMPETITIONS_TABS[0]]);
        expect(component.showSwitchers).toEqual(false);
        expect(component.activeTab).toEqual({ id: 'tab-competition-matches', name: 'matches' });

      }));

      it('should add outrights tab only if matches data is empty', fakeAsync(() => {
        (component.sport as any).arrangeEventsBySection.and.returnValue([]);
        component.loadCompetitionsData('typeName', 'className', sportConfig);
        tick();
        expect(component.competitionTabs).toEqual([COMPETITIONS_TABS[1]]);
        expect(component.showSwitchers).toEqual(false);
        expect(component.activeTab).toEqual({ id: 'tab-competition-outrights', name: 'outrights' });
      }));

      it('should not add any tab if no data is available', fakeAsync(() => {
        typeEventsByClassNameData.outrights = null;
        (component.sport as any).arrangeEventsBySection.and.returnValue([]);
        component.loadCompetitionsData('typeName', 'className', sportConfig);
        tick();
        expect(component.competitionTabs).toEqual([]);
        expect(component.showSwitchers).toEqual(false);
        expect(component.activeTab).toEqual({ id: '', name: '' });
      }));
      it('should call compitetionAutoSeoData', fakeAsync(() => {
        spyOn(component as any, 'compitetionAutoSeoData').and.callThrough();
        component.loadCompetitionsData('World Cup', 'className', sportConfig);
        tick();
        expect(component['compitetionAutoSeoData']).toHaveBeenCalled();
      }));
      it('should call schemaForCompetitions if deviceService.isRobot is true', fakeAsync(() => {
        component.loadCompetitionsData('World Cup', 'className', sportConfig);
        const events = { groupedByDate: [{ events: [{ id: '1' }] }, { events: [{ id: '2' }] }] } as any
        tick();
        expect(component['schemaForCompetitions']).toHaveBeenCalledWith(events);
      }));
    });
  });

  describe('#loadLeaguesData', () => {
    it('Should call loadLeaguesData method', fakeAsync(() => {
      commandService.executeAsync.and.returnValue(Promise.resolve({}));
      component['loadLeaguesData']('typeName', 'className', '16');
      tick();
      expect(commandService.executeAsync).toHaveBeenCalledWith('GET_SEASON', ['typeName', 'className', '16'], {});
      expect(component.seasonId).toEqual('');
    }));

    it('Should call loadLeaguesData method, then add results and standings tabs if seasonId is available', fakeAsync(() => {
      commandService.executeAsync.and.returnValue(Promise.resolve({ id: 'seasonId' }));
      component['loadLeaguesData']('typeName', 'className', '16');
      tick();
      expect(component.seasonId).toEqual('seasonId');
      expect(component.competitionTabs).toEqual([COMPETITIONS_TABS[2], COMPETITIONS_TABS[3]]);
      expect(component.showSwitchers).toEqual(true);
    }));

    it('Should call loadLeaguesData and throw error', fakeAsync(() => {
      commandService.executeAsync.and.returnValue(Promise.reject({}));
      component['loadLeaguesData']('typeName', 'className', '16');
      tick();
      expect(commandService.executeAsync).toHaveBeenCalledWith('GET_SEASON', ['typeName', 'className', '16'], {});
      expect(component.seasonId).toEqual('');
    }));
  });

  describe('ngAfterViewInit -> handleDomElements', () => {
    it('should subscribe on window resize and call overallRecalculation on resize event', () => {
      renderer.listen.and.callFake((el, event, cb) => cb());
      spyOn(component as any, 'overallRecalculation').and.callThrough();
      component.ngAfterViewInit();
      expect(renderer.listen).toHaveBeenCalledWith(windowRefService.nativeWindow, 'resize', jasmine.any(Function));
      expect(component['overallRecalculation']).toHaveBeenCalled();
    });

    describe('on the first run, on window resize and on connect event', () => {
      let connectCb = () => {},
        resizeCb = () => {};

      beforeEach(() => {
        pubsubService.subscribe.and.callFake((name, method, fn) => { connectCb = fn; });
        renderer.listen.and.callFake((el, name, fn) => { resizeCb = fn; });
      });

      describe('should update top title width in 100ms', () => {

        afterEach(fakeAsync(() => {
          component.ngAfterViewInit();
          expect(renderer.setStyle).not.toHaveBeenCalled();

          tick(100);
          expect(renderer.setStyle).toHaveBeenCalledWith({ tagName: 'element' }, 'width', '100px');
          renderer.setStyle.calls.reset();

          connectCb();
          tick(100);
          expect(renderer.setStyle).toHaveBeenCalledWith({ tagName: 'element' }, 'width', '100px');
          renderer.setStyle.calls.reset();

          resizeCb();
          renderer.setStyle.calls.reset(); // cleaning call tracking for calculateDropDownDimensions
          tick(100);
          expect(renderer.setStyle).toHaveBeenCalledWith({ tagName: 'element' }, 'width', '100px');

          renderer.setStyle.calls.reset();
          tick(100);
          expect(renderer.setStyle).not.toHaveBeenCalled();
        }));
      });

      it('should not update top title width in 100ms for mobile', fakeAsync(() => {
        component.ngAfterViewInit();
        connectCb();
        tick(100);
        expect(renderer.setStyle).not.toHaveBeenCalled();
      }));
    });
  });

  describe('#deleteEvent', () => {
    beforeEach(() => {
      component.eventsByCategory = {} as any;
    });

    it('should delete event', () => {
      component.eventsByCategory.events = [{ id: '1' }] as any;
      component['deleteEvent']('1');
      expect(component.eventsByCategory.events).toEqual([]);
    });

    it('should delete events grouped by date', () => {
      component.eventsByCategory.groupedByDate = {
        cat1: { title: 'cat1', events: [{ id: '1' }] },
        cat2: { title: 'cat2', events: [{ id: '1' }, { id: '2' }] },
        cat3: { title: 'cat3', events: [{ id: '3' }] }
      };
      component['deleteEvent']('1');
      expect(component.eventsByCategory.groupedByDate).toEqual({
        cat2: { title: 'cat2', events: [{ id: '2' }] },
        cat3: { title: 'cat3', events: [{ id: '3' }] }
      });
    });
  });

  describe('#tabsSwitcher', () => {
    it('Should call tabsSwitcher method', () => {
      component.tabsSwitcher({ id: 'tab-competition-matches', tab: { name: 'matches' } });

      expect(component.activeTab).toEqual({
        id: 'tab-competition-matches',
        name: 'matches'
      });
    });
  });

  describe('#goToPage', () => {
    it('Should call goToPage with path', () => {
      const result = component.goToPage('path');

      expect(result).toEqual(true);
    });

    it('Should call goToPage without path', () => {
      const result = component.goToPage('');

      expect(result).toEqual(false);
    });
  });

  describe('#trackByIndex', () => {
    it('Should call trackByIndex', () => {
      const result = component.trackByIndex(1);

      expect(result).toEqual(1);
    });
  });

  describe('showCompetitionsList', () => {
    beforeEach(() => {
      component.competitionsHeader = {} as any;
      spyOn(component as any, 'calculateDropDownDimensions').and.callThrough();
      spyOn(component as any, 'scrollToTop').and.callThrough();
    });

    it('should toggle isShowCompetitions', () => {
      component.showCompetitionsList();
      expect(component.isShowCompetitions).toBeTruthy();
      expect(component['calculateDropDownDimensions']).toHaveBeenCalled();
      expect(component['scrollToTop']).toHaveBeenCalled();
    });

    it('should set isShowCompetitions', () => {
      component.showCompetitionsList(false);
      expect(component.isShowCompetitions).toBeFalsy();
      expect(component['calculateDropDownDimensions']).toHaveBeenCalled();
      expect(component['scrollToTop']).toHaveBeenCalled();
    });
  });

  describe('scrollToTop', () => {
    it('should use default position', () => {
      component['scrollToTop']();
      expect(windowRefService.document.body.scrollTop).toBe(0);
      expect(windowRefService.document.documentElement.scrollTop).toBe(0);
    });

    it('should set position from parameter', () => {
      component['scrollToTop'](10);
      expect(windowRefService.document.body.scrollTop).toBe(10);
      expect(windowRefService.document.documentElement.scrollTop).toBe(10);
    });
  });
  describe('compitetionAutoSeoData', () => {
    it('should assign autoSeoData object and publish the data', fakeAsync(() => {
      component.sportName = 'Football';
      component.typeName = 'World cup';
      component['compitetionAutoSeoData']();
      tick();
      expect(component['autoSeoData']).toBeDefined();
      expect(component['autoSeoData']['isOutright']).toBeFalse();
      expect(component['autoSeoData']['categoryName']).toEqual(component.sportName);
      expect(component['autoSeoData']['typeName']).toEqual(component.typeName);
      expect(pubsubService.publish).toHaveBeenCalledWith('AUTOSEO_DATA_UPDATED', jasmine.any(Object));
    }));
  });
  describe('schemaForCompetitions', () => {
    it('should call getSeoSchemaEvents the data and url', () => {
      const competitionevents = { events: [{ id: '1', }], sport: 'football', typeName: 'premier-league', className: 'team', groupedByDate: [{ events: [{ id: '1', }] }] } as any
      component['schemaForCompetitions'](competitionevents);
      expect(competitionFiltersService.getSeoSchemaEvents).toHaveBeenCalledOnceWith(competitionevents.events);
      expect(pubsubService.publish).toHaveBeenCalledWith('SCHEMA_DATA_UPDATED', [[{ id: '1' }], '/football/premier-league']);
      expect(component['competitionUrl']).toEqual('/football/premier-league');
    });
    it('should not call getSeoSchemaEvents the data and url', () => {
      const competitionevents = null;
      component['schemaForCompetitions'](competitionevents);
      expect(competitionFiltersService.getSeoSchemaEvents).not.toHaveBeenCalled();
      expect(pubsubService.publish).not.toHaveBeenCalledWith('SCHEMA_DATA_UPDATED', [[{ id: '1' }], '/football/premier-league']);
    });
  });
  describe('removeSchemaForCompetitions', () => {
    it('should publish schema_removed with url', () => {
      component['competitionUrl'] = '/football/premier-league';
      component['removeSchemaForCompetitions']();
      expect(pubsubService.publish).toHaveBeenCalledWith(pubSubApi.SCHEMA_DATA_REMOVED, '/football/premier-league');
    });
    it('should not publish schema_removed with url', () => {
      component['competitionUrl'] = null;
      component['removeSchemaForCompetitions']();
      expect(pubsubService.publish).not.toHaveBeenCalledWith(pubSubApi.SCHEMA_DATA_REMOVED, '/football/premier-league');
    });
  });
});