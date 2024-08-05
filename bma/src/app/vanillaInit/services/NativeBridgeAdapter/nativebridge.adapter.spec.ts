import { NativeBridgeAdapter } from './nativebridge.adapter';
import { NativeEvent } from '@frontend/vanilla/core';
import { PortalNativeEvents } from '@vanillaInitModule/services/PortalNativeEventNotifier/portal-nativeEvents';

describe('NativeBridgeAdapter', () => {
  let service: NativeBridgeAdapter;
  let windowRefMock;
  let vanillaNativeAppServiceMock;
  let nativeEventMock: NativeEvent;

  beforeEach(() => {
    windowRefMock = {
      nativeWindow: {
        vanillaApp: {
          native: {
            messageToWeb: jasmine.createSpy()
          }
        }
      }
    };
    vanillaNativeAppServiceMock = {
      isNativeWrapper: true
    };
    service = new NativeBridgeAdapter(windowRefMock, vanillaNativeAppServiceMock);
    nativeEventMock = { eventName: 'TestEvent', parameters: {} };
  });

  it('attachNativeMessageReceiver is called', () => {
    service.attachNativeMessageReceiver = jasmine.createSpy();
    service.attachNativeMessageReceiver();
    expect(service.attachNativeMessageReceiver).toHaveBeenCalled();
  });

  it('messageToNative attached on window when attachNativeMessageReceiver called', () => {
    service.attachNativeMessageReceiver();
    expect(windowRefMock.nativeWindow.messageToNative).toBeDefined();
  });

  it('meesageToNative undefined when attachNativeMessageReceiver is not called', () => {
    expect(windowRefMock.nativeWindow.messageToNative).toBeUndefined();
  });

  it('meesageToNative undefined when not a native app', () => {
    vanillaNativeAppServiceMock.isNativeWrapper = false;
    service = new NativeBridgeAdapter(windowRefMock, vanillaNativeAppServiceMock);
    service.attachNativeMessageReceiver();
    expect(windowRefMock.nativeWindow.messageToNative).toBeUndefined();
  });

  it('Received native event broadcasted when messageToNative is called', () => {
    service.attachNativeMessageReceiver();
    windowRefMock.nativeWindow.messageToNative(nativeEventMock);
    service.nativeEventObservable.subscribe((event) => { expect(event).toBeDefined(); });
  });

  it('No event broadcasted when messageToNative is not called', () => {
    service.attachNativeMessageReceiver();
    service.nativeEventObservable.subscribe((event) => { expect(event).toBe(null); });
  });

  it('doNativeLogin is called', () => {
    service.doNativeLogin = jasmine.createSpy();
    service.doNativeLogin('TestUser', 'Password123');
    expect(service.doNativeLogin).toHaveBeenCalledWith('TestUser', 'Password123');
  });

  it('vanillaApp.native.messageToWeb on window is called when doNativeLogin is called', () => {
    service.doNativeLogin('TestUser', 'Password123', { 'isTouchIDEnabled': true });
    expect(windowRefMock.nativeWindow.vanillaApp.native.messageToWeb).toHaveBeenCalledWith(
      {
        'eventName': 'LOGIN',
        'parameters': {
          'username': 'TestUser',
          'password': 'Password123',
          'isDeviceSupported': true,
          'isTouchIDEnabled': true,
          'isFaceIDEnabled': undefined,
          'rememberMe': undefined
        }
      }
    );
  });

  describe('decorateEvent', () => {
    it('invoke after pre login', () => {
      const mockNativeEvent: NativeEvent = {
        eventName: PortalNativeEvents.PreLogin
      };

      service['handlePreLoginEvent'] = jasmine.createSpy().and.returnValue(null);
      expect(service['decorateEvent'](mockNativeEvent)).toBeNull();
      expect(service['handlePreLoginEvent']).toHaveBeenCalledWith(mockNativeEvent);
    });

    it('invoke after pre login with registrationParameters set', () => {
      const mockNativeEvent: NativeEvent = {
        eventName: PortalNativeEvents.PreLogin,
        parameters: {
          'userName': 'testUserName',
          'password': 'testPassword'
        }
      };
      const mockExpectedResult: NativeEvent = {
        eventName: PortalNativeEvents.RegistrationSuccessful,
        parameters: {
          'accountCurrency': 'GBP',
          'accountId': '12345',
          'language': 'en',
          'userName': 'testUserName',
          'password': 'testPassword'
        }
      };
      service['registrationParameters'] = {
        'accountCurrency': 'GBP',
        'accountId': '12345',
        'language': 'en'
      };

      service['handlePreLoginEvent'] = jasmine.createSpy().and.returnValue(mockExpectedResult);
      expect(service['decorateEvent'](mockNativeEvent)).toEqual(mockExpectedResult);
      expect(service['handlePreLoginEvent']).toHaveBeenCalledWith(mockNativeEvent);
    });

    it('invoke after post login', () => {
      const mockNativeEvent: NativeEvent = {
        eventName: PortalNativeEvents.PostLogin
      };
      const mockExpectedResult: NativeEvent = {
        eventName: PortalNativeEvents.PostLogin,
        parameters: {}
      };

      service['handlePostLoginEvent'] = jasmine.createSpy().and.returnValue(mockExpectedResult);
      expect(service['decorateEvent'](mockNativeEvent)).toEqual(mockExpectedResult);
      expect(service['handlePostLoginEvent']).toHaveBeenCalledWith(mockNativeEvent);
    });

    it('invoke after registration', () => {
      const mockNativeEvent: NativeEvent = {
        eventName: PortalNativeEvents.RegistrationSuccessful,
        parameters: {
          'accountCurrency': 'GBP',
          'accountId': '12345',
          'language': 'en'
        }
      };

      expect(service['decorateEvent'](mockNativeEvent)).toBeNull();
      expect(service['registrationParameters']).toEqual(mockNativeEvent.parameters);
    });

    it('invoke after post login with remember me set', () => {
      const mockNativeEvent: NativeEvent = {
        eventName: PortalNativeEvents.PostLogin
      };

      expect(service['handlePostLoginEvent'](mockNativeEvent)).toEqual(null);
      expect(service['decorateEvent'](mockNativeEvent)).toEqual(null);
    });

    it('invoke after post login with prelogin parameters null', () => {
      const mockNativeEvent: NativeEvent = {
        eventName: PortalNativeEvents.PostLogin
      };
      service['preLoginParameters'] = null;

      expect(service['handlePostLoginEvent'](mockNativeEvent)).toEqual(null);
      expect(service['decorateEvent'](mockNativeEvent)).toEqual(null);
    });

    it('invoke after registration screen become active', () => {
      const mockNativeEvent: NativeEvent = {
        eventName: PortalNativeEvents.RegistrationScreenActive
      };
      const mockExpectedResult: NativeEvent = {
        eventName: PortalNativeEvents.MenuScreenActive,
        parameters: {}
      };

      service['handleDummyMenuScreenActiveEvent'] = jasmine.createSpy().and.returnValue(mockExpectedResult);
      spyOn(service.nativeEventNotifier, 'next').and.callThrough();
      expect(service['decorateEvent'](mockNativeEvent)).toEqual(mockExpectedResult);
      expect(service.nativeEventNotifier.next).toHaveBeenCalledWith(mockNativeEvent);
      expect(service['handleDummyMenuScreenActiveEvent']).toHaveBeenCalledWith(mockNativeEvent);
    });

    it('invoke with not handled event name and return not altered event', () => {
      const mockNativeEvent: NativeEvent = {
        eventName: 'NotHandledEvent'
      };

      expect(service['decorateEvent'](mockNativeEvent)).toEqual(mockNativeEvent);
    });

    it('invoke with empty event name and return not changed event', () => {
      const mockNativeEvent = null;

      expect(service['decorateEvent'](mockNativeEvent)).toEqual(mockNativeEvent);
    });
  });

  it('handlePreLoginEvent should set preLoginParameters with event.parameters and return null', () => {
    const mockNativeEvent: NativeEvent = {
      eventName: PortalNativeEvents.PostLogin,
      parameters: {
        param: 'test'
      }
    };

    expect(service['handlePreLoginEvent'](mockNativeEvent)).toBeNull();
    expect(service['preLoginParameters']).toEqual(mockNativeEvent.parameters);
  });

  it('handlePostLoginEvent should return adjusted event', () => {
    const mockNativeEvent: NativeEvent = {
      eventName: PortalNativeEvents.PreLogin,
      parameters: {
        param: ''
      }
    };
    service['preLoginParameters'] = {
      preLoginParameter: ''
    };
    service['loginType'] = 'Manual';
    const mockExpectedResult: NativeEvent = {
      eventName: PortalNativeEvents.Login,
      parameters: {
        param: '',
        preLoginParameter: '',
        isFromBetSlip: false,
        type: 'Manual'
      }
    };

    expect(service['handlePostLoginEvent'](mockNativeEvent)).toEqual(mockExpectedResult);
  });
});
