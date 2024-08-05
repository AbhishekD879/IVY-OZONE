import { Injectable } from '@angular/core';
import { NativeEvent, NativeAppService } from '@frontend/vanilla/core';
import { WindowRefService } from '@app/core/services/windowRef/window-ref.service';
import { BehaviorSubject, Observable } from 'rxjs';
import { PortalNativeEvents, LoginType } from '@vanillaInitModule/services/PortalNativeEventNotifier/portal-nativeEvents';
import { NativeLoginOptions } from './nativebridge.models';

@Injectable()
export class NativeBridgeAdapter {

  nativeEventNotifier = new BehaviorSubject<NativeEvent>(null);
  nativeEventObservable: Observable<NativeEvent> = this.nativeEventNotifier.asObservable();
  private preLoginParameters: Object;
  private registrationParameters: Object;
  private loginType: LoginType = 'Manual';

  constructor(private windowRef: WindowRefService,
    private vanillaNativeAppService: NativeAppService) {
  }

  attachNativeMessageReceiver(): void {
    if (this.vanillaNativeAppService.isNativeWrapper && !this.windowRef.nativeWindow.messageToNative) {
      this.windowRef.nativeWindow.messageToNative = (event: NativeEvent) => {

        event = this.decorateEvent(event);

        // eslint-disable-next-line
        event && console.log('EventReceived::', event);

        event && this.nativeEventNotifier.next(event);
      };
    }
  }

  doNativeLogin(userName: string, password: string, options?: NativeLoginOptions): void {
    // Set login type to Autologin for native app login.
    this.loginType = 'Autologin';
    this.windowRef.nativeWindow.vanillaApp.native.messageToWeb(
      {
        'eventName': PortalNativeEvents.Login,
        'parameters': {
          'username': userName,
          'password': password,
          'isDeviceSupported': true,
          'isTouchIDEnabled': options && options.isTouchIDEnabled,
          'isFaceIDEnabled': options && options.isFaceIDEnabled,
          'rememberMe': options && options.rememberMe
        }
      });
  }

  private decorateEvent(event: NativeEvent): NativeEvent {
    if (event) {
      switch (event.eventName) {
        case PortalNativeEvents.PreLogin:
          return this.handlePreLoginEvent(event);
        case PortalNativeEvents.PostLogin:
          return this.handlePostLoginEvent(event);
        case PortalNativeEvents.RegistrationSuccessful:
          // Save registration event parameters and suppress registration event.
          this.registrationParameters = event.parameters;
          return null;
        case PortalNativeEvents.RegistrationScreenActive:
          // broadcast original registration screen active event before stubbing menu screen active.
          // eslint-disable-next-line
          console.log('EventReceived::', event.eventName, event.parameters);
          this.nativeEventNotifier.next(event);
          // Stub for broadcasting right menu click event. TODO: Remove after vanilla implementation.
          return this.handleDummyMenuScreenActiveEvent(event);
        default:
          return event;
      }
    }
    return event;
  }

  private handlePreLoginEvent(event: NativeEvent): NativeEvent {
    this.preLoginParameters = event.parameters;

    // Raise registration successful event if Pre-Login triggered after rgistration.
    if (this.registrationParameters) {
      const accumulatedParameters = Object.assign({}, this.registrationParameters, this.preLoginParameters);
      event.parameters = accumulatedParameters;
      event.eventName = PortalNativeEvents.RegistrationSuccessful;

      // To safeguard triggering registration event multiple times.
      this.registrationParameters = null;

      return event;
    }
    return null;
  }

  private handlePostLoginEvent(event: NativeEvent): NativeEvent {

    // Check for remember me login.
    if (!this.preLoginParameters) {
      return null;
    }

    const accumulatedParameters = Object.assign({}, this.preLoginParameters, event.parameters);
    event.parameters = accumulatedParameters;

    // safeguard to avoid multiple invocations and handle remember me scenario.
    this.preLoginParameters = null;

    // TODO: check for isFromBetSlip flag.
    event.parameters.isFromBetSlip = false;

    event.parameters.type = this.loginType;

    event.eventName = PortalNativeEvents.Login;

    return event;
  }

  private handleDummyMenuScreenActiveEvent(event: NativeEvent): NativeEvent {
    event.eventName = PortalNativeEvents.MenuScreenActive;
    event.parameters = {};
    return event;
  }
}
