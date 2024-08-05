import { BybProgressBarComponent } from './byb-progress-bar.component';

describe('BybProgressBarComponent', () => {
  let component: BybProgressBarComponent;

  beforeEach(() => {
    component = new BybProgressBarComponent();
  });

  describe('calcProgress', () => {
    it('progress should be 0% (min >= max)', () => {    
      component.min = component.max = component.value = 1;
      expect(component['calcProgress']()).toBe(0);
    });

    it('progress should be 0% (value < min)', () => {
      component.min = 0;
      component.value = -10;
      expect(component['calcProgress']()).toBe(0);
    });

    it('progress should be 100% (value > max)', () => {
      component.max = 10;
      component.value = 20;
      expect(component['calcProgress']()).toBe(100);
    });

    it('progress should be 50%', () => {
      component.min = 0;
      component.max = 50;
      component.value = 25;
      expect(component['calcProgress']()).toBe(50);
    });

    it('progress should be 75%', () => {
      component.min = 20;
      component.max = 60;
      component.value = 50;
      expect(component['calcProgress']()).toBe(75);
    });
  });
});
