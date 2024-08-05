import { OddsBoostInfoIconComponent } from './odds-boost-info-icon.component';

describe('OddsBoostInfoIconComponent', () => {
  let component;
  let localeService;
  let infoDialogService;

  beforeEach(() => {
    localeService = {
      getString: jasmine.createSpy('getString')
    };
    infoDialogService = {
      openInfoDialog: jasmine.createSpy('openInfoDialog')
    };

    component = new OddsBoostInfoIconComponent(
      localeService,
      infoDialogService
    );
  });

  it('showInfoDialog', () => {
    component.showInfoDialog();
    expect(infoDialogService.openInfoDialog).toHaveBeenCalledTimes(1);
    expect(localeService.getString).toHaveBeenCalledTimes(2);
  });
});
