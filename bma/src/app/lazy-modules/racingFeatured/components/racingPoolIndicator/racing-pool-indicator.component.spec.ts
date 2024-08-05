import { of } from 'rxjs';

import { RacingPoolIndicatorComponent } from './racing-pool-indicator.component';

describe('RacingPoolIndicatorComponent', () => {
  let component: RacingPoolIndicatorComponent;
  let gtmService, ukToteService, cmsService, router;

  beforeEach(() => {
    gtmService = {
      push: jasmine.createSpy('push')
    };
    ukToteService = {
      getPoolIndicators: jasmine.createSpy('getPoolIndicators')
    };
    cmsService = {
      getSystemConfig: jasmine.createSpy('getSystemConfig').and.returnValue(of({
        TotePools: { Enable_UK_Totepools: true }
      }))
    };
    router = {
      navigateByUrl: jasmine.createSpy('navigateByUrl')
    };
    component = new RacingPoolIndicatorComponent(gtmService, ukToteService, cmsService, router);
  });

  describe('ngOnInit', () => {
    it('should load pool indicators', () => {
      component.ngOnInit();
      expect(ukToteService.getPoolIndicators).toHaveBeenCalled();
    });

    it('should not load pool indicators', () => {
      cmsService.getSystemConfig.and.returnValue(of({}));
      component.ngOnInit();
      expect(ukToteService.getPoolIndicators).not.toHaveBeenCalled();
    });
  });

  describe('#trackById', () => {
    it('should trackById if id is exist', () => {
      expect(component.trackById(1, { id: '234234'} as any)).toBe('1234234');
    });

    it('should trackById if id is not exist', () => {
      expect(component.trackById(1, {} as any)).toBe('1');
    });
  });

  it('goToEvent', () => {
    component.overlayMenuClose.emit = jasmine.createSpy().and.returnValue(0);
    component.emitEvent=true
    component.goToEvent('/', 'type');
    expect(gtmService.push).toHaveBeenCalledWith('trackEvent', {
      eventCategory: 'uk tote',
      eventAction: 'entry',
      eventLabel: 'type'
    });
    expect(router.navigateByUrl).toHaveBeenCalledWith('/');
  });
});
