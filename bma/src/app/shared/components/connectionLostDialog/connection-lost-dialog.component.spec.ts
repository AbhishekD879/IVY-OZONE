import { ConnectionLostDialogComponent } from './connection-lost-dialog.component';
import { DeviceService } from '@core/services/device/device.service';

describe('ConnectionLostDialogComponent', () => {
  let component: ConnectionLostDialogComponent;
  let device;
  let windowRef;

  beforeEach(() => {
    device = DeviceService;
    windowRef = {};
    component = new ConnectionLostDialogComponent(device, windowRef);
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
