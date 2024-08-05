import { fakeAsync, tick } from '@angular/core/testing';
import { commandApi } from '@core/services/communication/command/command-api.constant';
import { of, Subject, throwError } from 'rxjs';

import { IGameMediaComponent } from '@lazy-modules/eventVideoStream/components/iGameMedia/i-game-media.component';

import { DialogService } from '@core/services/dialogService/dialog.service';

describe('IGameMediaComponent', () => {
  let component;
  const eventMock = {
    id: '8208340',
    name: '18:21 Club Hipico',
    typeId: '2009',
    categoryCode: 'code',
    categoryName: 'Horse Racing',
    className: 'Horse Racing - Live',
    drilldownTagNames: 'EVFLAG_EPR',
    eventStatusCode: 'A',
    startTime: '2018-06-30T16:57:00Z',
    categoryId: '21',
    isLiveNowEvent: 'true',
    typeName: '(USA) Club Hipico',
  };
  const iframeDimensionsMock = {
    width: 10,
    height: 10
  };
  let nativeBridgeService,
    device,
    iGameMediaService,
    sanitizer,
    gtm,
    windowRef,
    locale,
    command,
    elementRef,
    eventVideoStreamProvider,
    rendererService,
    domToolsService,
    watchRulesService,
    dialogService,
    componentFactoryResolver;

  beforeEach(() => {
    device = {
      isWrapper: false
    };
    iGameMediaService = {
      getIFrameDimensions: jasmine.createSpy('getIFrameDimensions').and.returnValue(iframeDimensionsMock),
      getStream: jasmine.createSpy().and.returnValue(of({
        streamLink: 'test'
      })),
      replaceAmps: jasmine.createSpy('replaceAmps').and.returnValue('')
    };
    sanitizer = {
      bypassSecurityTrustResourceUrl: jasmine.createSpy('bypassSecurityTrustResourceUrl')
    };
    gtm = {
      push: jasmine.createSpy('push')
    };
    windowRef = {};
    locale = {
      getString: jasmine.createSpy()
    };
    command = {
      API: commandApi,
      register: jasmine.createSpy('register'),
      unregister: jasmine.createSpy('unregister')
    };
    elementRef = {
      nativeElement: {}
    };
    rendererService = {
      renderer: {
        listen: jasmine.createSpy('listen')
      }
    };
    eventVideoStreamProvider = {
      playListener: new Subject<void>(),
      showHideStreamListener: new Subject<boolean>(),
      playSuccessErrorListener: new Subject<boolean>()
    };
    nativeBridgeService = {
      showVideoIfExist: jasmine.createSpy(),
      showErrorForNative: jasmine.createSpy(),
      hideVideoStream: jasmine.createSpy()
    };
    domToolsService = {
      getWidth: jasmine.createSpy('getWidth')
    };
    dialogService = {
      openDialog: jasmine.createSpy('openDialog')
    };
    componentFactoryResolver = {
      resolveComponentFactory: jasmine.createSpy('resolveComponentFactory').and.returnValue({ name: 'VideoStreamErrorDialogComponent'})
    };
    watchRulesService = {
      isInactiveUser: jasmine.createSpy('isInactiveUser').and.returnValue(false)
    };

    component = new IGameMediaComponent(
      iGameMediaService,
      sanitizer,
      gtm,
      windowRef,
      locale,
      command,
      elementRef,
      rendererService,
      device,
      nativeBridgeService,
      eventVideoStreamProvider,
      domToolsService,
      watchRulesService,
      dialogService,
      componentFactoryResolver
    );
    component.eventEntity = eventMock;
    component.desktopProperties = {
      isDesktop: false,
      videoDimensions: {
        width: '100%',
        height: '100%'
      }
    };
    component.dataLayerObj = {
      eventCategory: 'streaming',
      eventAction: 'click',
      eventLabel: 'watch video stream',
      sportID: '123',
      typeID: '12333',
      eventId: '321321'
    };
    component.dataLayerObjError = {
      event: 'trackEvent',
      eventCategory: 'Livestream',
      eventAction: 'error',
      liveStreamError: ''
    };
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  describe('ngOnInit', () => {
    it('should init stream', () => {
      component.streamShown = false;
      component.ngOnInit();
      expect(rendererService.renderer.listen).toHaveBeenCalledWith(windowRef.nativeWindow, 'orientationchange', jasmine.any(Function));
      expect(iGameMediaService.getStream).toHaveBeenCalled();
      expect(component.streamShown).toEqual(true);
    });

    describe('for wrapper', () => {
      beforeEach(() => {
        device.isWrapper = true;
      });

      it('should close the stream if native player is shown on initialization', () => {
        nativeBridgeService.playerStatus = true;
        component.ngOnInit();
        expect(iGameMediaService.getStream).not.toHaveBeenCalled();
        expect(nativeBridgeService.hideVideoStream).toHaveBeenCalled();
        expect(component.streamShown).toEqual(false);
      });
      it('should open the stream if native player is not shown on initialization', () => {
        nativeBridgeService.playerStatus = false;
        component.ngOnInit();
        expect(iGameMediaService.getStream).toHaveBeenCalled();
        expect(nativeBridgeService.hideVideoStream).not.toHaveBeenCalled();
        expect(component.streamShown).toEqual(true);
      });
    });
  });

  describe('showError', () => {
    it('set default error type if not mapped key passed', () => {
      const errorMessageType = 'servicesCrashed';

      component['isDesktop'] = true;
      component['showError'](errorMessageType);

      expect(component.streamError).toEqual(errorMessageType);
      expect(dialogService.openDialog).not.toHaveBeenCalled();
    });

    it('set default error type if not mapped key passed on mobile', () => {
      const errorMessageType = 'servicesCrashed';
      const translation = 'service error';

      locale.getString.and.returnValue(translation);
      component['isDesktop'] = false;
      component['showError'](errorMessageType);

      expect(component.streamError).toEqual(errorMessageType);
      expect(locale.getString).toHaveBeenCalledWith('sb.servicesCrashed');
      expect(dialogService.openDialog).toHaveBeenCalledWith(
        DialogService.API.videoStreamError, { name: 'VideoStreamErrorDialogComponent' }, true, {
          errorMsg: translation,
          eventEntity: eventMock,
          isInactivePopup: false
        }
      );
    });
  });

  it('should Init', fakeAsync(() => {
    component.isStreamActive = false;
    component.init();
    tick();
    expect(command.register).toHaveBeenCalledWith(command.API.GET_LIVE_STREAM_STATUS, jasmine.any(Function));
    expect(component.streamData).toBeDefined();
    expect(component.iFrameDimensions).toEqual(iframeDimensionsMock);
    expect(gtm.push).toHaveBeenCalledWith('trackEvent', component.dataLayerObj);
    expect(component.isStreamActive).toBeTruthy();
  }));


  it('should Init for wrappers', fakeAsync(() => {
    component.isStreamActive = false;
    device.isWrapper = true;
    component.init();
    tick();

    expect(gtm.push).toHaveBeenCalledWith('trackEvent', component.dataLayerObj);
    expect(component.isStreamActive).toBeTruthy();
    expect(nativeBridgeService.showVideoIfExist).toHaveBeenCalledWith('test', eventMock.id, eventMock.categoryCode, 'iGameMedia');
  }));

  it('should Init with error for wrappers', fakeAsync(() => {
    component.isStreamActive = false;
    const error = 'IGM streamservice.js not available';
    iGameMediaService.getStream.and.returnValue(throwError(error));
    device.isWrapper = true;
    component.init();
    tick();
    expect(nativeBridgeService.showErrorForNative).toHaveBeenCalledWith('streamIsNotAvailable');
  }));

  it('should Init: show error popup(web version) if it is wrapper but user is inactive', fakeAsync(() => {
    watchRulesService.isInactiveUser.and.returnValue(true);
    component.isStreamActive = false;
    iGameMediaService.getStream.and.returnValue(throwError('deniedByInactiveWatchRules'));
    device.isWrapper = true;
    component.init();
    tick();

    expect(nativeBridgeService.showErrorForNative).not.toHaveBeenCalledWith('streamIsNotAvailable');
    expect(component.streamError).toEqual('deniedByInactiveWatchRules');
  }));

  it('should Init with error for non wrappers', fakeAsync(() => {
    component.isStreamActive = false;
    const error = 'IGM streamservice.js not available';
    iGameMediaService.getStream.and.returnValue(throwError(error));
    device.isWrapper = false;
    component.init();
    tick();
    expect(component.streamError).toEqual('streamIsNotAvailable');
  }));

  it('should Init with error for non wrappers and the error is not equal "IGM streamservice.js not available"',
    fakeAsync(() => {
      component.isStreamActive = false;
      const error = 'error';
      iGameMediaService.getStream.and.returnValue(throwError(error));
      device.isWrapper = false;

      component.init();
      tick();
      expect(component.streamError).toEqual('error');
  }));

  it('should test resize', fakeAsync(() => {
    component.onResizeAndOrientation();
    tick(500);

    expect(iGameMediaService.getIFrameDimensions).toHaveBeenCalled();
    expect(component.iFrameDimensions).toEqual(iframeDimensionsMock);
  }));

  it('should test showError', fakeAsync(() => {
    component.streamError = '';
    component.showError('error');
    expect(component.streamError).toEqual('error');
  }));

  describe('addStreamDataToGTM', () => {
    it('should test addStreamDataToGTM with onResizeAndOrientation', () => {
      spyOn(component, 'onResizeAndOrientation').and.callThrough();
      component.streamData = {
        randomData: true
      };
      component['addStreamDataToGTM']();
      expect(component.onResizeAndOrientation).toHaveBeenCalled();
    });

    it('should push to gtm data layer error object', () => {
      component['streamError'] = 'servicesCrashed';
      component.ngOnInit();

      component['addStreamDataToGTM']();
      expect(gtm.push).toHaveBeenCalledWith('trackEvent', jasmine.objectContaining({
        event: 'trackEvent',
        eventCategory: 'Livestream',
        eventAction: 'error',
        liveStreamError: ''
      }));
    });

    it('should push to gtm data layer data object', () => {
      component['streamError'] = '';
      component.ngOnInit();

      component['addStreamDataToGTM']();
      expect(gtm.push).toHaveBeenCalledWith('trackEvent', jasmine.objectContaining({
        eventCategory: 'streaming',
        eventAction: 'click',
        eventLabel: 'watch video stream',
        sportID: eventMock.categoryId,
        typeID: eventMock.typeId,
        eventId: eventMock.id
      }));
    });
  });

  it('should test get streamErrorKey', () => {
    component.streamError = 'test';
    expect(component.streamErrorKey).toEqual('sb.test');
  });

  it('should test handleLiveStreamStatus', () => {
    component['handleLiveStreamStatus']().then(
      expect(component)
    );
  });

  it('should test handlePlayingStream', () => {
    component['handlePlayingStream'](false);
    expect(nativeBridgeService.hideVideoStream).toHaveBeenCalled();
  });

  it('should destroy component', () => {
    component.actionSubscriber = new Subject<void>();
    const orientationChangeListener = jasmine.createSpy('orientationChangeListener');
    component['orientationChangeListener'] = orientationChangeListener;
    component.ngOnDestroy();

    expect(orientationChangeListener).toHaveBeenCalled();
    expect(command.unregister).toHaveBeenCalledWith(command.API.GET_LIVE_STREAM_STATUS);
    expect(component.isStreamActive).toBeFalsy();
  });

  it('should test handleLiveStreamStatus', fakeAsync(() => {
    const actualResult = component['handleLiveStreamStatus']();
    const data = { streamID: null, streamActive: false };
    actualResult.then(result => {
        expect(result).toEqual(data);
      }
    );
  }));

  describe('offsetWidth', () => {
    const offsetWidth = 100;
    const parentNode = { tag: 'div' };
    it('should handle case when element does not have parentElement', () => {
      elementRef.nativeElement.parentNode = parentNode;
      domToolsService.getWidth.and.returnValue(offsetWidth);

      expect(component['offsetWidth']).toEqual(offsetWidth);
      expect(domToolsService.getWidth).toHaveBeenCalledWith(parentNode);
    });

    it('should handle case when parentElement does not have parentNode', () => {
      elementRef.nativeElement.parentElement = {
        parentElement: null
      };
      elementRef.nativeElement.parentNode = parentNode;
      domToolsService.getWidth.and.returnValue(offsetWidth);

      expect(component['offsetWidth']).toEqual(offsetWidth);
      expect(domToolsService.getWidth).toHaveBeenCalledWith(parentNode);
    });

    it('should handle case when parentElement has have parentNode', () => {
      const parentElement = { tag: 'body' };
      elementRef.nativeElement.parentElement = {
        parentElement: {
          parentNode: parentElement
        }
      };
      elementRef.nativeElement.parentNode = parentNode;
      domToolsService.getWidth.and.returnValue(offsetWidth);

      expect(component['offsetWidth']).toEqual(offsetWidth);
      expect(domToolsService.getWidth).toHaveBeenCalledWith(parentElement);
    });
  });
});
