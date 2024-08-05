import { PortalNativeEventNotifier } from './portal-nativeEvent-notifier';
import { NativeBridgeAdapter } from '../NativeBridgeAdapter/nativebridge.adapter';
import { NativeEvent } from '@frontend/vanilla/core';
import { PortalNativeEvents } from './portal-nativeEvents';

describe('PortalNativeEventNotifier', () => {
  let service: PortalNativeEventNotifier;
  let nativeBridgeAdapterMock: NativeBridgeAdapter;
  let nativeBridgeServiceMock;
  let windowRefMock;
  let vanillaNativeAppServiceMock;
  let nativeEventMock: Map<string, NativeEvent>;
  let vanillaAuthServiceMock;

  beforeEach(() => {
    windowRefMock = {
      nativeWindow: {
        setTimeout: jasmine.createSpy().and.callFake((cb) => {
          cb && cb();
        })
      }
    };
    vanillaNativeAppServiceMock = {
      isNativeWrapper: true
    };
    vanillaAuthServiceMock = {
      handleRegistrationRedirection: jasmine.createSpy(),
      handleMobileAutoLogin: jasmine.createSpy(),
      setAppsFlyerCookies: jasmine.createSpy()
    };

    nativeBridgeAdapterMock = new NativeBridgeAdapter(windowRefMock, vanillaNativeAppServiceMock);

    nativeBridgeServiceMock = jasmine.createSpyObj('nativeBridgeServiceMock',
      [
        'registrationStartedIfExist',
        'registrationFinishedIfExist',
        'registrationFinishedSalesForce',
        'passwordChangedIfExist',
        'showNotificationSettings',
        'onClosePopup'
      ]);

    service = new PortalNativeEventNotifier(
      nativeBridgeAdapterMock,
      nativeBridgeServiceMock,
      vanillaNativeAppServiceMock,
      vanillaAuthServiceMock
    );

    nativeEventMock = new Map<string, NativeEvent>([
      ['Login', { eventName: PortalNativeEvents.Login }],
      ['OpenRegistrationScreen', { eventName: PortalNativeEvents.OpenRegistrationScreen }],
      ['CloseRegistrationScreen', { eventName: PortalNativeEvents.CloseRegistrationScreen }],
      ['RegistrationScreenActive', { eventName: PortalNativeEvents.RegistrationScreenActive }],
      ['RegistrationSuccessful',
        {
          eventName: PortalNativeEvents.RegistrationSuccessful,
          parameters: { accountId: '12345', userName: 'testusername' }
        }],
      ['PreLogin',
        {
          eventName: PortalNativeEvents.PreLogin,
          parameters: { password: '12345' }
        }],
      ['UpdatePassword',
        {
          eventName: PortalNativeEvents.UpdatePassword,
          parameters: { newPassword: 'testpassword', username: 'testusername' }
        }]
    ]);

    service.attachNativeMessageNotifier();

    nativeBridgeAdapterMock.attachNativeMessageReceiver();
  });

  it('nativeBridgeAdapter.nativeEventObservable.subscribe not called when not native app', () => {
    const spyObj = jasmine.createSpy();
    nativeBridgeAdapterMock.nativeEventObservable.subscribe = spyObj;
    vanillaNativeAppServiceMock.isNativeWrapper = false;
    service = new PortalNativeEventNotifier(
      nativeBridgeAdapterMock,
      nativeBridgeServiceMock,
      vanillaNativeAppServiceMock,
      vanillaAuthServiceMock
    );
    service.attachNativeMessageNotifier();
    expect(spyObj).not.toHaveBeenCalled();
  });

  it('calls vanilla auth service handleMobileAutoLogin when Login event is raised', () => {
    windowRefMock.nativeWindow.messageToNative(nativeEventMock.get('Login'));
    expect(vanillaAuthServiceMock.handleMobileAutoLogin).toHaveBeenCalledWith(jasmine.objectContaining({
      eventName: PortalNativeEvents.Login
    }));
  });

  it('calls vanilla auth service handleRegistrationRedirection when openRegistrationScreen event is raised', () => {
    windowRefMock.nativeWindow.messageToNative(nativeEventMock.get('OpenRegistrationScreen'));
    expect(vanillaAuthServiceMock.handleRegistrationRedirection).toHaveBeenCalled();
  });

  it('calls native bridge onClosePopup when closeRegistrationScreen event is raised', () => {
    windowRefMock.nativeWindow.messageToNative(nativeEventMock.get('CloseRegistrationScreen'));
    expect(nativeBridgeServiceMock.onClosePopup).toHaveBeenCalled();
  });

  it('calls native bridge registrationStartedIfExist when Registration_Screen_Active event is raised', () => {
    windowRefMock.nativeWindow.messageToNative(nativeEventMock.get('RegistrationScreenActive'));
    expect(nativeBridgeServiceMock.registrationStartedIfExist).toHaveBeenCalled();
    expect(vanillaAuthServiceMock.setAppsFlyerCookies).toHaveBeenCalled();
  });

  it('calls native bridge passwordChangedIfExist when PasswordUpdate event is raised', () => {
    windowRefMock.nativeWindow.messageToNative(nativeEventMock.get('UpdatePassword'));
    expect(nativeBridgeServiceMock.passwordChangedIfExist).toHaveBeenCalledWith('testpassword', 'testusername');
  });

  it('calls native bridge registrationFinishedIfExist when Pre Login event is raised after Registration', () => {
    windowRefMock.nativeWindow.messageToNative(nativeEventMock.get('RegistrationSuccessful'));
    windowRefMock.nativeWindow.messageToNative(nativeEventMock.get('PreLogin'));
    expect(nativeBridgeServiceMock.registrationFinishedIfExist).toHaveBeenCalledWith('12345', '12345');
    expect(nativeBridgeServiceMock.registrationFinishedSalesForce).toHaveBeenCalledWith('cl_testusername');
  });

  describe('destroyNativeEventNotifierSubscription', () => {
    it('nativeEventObservablesubscription = true ,  nativeEventObservablesubscription = true', () => {
      service['nativeEventObservablesubscription'] = {} as any;
      service['nativeEventObservablesubscription'].unsubscribe = jasmine.createSpy('nativeEventObservablesubscription.unsubscribe');
      service.destroyNativeEventNotifierSubscription();
      expect(service['nativeEventObservablesubscription'].unsubscribe).toHaveBeenCalled();
    });
  });
});
