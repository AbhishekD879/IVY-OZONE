import { fakeAsync, discardPeriodicTasks, tick } from '@angular/core/testing';
import { NETWORK_CONSTANTS } from '@app/lazy-modules/networkIndicator/components/network-indicator/network-indicator.constants';
import { of, throwError } from 'rxjs';

import { InsomniaService } from './insomnia.service';

describe('InsomniaService', () => {
  let service: InsomniaService;
  let pubSubService;
  let storageService;
  let reloadService;
  let cmsService;
  let windowRef;
  let nativeBridgeService;
  let device;
  const RESPONSE = {
    'id': '62e8be4cb50ad87c69165633',
    'pollingInterval': 5000,
    'networkIndicatorEnabled': true,
    'networkSpeed': {
      'slow': {
        'displayText': 'Network connection interrupted',
        'infoMsg': 'sometext'
      },
      'online': {
        'displayText': 'Network connection is restored',
        'timeout': 3000
      },
      'offline': {
        'displayText': 'Network is offine'
      }
    },
    'thresholdTime': 200,
    'slowTimeout': 3000,
    'imageURL': 'https: //scmedia.itsfogo.com/$-$/8abaa65e01f24df587aadff849e25915.jpg'
  };

  beforeEach(() => {
    pubSubService = {
      publish: jasmine.createSpy('publish')
    };
    storageService = {
      setCookie: jasmine.createSpy('setCookie'),
      set: jasmine.createSpy('storageService.set'),
      get: jasmine.createSpy('storageService.get')
    };
    reloadService = {
      reload: jasmine.createSpy('reload')
    };
    cmsService = {
      get: jasmine.createSpy('get'),
      getNetworkIndicatorConfig: jasmine.createSpy('getNetworkIndicatorConfig').and.returnValue(of(RESPONSE))
    };
    windowRef = {
      document: {
        visibilityState: 'hidden',
        body: {},
        documentElement: {},
        querySelector: jasmine.createSpy('querySelector').and.returnValue({}),
        getElementById: jasmine.createSpy('getElementById')
      },
      nativeWindow: {
        addEventListener: jasmine.createSpy('addEventListener'),
        clearTimeout: jasmine.createSpy('clearTimeout'),
        setTimeout: jasmine.createSpy('setTimeout')
      }
    };
    nativeBridgeService = {
      networkIndicatorEnabled: jasmine.createSpy('networkIndicatorEnabled')
    };
    device = {
      isMobile: true,
      isTablet: false,
      isDesktop: false
    };
    service = new InsomniaService(
      pubSubService,
      storageService,
      reloadService,
      cmsService,
      windowRef,
      nativeBridgeService,
      device
    );
  });

  it('constructor', () => {
    expect(service).toBeTruthy();
  });

  it('init', () => {
    service['addWorkerListeners'] = jasmine.createSpy();
    service['checkWorkerSync'] = jasmine.createSpy();

    service.init();

    expect(service.worker).toEqual(jasmine.any(Worker));
    expect(service['addWorkerListeners']).toHaveBeenCalled();
    expect(service['checkWorkerSync']).toHaveBeenCalled();
  });

  it('setTimeoutAction (worker supported)', () => {
    service.workerSupport = true;
    service.worker = {
      postMessage: jasmine.createSpy()
    } as any;

    const eventData: any = {};
    const interval = 1000;
    service.setTimeoutAction(eventData, interval);

    expect(service.worker.postMessage).toHaveBeenCalledWith({
      eventData, interval, type: 'timeout'
    });
  });

  it('setTimeoutAction (worker not supported)', () => {
    service.workerSupport = false;
    service['workerEmu'] = jasmine.createSpy();

    const eventData: any = {};
    const interval = 1000;
    service.setTimeoutAction(eventData, interval);

    expect(service['workerEmu']).toHaveBeenCalledWith({
      eventData, interval, type: 'timeout'
    });
  });

  it('findTimeEvent', () => {
    expect(service['findTimeEvent']('event1')).toBeFalsy();
    expect(service['findTimeEvent']('event2')).toBeFalsy();

    service['timeTimeoutEvents']['event1'] = {};
    expect(service['findTimeEvent']('event1')).toBeTruthy();

    service['timeIntervalEvents']['event2'] = {};
    expect(service['findTimeEvent']('event2')).toBeTruthy();
  });

  it('workerEmu (clear)', () => {
    service['timeTimeoutEvents'] = { event1: true };
    service['timeIntervalEvents'] = { event2: true };

    const data: any = {
      clearTimeouts: true, clearIntervals: true
    };

    service['workerEmu'](data);

    expect(service['timeTimeoutEvents']).toEqual({});
    expect(service['timeIntervalEvents']).toEqual({});
  });

  it('workerEmu (timeout)', fakeAsync(() => {
    const data: any = {
      type: 'timeout',
      eventData: { eventName: 'event1' },
      interval: 1
    };

    service['findTimeEvent'] = jasmine.createSpy().and.returnValue(true);
    service['timeTimeoutEvents'][data.eventData.eventName] = { timeout: 123 };

    service['workerEmu'](data);
    tick(1);

    expect(service['findTimeEvent']).toHaveBeenCalledWith(data.eventData.eventName);
    expect(pubSubService.publish).toHaveBeenCalledWith('INSOMNIA', [data.eventData]);
    expect(service['timeTimeoutEvents'][data.eventData.eventName]).toEqual({
      timeout: jasmine.any(Number),
      eventData: data.eventData
    });
  }));

  it('workerEmu (interval)', fakeAsync(() => {
    const data: any = {
      type: 'interval',
      eventData: { eventName: 'event1' },
      interval: 1
    };

    service['findTimeEvent'] = jasmine.createSpy().and.returnValue(false);
    service['timeIntervalEvents'][data.eventData.eventName] = { timeout: 123 };

    service['workerEmu'](data);
    tick(1);

    expect(service['findTimeEvent']).toHaveBeenCalledWith(data.eventData.eventName);
    expect(pubSubService.publish).toHaveBeenCalledWith('INSOMNIA', [data.eventData]);
    expect(service['timeIntervalEvents'][data.eventData.eventName]).toEqual({
      interval: jasmine.any(Number),
      eventData: data.eventData
    });
    discardPeriodicTasks();
  }));

  it('reloadApp', () => {
    spyOn(sessionStorage, 'setItem');

    storageService.isSupported = true;
    service['reloadApp']();
    expect(reloadService.reload).toHaveBeenCalled();
    expect(sessionStorage.setItem).toHaveBeenCalledWith('show-alternative-screen', 'true');

    storageService.isSupported = false;
    service['reloadApp']();
    expect(storageService.setCookie).toHaveBeenCalledWith(
      'show-alternative-screen', 'true', null, 1
    );
    expect(reloadService.reload).toHaveBeenCalled();
  });

  it('addWorkerListeners', () => {
    service.worker = {} as any;
    service['addWorkerListeners']();

    expect(service.worker.onmessage).toEqual(jasmine.any(Function));
    expect(service.worker.onerror).toEqual(jasmine.any(Function));
  });

  it('addWorkerListeners (check worker availability)', () => {
    service.worker = {} as any;
    service['addWorkerListeners']();

    service.worker.onmessage({
      data: { checkWorkerAvailability: true }
    } as any);

    expect(service.workerSupport).toBeTruthy();
  });

  it('addWorkerListeners (check worker sync)', () => {
    service.worker = {} as any;
    service['reloadApp'] = jasmine.createSpy();
    service['addWorkerListeners']();

    service.worker.onmessage({
      data: { checkWorkerSync: true }
    } as any);

    expect(service['reloadApp']).toHaveBeenCalled();
  });

  it('addWorkerListeners (insomnia)', () => {
    service.worker = {} as any;
    service['reloadApp'] = jasmine.createSpy();
    service['addWorkerListeners']();

    service.worker.onmessage({
      data: {}
    } as any);

    expect(pubSubService.publish).toHaveBeenCalledWith('INSOMNIA', [{}]);
  });

  it('addWorkerListeners should instantly return', () => {
    service.worker = {} as any;
    service['isTriggeredMap'].set(1, true);
    service['addWorkerListeners']();

    service.worker.onmessage({
      data: {
        classId: 1
      }
    } as any);

    expect(pubSubService.publish).not.toHaveBeenCalled();
  });

  it('addWorkerListeners should properly set isTriggeredMap', fakeAsync(() => {
    service.worker = {} as any;
    service['addWorkerListeners']();
    service.worker.onmessage({
      data: {
        classId: 1
      }
    } as any);
    expect(service['isTriggeredMap'].get(1)).toBe(true);
    tick(10000);
    expect(service['isTriggeredMap'].get(1)).toBe(false);
  }));

  it('checkWorkerSync', () => {
    service.worker = {
      postMessage: jasmine.createSpy()
    } as any;

    service['checkWorkerSync']();

    expect(service.worker.postMessage).toHaveBeenCalledWith({
      checkWorkerAvailability: true
    });
    expect(service.worker.postMessage).toHaveBeenCalledWith({
      checkWorkerSync: true, interval: 5000, type: 'interval'
    });
  });

  describe('#initNetworkIndicator', () => {
    it('terminate webworker when message is offline', () => {
      service.networkWorker = {
        postMessage: jasmine.createSpy(),
        terminate: jasmine.createSpy()
      } as any;
      service.cmsNetworkData = {
        networkIndicatorEnabled: true
      } as any;
      service['initializeNetworkWebWorker'] = jasmine.createSpy('initializeNetworkWebWorker');
      service['emitNetworkMessageInfo'] = jasmine.createSpy('emitNetworkMessageInfo');
      const update = 'offline';
      service['pubSubService'].subscribe = jasmine.createSpy().and.callFake((sb, ch, fn) => {
        if (ch === NETWORK_CONSTANTS.NW_I_STATUS_RELOAD) {
          fn(update);
        }
      });
      service['initNetworkIndicator']();
      expect(service.networkWorker.terminate).toHaveBeenCalled();
    });

    it('webworker when message is not offline', () => {
      service.networkWorker = {
        postMessage: jasmine.createSpy(),
        terminate: jasmine.createSpy()
      } as any;
      service.cmsNetworkData = {
        networkIndicatorEnabled: true
      } as any;
      service['initializeNetworkWebWorker'] = jasmine.createSpy('initializeNetworkWebWorker');
      service['emitNetworkMessageInfo'] = jasmine.createSpy('emitNetworkMessageInfo');
      const update = 'offline';
      service['pubSubService'].subscribe = jasmine.createSpy().and.callFake((sb, ch, fn) => {
        if (ch === NETWORK_CONSTANTS.NW_I_STATUS_RELOAD) {
          fn(update);
        }
      });
      service['initNetworkIndicator']();
      expect(service.initializeNetworkWebWorker).toHaveBeenCalled();
    });

    it('initializeNetworkWebWorker should not be called if response is failed', () => {
      service.networkWorker = {
        postMessage: jasmine.createSpy(),
        terminate: jasmine.createSpy()
      } as any;
      service.cmsNetworkData = {
        networkIndicatorEnabled: true
      } as any;
      service['initializeNetworkWebWorker'] = jasmine.createSpy('initializeNetworkWebWorker');
      service['emitNetworkMessageInfo'] = jasmine.createSpy('emitNetworkMessageInfo');
      cmsService.getNetworkIndicatorConfig.and.returnValue(throwError({ status: 404 }));
      const update = 'offline';
      service['pubSubService'].subscribe = jasmine.createSpy().and.callFake((sb, ch, fn) => {
        if (ch === NETWORK_CONSTANTS.NW_I_STATUS_RELOAD) {
          fn(update);
        }
      });
      service['initNetworkIndicator']();
      expect(service.initializeNetworkWebWorker).not.toHaveBeenCalled();
    });
    it('initializeNetworkWebWorker should not be called if networkIndicatorEnabled is false', () => {
      service.networkWorker = {
        postMessage: jasmine.createSpy(),
        terminate: jasmine.createSpy()
      } as any;
      service['initializeNetworkWebWorker'] = jasmine.createSpy('initializeNetworkWebWorker');
      service['emitNetworkMessageInfo'] = jasmine.createSpy('emitNetworkMessageInfo');
      const resp = {...RESPONSE};
      resp.networkIndicatorEnabled = false;
      cmsService.getNetworkIndicatorConfig.and.returnValue(of(resp));
      const update = 'offline';
      service['pubSubService'].subscribe = jasmine.createSpy().and.callFake((sb, ch, fn) => {
        if (ch === NETWORK_CONSTANTS.NW_I_STATUS_RELOAD) {
          fn(update);
        }
      });
      service['initNetworkIndicator']();
      expect(service.emitNetworkMessageInfo).not.toHaveBeenCalled();
    });
    it('initializeNetworkWebWorker should not be called if response is undefined', () => {
      service.networkWorker = {
        postMessage: jasmine.createSpy(),
        terminate: jasmine.createSpy()
      } as any;
      service.cmsNetworkData = {
        networkIndicatorEnabled: true
      } as any;
      service['initializeNetworkWebWorker'] = jasmine.createSpy('initializeNetworkWebWorker');
      service['emitNetworkMessageInfo'] = jasmine.createSpy('emitNetworkMessageInfo');
      cmsService.getNetworkIndicatorConfig.and.returnValue(of(undefined));
      const update = 'offline';
      service['pubSubService'].subscribe = jasmine.createSpy().and.callFake((sb, ch, fn) => {
        if (ch === NETWORK_CONSTANTS.NW_I_STATUS_RELOAD) {
          fn(update);
        }
      });
      service['initNetworkIndicator']();
      expect(service.initializeNetworkWebWorker).not.toHaveBeenCalled();
    });
    it('initializeNetworkWebWorker should be called when message is online', () => {
      service.networkWorker = {
        postMessage: jasmine.createSpy(),
        terminate: jasmine.createSpy()
      } as any;
      service.cmsNetworkData = {
        networkIndicatorEnabled: true
      } as any;
      service['initializeNetworkWebWorker'] = jasmine.createSpy('initializeNetworkWebWorker');
      service['emitNetworkMessageInfo'] = jasmine.createSpy('emitNetworkMessageInfo');
      const resp = { ...RESPONSE };
      resp.networkIndicatorEnabled = true;
      cmsService.getNetworkIndicatorConfig.and.returnValue(of(resp));
      const update = 'online';
      service['pubSubService'].subscribe = jasmine.createSpy().and.callFake((sb, ch, fn) => {
        if (ch === NETWORK_CONSTANTS.NW_I_STATUS_RELOAD) {
          fn(update);
        }
      });
      service['initNetworkIndicator']();
      expect(service.initializeNetworkWebWorker).toHaveBeenCalled();
    });
  });

  describe('#initializeNetworkWebWorker', () => {
    it('postMessage to have been called when networkIndicatorEnabled is true', () => {
      service.cmsNetworkData = {
        networkIndicatorEnabled: true
      } as any;
      service['networkIndicatorFileUrl']= '';
      service['initializeNetworkWebWorker']();
    });
    it('should not create Worker when the device type is mobile false', () => {
      service.cmsNetworkData = {
        networkIndicatorEnabled: true
      } as any;
      device.isMobile = false;
      service['networkIndicatorFileUrl']= '';
      service['initializeNetworkWebWorker']();
    });
    it('postMessage not to be called when networkIndicatorEnabled is false', () => {
      service.cmsNetworkData = {
        networkIndicatorEnabled: false
      } as any;
      service['networkIndicatorFileUrl']= '';
      service['initializeNetworkWebWorker']();
    });
    it('postMessage not to be called when cmsNetworkData is null', () => {
      service.cmsNetworkData = null;
      service['networkIndicatorFileUrl']= '';
      service['initializeNetworkWebWorker']();
    });
    it('postMessage to have been called when networkIndicatorEnabled is true', () => {
      service.cmsNetworkData = {
        networkIndicatorEnabled: true
      } as any;
      device.isMobile = true;
      service['networkIndicatorFileUrl'] = '';
      service['emitNetworkMessageInfo'] = jasmine.createSpy('emitNetworkMessageInfo');
      service['initializeNetworkWebWorker']();
      service.networkWorker.onmessage({} as any);
    });
  });

  describe('#handleVisibilityForWebworker', () => {
    it('if visibilityState is hidden, should call terminate', () => {
      service.cmsNetworkData = {
        networkIndicatorEnabled: true
      } as any;
      service['initializeNetworkWebWorker'] = jasmine.createSpy('initializeNetworkWebWorker');
      service.networkWorker = {
        postMessage: jasmine.createSpy(),
        terminate: jasmine.createSpy()
      } as any;
      service['handleVisibilityForWebworker']();
      expect(service.networkWorker.terminate).toHaveBeenCalled();
    });
    it('if visibilityState is not hidden, should call initializeNetworkWebWorker', () => {
      service.cmsNetworkData = {
        networkIndicatorEnabled: true
      } as any;
      windowRef.document.visibilityState = 'shown';
      service['initializeNetworkWebWorker'] = jasmine.createSpy('initializeNetworkWebWorker');
      service['handleVisibilityForWebworker']();
      expect(service.initializeNetworkWebWorker).toHaveBeenCalled();
    });
  });

  describe('#emitNetworkMessageInfo', () => {
    it('change networkState to offline if isOffline is true', () => {
      service.isOffline = true;
      service.cmsNetworkData = {
        networkIndicatorEnabled: true,
        pollingInterval: 5000,
        networkSpeed: {
          slow: { displayText: 'Network connection interrupted', infoMsg: 'Please check your internet connection' },
          online: { displayText: 'Network connection is restored', timeout: 3000 },
          offline: { displayText: 'Network is offine' }
        },
        thresholdTime: 200,
        slowTimeout: 3000,
        imageURL: 'https://i.picsum.photos/id/777/640/480.jpg?hmac=xOTAokwb7BeCdNpwD2qMOaTjyB9_TzMksL-oV9CQLcU'
      } as any;
      service['emitNetworkMessageInfo']('slow');
      expect(pubSubService.publish).toHaveBeenCalled();
    });
    it('do not change networkState to offline if isOffline is false', () => {
      service.isOffline = false;
      service.cmsNetworkData = {
        networkIndicatorEnabled: true,
        pollingInterval: 5000,
        networkSpeed: {
          slow: { displayText: 'Network connection interrupted', infoMsg: 'Please check your internet connection' },
          online: { displayText: 'Network connection is restored', timeout: 3000 },
          offline: { displayText: 'Network is offine' }
        } as any,
        thresholdTime: 200,
        slowTimeout: 3000,
        imageURL: 'https://i.picsum.photos/id/777/640/480.jpg?hmac=xOTAokwb7BeCdNpwD2qMOaTjyB9_TzMksL-oV9CQLcU'
      } as any;
      service['emitNetworkMessageInfo']('online');
      expect(pubSubService.publish).toHaveBeenCalled();
    });
    it('do not change networkState to offline if networkstate is invalid', () => {
      service.isOffline = false;
      service.cmsNetworkData = {
        networkIndicatorEnabled: true,
        pollingInterval: 5000,
        networkSpeed: {
          slow: { displayText: 'Network connection interrupted', infoMsg: 'Please check your internet connection' },
          online: { displayText: 'Network connection is restored', timeout: 3000 },
          offline: { displayText: 'Network is offine' }
        } as any,
        thresholdTime: 200,
        slowTimeout: 3000,
        imageURL: 'https://i.picsum.photos/id/777/640/480.jpg?hmac=xOTAokwb7BeCdNpwD2qMOaTjyB9_TzMksL-oV9CQLcU'
      } as any;
      service['emitNetworkMessageInfo']('invalid');
      expect(pubSubService.publish).not.toHaveBeenCalled();
    });
  });
});
