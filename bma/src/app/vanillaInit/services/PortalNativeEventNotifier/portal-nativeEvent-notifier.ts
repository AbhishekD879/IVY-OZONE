import { Injectable } from '@angular/core';
import { NativeBridgeAdapter } from '../NativeBridgeAdapter/nativebridge.adapter';
import { NativeEvent, NativeAppService } from '@frontend/vanilla/core';
import { NativeBridgeService } from '@app/core/services/nativeBridge/native-bridge.service';
import { PortalNativeEvents } from './portal-nativeEvents';
import { Subscription } from 'rxjs';
import { VanillaAuthService } from '@vanillaInitModule/services/vanillaAuth/vanilla-auth.service';
import { BRAND_PREFIXES_CONSTANTS } from '@vanillaInitModule/constants/brand-prefixes.constants';

@Injectable()
export class PortalNativeEventNotifier {

  private nativeEventObservablesubscription: Subscription;

  constructor(private nativeBridgeAdapter: NativeBridgeAdapter,
              private nativeBridgeService: NativeBridgeService,
              private vanillaNativeAppService: NativeAppService,
              private vanillaAuthService: VanillaAuthService) {
  }

  attachNativeMessageNotifier(): void {
    if (this.vanillaNativeAppService.isNativeWrapper) {
      this.nativeEventObservablesubscription = this.nativeBridgeAdapter.nativeEventObservable.subscribe((event: NativeEvent) => {
        if (event) {
          switch (event.eventName) {
            case PortalNativeEvents.Login:
              this.vanillaAuthService.handleMobileAutoLogin(event);
              break;
            case PortalNativeEvents.OpenRegistrationScreen:
              this.vanillaAuthService.handleRegistrationRedirection();
              break;
            case PortalNativeEvents.CloseRegistrationScreen:
              this.nativeBridgeService.onClosePopup('Registration');
              break;
            case PortalNativeEvents.RegistrationScreenActive:
              this.nativeBridgeService.registrationStartedIfExist();
              this.vanillaAuthService.setAppsFlyerCookies();
              break;
            case PortalNativeEvents.RegistrationSuccessful:
              this.nativeBridgeService.registrationFinishedIfExist(event.parameters.accountId, event.parameters.password);
              this.nativeBridgeService.registrationFinishedSalesForce(`${BRAND_PREFIXES_CONSTANTS.PREFIX}${event.parameters.userName}`);
              break;
            case PortalNativeEvents.UpdatePassword:
              this.nativeBridgeService.passwordChangedIfExist(event.parameters.newPassword, event.parameters.username);
              break;
          }
        }
      });
    }
  }

  destroyNativeEventNotifierSubscription(): void {
    this.nativeEventObservablesubscription && this.nativeEventObservablesubscription.unsubscribe();
  }
}
