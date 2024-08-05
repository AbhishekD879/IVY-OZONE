import { AbstractOutletComponent } from '@shared/components/abstractOutlet/abstract-outlet.component';

describe('AbstractOutletComponent', () => {
  let component: AbstractOutletComponent;

  beforeEach(() => {
    component = new AbstractOutletComponent();
  });

  it('reloadComponent should destroy and reinit component', () => {
    expect(component.state.loading).toBe(true);
    expect(component.state.error).toBe(false);
    component.state = {
      loading: false,
      error: true
    };

    component['reloadComponent']();
    expect(component.state.loading).toBe(true);
    expect(component.state.error).toBe(false);
    expect(component.reloadInitiated).toBe(true);
  });

  it('showError', () => {
    component.showError();
    expect(component.state.loading).toBe(false);
    expect(component.state.error).toBe(true);
    expect(component.reloadInitiated).toBe(false);
  });
});
