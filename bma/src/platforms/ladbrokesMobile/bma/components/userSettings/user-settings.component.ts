import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import * as _ from 'underscore';

import { UserSettingsComponent } from '@bma/components/userSettings/user-settings.component';
import { UserService } from '@core/services/user/user.service';
import { NativeBridgeService } from '@core/services/nativeBridge/native-bridge.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { DeviceService } from '@core/services/device/device.service';
import { CmsService } from '@ladbrokesMobile/core/services/cms/cms.service';
import { SessionService } from '@authModule/services/session/session.service';
import { GtmService } from '@core/services/gtm/gtm.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { ArcUserService } from '@app/lazy-modules/arcUser/service/arcUser.service';
import { UserPreferenceProvider } from '@app/bma/components/userSettings/user-settings.service';

@Component({
  selector: 'user-settings',
  templateUrl: './user-settings.component.html',
  styleUrls: ['./user-settings.component.scss']
})
export class LadbrokesUserSettingsComponent extends UserSettingsComponent implements OnInit {
  touchIdMap = {
    disabled: false,
    enabled: true
  };
  touchIdLoginLad: boolean;
  timelineObj: { status: boolean };
  constructor(
    userService: UserService,
    nativeBridgeService: NativeBridgeService,
    pubSubService: PubSubService,
    deviceService: DeviceService,
    cms: CmsService,
    sessionService: SessionService,
    router: Router,
    gtmService: GtmService,
    locale: LocaleService,
    arcUserService: ArcUserService,
    upms: UserPreferenceProvider
  ) {
    super(userService, nativeBridgeService, pubSubService, deviceService, cms, sessionService, router, gtmService, locale, arcUserService, upms);
  }

  /**
   * Set initial settings
   * @param {Object} config
   */
  setSetting(): void {
    this.oddsFormat = this.userService.oddsFormat;
    this.touchIdLoginLad = this.touchIdMap[this.userService.getTouchIdLogin()];
    this.allowQuickBetNotifications = this.config.quickBet && this.config.quickBet.EnableQuickBet;
    this.checkArcUser();
    this.timelineObj = { status: this.userService.timeline };

    this.switchers = [{
      name: 'bma.userSettingsOddsFormatFrac',
      onClick: type => this.setOddsFormat(type),
      viewByFilters: 'frac'
    }, {
      name: 'bma.userSettingsOddsFormatDec',
      onClick: type => this.setOddsFormat(type),
      viewByFilters: 'dec'
    }];

    if (this.deviceService.isWrapper) {
      // Checking if an Android application is in use
      this.isAndroid = this.deviceService.isAndroid;
      // to show Touch ID Login setting
      this.touchIDConfiguredShow = this.nativeBridgeService.touchIDConfigured;
      // show diagnostics button
      const os = this.deviceService.osName.toLowerCase();
      this.showDiagnostics = _.contains(this.config.NativeConfig.visibleDiagnosticsButton, os);
    }
  }

  /*
   * @description Change Touch ID login setting
   * This setting applicable only for native wrapper app
   * @params {string} settingValue // 'enabled' or 'disabled'
   */
  setTouchIdLoginLad(settingValue: boolean): void {
    this.touchIdLoginLad = settingValue;
    this.userService.setTouchIdLogin(settingValue ? 'enabled' : 'disabled');
    this.nativeBridgeService.touchIDSettingsUpdate(settingValue);
  }
}
