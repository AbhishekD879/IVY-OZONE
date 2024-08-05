import { BreadcrumbsComponent } from '@coralDesktop/shared/components/breadcrumbs/breadcrumbs.component';

import { Subscription } from 'rxjs';

describe('BreadcrumbsComponent', () => {
  let component: BreadcrumbsComponent, breadcrumbsService, router, route, routingState, location;

  beforeEach(() => {
    breadcrumbsService = jasmine.createSpyObj('BreadcrumbsService', ['getBreadcrumbsList']);
    router = {
      events: {
        subscribe: jasmine.createSpy('subscribe').and.returnValue(new Subscription())
      }
    };
    route = {
      snapshot: ''
    };
    routingState = jasmine.createSpyObj('RoutingState', ['getRouteParam', 'navigateUri']);
    location = {
      path: jasmine.createSpy('path').and.returnValue('')
    };

    component = new BreadcrumbsComponent(breadcrumbsService, router, route, routingState, location);
    component.sportName = '';
    component.sportEvent = '';
  });

  it('should create BreadcrumbsComponent instance', () => {
    expect(component).toBeTruthy();
  });

  describe('ngOnInit', () => {
    it('should reset Breadcrumbs List and register Event Handlers', () => {
      component.ngOnInit();
      expect(breadcrumbsService.getBreadcrumbsList).toHaveBeenCalled();
    });
  });

  describe('ngOnDestroy', () => {
    it('should unsubscribe on destroy', () => {
      component['subscription'] = new Subscription();
      component['subscription'].unsubscribe = jasmine.createSpy('unsubscribe');
      component.ngOnDestroy();
      expect(component['subscription'].unsubscribe).toHaveBeenCalled();
    });
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

