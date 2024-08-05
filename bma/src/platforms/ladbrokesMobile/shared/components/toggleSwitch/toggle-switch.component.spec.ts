import { LadbrokesToggleSwitchComponent } from './toggle-switch.component';

describe('ToggleSwitchComponent', () => {
  let component: LadbrokesToggleSwitchComponent;

  beforeEach(() => {
    component = new LadbrokesToggleSwitchComponent();
  });

  it('onChange should emit a value', () => {
    spyOn(component.switcherControl, 'emit');
    component.onChange({}, true);

    expect(component.switcherControl.emit).toHaveBeenCalled();
  });

  it('onChange should not emit a value', () => {
    spyOn(component, 'onChange');
    component.onChange({}, true);

    expect(component.onChange).toHaveBeenCalled();
  });

  it('onClick should emit an event', () => {
    spyOn(component.clickIfDisabled, 'emit');
    component.disabled = true;
    component.onClick({});

    expect(component.clickIfDisabled.emit).toHaveBeenCalled();
  });

  it('onClick should not emit an event', () => {
    spyOn(component.clickIfDisabled, 'emit');
    component.disabled = false;
    component.onClick({});

    expect(component.clickIfDisabled.emit).not.toHaveBeenCalled();
  });
});
