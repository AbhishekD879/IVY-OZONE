import {
  BetslipDepositErrorContainerComponent
} from '@ladbrokesMobile/betslip/components/betslipDepositErrorContainer/betslip-deposit-error-container.component';

describe('BetslipDepositErrorContainerComponent', () => {
  let component: BetslipDepositErrorContainerComponent;

  beforeEach(() => {
    component = new BetslipDepositErrorContainerComponent();
    component.errorMsg = 'Test message';
    component.errorType = 'error';
    component.neededAmountForPlaceBet = '2.00';
  });

  it('isAmountNeeded', () => {
    expect(component.isAmountNeeded()).toBeTruthy();
  });

  it('isAmountNeeded(negative case)', () => {
    component.neededAmountForPlaceBet = '0.00';
    expect(component.isAmountNeeded()).toBeFalsy();
  });
});
