import { RangeSliderComponent } from './range-slider.component';

describe('RangeSliderComponent', () => {
  let component: RangeSliderComponent;

  beforeEach(() => {
    component = new RangeSliderComponent();
  });

  it ('should init component', () => {
    component.ngOnInit();
    const customValue = component.options.customValueToPosition(4, 2, 6),
      translateValue = component.options.translate(50, 1);
    expect(translateValue).toBe('50%');
    expect(customValue).toBe(0.5);
  });

  it ('updateValue', () => {
    component.modelChangeHandler.emit = jasmine.createSpy('modelChangeHandler.emit');
    component.updateValue({ value: 12 } as any);
    expect(component.modelChangeHandler.emit).toHaveBeenCalledWith(12);
  });
});
