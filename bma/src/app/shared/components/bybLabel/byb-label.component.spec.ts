import { BybLabelComponent } from './byb-label.component';

describe('BybLabelComponent', () => {
  let component;
  let device;

  beforeEach(() => {
    device = {
      isMobileOnly: true
    };
    component = new BybLabelComponent(device);
  });

  it('should create component instance', () => {
    expect(component).toBeTruthy();
  });

  it ('should set values true fot isMobileOnly', () => {
    expect(component.isMobileOnly).toBeTruthy();
  });
});
