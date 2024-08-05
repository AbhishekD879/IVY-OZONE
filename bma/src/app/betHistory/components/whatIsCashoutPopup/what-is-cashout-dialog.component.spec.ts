import { WhatIsCashOutDialogComponent } from '@app/betHistory/components/whatIsCashoutPopup/what-is-cashout-dialog.component';

describe('WhatIsCashOutDialogComponent', () => {
  let component: WhatIsCashOutDialogComponent;
  let device, windowRef;
  beforeEach(() => {
    device = {};
    windowRef = {};
    component = new WhatIsCashOutDialogComponent(device, windowRef);
  });
  it('should create component instance', () => {
    expect(component).toBeTruthy();
  });
});
