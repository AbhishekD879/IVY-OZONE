import { OddsBoostButtonComponent } from './odds-boost-button.component';

describe('OddsBoostButtonComponent', () => {
  let component;

  beforeEach(() => {
    component = new OddsBoostButtonComponent();
  });

  describe('set enabled', () => {
    it('enabled=true', () => {
      component.enabled = false;
      expect(component.enabled).toBeFalsy();
      expect(component.canAnimate).toBeFalsy();
      expect(component.oddsBoostLabel).toEqual('oddsboost.boostButton.disabled');
    });

    it('enabled=false', () => {
      component.enabled = true;
      expect(component.enabled).toBeTruthy();
      expect(component.canAnimate).toBeTruthy();
      expect(component.oddsBoostLabel).toEqual('oddsboost.boostButton.enabled');
    });
  });

  describe('set reboost', () => {
    it('enabled=false, reboost=false', () => {
      component.enabled = false;
      component.reboost = false;
      expect(component.oddsBoostLabel).toEqual('oddsboost.boostButton.disabled');
    });

    it('enabled=false, reboost=true', () => {
      component.enabled = false;
      component.reboost = true;
      expect(component.oddsBoostLabel).toEqual('oddsboost.boostButton.disabled');
    });

    it('enabled=true, reboost=true', () => {
      component.enabled = true;
      component.reboost = true;
      expect(component.oddsBoostLabel).toEqual('oddsboost.boostButton.reboost');
    });
  });
});
