import { of, throwError } from 'rxjs';
import { fakeAsync, flush, tick } from '@angular/core/testing';

import { CSBPlayerComponent } from './csb-player.component';
import {
  IPerformGroupConfig,
  IStreamProvidersResponse
} from '@lazy-modules/eventVideoStream/models/video-stream.model';
import { ISportEvent } from '@core/models/sport-event.model';

describe('CsbPlayerComponent', () => {
  let component: CSBPlayerComponent;

  let performGroupService;
  let deviceService;
  let racingStreamService;
  let elementRef;
  let eventVideoStreamProvider;
  let windowRefService;
  let watchRulesService;
  let sanitizer;
  let eventEntity;
  let successHandler;
  let errorHandler;


  beforeEach(() => {
    performGroupService = jasmine.createSpyObj(['getElementWidth', 'performGroupId', 'isPerformStreamStarted']);
    deviceService = {};
    racingStreamService = jasmine.createSpyObj(['getVideoCSBUrl']);
    elementRef = {};
    eventVideoStreamProvider = { playSuccessErrorListener: jasmine.createSpyObj(['next']) };
    windowRefService = {
      nativeWindow: {
        addEventListener: jasmine.createSpy('addEventListener'),
        removeEventListener: jasmine.createSpy('removeEventListener'),
        dispatchEvent: jasmine.createSpy('dispatchEvent')
      }
    };
    watchRulesService = {
      canWatchEvent: jasmine.createSpy('canWatchEvent'),
      shouldShowCSBIframe: jasmine.createSpy('shouldShowCSBIframe'),
      isInactiveUser: jasmine.createSpy('isInactiveUser'),
      SPORTS_WITH_WATCH_RULES: ''
    } as any;
    sanitizer = jasmine.createSpyObj(['bypassSecurityTrustResourceUrl']);
    eventEntity = {
      id: 111,
      typeId: '11',
      categoryId: '1',
      categoryCode: 'FOOTBALL',
      streamProviders: {
        ATR: false,
        RPGTV: false,
        RacingUK: false,
        IMG: false,
        Perform: false
      }
    } as ISportEvent;


    successHandler = jasmine.createSpy('success');
    errorHandler = jasmine.createSpy('errorHandler');

    component = new CSBPlayerComponent(performGroupService, deviceService, racingStreamService, elementRef,
      eventVideoStreamProvider, windowRefService, watchRulesService, sanitizer);

    component.streamCache = new Map();
    component.eventEntity = eventEntity;

  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  describe('ngOnInit', () => {
    const url = 'url';

    beforeEach(() => {
      spyOn(component, 'onError');
      spyOn(component, 'showStream').and.returnValue(of(url));
      spyOn(component as any, 'setPlayerDimensions');
      spyOn(component as any, 'addWindowListener');

      component.performConfig = {} as any;
      performGroupService.isPerformStreamStarted.and.returnValue(true);
      watchRulesService.canWatchEvent.and.returnValue(of(null));
      component.streamCache.set(eventEntity.id, { stream: '' } as IStreamProvidersResponse);
    });

    it(`should handle error`, () => {
      watchRulesService.canWatchEvent.and.returnValue(throwError('error'));

      component.ngOnInit();

      expect(component.onError).toHaveBeenCalledWith('error');
    });

    it(`should run onError if streamNotStartedMsg`, () => {
      performGroupService.isPerformStreamStarted.and.returnValue(false);
      component.ngOnInit();

      expect(component.onError).toHaveBeenCalledWith('eventNotStarted');
    });

    it(`should run onError if Not performConfig`, () => {
      performGroupService.isPerformStreamStarted.and.returnValue(false);
      component.performConfig = undefined;

      component.ngOnInit();

      expect(component.onError).toHaveBeenCalledWith('eventNotStarted');
    });

    it(`should check canWatchPerformStream`, () => {
      component.ngOnInit();

      expect(watchRulesService.canWatchEvent).toHaveBeenCalledWith(component.providerInfo, '1', 111);
      expect(component.showStream).toHaveBeenCalledWith(component.providerInfo);
    });

    it(`should error if showStream do nor return url `, fakeAsync(() => {
      (component['showStream'] as any).and.returnValue(of(null));

      component.ngOnInit();
      flush();

      expect(component.onError).toHaveBeenCalled();
      expect(component['setPlayerDimensions']).not.toHaveBeenCalled();
    }));

    it(`should define streamingClearUrl`, fakeAsync(() => {
      component.ngOnInit();
      flush();

      expect(component.streamingClearUrl).toEqual(url);
    }));

    it(`should define stream for streamCache`, fakeAsync(() => {
      component.ngOnInit();
      flush();

      expect(eventVideoStreamProvider.playSuccessErrorListener.next).toHaveBeenCalledWith(true);
    }));

    it(`should setPlayerDimensions`, fakeAsync(() => {
      component.ngOnInit();
      flush();

      expect(component['setPlayerDimensions']).toHaveBeenCalled();
    }));

    it(`should add resize listener`, fakeAsync(() => {
      component.ngOnInit();
      flush();

      expect(component['addWindowListener']).toHaveBeenCalled();
    }));

    it(`should Not add resize listener if isMobile`, fakeAsync(() => {
      deviceService.isMobile = true;

      component.ngOnInit();
      flush();

      expect(component['addWindowListener']).not.toHaveBeenCalled();
    }));
  });

  describe('showStream', () => {
    it('should return null if cached stream has error', fakeAsync(() => {
      const providerInfo = {
        priorityProviderName: 'Perform',
        listOfMediaProviders: [{
          name: 'At The Races',
          children: []
        }, {
          name: 'Perform',
          children: [{
            media: {
              accessProperties: 'perform,1231223:0'
            }
          }]
        }]
      } as IStreamProvidersResponse;

      component.streamCache.set(eventEntity.id, { error: 'notLoggedIn' } as IStreamProvidersResponse);
      component['showStream'](providerInfo).subscribe(successHandler, errorHandler);
      tick();

      expect(successHandler).toHaveBeenCalledWith(null);
    }));

    it('should return null if no performConfig were found', fakeAsync(() => {
      const providerInfo = {
        priorityProviderName: 'Perform',
        listOfMediaProviders: [{
          name: 'At The Races',
          children: []
        }, {
          name: 'Perform',
          children: [{
            media: {
              accessProperties: 'perform,1231223:0'
            }
          }]
        }]
      } as IStreamProvidersResponse;
      component.performConfig = undefined;

      component.streamCache.set(eventEntity.id, {} as IStreamProvidersResponse);
      component['showStream'](providerInfo).subscribe(successHandler, errorHandler);
      tick();

      expect(successHandler).toHaveBeenCalledWith(null);
    }));

    it('should handle Perform provider by provider info', fakeAsync(() => {
      const url = 'url';
      performGroupService.performGroupId.and.returnValue(of(null));
      racingStreamService.getVideoCSBUrl.and.returnValue(url);
      component.performConfig = {} as IPerformGroupConfig;
      const providerInfo = {
        priorityProviderName: 'Perform',
        listOfMediaProviders: [{
          name: 'Perform',
          children: [{
            media: {
              accessProperties: 'Perform,1231223:0'
            }
          }]
        }]
      } as IStreamProvidersResponse;

      component['showStream'](providerInfo).subscribe(successHandler, errorHandler);
      tick();

      expect(performGroupService.performGroupId).toHaveBeenCalledWith(providerInfo,
        component.performConfig, 111);
      expect(racingStreamService.getVideoCSBUrl).toHaveBeenCalledWith(providerInfo,
        component.performConfig);
      expect(successHandler).toHaveBeenCalledWith(url);
    }));
  });

  describe('onError', () => {
    beforeEach(() => {
      spyOn(component.playStreamError, 'emit');
    });

    it(`should emmit error`, () => {
      component.onError();

      expect(component.playStreamError.emit).toHaveBeenCalledWith(undefined);
    });

    it(`should emmit error with string`, () => {
      const str = 'str';

      component.onError(str);

      expect(component.playStreamError.emit).toHaveBeenCalledWith(str);
    });
  });

  describe('ngOnDestroy', () => {
    it(`should unsubscribe of resizeListener`, () => {
      component['resizeListener'] = {
        unsubscribe: jasmine.createSpy('unsubscribe')
      } as any;

      component['watchPerformStreamSubscription'] = {
        unsubscribe: jasmine.createSpy('unsubscribe')
      } as any;

      component.ngOnDestroy();

      expect(component['resizeListener'].unsubscribe).toHaveBeenCalled();
      expect(component['watchPerformStreamSubscription'].unsubscribe).toHaveBeenCalled();
    });
  });

  it(`should add resize listener`, fakeAsync(() => {
    spyOn(component as any, 'setPlayerDimensions');
    let listenerCb;
    windowRefService.nativeWindow.addEventListener.and.callFake((name, cb) => listenerCb = cb);

    component['addWindowListener']();

    listenerCb(new Event('resize'));
    listenerCb(new Event('resize'));
    listenerCb(new Event('resize'));

    tick(300);

    expect(component['resizeListener']).toBeDefined();
    expect(component['setPlayerDimensions']).toHaveBeenCalledTimes(1);
  }));

  describe('generateStreamingUrl', () => {
    const secUrl = 'secUrl';

    beforeEach(() => {
      sanitizer.bypassSecurityTrustResourceUrl.and.returnValue(secUrl);
      component.frameWidth = 20;
      component.frameHeight = 10;
    });

    it(`should generate Streaming Url with Dimensions`, () => {
      const urlWithDimensions = 'url&width=20&height=10';

      component['generateStreamingUrl']('url');

      expect(sanitizer.bypassSecurityTrustResourceUrl).toHaveBeenCalledWith(urlWithDimensions);
    });

    it(`should set 'streamingUrl'`, () => {
      component['generateStreamingUrl']('url');

      expect(component.streamingUrl).toEqual(secUrl);
    });

    it(`should use 'streamingClearUrl' as default url`, () => {
      component.streamingClearUrl = 'streamingClearUrl';
      const urlWithDimensions = 'streamingClearUrl&width=20&height=10';

      component['generateStreamingUrl']();

      expect(component.streamingUrl).toEqual(secUrl);
      expect(sanitizer.bypassSecurityTrustResourceUrl).toHaveBeenCalledWith(urlWithDimensions);
    });
  });

  describe('setPlayerDimensions', () => {
    beforeEach(() => {
      spyOn(component as any, 'generateStreamingUrl');
    });

    it(`should define frameWidth if elWidth is Not bigger than MAX_FRAME_WIDTH`, () => {
      performGroupService.getElementWidth.and.returnValue(500);

      component['setPlayerDimensions']();

      expect(component.frameWidth).toEqual(500);
    });

    it(`should define frameWidth as MAX_FRAME_WIDTH if elWidth is bigger than MAX_FRAME_WIDTH`, () => {
      performGroupService.getElementWidth.and.returnValue(700);

      component['setPlayerDimensions']();

      expect(component.frameWidth).toEqual(600);
      expect(component['generateStreamingUrl']).toHaveBeenCalled();
    });

    it(`should NOT define frameWidth if widths do Not changed`, () => {
      performGroupService.getElementWidth.and.returnValue(500);
      component.frameWidth = 500;

      component['setPlayerDimensions']();

      expect(component.frameWidth).toEqual(500);
      expect(component['generateStreamingUrl']).not.toHaveBeenCalled();
    });

    it(`should define frame Dimensions and generateStreamingUrl`, () => {
      performGroupService.getElementWidth.and.returnValue(600);

      component['setPlayerDimensions']();

      expect(component.frameWidth).toEqual(600);
      expect(component.frameHeight).toEqual(438);
      expect(component['generateStreamingUrl']).toHaveBeenCalled();
    });
  });
});
