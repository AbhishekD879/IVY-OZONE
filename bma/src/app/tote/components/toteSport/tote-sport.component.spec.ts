import { of as observableOf, throwError } from 'rxjs';

import { ToteSportComponent } from './tote-sport.component';

describe('ToteSportComponent', () => {
  let component: ToteSportComponent,
      location,
      router,
      route,
      toteService,
      navigationService;

  beforeEach(() => {
    location = {};
    router = {
      navigateByUrl: jasmine.createSpy('router.navigateByUrl'),
      navigate: jasmine.createSpy('navigate'),
    };
    route = {};
    toteService = {
      getToteEvents: jasmine.createSpy('toteService.getToteEvents')
    };

    navigationService = jasmine.createSpyObj(['openUrl']);

    component = new ToteSportComponent(location, router, route, toteService, navigationService);

    spyOn(component, 'showSpinner');
    spyOn(component, 'hideSpinner');
    spyOn(component, 'showError');
  });

  it('reloadSport success', () => {
    component['init'] = jasmine.createSpy('init');
    toteService.getToteEvents.and.returnValue(observableOf({}));

    component.reloadSport();

    expect(component.showSpinner).toHaveBeenCalled();
    expect(toteService.getToteEvents).toHaveBeenCalled();
    expect(component['init']).toHaveBeenCalled();
  });

  it('reloadSport success', () => {
    toteService.getToteEvents.and.returnValue(throwError('error'));

    component.reloadSport();

    expect(component.showError).toHaveBeenCalled();
  });

  describe('ngOnInit', () => {

    it('No redirect', () => {
      component['init'] = jasmine.createSpy('init');
      route.params = observableOf({filter: 'by-time', sport: 'greyhounds'});
      toteService.getToteEvents.and.returnValue(observableOf({}));

      component.ngOnInit();

      expect(component.filter).toBe('by-time');
      expect(component.sport).toBe('greyhounds');
      expect(toteService.getToteEvents).toHaveBeenCalled();
      expect(component['init']).toHaveBeenCalled();
    });

    it('Redirect to sport with filter', () => {
      component['redirectToUrl'] = jasmine.createSpy('redirectToUrl');
      route.params = observableOf({filter: 'tst_filter', sport: 'horse racing'});

      component.ngOnInit();

      expect(component.filter).toBe('tst_filter');
      expect(component['redirectToUrl']).toHaveBeenCalledWith('/tote/horseracing/by-meeting');
    });

    it('Redirect to homepage', () => {
      component['redirectToUrl'] = jasmine.createSpy('redirectToUrl');
      route.params = observableOf({filter: 'by-time', sport: 'tst_sport'});

      component.ngOnInit();

      expect(component['redirectToUrl']).toHaveBeenCalled();
    });

    it('Error', () => {
      route.params = observableOf({filter: 'by-time', sport: 'greyhounds'});
      toteService.getToteEvents.and.returnValue(throwError('Error'));

      component.ngOnInit();

      expect(component.showError).toHaveBeenCalled();
    });

    it('empty params', () => {
      route.params = observableOf({});
      toteService.getToteEvents.and.returnValue(observableOf(null));
      component.ngOnInit();
      expect(component.sport).toBe('horseracing');
    });
  });

  describe('goToFilter', () => {

    it('should update filter but dont trigger routing', () => {
      component.sport = 'football';
      location.path = () => '/tote/football/test_filter';

      component.goToFilter('test_filter');

      expect(component.filter).toBe('test_filter');
      expect(navigationService.openUrl).not.toHaveBeenCalled();
    });

    it('should trigger routing', () => {
      component.sport = 'football';
      location.path = () => '/tote/football/test_filter';

      component.goToFilter('test_filter2');

      expect(component.filter).toBe('test_filter2');
      expect(navigationService.openUrl).toHaveBeenCalledWith('/tote/football/test_filter2', true, true);
    });
  });

  it('init', () => {
    component.sport = 'football';
    component.activeTab = {} as any;
    component.goToFilter = jasmine.createSpy('goTofilter');

    component['init']({id: '1'} as any);
    component.switchers[0].onClick();
    component.switchers[1].onClick();

    expect(component.eventsData).toEqual({id: '1'} as any);
    expect(component.activeTab.id).toBe('tab-football');
    expect(component.switchers).toBeDefined();
    expect(component.hideSpinner).toHaveBeenCalled();
    expect(component.goToFilter).toHaveBeenCalledTimes(2);
  });

  it('redirectToUrl', () => {
    component['redirectToUrl']('test');

    expect(router.navigateByUrl).toHaveBeenCalled();
  });
});
