import { ProgressBarComponent } from './progress-bar.component';

describe('ProgressBarComponent', () => {
  let component: ProgressBarComponent;

  beforeEach(() => {
    component = new ProgressBarComponent();
  });

  it('ngOnInit', () => {
    spyOn(component as any, 'setProgress').and.callThrough();
    component.ngOnInit();
    expect(component['setProgress']).toHaveBeenCalledTimes(1);
  });

  it('ngOnChanges', () => {
    spyOn(component as any, 'setProgress').and.callThrough();
    component.ngOnChanges();
    expect(component['setProgress']).toHaveBeenCalledTimes(1);
  });

  describe('setProgress', () => {
    it('progress should be 0% (min >= max)', () => {
      component.min = component.max = 1;
      component.value = 1;
      component['setProgress']();
      expect(component['progress']).toBe(0);
    });

    it('progress should be 0% (value < min)', () => {
      component.min = 0;
      component.value = -10;
      component['setProgress']();
      expect(component['progress']).toBe(0);
    });

    it('progress should be 100% (value > max)', () => {
      component.max = 10;
      component.value = 20;
      component['setProgress']();
      expect(component['progress']).toBe(100);
    });

    it('progress should be 50%', () => {
      component.min = 0;
      component.max = 50;
      component.value = 25;
      component['setProgress']();
      expect(component['progress']).toBe(50);
    });

    it('progress should be 75%', () => {
      component.min = 20;
      component.max = 60;
      component.value = 50;
      component['setProgress']();
      expect(component['progress']).toBe(75);
    });
  });
});
