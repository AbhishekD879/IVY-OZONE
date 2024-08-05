import {
  VideoStreamErrorDialogComponent
} from '@lazy-modules/eventVideoStream/components/videoStreamErrorDialog/video-stream-error-dialog.component';
import { AbstractDialogComponent } from '@shared/components/oxygenDialogs/abstract-dialog';

import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';

describe('VideoStreamErrorDialogComponent', () => {
  let component;
  let windowRefService;
  let device;
  let timeSyncService;
  let router;
  let gtmService;
  let changeDetectorRef;
  let infoDialog;
  let pubSubService;

  let eventMock = {
    startTime: (+(new Date) + 111111),
    isResulted: 'false',
    isStarted: 'false',
  };

  beforeEach(() => {
    device = {
      isOnline: jasmine.createSpy('isOnline')
    };
    infoDialog = {
      openConnectionLostPopup: jasmine.createSpy('openConnectionLostPopup')
    };

    windowRefService = {
      nativeWindow: {
        setInterval: jasmine.createSpy().and.returnValue(1),
        clearInterval: jasmine.createSpy()
      },
      document: {
        body: {
          classList: {
            add: jasmine.createSpy('add'),
            remove: jasmine.createSpy('remove')
          }
        }
      }
    };
    timeSyncService  = {
      getTimeDelta: jasmine.createSpy().and.returnValue(0)
    };
    gtmService = {
      push: jasmine.createSpy('gtmService.push')
    };

    pubSubService = {
      publish: jasmine.createSpy('publish'),
      API: pubSubApi
    };

    changeDetectorRef = {
      markForCheck: jasmine.createSpy('markForCheck')
    };

    router = {
      navigate: jasmine.createSpy('navigate')
    };

    changeDetectorRef = {
      markForCheck: jasmine.createSpy('markForCheck')
    };

    component = new VideoStreamErrorDialogComponent(
      windowRefService,
      device,
      timeSyncService,
      router,
      changeDetectorRef,
      gtmService,
      infoDialog,
      pubSubService
    );
    component.dialog = {
      close: jasmine.createSpy(),
      onKeyDownHandler: jasmine.createSpy(),
      changeDetectorRef: { detectChanges: jasmine.createSpy('detectChanges') }
    };
    component.initialState = false;
    component.showBoxError = false;
    component.params = {
      errorMsg: 'sb.error'
    };
  });

  it ('should InitComponent', () => {
    expect(AbstractDialogComponent).isPrototypeOf(component);
  });

  it ('should  init counter with EventEntity on Open', () => {
    eventMock = {
      startTime: (+(new Date) + 111111),
      isResulted: 'false',
      isStarted: 'false',
    };

    component.params.eventEntity = eventMock;
    component.open();
    expect(component.countDownInterval).toBeDefined();
    expect(component.countDown).toBeDefined();
    expect(changeDetectorRef.markForCheck).toHaveBeenCalled();
  });

  it ('should not init counter without EventEntity on Open', () => {
    component.open();
    expect(component.countDownInterval).not.toBeDefined();
    expect(changeDetectorRef.markForCheck).toHaveBeenCalled();
  });

  it ('should not init counter when event is resulted', () => {
    eventMock.isResulted = 'true';
    component.params.eventEntity = eventMock;
    component.open();
    expect(component.countDownInterval).not.toBeDefined();
    expect(changeDetectorRef.markForCheck).toHaveBeenCalled();
  });

  it ('should not init counter when event is isStarted', () => {
    eventMock.isStarted = 'true';
    component.params.eventEntity = eventMock;
    component.open();
    expect(component.countDownInterval).not.toBeDefined();
    expect(changeDetectorRef.markForCheck).toHaveBeenCalled();
  });

  it ('should not init counter when event startTime in past', () => {
    eventMock.startTime = (+(new Date()) - 111);
    component.params.eventEntity = eventMock;
    component.open();
    expect(component.countDownInterval).not.toBeDefined();
    expect(changeDetectorRef.markForCheck).toHaveBeenCalled();
  });

  it ('should not init counter when event startTime in future but not Today', () => {
    spyOn(component, 'isStartTimeToday').and.callThrough();

    eventMock.startTime = (+(new Date()) + 1111111111);
    component.params.eventEntity = eventMock;

    expect(component.isCountTimerAvailable()).toBeFalsy();

    component.open();

    expect(component.isStartTimeToday).toHaveBeenCalledWith(eventMock.startTime);
    expect(component.countDownInterval).not.toBeDefined();
    expect(changeDetectorRef.markForCheck).toHaveBeenCalled();
  });

  it ('should clearCounter interval on Close', () => {
    spyOn(component, 'closeDialog');

    component.params.eventEntity = eventMock;
    component.open();
    component.close();

    expect(windowRefService.nativeWindow.clearInterval).toHaveBeenCalled();
    expect(component.closeDialog).toHaveBeenCalled();
    expect(component.countDown).toBeNull();
    expect(changeDetectorRef.markForCheck).toHaveBeenCalledTimes(2);
    expect(pubSubService.publish).toHaveBeenCalledWith(pubSubService.API.VIDEO_STREAM_ERROR_DIALOG_CLOSED);
  });

  it('@openDeposit is online', () => {
    device.isOnline.and.returnValue(true);
    spyOn(component, 'closeDialog');
    component.openDeposit();
    expect(changeDetectorRef.markForCheck).toHaveBeenCalled();
    expect(router.navigate).toHaveBeenCalledWith(['deposit']);
    expect(component.closeDialog).toHaveBeenCalled();
  });

  it('@openDeposit is offline', () => {
    device.isOnline.and.returnValue(false);
    component.openDeposit();
    expect(changeDetectorRef.markForCheck).toHaveBeenCalled();
    expect(router.navigate).not.toHaveBeenCalledWith(['deposit']);
    expect(infoDialog.openConnectionLostPopup).toHaveBeenCalled();
  });

  describe('onBeforeCloseHandler', () => {
    it('should call pubsub publish', () => {
      const originalOnBeforeClose = jasmine.createSpy('originalOnBeforeClose');

      component.params.onBeforeClose = originalOnBeforeClose;
      component.open();
      component.close();
      component.params.onBeforeClose();

      expect(originalOnBeforeClose).toHaveBeenCalled();
      expect(component.params.onBeforeClose).toEqual(jasmine.any(Function));
      expect(pubSubService.publish).toHaveBeenCalledWith(pubSubService.API.VIDEO_STREAM_ERROR_DIALOG_CLOSED);
    });

    it('should not add handler for trackPopUpButtonClick', () => {
      component.open();

      expect(gtmService.push).not.toHaveBeenCalled();
    });

    describe('should keep original onBeforeClose handler and', () => {
      beforeEach(() => {
        component.params.isInactivePopup = true;
        device.isOnline.and.returnValue(true);
      });

      it('should add handler for trackPopUpButtonClick on Greyhounds edp', () => {
        (eventMock as any) = {
          categoryCode: 'GREYHOUNDS',
          categoryId: '1',
          typeId: '2',
          id: 3
        };
        component.params.eventEntity = eventMock;

        component.open();
        component.close();
        component.params.onBeforeClose();

        expect(gtmService.push).toHaveBeenCalledWith('trackEvent', {
          eventCategory: 'streaming',
          eventAction: 'pop up',
          eventLabel: 'Ok,Thanks',
          sportID: '1',
          typeID: '2',
          eventID: 3
        });
      });

      it('should add handler for trackPopUpButtonClick on Horse Racing edp', () => {
        (eventMock as any) = {
          categoryCode: 'HORSE_RACING',
          categoryId: '4',
          typeId: '5',
          id: 6
        };
        component.params.eventEntity = eventMock;

        component.open();
        component.openDeposit();
        component.params.onBeforeClose();

        expect(gtmService.push).toHaveBeenCalledWith('trackEvent', {
          eventCategory: 'streaming',
          eventAction: 'pop up',
          eventLabel: 'Deposit',
          sportID: '4',
          typeID: '5',
          eventID: 6
        });
      });
    });
  });
});
