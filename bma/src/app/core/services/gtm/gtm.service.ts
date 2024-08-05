import { Injectable } from '@angular/core';
import * as _ from 'underscore';
import environment from '@environment/oxygenEnvConfig';
import { PubSubService } from '../communication/pubsub/pubsub.service';
import { DeviceService } from '../device/device.service';
import { StorageService } from '../storage/storage.service';
import { UserService } from '@core/services/user/user.service';
import { WindowRefService } from '../windowRef/window-ref.service';
import { ITrackEvent } from './models';
import { BRANDS_MAP } from '@core/services/gtm/constans/brands.constant';
import { SessionStorageService } from '@core/services/storage/session-storage.service';
import { ISBbetslipGATracking } from '@app/quickbet/models/quickbet-common.model';

@Injectable()
export class GtmService {
  shopLocatorTrack: boolean = false;
  private platform: { 'signup-delivery-platform': string };
  private cachedEvents: {[key: string]: any} = [];
  sbTracking: string = 'SBTrackingData';
  constructor (
      private user: UserService,
      private device: DeviceService,
      private storage: StorageService,
      pubsub: PubSubService,
      private windowRef: WindowRefService,
      private sessionStorage: SessionStorageService,
    ) {
        this.platform = { 'signup-delivery-platform': this.device.deliveryPlatform };

        pubsub.subscribe('GTM', pubsub.API.SET_PLAYER_INFO, () => this.extendBmaData());
        pubsub.subscribe('GTM', pubsub.API.PUSH_TO_GTM, this.push.bind(this));
    }

    init(): void {
        this.windowRef.nativeWindow.gcData = {
            brand: BRANDS_MAP[environment.brand],
            userInterfaceName: 'Oxygen',
            signUpDeliveryPlatform: this.device.deliveryPlatform,
            userInterface: this.getUserInterface()
        };

        this.extendBmaData();
    }

    /**
     * Push data to the GTM container
     * @param {String} event
     * @param {Object} data
     */
    push<T>(event: string, data: T): void {
      const payload = _.extend({ event }, data);
      const dataLayer = this.windowRef.nativeWindow.dataLayer;

      if (dataLayer) {
        dataLayer.push(payload);
      } else {
        this.cachedEvents.push(payload);
      }
    }

    /**
     * Action on Bet Placement Error.
     * @param  {[Object]} data [data for google tag manager]
     */
    pushBetPlacementErrorInfo(data: any): void {
        _.extend(data, this.platform);
        this.push('bet_placement_error', data);
    }

    /**
     * Action when user logout.
     */
    pushLogoutInfo(): void {
        const gtmData = _.extend({ success: 'true' }, this.getUserIds(), this.platform);
        this.extendBmaData();
        this.push('logout', gtmData);
    }

    /**
     * Action on signup button click
     */
    signUpClick(): void {
        if (this.device.isMobile) {
            const signUpTrackEvent: ITrackEvent = {
                event: 'trackEvent',
                eventCategory: 'registration',
                eventAction: 'click',
                eventLabel: 'join now'
            };

            this.push(signUpTrackEvent.event, signUpTrackEvent);
        }
    }

    /**
     * Format errorMessage property
     * @param string
     * @returns {string}
     */
    formatErrorMessage(value: string): string {
        return value.replace(/(&nbsp;|<\/?[^>]+(>|$)|<br>|_|<br\/>|(?:\\[rn])+)/g, ' ')
            .replace(/\s\s+/g, ' ')
            .trim()
            .toLowerCase();
    }

    pushCachedEvents(): void {
      _.forEach(this.cachedEvents, (payload: {[key: string]: any}) => {
        this.windowRef.nativeWindow.dataLayer.push(payload);
      });
      this.cachedEvents = [];
    }

    /**
     * Return users id and profile id.
     * @return {Object | null} [User id and profile id]
     */
    private getUserIds(): { player_id: any, profile_id: any } {
        return {
            player_id: this.user.playerCode || null,
            profile_id: this.user.profileId || null
        };
    }

    private getUserInterface(): string {
        return this.device.deliveryPlatform === 'HTML5' ? 'HTML5' : 'Wrapped App';
    }

    private extendBmaData(): void {
        _.extend(this.windowRef.nativeWindow.gcData, {
            currency: this.user.currency || null,
            email: this.user.email || null,
            firstName: this.user.firstname || null,
            lastName: this.user.lastname || null,
            profileID: this.user.advertiser || null,
            postCode: this.user.postCode || null,
            username: this.user.username || null,
            vipLevel: this.user.vipLevel || null,
            loggedIn: !!this.user.username,
            convertibleUser: this.isConvertibleUser(),
            customerID: this.user.playerCode || null,
            loginID: this.user.sessionToken || null,
            region: this.user.countryCode || null,
            userType: this.getUserType()
        });
    }

    private isConvertibleUser(): boolean {
        return !this.storage.get('lastUsername') && !this.user.username;
    }

    private getUserType(): string {
        if (this.user.username) {
            return 'Logged in Customer';
        } else if (this.storage.get('lastUsername')) {
            return 'Browsing Customer';
        }
        return 'Visitor';
    }

  setSBTrackingData(trackingData: ISBbetslipGATracking) { // function handles the dimenstion94 for surfacebet GA Tracking
    if(!trackingData.GTMObject || !trackingData.GTMObject.betData
      || !trackingData.GTMObject.betData['dimension94']) {
      return false;
    }
    let dimensions = this.getSBTrackingData();
    if (dimensions.length > 0) {
      const index = dimensions.findIndex((res: ISBbetslipGATracking) => {
        return (res.outcomeId && res.outcomeId.length && trackingData.outcomeId && trackingData.outcomeId.length) 
        && res.outcomeId[0] === trackingData.outcomeId[0];
      });
      if (index > -1) {
        dimensions[index] = trackingData;
      } else {
        dimensions.push(trackingData)
      }
    } else {
      dimensions = [trackingData];
    }
    this.sessionStorage.set(this.sbTracking, dimensions);
  }

  getSBTrackingData() {
    return this.sessionStorage.get(this.sbTracking) || [];
  }

  removeSBTrackingItem(trackingData: ISBbetslipGATracking) {
    let dimensions = this.getSBTrackingData();
    if (dimensions.length) {
      dimensions = dimensions.filter(res => {
        return res.outcomeId[0] != trackingData.outcomeId[0]});
    }
    this.sessionStorage.set(this.sbTracking, dimensions);
  }
}
