import { BreadcrumbsComponent } from '@app/shared/components/breadcrumbs/breadcrumbs.component';

describe('BreadcrumbsComponent', () => {
  let component;
  let routingState;

  beforeEach(() => {
    routingState = {
      navigateUri: jasmine.createSpy()
    };
    component = new BreadcrumbsComponent(routingState);
    component.menuItems = [
      {
        flag: 'UK',
        data: [
          {
            meeting: 'meeting',
            events: event
          }
        ]
      }
    ] as any[];
    component.navigationMenu.emit = jasmine.createSpy('emit');
  });

  it('should create BreadcrumbsComponent instance', () => {
    expect(component).toBeTruthy();
  });

  it('should call trackByBreadcrumb', () => {
    const breadcrumb = { name: 'horse racing', targetUrl: '/horse-racing' };
    const result = component.trackByBreadcrumb(breadcrumb);

    expect(result).toEqual(breadcrumb.name);
  });

  describe('#lastItemClick', () => {
    it('should emit navigationMenu', () => {
      component.isExpanded = false;
      component.lastItemClick();
      expect(component.navigationMenu.emit).toHaveBeenCalled();
    });

    it('navigationMenu.emit should be called', () => {
      component.lastItemClick();

      expect(component.navigationMenu.emit).toHaveBeenCalled();
    });

    it('navigationMenu.emit should not be called', () => {
      component.menuItems = [] as any[];
      component.lastItemClick();

      expect(component.navigationMenu.emit).not.toHaveBeenCalled();
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
