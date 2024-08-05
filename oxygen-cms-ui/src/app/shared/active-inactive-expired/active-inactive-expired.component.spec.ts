import { ActiveInactiveExpiredComponent } from './active-inactive-expired.component';

describe('ActiveInactiveExpiredComponent', () => {
  let component;

  beforeEach(() => {
    component = new ActiveInactiveExpiredComponent();
    component.ngOnInit();
  });

  it('should get correct Total value', () => {
    component.collection = {
      active: 1,
      inactive: 1,
      expired: 1
    };

    expect(component.total).toEqual(3);
  });

  it('should get correct Total value', () => {
    component.collection = {
      active: 1,
      expired: 1
    };

    expect(component.total).toEqual(2);
  });

  it('should get correct Total value', () => {
    component.collection = {
      active: 1
    };

    expect(component.total).toEqual(1);
  });
});
