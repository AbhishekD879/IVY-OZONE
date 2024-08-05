import { YourCallTabDialogComponent } from '@yourcall/components/yourCallTabDialog/your-call-tab-dialog.component';

describe('YourCallTabDialogComponent', () => {
  let component: YourCallTabDialogComponent;
  let device, windowRef;
  beforeEach(() => {
    device = {};
    windowRef = {};
    component = new YourCallTabDialogComponent(device, windowRef);
  });
  it('should create component instance', () => {
    expect(component).toBeTruthy();
  });
});
