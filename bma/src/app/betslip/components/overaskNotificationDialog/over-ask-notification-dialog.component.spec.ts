import { OverAskNotificationDialogComponent } from './over-ask-notification-dialog.component';

describe('OverAskNotificationDialogComponent', () => {
  let device;
  let windowRef;

  let component: OverAskNotificationDialogComponent;

  beforeEach(() => {
    device = {};
    windowRef = {};
    component = new OverAskNotificationDialogComponent(device, windowRef);
  });

  it('ngOnInit', () => {
    component.params = {
      p1: 'p1'
    };

    component.dialog = {
      close: jasmine.createSpy('close'),
      onKeyDownHandler: jasmine.createSpy('onKeyDownHandler'),
      changeDetectorRef: { detectChanges: jasmine.createSpy('detectChanges') }
    };
    component.ngOnInit();
    expect(component.params.closeByEsc).toBeUndefined();
  });

});
