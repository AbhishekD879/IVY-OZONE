import { DeviceService } from '@core/services/device/device.service';
import { ConnectionInterruptionDialogComponent } from './connection-interruption-dialog.component';

describe('ConnectionInterruptionDialogComponent', () => {
  let component: ConnectionInterruptionDialogComponent;
  let device;
  let windowRef;
  let gtmService;

  beforeEach(() => {
    device = DeviceService;
    windowRef = {};
    gtmService = { push: jasmine.createSpy() };
    component = new ConnectionInterruptionDialogComponent(device, windowRef, gtmService);
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should call closeInterruptionPopup', () => {
    const closeDialogSpy = spyOn(ConnectionInterruptionDialogComponent.prototype['__proto__'], 'closeDialog');
    component['closeInterruptionPopup']();
    expect(closeDialogSpy).toHaveBeenCalled();
    expect(gtmService.push).toHaveBeenCalled();
  });
});
