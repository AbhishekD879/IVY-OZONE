
import { BreadcrumbsComponent } from './breadcrumbs.component';
import { Subscription } from 'rxjs';

describe('BreadcrumbsComponent', () => {
  let component;
  let breadcrumbsService;
  let router;
  let route;
  let routingState;
  let location;

  beforeEach(() => {
    breadcrumbsService = {
      getBreadcrumbsList: jasmine.createSpy('getBreadcrumbsList').and.returnValue([
        {
          name: 'next',
          targetUri: '/horse-racing/races/next',
        }
      ])
    };
    router = {
      events: {
        subscribe: jasmine.createSpy('subscribe').and.returnValue(new Subscription())
      }
    };
    route = {
      snapshot: {
        firstChild: {
          routeConfig: {
            path: 'next-races'
          }
        }
      },
    };
    routingState = jasmine.createSpyObj('RoutingState', ['getRouteParam', 'navigateUri']);
    location = {
      path: jasmine.createSpy('path').and.returnValue('')
    };

    component = new BreadcrumbsComponent(
      breadcrumbsService,
      router,
      route,
      routingState,
      location
    );
    component.sportName = '';
    component.sportEvent = '';
    component['subscripton'] = {
      unsubscribe: jasmine.createSpy('unsubscribe')
    };
  });

  describe('check isEDP', () => {
    it('should check isEDP config when isEDPPage is true', () => {
      component.isEDPpage = true;
      const result = component['buildConfig']();
      expect(result.isEDPPage).toBeTruthy();
    });

    it('should check isEDP config when isEDPPage is false', () => {
      component.sportName = 'test_sport';
      component.sportEvent = 'test_event';
      const result = component['buildConfig']();
      expect(result.isEDPPage).toBeTruthy();
    });
  });

  describe('check isOlympics', () => {
    it('should check isOlympics config when isOlympics is true', () => {
      component.isOlympics = true;
      const result = component['buildConfig']();
      expect(result.isOlympicsPage).toBeTruthy();
    });

    it('should check isOlympics config when path contains olypics', () => {
      location.path.and.returnValue('olympics');
      const result = component['buildConfig']();
      expect(result.isOlympicsPage).toBeTruthy();
    });
  });

  describe('resetBreadcrumbsList', () => {
    it('should call adaptBreadcrumbsForNextRaces', () => {
      component['adaptBreadcrumbsForNextRaces'] = jasmine.createSpy('adaptBreadcrumbsForNextRaces');
      component['resetBreadcrumbsList']();
      expect(component['adaptBreadcrumbsForNextRaces']).toHaveBeenCalled();
    });
  });

  describe('adaptBreadcrumbsForNextRaces', () => {
    it('adaptBreadcrumbsForNextRaces', () => {
      component.breadcrumbsItems = [
        {
          name: 'races',
          targetUri: '/horse-racing/races'
        },
        {
          name: 'next',
          targetUri: '/horse-racing/races/next'
        },
        {
          name: 'test',
          targetUri: '/test'
        },
        {
          name: 'greyhound racing',
          targetUri: '/test'
        }
      ];
      component['adaptBreadcrumbsForNextRaces']();
      expect(component.breadcrumbsItems).toEqual([
        {
          name: 'next races',
          targetUri: '/horse-racing/races/next',
        },
        {
          name: 'test',
          targetUri: '/test'
        },
        {
          name: 'greyhound racing',
          targetUri: '/greyhound-racing/races/next'
        }
      ]);
    });
    it('adaptBreadcrumbsForNextRaces with defaultTab as today', () => {
      component.defaultTab = 'today';
      component.breadcrumbsItems = [
        {
          name: 'greyhound racing',
          targetUri: '/test'
        }, {
          name: 'today',
          targetUri: '/greyhound-racing/today'
        }
      ];
      component['adaptBreadcrumbsForNextRaces']();
      expect(component.breadcrumbsItems).toEqual([
        {
          name: 'greyhound racing',
          targetUri: '/greyhound-racing/today'
        }, {
          name: 'today',
          targetUri: '/greyhound-racing/today'
        }
      ]);
    });
  });
  
  describe('#navigateUri', () => {
    it('should call routingState navigateUri method', () => {
      const event = {
        preventDefault: jasmine.createSpy()
      } as any;
      component.sportName = 'horseracing';
      component.navigateUri(event, '/horse-racing/featured');
      expect(component['routingState'].navigateUri).toHaveBeenCalledWith(event, '/horse-racing/featured', 'horseracing', '');
    });
  });
});

