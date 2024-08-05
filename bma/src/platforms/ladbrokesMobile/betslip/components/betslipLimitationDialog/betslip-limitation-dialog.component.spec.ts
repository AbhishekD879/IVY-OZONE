import { BetslipLimitationDialogComponent } from './betslip-limitation-dialog.component';
// eslint-disable-next-line max-len
import { BetslipLimitationDialogComponent as AppBetslipLimitationDialogComponent } from '@betslip/components/betslipLimitationDialog/betslip-limitation-dialog.component';


describe('BetslipLimitationDialogComponent', () => {
  let component: BetslipLimitationDialogComponent;
  let device, windowRef;

  beforeEach(() => {
    device = {};
    windowRef = {};
    component = new BetslipLimitationDialogComponent(device, windowRef);
  });

  it('should create component instance', () => {
    expect(component).toBeDefined();
  });

  it(`should extend mobile BetslipLimitationDialogComponent`, () => {
    expect(component instanceof AppBetslipLimitationDialogComponent).toBeTruthy();
  });
});
