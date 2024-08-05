import { of as observableOf, throwError as observableThrowError } from 'rxjs';
import {
  BigCompetitionTabsComponent
} from '@app/bigCompetitions/components/bigCompetitionTabs/big-competition-tabs.component';

describe('BigCompetitionTabsComponent', () => {
  let component: BigCompetitionTabsComponent;

  let bigCompetitionsService;
  let route;
  let routingState;
  let router;
  let deviceService;

  beforeEach(() => {
    bigCompetitionsService = {
      gModules: ['AEM', 'SURFACEBET', 'HIGHLIGHT_CAROUSEL']
    };
    route = {
      params: observableOf({ tab: {} })
    };
    routingState = {
      getRouteParam: jasmine.createSpy().and.returnValue('uri2')
    };
    router = {
      navigateByUrl: jasmine.createSpy()
    };

    component = new BigCompetitionTabsComponent(bigCompetitionsService, route, deviceService, routingState, router);
  });

  it('should run destory without errors', () => {
    component.ngOnDestroy();
  });

  it('#ngOnInit', () => {
    component['getSubTabs'] = jasmine.createSpy();
    component.ngOnInit();
    expect(component['getSubTabs']).toHaveBeenCalled();
    expect(component.routeSubscriber).toBeDefined();
  });

  it('#ngOnInit', () => {
    route = {
      params: observableOf({ })
    };
    component['route'] = route;
    component['getSubTabs'] = jasmine.createSpy();
    component.ngOnInit();
    expect(component['getSubTabs']).not.toHaveBeenCalled();
    expect(component.routeSubscriber).toBeDefined();
  });

  it('#ngOnInit with params tab', () => {
    route = {
      params: observableOf({ })
    };
    component.tab = 'home';
    component['route'] = route;
    component['getSubTabs'] = jasmine.createSpy();
    component.ngOnInit();
    expect(component['getSubTabs']).toHaveBeenCalled();
    expect(component.currentTab).toBe('home');
    expect(component.routeSubscriber).toBeDefined();
  });

  it('#ngOnDestroy', () => {
    component.routeSubscriber = {
      unsubscribe: jasmine.createSpy('unsubscribe')
    } as any;
    component.loadDataSubscriber = {
      unsubscribe: jasmine.createSpy('unsubscribe')
    } as any;
    component.ngOnDestroy();
    expect(component.routeSubscriber.unsubscribe).toHaveBeenCalled();
    expect(component.loadDataSubscriber.unsubscribe).toHaveBeenCalled();
  });


  it('should return correct result', () => {
    const subTabs = [
      {
        id: 'id1',
        path: 'path1',
        url: 'url1',
        uri: 'uri1',
        name: 'name1'
      },
      {
        id: 'id2',
        path: 'path2',
        url: 'url2',
        uri: 'uri2',
        name: 'name2'
      }
    ];
    const result = component.generateSwitchers(subTabs);
    expect(result.length).toBe(2);
    expect(result[0]).toEqual(jasmine.objectContaining({
      onClick: jasmine.any(Function),
      viewByFilters: 'uri1',
      label: 'name1',
      name: 'name1',
      uri: 'uri1',
      url: 'path1'
    }));
    expect(result[1]).toEqual(jasmine.objectContaining({
      onClick: jasmine.any(Function),
      viewByFilters: 'uri2',
      label: 'name2',
      name: 'name2',
      uri: 'uri2',
      url: 'path2'
    }));
    result[0].onClick();
    result[1].onClick();
    expect(router.navigateByUrl).toHaveBeenCalledWith(subTabs[0].path);
    expect(router.navigateByUrl).toHaveBeenCalledWith(subTabs[1].path);
  });

  it('should return item id', () => {
    const item = {
      id: '25',
      name: 'name',
      type: 'type',
      markets: [],
      events: [],
      knockoutEvents: [],
      knockoutRounds: [],
      maxDisplay: 10,
      viewType: '',
      typeId: ''
    };
    expect(component.trackByIndex(0, item)).toBe('25');
  });

  it('should call correct methods and set properties', () => {
    component.switchers = [
      {
        onClick: () => {},
        viewByFilters: '',
        name: 'name1',
        uri: '/uri1'
      },
      {
        onClick: () => {},
        viewByFilters: '',
        name: 'name2',
        uri: '/uri2'
      }
    ];
    component.loadModules = jasmine.createSpy();
    component.setActiveTab();
    expect(component.filter).toBe(1);
    expect(component.loadModules).toHaveBeenCalled();
  });

  it('should call correct methods and set properties', () => {
    component.switchers = [
      {
        onClick: () => {},
        viewByFilters: '',
        name: 'name1',
        uri: '/uri5'
      },
      {
        onClick: () => {},
        viewByFilters: '',
        name: 'name2',
        uri: '/uri7'
      }
    ];
    component.setActiveTab();
    expect(component.filter).toBe(0);
    expect(router.navigateByUrl).toHaveBeenCalledWith('/');
  });

  it('should call correct methods and set properties when routeParam has subTab', () => {
    component['routingState'].getRouteParam = jasmine.createSpy().and.returnValue(null);
    component.switchers = [
      {
        onClick: () => {},
        viewByFilters: '',
        name: 'name1',
        uri: '/uri1'
      },
      {
        onClick: () => {},
        viewByFilters: '',
        name: 'name2',
        uri: '/uri2'
      }
    ];
    component.loadModules = jasmine.createSpy();
    component.setActiveTab();
    expect(component.filter).toBe(0);
    expect(component.loadModules).toHaveBeenCalled();
  });
it('should call correct methods and set properties when routeParam does not have subTab', () => {
    component['routingState'].getRouteParam = jasmine.createSpy().and.returnValue(null);
    component.switchers = [
      {
        onClick: () => {},
        viewByFilters: '',
        name: 'name1',
        uri: '/uri1'
      },
      {
        onClick: () => {},
        viewByFilters: '',
        name: 'name2',
        uri: '/uri2'
      }
    ];
    component.subtabData = [
      {
        id: '',
        path: '',
        url: '/uri1',
        name: 'name1'
      }
    ];
    component.loadModules = jasmine.createSpy();
    component.setActiveTab();
    expect(component.filter).toBe(0);
    expect(component.loadModules).toHaveBeenCalledWith('name1');
  });
  describe('bigCompetitionsService returns success results', () => {
    let modules;
    let subTabs;

    beforeEach(() => {
      modules = [
        {
          id: 'id',
          name: '',
          type: '',
          markets: [],
          events: [],
          knockoutEvents: [],
          knockoutRounds: [],
          maxDisplay: 100,
          viewType: '',
          typeId: ''
        }
      ];
      subTabs = [
        {
          id: '',
          path: '',
          url: ''
        }
      ];

      bigCompetitionsService = {
        gModules: ['AEM', 'SURFACEBET', 'HIGHLIGHT_CAROUSEL'],
        getModules: jasmine.createSpy().and.returnValue(observableOf(modules)),
        getSubTabs: jasmine.createSpy().and.returnValue(observableOf(subTabs))
      };

      component = new BigCompetitionTabsComponent(bigCompetitionsService, route, deviceService, routingState, router);
    });

    it('should call correct methods and set properties', () => {
      component.state.loading = true;
      component.hideSpinner = jasmine.createSpy();
      component.loadModules();
      expect(component.loadDataSubscriber).toBeDefined();
      expect(bigCompetitionsService.getModules).toHaveBeenCalled();
      expect(component.showLoader).toBeFalsy();
      component.modulesData = modules;
      expect(component.modulesData).toBe(modules);
      expect(component.hideSpinner).toHaveBeenCalled();
    });

    it('should call unsubscribe before next content load if subscription present', () => {
      const fakeUnsubscribe = jasmine.createSpy('fakeUnsubscribe');

      component.loadDataSubscriber = {
        unsubscribe: fakeUnsubscribe
      } as any;

      component.loadModules();

      expect(fakeUnsubscribe).toHaveBeenCalled();
    });

    it('should call correct methods and set properties, subtabData is exists', () => {
      const switchers = [];
      component.generateSwitchers = jasmine.createSpy().and.returnValue(switchers);
      component.setActiveTab = jasmine.createSpy();
      component.loadModules = jasmine.createSpy();
      component['getSubTabs']();
      expect(component.showLoader).toBeTruthy();
      expect(bigCompetitionsService.getSubTabs).toHaveBeenCalled();
      expect(component.subtabData).toBe(subTabs);
      expect(component.generateSwitchers).toHaveBeenCalledWith(component.subtabData);
      expect(component.switchers).toBe(switchers);
      expect(component.setActiveTab).toHaveBeenCalled();
      expect(component.loadModules).not.toHaveBeenCalled();
    });

    it('should call correct methods and set properties, subtabData is not exists', () => {
      bigCompetitionsService.getSubTabs = jasmine.createSpy().and.returnValue(observableOf([]));
      component.setActiveTab = jasmine.createSpy();
      component.loadModules = jasmine.createSpy();

      component['getSubTabs']();

      expect(bigCompetitionsService.getSubTabs).toHaveBeenCalled();
      expect(component.subtabData).toEqual([]);
      expect(component.setActiveTab).not.toHaveBeenCalled();
      expect(component.loadModules).toHaveBeenCalled();
    });
  });

  describe('bigCompetitionsService returns fail results', () => {
    beforeEach(() => {
      bigCompetitionsService = {
        gModules: ['AEM', 'SURFACEBET', 'HIGHLIGHT_CAROUSEL'],
        getModules: jasmine.createSpy().and.returnValue(observableThrowError(null)),
        getSubTabs: jasmine.createSpy().and.returnValue(observableThrowError(null))
      };

      component = new BigCompetitionTabsComponent(bigCompetitionsService, route, deviceService, routingState, router);
    });

    it('modulesData should be empty array and errors should be displayed', () => {
      component.showError = jasmine.createSpy();
      component.loadModules();
      expect(component.modulesData.length).toBe(0);
      expect(component.showError).toHaveBeenCalled();
    });

    it('should hide loader and show errors', () => {
      component.showError = jasmine.createSpy();
      component['getSubTabs']();
      expect(component.showLoader).toBeFalsy();
      expect(component.showError).toHaveBeenCalled();
    });
  });

  describe('loadModules - should check Promotions Module', () => {
    it('should check if Promotion Unavailable = false, loading = true', () => {
      component.state.loading = true;
      component.hideSpinner = jasmine.createSpy();
      bigCompetitionsService.getModules = jasmine.createSpy().and.returnValue(observableOf([{
        type: 'PROMOTIONS',
        promotionsData: {
          promotions: ['1']
        }
      }, {
        type: 'PROMOTIONS'
      }]));
      component.loadModules();
      expect(component.isPromoUnavailable).toBeFalsy();
      expect(component.hideSpinner).toHaveBeenCalled();
    });

    it('should check if Promotion Unavailable = false (one empty promo), loading = false', () => {
      component.state.loading = false;
      component.hideSpinner = jasmine.createSpy();
      bigCompetitionsService.getModules = jasmine.createSpy().and.returnValue(observableOf([{
        type: 'PROMOTIONS',
        promotionsData: {
          promotions: ['1']
        }
      }, {
        type: 'PROMOTIONS',
        promotionsData: {
          promotions: []
        }
      }]));
      component.loadModules();
      expect(component.isPromoUnavailable).toBeFalsy();
      expect(component.hideSpinner).not.toHaveBeenCalled();
    });

    it('should check if Promotion Unavailable = data is undefined ', () => {
      bigCompetitionsService.getModules = jasmine.createSpy().and.returnValue(observableOf(undefined));
      component.loadModules();
      expect(component.isPromoUnavailable).toBeFalsy();
    });

    it('should check if Promotion Unavailable = true (empty array)', () => {
      bigCompetitionsService.getModules = jasmine.createSpy().and.returnValue(observableOf([{
        type: 'PROMOTIONS',
        promotionsData: {
          promotions: []
        }
      }]));
      component.loadModules();
      expect(component.isPromoUnavailable).toBeTruthy();
    });

    it('should check if Promotion Unavailable = false', () => {
      bigCompetitionsService.getModules = jasmine.createSpy().and.returnValue(observableOf([{
        type: 'OUTRIGHT'
      }]));
      component.loadModules();
      expect(component.isPromoUnavailable).toBeFalsy();
    });
  });
});
