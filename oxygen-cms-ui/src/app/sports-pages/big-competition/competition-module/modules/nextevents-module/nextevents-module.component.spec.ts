import {NexteventsModuleComponent} from './nextevents-module.component';

describe('NexteventsModuleComponent', () => {
  let component;

  beforeEach(() => {
    component = new NexteventsModuleComponent();

    component.module = {
      maxDisplay: 2,
      typeId: '222'
    };
  });

  it('should validate Form', () => {
    expect(component.isValidForm()).toBeTruthy();
  });

  it('should  validate Form', () => {
    component.module = {
      maxDisplay: 0,
      typeId: '222'
    };

    expect(component.isValidForm()).toBeFalse();
  });

  it('should  validate Form', () => {
    component.module = {
      maxDisplay: 3,
      typeId: null
    };

    expect(component.isValidForm()).toBeFalse();
  });
});
