import { WnPoolStakesComponent } from './wn-pool-stakes.component';


describe('WnPoolStakesComponent', () => {
  let component: WnPoolStakesComponent;
  let userService;

  beforeEach(() => {
    userService = {
      currencySymbol: '$'
    };

    component = new WnPoolStakesComponent(userService);
  });

  describe('ngOnInit', () => {
    it('no field controls', () => {
      component.fieldControls = null;
      expect(() => component.ngOnInit()).not.toThrowError();
    });

    it('field controls exist', () => {
      component.fieldControls = { clearField: [] };
      component.ngOnInit();
      expect(component.fieldControls.clearField.length).toBe(1);
    });
  });

  it('onChange', () => {
    component.displayError.emit = jasmine.createSpy('emit');
    component.checkFn.emit = jasmine.createSpy('emit');
    component.onChange();
    expect(component.displayError.emit).toHaveBeenCalledWith(jasmine.any(Object));
    expect(component.checkFn.emit).toHaveBeenCalledWith(jasmine.any(Object));
  });

  it('clearStakeError', () => {
    component.displayError.emit = jasmine.createSpy('emit');
    component.clearStakeError();
    expect(component.displayError.emit).toHaveBeenCalledWith(jasmine.any(Object));
    expect(component.stakeError).toBeUndefined();
  });

  it("should replace comma setStake", () => {
    component.value = "1.2";
    component.setStake();
    expect(component.value).toEqual("1.2");
  })

  describe('convertValue', () => {
    it('should use currency calculator', () => {
      component.value = '1';
      component.currencyCalculator = {
        currencyExchange: jasmine.createSpy('currencyExchange')
      };
      component.convertValue();
      expect(component.currencyCalculator.currencyExchange).toHaveBeenCalled();
    });

    it('should concat currency and value', () => {
      expect(component.convertValue()).toBe('$null');
    });
  });

  it('onFormSubmit', () => {
    const event: any = { preventDefault: jasmine.createSpy('preventDefault') };
    component.onFormSubmit(event);
    expect(event.preventDefault).toHaveBeenCalled();
  });

  it('_clearField', () => {
    component['_clearField']();
    expect(component.value).toBe('');
    expect(component.convertedValue).toBe('');
  });
});
