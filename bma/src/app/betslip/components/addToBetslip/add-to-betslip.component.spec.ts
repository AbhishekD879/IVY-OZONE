import { of as observableOf, throwError } from 'rxjs';
import { fakeAsync, tick } from '@angular/core/testing';
import { AddToBetslipComponent } from '@betslip/components/addToBetslip/add-to-betslip.component';

describe('AddToBetslipComponent', () => {
  let component: AddToBetslipComponent;
  let addToBetslipByOutcomeIdService;
  let commandService;
  let route;

  beforeEach(() => {
    commandService = {
      executeAsync: jasmine.createSpy('executeAsync').and.returnValue(Promise.resolve()),
      API: {
        BETSLIP_READY: ''
      }
    };
    addToBetslipByOutcomeIdService = {
      addToBetSlip: jasmine.createSpy().and.returnValue(observableOf(true)),
      isValidOutcome: jasmine.createSpy().and.returnValue(observableOf(true)),
      filteredOutcomeIds: {
        includes: jasmine.createSpy().and.returnValue(true)
      }
    };
    route = {
      snapshot: {
        params: {
          outcomeId: "240480152,240480151,240985648"
        }
      }
    };
  });

  function createComponent() {
    component = new AddToBetslipComponent(
      addToBetslipByOutcomeIdService,
      route,
      commandService
    );

    component.ngOnInit();
  }

  it('should create AddToBetslipComponent instance', () => {
    createComponent();
    expect(component).toBeTruthy();
  });

  it('should add to betslip', fakeAsync(() => {
    addToBetslipByOutcomeIdService.addToBetSlip.and.returnValue(observableOf(null));

    createComponent();

    tick();
    expect(addToBetslipByOutcomeIdService.addToBetSlip).
    toHaveBeenCalledWith('', true, true, true, false, false, true);
    expect(component.state.loading).toBeFalsy();
  }));

  it('should show error if any occurs during adding to betslip', fakeAsync(() => {
    addToBetslipByOutcomeIdService.addToBetSlip.and.returnValue(throwError('error'));

    createComponent();

    tick();
    expect(component.state.error).toBeTruthy();
  }));
});
