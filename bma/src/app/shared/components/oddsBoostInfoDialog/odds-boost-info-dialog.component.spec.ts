import { OddsBoostInfoDialogComponent } from './odds-boost-info-dialog.component';

describe('OddsBoostInfoDialogComponent', () => {
  let component: OddsBoostInfoDialogComponent;
  let device;
  let windowRef;
  let localeService;
  let userService;
  let storageService;
  let casinoMyBetsIntegratedService;

  beforeEach(() => {
    device = {};
    windowRef = {
      document: {
        body: {
          classList: {
            add: jasmine.createSpy('add')
          }
        }
      }
    };
    localeService = {
      getString: jasmine.createSpy('getString').and.callFake((text, params) => {
        return params ? params[0] : text;
      })
    };

    storageService = {
      get: () => { },
      set: jasmine.createSpy('set'),
      remove: jasmine.createSpy('remove')
    };

    userService = {
      username: 'super'
    };

    casinoMyBetsIntegratedService = {};

    component = new OddsBoostInfoDialogComponent(
      device,
      localeService,
      windowRef,
      storageService,
      userService,
      casinoMyBetsIntegratedService
    );
    component.dialog = {
      close: jasmine.createSpy('close'),
      changeDetectorRef: { detectChanges: jasmine.createSpy('detectChanges') }
    };
  });

  it('constructor', () => {
    expect(component).toBeTruthy();
  });

  describe('OddsBoostInfoDialogComponent', () => {
    it('open (single token)', () => {
      component.params = {
        oddsBoostTokens: [{}],
        oddsBoostConfig: {}
      };
      component.open();
      expect(component.tokens).toBe(component.params.oddsBoostTokens);
      expect(component.avaiLableBoostsText).toBe('oddsboost.tokensInfoDialog.boost');
    });

    it('open (multiple tokens)', () => {
      component.params = {
        oddsBoostTokens: [{}, {}],
        oddsBoostConfig: {}
      };
      component.open();
      expect(component.tokens).toBe(component.params.oddsBoostTokens);
      expect(component.avaiLableBoostsText).toBe('oddsboost.tokensInfoDialog.boosts');
    });

    it('saves date to local storage when checkbox is selected', () => {
      component.params = {
        oddsBoostTokens: [{}, {}],
        oddsBoostConfig: {
          allowUserToToggleVisibility: true
        }
      };
      component.open();
      expect(component.showToggle).toEqual(true);
      component.dontShowPopupAgain.setValue(true);
      component.closeDialog();
      expect(storageService.set).toHaveBeenCalledWith('keepOddsBoostPopupHidden', jasmine.any(Object));
    });

    it('deletes date from local storage when checkbox is unselected', () => {
      component.params = {
        oddsBoostTokens: [{}, {}],
        oddsBoostConfig: {
          allowUserToToggleVisibility: true
        }
      };
      component.open();
      expect(component.showToggle).toEqual(true);
      component.dontShowPopupAgain.setValue(false);
      component.closeDialog();
      expect(storageService.set).toHaveBeenCalledWith('keepOddsBoostPopupHidden', Object({}));
    });
  });
});
