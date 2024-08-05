import { PoolStakeComponent } from './pool-stake.component';

describe('PoolStakeComponent', () => {
  let component: PoolStakeComponent;

  const validationObjMock = {
    outcomeId: '1',
    value: 1,
    poolData: {id: '1'}
  } as any;

  beforeEach(() => {
    component = new PoolStakeComponent();
  });

  it('ngOnInit', () => {
    component.fieldControls = {
      clearField: {
        push : jasmine.createSpy('fieldControls.clearField.push')
      }
    } as any;

    component.ngOnInit();

    expect(component.fieldControls.clearField.push).toHaveBeenCalled();
  });

  it('createValidationObject', () => {
    component.outcomeId = '1';
    const result = component.createValidationObject(1, {id: '1'} as any);

    expect(result).toEqual(validationObjMock);
  });

  it("should replace comma setStake", () => {
    component.value = "1.2";
    component.setStake();
    expect(component.value).toEqual("1.2");
})

  it('onChange', () => {
    component.createValidationObject = jasmine.createSpy('createValidationObject').and.returnValue(validationObjMock);
    spyOn(component.displayError, 'emit');
    spyOn(component.checkFn, 'emit');

    component.onChange();

    expect(component.createValidationObject).toHaveBeenCalled();
    expect(component.displayError.emit).toHaveBeenCalled();
    expect(component.checkFn.emit).toHaveBeenCalled();
    expect(component.stakeError).toBeUndefined();
  });

  it('clearStakeError', () => {
    component.clearStakeError();
    expect(component.stakeError).toBeUndefined();
  });

  it('onFormSubmit', () => {
    const eventMock = {
      preventDefault: jasmine.createSpy('event.preventDefault')
    } as any;

    component.onFormSubmit(eventMock);
    expect(eventMock.preventDefault).toHaveBeenCalled();
  });

  it('clearField', () => {
    component['_clearField']();
    expect(component.value).toBeNull();
  });
});
