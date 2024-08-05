import { MarketTooltipComponent } from './market-tooltip.component';

describe('MarketTooltipComponent', () => {
  let component;
  let gtmService;
  let localeService;

  beforeEach(() => {
    gtmService = {
      push: jasmine.createSpy('push')
    };
    localeService = {
      getString: jasmine.createSpy('getString').and.returnValue('test_string')
    };
    component = new MarketTooltipComponent(gtmService, localeService);
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  describe('#setTooltipEvent', () => {
    it('should call trackevent', () => {
      component.setTooltipEvent(true);
      expect(gtmService.push).toHaveBeenCalled();
    });
    it('should not call track event', () => {
      component.setTooltipEvent(false);
      expect(gtmService.push).not.toHaveBeenCalled();
    });
  });
});
