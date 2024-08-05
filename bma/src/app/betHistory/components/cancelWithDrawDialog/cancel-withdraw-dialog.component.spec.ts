import { CancelWithDrawDialogComponent } from '@app/betHistory/components/cancelWithDrawDialog/cancel-withdraw-dialog.component';

describe('CancelWithDrawDialogComponent', () => {
  let component: CancelWithDrawDialogComponent;
  let device, windowRef;
  beforeEach(() => {
    device = {};
    windowRef = {};
    component = new CancelWithDrawDialogComponent(device, windowRef);
  });
  it('should create component instance', () => {
    expect(component).toBeTruthy();
  });
});
