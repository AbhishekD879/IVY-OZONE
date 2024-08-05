import { BetslipLimitationDialogComponent } from './betslip-limitation-dialog.component';
import { AbstractDialogComponent } from '@shared/components/oxygenDialogs/abstract-dialog';

describe('BetslipLimitationDialogComponent', () => {
  let component: BetslipLimitationDialogComponent;
  let deviceService;
  let windowRef;

  beforeEach(() => {
    deviceService = {
      isMobile: true
    };
    windowRef = {};
    component = new BetslipLimitationDialogComponent(deviceService, windowRef);
  });

  it('should create component instance', () => {
    expect(component).toBeDefined();
    expect(component instanceof AbstractDialogComponent).toBeTruthy();
  });
});
