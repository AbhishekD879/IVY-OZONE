import { ExpandPanelComponent } from '@app/shared/components/expandPanel/expand-panel.component';

describe('ExpandPanelComponent', () => {
  let component: ExpandPanelComponent;
  let localeService;

  beforeEach(() => {
    localeService = {
      getString: jasmine.createSpy('getString')
    };
    component = new ExpandPanelComponent(localeService);
  });

  describe('#ExpandPanelComponent', () => {
    it('@ngOnInit', () => {
      component.ngOnInit();
      expect(localeService.getString).toHaveBeenCalledTimes(2);
    });
  });
});
