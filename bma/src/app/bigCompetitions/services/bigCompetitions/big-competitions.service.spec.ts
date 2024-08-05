import { tick, fakeAsync } from '@angular/core/testing';
import { of, throwError } from 'rxjs';

import { BigCompetitionsService } from './big-competitions.service';

describe('BigCompetitionsService', () => {
  let service,
    cacheEventsService,
    bigCompetitionLiveUpdatesService,
    bigCompetitionsProvider,
    routingState,
    route,
    router,
    outcomeTemplateHelperService,
    cmsToolsService;

  beforeEach(() => {
    cacheEventsService = jasmine.createSpyObj('cacheEventsService', ['store']);
    bigCompetitionLiveUpdatesService = jasmine.createSpyObj('bigCompetitionLiveUpdatesService', ['subscribe', 'unsubscribe']);
    bigCompetitionsProvider = {
      tab: jasmine.createSpy('tab'),
      tabs: jasmine.createSpy('tabs'),
      subtab: jasmine.createSpy('subtab'),
      module: jasmine.createSpy('module'),
      participants: jasmine.createSpy('participants')
    };
    routingState = {
      getRouteParam: jasmine.createSpy('getRouteParam')
    };
    route = {
      snapshot: {}
    };
    router = {
      navigate: jasmine.createSpy('navigate')
    };
    outcomeTemplateHelperService = {
      setOutcomeMeaningMinorCode: jasmine.createSpy('setOutcomeMeaningMinorCode')
    };
    cmsToolsService = {
      processResult: jasmine.createSpy('processResult')
    };

    service = new BigCompetitionsService(
      cacheEventsService,
      bigCompetitionsProvider,
      bigCompetitionLiveUpdatesService,
      routingState,
      route,
      router,
      outcomeTemplateHelperService,
      cmsToolsService
    );
  });

  describe('@storeCategoryId', () => {
    it('should set activeCategoryId to empty string', () => {
      service.storeCategoryId('');

      expect(service.activeCategoryId).toBe('');
    });

    it('should activeCategoryId = undefined', () => {
      service.storeCategoryId();

      expect(service.activeCategoryId).toBe(undefined);
    });

    it('should activeCategoryId = test', () => {
      service.storeCategoryId('testId');

      expect(service.activeCategoryId).toBe('testId');
    });
  });

  describe('@getTabs', () => {
    let bigCompetitionsProviderData;

    beforeEach(() => {
      routingState.getRouteParam = jasmine.createSpy('getRouteParam').and.returnValue('name');
      service.parseTabs = jasmine.createSpy('parseTabs').and.returnValue([]);
    });

    it('should parseTabs', fakeAsync(() => {
      bigCompetitionsProviderData = {
        competitionTabs: [ {}, {} ]
      };
      bigCompetitionsProvider.tabs = jasmine.createSpy('tabs').and.returnValue(of(bigCompetitionsProviderData));

      service.getTabs().subscribe();
      tick();

      expect(service.parseTabs).toHaveBeenCalledWith(bigCompetitionsProviderData);
      expect(router.navigate).not.toHaveBeenCalled();
    }));

    it('should not parseTabs', fakeAsync(() => {
      bigCompetitionsProvider.tabs = jasmine.createSpy('tabs').and.returnValue(of({ competitionTabs: [] }));

      service.getTabs().subscribe();
      tick();

      expect(service.parseTabs).not.toHaveBeenCalled();
      expect(router.navigate).toHaveBeenCalledWith(['/']);
    }));

    it('should not parseTabs', fakeAsync(() => {
      bigCompetitionsProviderData = {};
      bigCompetitionsProvider.tabs = jasmine.createSpy('tabs').and.returnValue(of({}));

      service.getTabs().subscribe();
      tick();

      expect(service.parseTabs).not.toHaveBeenCalled();
      expect(router.navigate).toHaveBeenCalledWith(['/']);
    }));

    it('should handle error', fakeAsync(() => {
      bigCompetitionsProvider.tabs = jasmine.createSpy('tabs').and.returnValue(throwError(null));

      service.getTabs().subscribe();
      tick();

      expect(service.parseTabs).not.toHaveBeenCalled();
      expect(router.navigate).toHaveBeenCalledWith(['/']);
    }));
  });

  describe('groupEvents', () => {
    it('should handle unique events', () => {
      const events = [{
        id: '1',
        markets: [{ id: '11' }, { id: '22' }]
      }, {
        id: '2',
        markets: [{ id: '11' }, { id: '22' }]
      }] as any;
      const result = service['groupEvents'](events);

      expect(result.length).toEqual(2);
      expect(result[0].markets.length).toEqual(2);
      expect(result[1].markets.length).toEqual(2);
    });

    it('should group same event and store unique markets under this event', () => {
      const events = [{
        id: '1',
        markets: [{ id: '11' }, { id: '22' }]
      }, {
        id: '1',
        markets: [{ id: '33' }, { id: '22' }]
      }, {
        id: '2',
        markets: [{ id: '11' }, { id: '22' }]
      }, {
        id: '1',
        markets: [{ id: '33' }, { id: '44' }]
      }, {
        id: '2',
        markets: [{ id: '22' }, { id: '11' }]
      }] as any;
      const result = service['groupEvents'](events);

      expect(result.length).toEqual(2);
      expect(events[0].markets.length).toEqual(2);
      expect(result[0].markets.length).toEqual(4);
      expect(result[1].markets.length).toEqual(2);
    });
  });

  describe('getModules', () => {
    let promotions,
      bigCompetitionsProviderData,
      bigCompetitionPromotions;

    beforeEach(() => {
      promotions = [];
      bigCompetitionsProviderData = {
        competitionModules: [
          {
            promotionsData: {
              promotions: []
            }
          }
        ]
      };
      bigCompetitionPromotions = bigCompetitionsProviderData.competitionModules[0].promotionsData.promotions;
      routingState.getRouteParam = jasmine.createSpy('getRouteParam').and.returnValue(null);
      service.bigCompetitionsLiveUpdatesService = {
        subscribe: jasmine.createSpy('subscribe'),
        unsubscribe: jasmine.createSpy('unsubscribe')
      };
      service.findSubTab = jasmine.createSpy('findSubTab').and.returnValue({ id: 'id'});
      service.findTab = jasmine.createSpy('findTab').and.returnValue({ id: 'id'});
      service.storedModules = [];
      cmsToolsService.processResult = jasmine.createSpy('processResult');
      service.getEvents = jasmine.createSpy('getEvents').and.returnValue([]);
    });

    describe('subtab', () => {
      beforeEach(() => {
        service.groupEvents = jasmine.createSpy('groupEvents').and.returnValue([{}, {}]);
        cmsToolsService.processResult = jasmine.createSpy('processResult').and.returnValue(promotions);
      });

      it('should set promotions for subtab', () => {
        routingState.getRouteParam = jasmine.createSpy('getRouteParam').and.returnValue('some');
        service.storedModules = [{}, {}];
        bigCompetitionsProvider.subtab = jasmine.createSpy().and.returnValue(of(bigCompetitionsProviderData));
        service.getEvents = jasmine.createSpy('getEvents').and.returnValue([{}, {}]);

        service.getModules().subscribe(() => {
          expect(service.findSubTab).toHaveBeenCalled();
          expect(service.findTab).not.toHaveBeenCalled();
          expect(service.bigCompetitionsLiveUpdatesService.unsubscribe).toHaveBeenCalled();
          expect(bigCompetitionsProvider.subtab).toHaveBeenCalledWith('id');
          expect(service.getEvents).toHaveBeenCalledWith(bigCompetitionsProviderData.competitionModules);
          expect(service.storedModules).toEqual(bigCompetitionsProviderData.competitionModules);
          expect(service.cacheEventsService.store).toHaveBeenCalledWith('bigCompetitions', [{}, {}]);
          expect(service.groupEvents).toHaveBeenCalled();
          expect(service.bigCompetitionsLiveUpdatesService.subscribe).toHaveBeenCalledWith([{}, {}]);
          expect(cmsToolsService.processResult).toHaveBeenCalledWith(bigCompetitionPromotions);
          expect(bigCompetitionsProviderData.competitionModules[0].promotionsData.promotions).toBe(promotions);
        });
      });

      it('should not set promotions for subtab', () => {
        bigCompetitionsProvider.tab = jasmine.createSpy('tab').and.returnValue(of(bigCompetitionsProviderData));
        bigCompetitionsProviderData.competitionModules[0].promotionsData.promotions = null;

        service.getModules().subscribe(() => {
          expect(service.findSubTab).not.toHaveBeenCalled();
          expect(service.findTab).toHaveBeenCalled();
          expect(service.bigCompetitionsLiveUpdatesService.unsubscribe).not.toHaveBeenCalled();
          expect(bigCompetitionsProvider.tab).toHaveBeenCalledWith('id');
          expect(service.storedModules).toEqual([]);
          expect(service.cacheEventsService.store).not.toHaveBeenCalled();
          expect(service.groupEvents).not.toHaveBeenCalled();
          expect(service.bigCompetitionsLiveUpdatesService.subscribe).not.toHaveBeenCalledWith();
          expect(cmsToolsService.processResult).not.toHaveBeenCalled();
        });
      });

      afterEach(() => {
        expect(service.getEvents).toHaveBeenCalledWith(bigCompetitionsProviderData.competitionModules);
      });
    });

    describe('tab', () => {
      beforeEach(() => {
        bigCompetitionsProvider.tab = jasmine.createSpy('tab').and.returnValue(of(bigCompetitionsProviderData));
      });

      it('should set promotions', () => {
        cmsToolsService.processResult = jasmine.createSpy('processResult').and.returnValue(promotions);

        service.getModules().subscribe(() => {
          expect(cmsToolsService.processResult).toHaveBeenCalledWith(bigCompetitionPromotions);
          expect(bigCompetitionsProviderData.competitionModules[0].promotionsData.promotions).toBe(promotions);
        });
      });

      it('should not set promotions', () => {
        bigCompetitionsProviderData.competitionModules[0].promotionsData.promotions = null;

        service.getModules().subscribe(() => {
          expect(cmsToolsService.processResult).not.toHaveBeenCalled();
        });
      });

      afterEach(() => {
        expect(service.findTab).toHaveBeenCalled();
        expect(bigCompetitionsProvider.tab).toHaveBeenCalledWith('id');
        expect(service.getEvents).toHaveBeenCalledWith(bigCompetitionsProviderData.competitionModules);
      });
    });

    xit('should handle error', () => {
      bigCompetitionsProvider.tab = jasmine.createSpy('tab').and.returnValue(of(null));
      service.groupEvents = jasmine.createSpy('groupEvents').and.returnValue([{}, {}]);

      service.getModules().subscribe(() => {
        expect(service.findTab).toHaveBeenCalled();
        expect(service.findSubTab).not.toHaveBeenCalled();
        expect(service.bigCompetitionsLiveUpdatesService.unsubscribe).not.toHaveBeenCalled();
        expect(bigCompetitionsProvider.tab).toHaveBeenCalledWith('id');
        expect(service.getEvents).not.toHaveBeenCalled();
        expect(service.storedModules).toEqual([]);
        expect(cmsToolsService.processResult).not.toHaveBeenCalled();
        expect(service.cacheEventsService.store).not.toHaveBeenCalled();
        expect(service.groupEvents).not.toHaveBeenCalled();
        expect(service.bigCompetitionsLiveUpdatesService.subscribe).not.toHaveBeenCalledWith();
      });
    });

    afterEach(() => {
      expect(routingState.getRouteParam).toHaveBeenCalledWith('subTab', service.route.snapshot);
    });
  });

  describe('@getEvents', () => {
    let result,
      modules;

    it('should return []', () => {
      modules = [];
      result = service.getEvents([]);

      expect(result).toEqual(modules);
    });

    it('should return groupModuleData.data', () => {
      modules = [{
        groupModuleData: {
          data: [
            {
              ssEvents: [{}, {}]
            }
          ]
        }
      }];
      result = service.getEvents(modules);

      expect(result).toEqual(modules[0].groupModuleData.data[0].ssEvents);
    });

    it('should return markets.data', () => {
      modules = [{
        markets: [
          {
            data: [{}]
          }
        ]
      }];
      result = service.getEvents(modules);

      expect(result).toEqual([[{}]]);
    });

    it('should return events', () => {
      modules = [{
        events: [
          {}, {}, {}
        ]
      }];
      result = service.getEvents(modules);

      expect(result).toEqual(modules[0].events);
    });

    it('should return []', () => {
      modules = [{
        events: []
      }];
      result = service.getEvents(modules);

      expect(result).toEqual(modules[0].events);
    });

    it('should return knockoutEvents', () => {
      modules = [{
        knockoutEvents: [
          {
            obEvent: {}
          },
          {}
        ]
      }];
      result = service.getEvents(modules);

      expect(result).toEqual([{}]);
    });

    it('should return knockoutEvents', () => {
      modules = [{
        knockoutEvents: [{}, {}]
      }];
      result = service.getEvents(modules);

      expect(result).toEqual([]);
    });

    it('should return []', () => {
      modules = [{
        knockoutEvents: []
      }];
      result = service.getEvents(modules);

      expect(result).toEqual(modules[0].knockoutEvents);
    });
  });

  describe('getModule', () => {
    it('should bigCompetitionsProvider.module call width id', () => {
      service.getModule('id');

      expect(service.bigCompetitionsProvider.module).toHaveBeenCalledWith('id');
    });
    it('should bigCompetitionsProvider.module call width undefined', () => {
      service.getModule();

      expect(service.bigCompetitionsProvider.module).toHaveBeenCalledWith(undefined);
    });
    it('should bigCompetitionsProvider.module call width null', () => {
      service.getModule(null);

      expect(service.bigCompetitionsProvider.module).toHaveBeenCalledWith(null);
    });
  });

  describe('getSubTabs', () => {
    it('should get sub tabs', () => {
      service.competitionObservable = jasmine.createSpy('competitionObservable').and.returnValue(of({}));
      service.structure = { id: '' };
      service.findTab = jasmine.createSpy('findTab').and.returnValue({ id: 'id'});

      service.getSubTabs().subscribe();

      expect(service.findTab).toHaveBeenCalled();
      expect(service.competitionObservable).not.toHaveBeenCalled();
    });

    it('should get sub tabs if structure is empty', () => {
      service.competitionObservable = of({});
      service.structure = {};
      service.findTab = jasmine.createSpy('findTab').and.returnValue({ competitionSubTabs: 'competitionSubTabs'});

      service.getSubTabs().subscribe((result: Object) => {
        expect(service.findTab).toHaveBeenCalled();
        expect(result).toEqual('competitionSubTabs');
      });
    });

    it('should get sub tabs if structure is empty and tab is null', () => {
      service.competitionObservable = of({});
      service.structure = {};
      service.findTab = jasmine.createSpy('findTab').and.returnValue(null);

      service.getSubTabs().subscribe((result: Object) => {
        expect(service.findTab).toHaveBeenCalled();
        expect(result).toEqual([]);
      });
    });
  });


  describe('addOutcomeMeaningMinorCode', () => {
    let events;

    it('should not add outcome minor code', () => {

      service.addOutcomeMeaningMinorCode();

      expect(outcomeTemplateHelperService.setOutcomeMeaningMinorCode).not.toHaveBeenCalled();
    });

    it('should not add outcome minor code', () => {
      events = [];

      service.addOutcomeMeaningMinorCode(events);

      expect(outcomeTemplateHelperService.setOutcomeMeaningMinorCode).not.toHaveBeenCalled();
    });

    it('should add outcome minor code', () => {
      events = [{
        markets: []
      }];

      service.addOutcomeMeaningMinorCode(events);

      expect(outcomeTemplateHelperService.setOutcomeMeaningMinorCode).toHaveBeenCalledWith(events[0].markets, events[0]);
    });
  });

  describe('findTab', () => {
    let result;

    beforeEach(() => {
      routingState.getRouteParam = jasmine.createSpy('getRouteParam').and.returnValue('competitionModules');
      service.structure = {
        competitionModules: {
          competitionTabs: [{
            id: 'id',
            path: '',
            name: ''
          }]
        }
      };
    });

    it('should return tabs[0]', () => {
      result = service.findTab();

      expect(routingState.getRouteParam).toHaveBeenCalledWith('name', {});
      expect(routingState.getRouteParam).toHaveBeenCalledWith('tab', {});
      expect(router.navigate).toHaveBeenCalled();
      expect(result).toEqual(service.structure.competitionModules.competitionTabs[0]);
    });

    it('should find tabs path', () => {
      service.structure.competitionModules.competitionTabs[0].path = 'path/id';

      result = service.findTab();

      expect(routingState.getRouteParam).toHaveBeenCalledWith('name', {});
      expect(routingState.getRouteParam).toHaveBeenCalledWith('tab', {});
      expect(router.navigate).toHaveBeenCalled();
      expect(result).toEqual(service.structure.competitionModules.competitionTabs[0]);
    });

    it('should return null', () => {
      service.structure.competitionModules.competitionTabs =[];

      result = service.findTab();

      expect(routingState.getRouteParam).toHaveBeenCalledWith('name', {});
      expect(routingState.getRouteParam).toHaveBeenCalledWith('tab', {});
      expect(router.navigate).toHaveBeenCalled();
      expect(result).toEqual(null);
    });
  });

  describe('parseTabs', () => {
    let data,
      result;

    beforeEach(() => {
      service.basePath = 'basePath';
      data = {
        path: '',
        competitionTabs: [{
          path: ''
        }]
      };
    });

    it('should return { path: basePath }', () => {
      data = { path: '' };
      result = service['parseTabs'](data);

      expect(result).toEqual({ path: 'basePath' } as any);
    });

    it('should return object with competitionTabs', () => {
      data = {
        path: '',
        competitionTabs: [{
          path: ''
        }]
      };
      result = service['parseTabs'](data);

      expect(result).toEqual({
        path: 'basePath',
        competitionTabs: [{
          url: 'basePath',
          path: 'basePath'
        }]} as any);
    });

    it('should return object with competitionSubTabs', () => {
      data.competitionTabs[0].competitionSubTabs = [{
        path: ''
      }];
      result = service['parseTabs'](data);

      expect(result).toEqual({
        path: 'basePath',
        competitionTabs: [{
          url: 'basePath',
          path: 'basePath',
          competitionSubTabs: [{
            path: 'basePath'
          }]
        }]} as any);
    });
  });

  describe('findSubTab', () => {
    let result,
      value;

    it('should return tab.competitionSubTabs[0]', () => {
      value = { competitionSubTabs: [{}] };
      service.findTab = jasmine.createSpy('findTab').and.returnValue(value);
      result = service['findSubTab']();

      expect(service.findTab).toHaveBeenCalled();
      expect(routingState.getRouteParam).toHaveBeenCalledWith('subTab', {});
      expect(result).toEqual({});
    });

    it('should find path in tab.competitionSubTabs', () => {
      value = {
        path: 'path',
        competitionSubTabs: [{
          path: 'path/subtab'
        }]
      };
      service.findTab = jasmine.createSpy('findTab').and.returnValue(value);
      routingState.getRouteParam = jasmine.createSpy('getRouteParam').and.returnValue('subtab');
      result = service['findSubTab']();

      expect(service.findTab).toHaveBeenCalled();
      expect(routingState.getRouteParam).toHaveBeenCalledWith('subTab', {});
      expect(result).toEqual({ path: 'path/subtab' });
    });
  });

  describe('getParticipants', () => {
    it('should bigCompetitionsProvider.participants call width competition', () => {
      service.getParticipants('competition');
      expect(service.bigCompetitionsProvider.participants).toHaveBeenCalledWith('competition');
    });
  });

});
