import { forkJoin, from as observableFrom, iif, of } from 'rxjs';

import { concatMap } from 'rxjs/operators';
import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import * as _ from 'underscore';

import { UserService } from '@core/services/user/user.service';
import { NativeBridgeService } from '@core/services/nativeBridge/native-bridge.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { DeviceService } from '@core/services/device/device.service';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { SessionService } from '@authModule/services/session/session.service';
import { AbstractOutletComponent } from '@shared/components/abstractOutlet/abstract-outlet.component';
import { ISystemConfig } from '@core/services/cms/models';
import { ISwitcherConfig } from '@core/models/switcher-config.model';
import { GtmService } from '@core/services/gtm/gtm.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { ArcUserService } from '@app/lazy-modules/arcUser/service/arcUser.service';
import { UserPreferenceProvider } from './user-settings.service';

@Component({
  selector: 'user-settings',
  templateUrl: './user-settings.component.html'
})
export class UserSettingsComponent extends AbstractOutletComponent implements OnInit {
  config: ISystemConfig;
  oddsFormat: string;
  touchIdLogin: string;
  allowQuickBetNotifications: boolean;
  quickBetNotificationObj: { status: boolean };
  switchers: ISwitcherConfig[];
  isAndroid: boolean;
  touchIDConfiguredShow: boolean;
  timelineObj: { status: boolean };
  showDiagnostics: boolean;
  isTabletOrDesktop: boolean;
  private readonly BETTING_SETTINGS: string = 'betting settings';
  private readonly TOGGLE_ON: string = 'toggle on';
  private readonly TOGGLE_OFF: string = 'toggle off';

  constructor(
    protected userService: UserService,
    protected nativeBridgeService: NativeBridgeService,
    protected pubSubService: PubSubService,
    protected deviceService: DeviceService,
    protected cms: CmsService,
    protected sessionService: SessionService,
    protected router: Router,
    protected gtmService: GtmService,
    protected locale: LocaleService,
    protected arcUserService: ArcUserService,
    protected upms: UserPreferenceProvider
  ) {
    super()/* istanbul ignore next */;
    this.isTabletOrDesktop = this.deviceService.isTablet || this.deviceService.isDesktop;
  }

  ngOnInit(): void {
    observableFrom(this.sessionService.whenSession()).pipe(
      concatMap(() => {
        return this.cms.getSystemConfig(true);
      }),
      concatMap(data =>
        iif(
          () => this.deviceService.isWrapper,
          forkJoin(of(data), this.cms.getFeatureConfig('NativeConfig',false, true)),
          of([data]))
      ))
      .subscribe(([config, nativeConfig]) => {
        this.config = config;
        this.config.NativeConfig = nativeConfig;
        this.setSetting();
        this.hideSpinner();
      }, () => {
        this.router.navigate(['/']);
      });
  }

  /**
   * Set initial settings
   * @param {Object} config
   */
  setSetting(): void {
    this.oddsFormat = this.userService.oddsFormat;
    this.touchIdLogin = this.userService.getTouchIdLogin();
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
   * Change odds for user
   * @params {string} settingValue
   */
  setOddsFormat(settingValue: string): void {
    if(this.oddsFormat === settingValue){return;}
    const preferenceData = {brand: '', oddPreference: settingValue};
    this.upms.setOddsPreference(preferenceData, this.userService.bppToken).subscribe((data) => {
      if(data && data.preferences){
        this.oddsFormat = data.preferences.oddPreference;
        this.userService.set({ oddsFormat: data.preferences.oddPreference });
      }
      this.pubSubService.publish(this.pubSubService.API.SET_ODDS_FORMAT, settingValue);
    })
  }

  /*
   * @description Change Touch ID login setting
   * This setting applicable only for native wrapper app
   * @params {string} settingValue // 'enabled' or 'disabled'
   */
  setTouchIdLogin(settingValue: string): void {
    this.touchIdLogin = settingValue;
    this.userService.setTouchIdLogin(settingValue);
    this.nativeBridgeService.touchIDSettingsUpdate(settingValue === 'enabled');
  }

  /**
   * Set quick bet notifications status into User object(Local storage)
   */
  changeQuickBetSetting(status: boolean): void {
    this.userService.set({ quickBetNotification: status });
  }

  sendReport(): void {
    this.nativeBridgeService.sendReport();
  }

  /**
   * Set timeline status into User object(Local storage)
   * status: boolean value
   */
  changeTimelineSetting(status: boolean): void {
    this.gtmService.push('trackEvent', {
      eventAction : this.BETTING_SETTINGS,
      eventCategory : this.locale.getString('bma.userSettingsTimeline').toLowerCase(),
      eventLabel: `${ status ? this.TOGGLE_ON : this.TOGGLE_OFF }`
    });
    this.userService.set({ timeline: status });
    this.pubSubService.publish(this.pubSubService.API.TIMELINE_SETTINGS_CHANGE);
  }
  /**
   * Check whether user is an Arc User and disable quickbet
   * @returns void
   */
  checkArcUser(): void {
    if (this.arcUserService.quickbet) {
      this.quickBetNotificationObj = { status: false };
    } else {
      this.quickBetNotificationObj = { status: this.userService.quickBetNotification };
    }
  }
}
