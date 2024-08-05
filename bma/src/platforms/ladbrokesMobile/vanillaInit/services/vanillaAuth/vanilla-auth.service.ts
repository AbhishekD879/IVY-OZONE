import { Injectable, NgZone } from '@angular/core';
import { Router } from '@angular/router';

import { VanillaAuthService as AppVanillaAuthService  } from '@app/vanillaInit/services/vanillaAuth/vanilla-auth.service';
import {
  UserService as VanillaUserService,
  RememberMeService as RememberMeStatusService,
  AuthService as VanillaAuth,
  ClaimsService,
  LoginDialogService,
  LoginNavigationService
} from '@frontend/vanilla/core';
import { UserService } from '@coreModule/services/user/user.service';
import { NativeBridgeService } from '@coreModule/services/nativeBridge/native-bridge.service';
import { PubSubService } from '@coreModule/services/communication/pubsub/pubsub.service';
import { CoreToolsService } from '@coreModule/services/coreTools/core-tools.service';
import { FiltersService } from '@coreModule/services/filters/filters.service';
import { AfterLoginNotificationsService } from '@coreModule/services/afterLoginNotifications/after-login-notifications.service';
import { AuthService } from '@authModule/services/auth/auth.service';
import { VanillaFreebetsBadgeDynamicLoaderService } from '@platform/vanillaInit/services/vanillaFreeBets/vanilla-fb-badges-loader.service';
import { AccountUpgradeLinkService } from '@vanillaInitModule/services/accountUpgradeLink/account-upgrade-link.service';
import { NativeBridgeAdapter } from '@vanillaInitModule/services/NativeBridgeAdapter/nativebridge.adapter';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { StorageService } from '@core/services/storage/storage.service';
import { SessionService } from '@authModule/services/session/session.service';
import { ProxyHeadersService } from '@bpp/services/proxyHeaders/proxy-headers.service';
import { DeviceService } from '@core/services/device/device.service';
import { GermanSupportService } from '@core/services/germanSupport/german-support.service';
import { AWSFirehoseService } from '@lazy-modules/awsFirehose/service/aws-firehose.service';
import { BalancePropertiesService } from '@frontend/vanilla/features/balance-properties';
import { UserInterfaceClientConfig } from '@app/client-config/bma-user-interface-config';

@Injectable({
  providedIn: 'root'
})
export class VanillaAuthService extends AppVanillaAuthService {

  static ngInjectableDef = undefined;

  constructor(
     vanillaUser: VanillaUserService,
     user: UserService,
     nativeBridgeService: NativeBridgeService,
     awsService: AWSFirehoseService,
     pubsub: PubSubService,
     coreToolsService: CoreToolsService,
     filtersService: FiltersService,
     vanillaLoginDialogService: LoginDialogService,
     balanceService: BalancePropertiesService,
     afterLoginNotifications: AfterLoginNotificationsService,
     authService: AuthService,
     vanillaAuth: VanillaAuth,
     claimsService: ClaimsService,
     freeBetsBadgeLoader: VanillaFreebetsBadgeDynamicLoaderService,
     accountUpgradeLinkService: AccountUpgradeLinkService,
     nativeBridgeAdapter: NativeBridgeAdapter,
     storage: StorageService,
     windowRef: WindowRefService,
     router: Router,
     sessionService: SessionService,
     proxyHeadersService: ProxyHeadersService,
     device: DeviceService,
     rememberMeStatusService: RememberMeStatusService,
     navigationService: LoginNavigationService,
     userInterfaceConfig: UserInterfaceClientConfig,
     private germanSupportService: GermanSupportService,
     protected ngZone: NgZone
  ) {
    super(
      vanillaUser,
      user,
      nativeBridgeService,
      awsService,
      pubsub,
      coreToolsService,
      filtersService,
      vanillaLoginDialogService,
      balanceService,
      afterLoginNotifications,
      authService,
      vanillaAuth,
      claimsService,
      freeBetsBadgeLoader,
      accountUpgradeLinkService,
      nativeBridgeAdapter,
      storage,
      windowRef,
      router,
      sessionService,
      proxyHeadersService,
      device,
      rememberMeStatusService,
      navigationService,
      userInterfaceConfig,
      ngZone
    );
  }

  protected mapUserData(): void {
    super.mapUserData();
    this.storage.set('countryCode', this.vanillaUser.country);
  }

  protected login(): void {
    if(this.user.getPostLoginBonusSupValue()) {
      this.pubsub.publish(this.pubsub.API.INITIATE_RGY_CALL, true);
      this.pubsub.subscribe('authFactory', this.pubsub.API.RGY_DATA_LOADED, () =>
        this.loginFlow()
      );
    } else {
      this.loginFlow();
    }
  }

  protected loginFlow(): void {
    this.user.login(this.vanillaUser.ssoToken);
    this.user.resolveOpenApiAuth();
    this.authService.innerSessionLoggedIn.next(null);
    // redirect german user to main page
    this.germanSupportService.redirectToMainPageOnLogin();
    this.pubsub.publish(this.pubsub.API.LOGIN_PENDING, true);
    this.pubsub.publish(this.pubsub.API.SESSION_LOGIN, [{ User: this.user, options: {} }]);
  }
}
