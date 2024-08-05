import { AbstractDialogComponent } from '@app/shared/components/oxygenDialogs/abstract-dialog';
import { CashOutPopUpComponent } from './cash-out-popup.component';

describe('CashOutPopUpComponent', () => {
  let component: CashOutPopUpComponent;
  let device, windowRef;
  beforeEach(() => {
    device = {};
    windowRef = {};
    component = new CashOutPopUpComponent(device, windowRef);
  });
  it(`should be instance of 'AbstractDialogComponent'`, () => {
    expect(AbstractDialogComponent).isPrototypeOf(component);
  });
  it('should create component instance', () => {
    expect(component).toBeTruthy();
  });
  describe('open', () => {
    it('should show event names', () => {
      const openSpy = spyOn(CashOutPopUpComponent.prototype['__proto__'], 'open');
      const params = {
        data: {
          eventName: ['a vs b', 'c vs d'],
          suspension: 'cashout-freebet'
        }
      };
      AbstractDialogComponent.prototype.setParams(params);
      component.open();
      expect(openSpy).toHaveBeenCalled();
      expect(params.data.eventName.length).not.toBe(0);
      expect(component.eventFlag).toBe(true);
    });
    it('not contain event names', () => {
      const openSpy = spyOn(CashOutPopUpComponent.prototype['__proto__'], 'open');
      const params = {
        data: {
          eventName: [],
          suspension: 'cashout-freebet'
        }
      };
      AbstractDialogComponent.prototype.setParams(params);
      component.open();
      expect(openSpy).toHaveBeenCalled();
      expect(params.data.eventName.length).toBe(0);
      expect(component.eventFlag).toBe(false);
    });
    it('params are not present', () => {
      const openSpy = spyOn(CashOutPopUpComponent.prototype['__proto__'], 'open');
      const params = undefined;
      AbstractDialogComponent.prototype.setParams(params);
      component.open();
      expect(openSpy).toHaveBeenCalled();
    });
    it('data are not present', () => {
      const openSpy = spyOn(CashOutPopUpComponent.prototype['__proto__'], 'open');
      const params = { data: undefined };
      AbstractDialogComponent.prototype.setParams(params);
      component.open();
      expect(openSpy).toHaveBeenCalled();
    });
  });
});
