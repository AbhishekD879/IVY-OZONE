import {
  BetslipOverlayNotificationComponent
} from '@ladbrokesMobile/betslip/components/betslipOverlayNotification/betslip-overlay-notification.component';

describe('BetslipOverlayNotification', () => {
  let windowRefService;
  let component: BetslipOverlayNotificationComponent;

  beforeEach(() => {
    windowRefService = {
      nativeWindow: {
        setTimeout: jasmine.createSpy('setTimeout'),
        clearTimeout: jasmine.createSpy('clearTimeout')
      },
      document: {
        querySelector: jasmine.createSpy('querySelector').and.returnValue({ style: {} })
      }
    };

    component = new BetslipOverlayNotificationComponent(
      windowRefService
    );
    component.messageConfig = {};
    component.messageType = '';
    component.overlayMsg = '';
  });

  it('should create an instance', () => {
    expect(BetslipOverlayNotificationComponent).toBeTruthy();
  });

  describe('#ngOnInit', () => {
    it('should call ngOnInit', () => {
      component.messageConfig = { message: 'test message' };
      component.ngOnInit();
      expect(windowRefService.nativeWindow.setTimeout).toHaveBeenCalled();
    });

    it('should call ngOnInit no message config', () => {
      component.ngOnInit();
      expect(windowRefService.nativeWindow.setTimeout).not.toHaveBeenCalled();
    });
  });

  describe('#ngOnChanges', () => {
    it('should call ngOnChanges', () => {
      component.messageConfig = {};
      const changes = {
        messageConfig: {
          currentValue: { message: 'testMessage', type: ''}
        }
      };
      component.ngOnChanges(changes as any);
      expect(windowRefService.nativeWindow.setTimeout).toHaveBeenCalled();
    });

    it('should call ngOnChanges not called', () => {
      const changes = {
        messageConfig: {
          currentValue: {}
        }
      };
      component.ngOnChanges(changes as any);
      expect(windowRefService.nativeWindow.setTimeout).not.toHaveBeenCalled();
    });
  });

  it('ngOnDestroy', () => {
    component.clear.emit = jasmine.createSpy('clear');
    component.ngOnDestroy();
    expect(component.clear.emit).toHaveBeenCalledTimes(1);
  });

  it('should call showMessage', () => {
    const message = 'message';
    component.messageConfig = { type: 'ACCA'};

    component['showMessage'](message);
    expect(component.messageType).toEqual('animated error acca-transparent');
    expect(component.overlayMsg).toEqual(message);
    expect(windowRefService.nativeWindow.clearTimeout).toHaveBeenCalled();
    expect(windowRefService.nativeWindow.setTimeout).toHaveBeenCalledWith(jasmine.any(Function), 5000);
  });

  it('should call showMessage not acca type message', () => {
    const message = 'message';
    component.messageConfig = { type: ''};

    component['showMessage'](message);
    expect(component.messageType).toEqual('animated error');
    expect(component.overlayMsg).toEqual(message);
    expect(windowRefService.nativeWindow.clearTimeout).toHaveBeenCalled();
    expect(windowRefService.nativeWindow.setTimeout).toHaveBeenCalledWith(jasmine.any(Function), 5000);
  });

  it('should hide message if time out', () => {
    windowRefService.nativeWindow.setTimeout.and.callFake(cb => cb());
    component.clear.emit = jasmine.createSpy('emit');
    component['showMessage']('test');
    expect(component.overlayMsg).toEqual('');
    expect(component.clear.emit).toHaveBeenCalled();
  });
});
