import { of as observableOf } from 'rxjs';
import { VerticalMenuComponent } from './vertical-menu.component';

describe('VerticalMenuComponent - ', () => {
  let component: VerticalMenuComponent;
  let navigationService;
  let dynamicComponentLoader;
  let cmsService;

  const verticalMenuMock = {
    action: () => observableOf({targetUri: '/foo'} as any),
    inApp: true
  } as any;


  beforeEach(() => {
    navigationService = {
      openUrl: jasmine.createSpy('openUrl')
    };
    dynamicComponentLoader = {
      destroyDynamicComponent: jasmine.createSpy('destroyDynamicComponent')
    };
    cmsService = {
      getOddsBoost: jasmine.createSpy('getOddsBoost').and.returnValue(observableOf({enabled: true}))
    };
    component = new VerticalMenuComponent(
      navigationService,
      cmsService
    );
  });

  it('should be created', () => {
    expect(component).toBeDefined();
  });

  it('should call menu action and do routing if success', (done: DoneFn) => {
    spyOn(component as any, 'doMenuRouting');
    component.menuItemClick(verticalMenuMock);

    verticalMenuMock.action().subscribe(() => {
      expect(component['doMenuRouting']).toHaveBeenCalled();
      done();
    });
  });

  it('doMenuRouting redirect', () => {
    component.disableDefaultNavigation = false;
    component['doMenuRouting']({
      type: 'link',
      inApp: true,
      targetUri: 'test'
    } as any);
    expect(navigationService.openUrl).toHaveBeenCalledWith( 'test', true, false, Object({ type: 'link', inApp: true, targetUri: 'test' }),undefined );
  });

  it('doMenuRouting no redirect#1', () => {
    component.disableDefaultNavigation = false;
    component['doMenuRouting']({
      type: 'button',
    } as any);
    expect(navigationService.openUrl).not.toHaveBeenCalled();
  });

  it('doMenuRoutingno redirect#2', () => {
    component.disableDefaultNavigation = true;
    component['doMenuRouting']({
      type: 'link',
    } as any);
    expect(navigationService.openUrl).not.toHaveBeenCalled();
  });
});
