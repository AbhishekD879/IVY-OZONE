import { Component, OnInit, OnDestroy, ChangeDetectorRef } from '@angular/core';
import { Router } from '@angular/router';

import { DynamicLoaderService } from '@app/dynamicLoader/dynamic-loader.service';
import { CmsService } from '@coreModule/services/cms/cms.service';

import { PubSubService } from '@app/core/services/communication/pubsub/pubsub.service';
import { ISiteCoreTeaserFromServer } from '@app/core/models/aem-banners-section.model';
import { VanillaApiService } from '@frontend/vanilla/core';
import { Observable } from 'rxjs';
import { FanzoneHelperService } from '@app/core/services/fanzone/fanzone-helper.service';
import { FANZONE, pubSubChannelName } from '@app/fanzone/constants/fanzoneconstants';
import { UserService } from '@app/core/services/user/user.service';
import * as fanzoneConst from '@lazy-modules/fanzone/fanzone.constant';
import { GtmService } from '@app/core/services/gtm/gtm.service';
import { DeviceService } from '@frontend/vanilla/core';
import { FanzoneStorageService } from '@app/core/services/fanzone/fanzone-storage.service';

@Component({
  selector: 'fanzone-banner-entry',
  templateUrl: './fanzone-banner-entry.component.html',
  styleUrls: ['./fanzone-banner-entry.component.scss']
})

export class FanzoneBannerComponent implements OnInit, OnDestroy {
  isFootballPage: boolean = false;
  fanzoneName: string;
  isFanzoneEnabled: boolean = false;
  siteCoreFanzone: ISiteCoreTeaserFromServer[];
  fanzoneBannerImage: string;
  fanzoneRoutingUrl: string;
  readonly PATH: string = FANZONE.desktopPath;
  channelName: string = pubSubChannelName;
  gtmData = {
    event: fanzoneConst.GTM_DATA_FZ_BANNER.TRACKEVENT,
    eventAction: fanzoneConst.GTM_DATA_FZ_BANNER.EVENT_ACTION_FZ_ENTRY,
    eventCategory: fanzoneConst.GTM_DATA_FZ_BANNER.EVENTCATEGORY,
    eventLabel: fanzoneConst.GTM_DATA_FZ_BANNER.EVENTLABEL,
    eventDetails: fanzoneConst.GTM_DATA_FZ_BANNER.EVENT_DETAILS
  };

  constructor(
    protected router: Router,
    protected cmsService: CmsService,
    protected dynamicComponentLoader: DynamicLoaderService,
    protected pubSubService: PubSubService,
    protected user: UserService,
    protected vanillaApiService: VanillaApiService,
    protected fanzoneHelperService: FanzoneHelperService,
    protected gtmService: GtmService,
    protected fanzoneStorageService: FanzoneStorageService,
    private cdRef: ChangeDetectorRef,
    protected device: DeviceService
  ) {
    this.fanzoneHelperService.getSelectedFzUpdate().subscribe(() => {
     this.fanzoneHelperService.selectedFanzone && this.checkIfFanzoneEnabled(this.fanzoneHelperService.selectedFanzone);
    });
 }

  ngOnInit() {
   this.fanzoneHelperService.selectedFanzone && this.checkIfFanzoneEnabled(this.fanzoneHelperService.selectedFanzone);
    this.pubSubService.subscribe(this.channelName, [this.pubSubService.API.SESSION_LOGIN], () => {
      this.fanzoneHelperService.getSelectedFzUpdate().subscribe(() => {
      this.fanzoneHelperService.selectedFanzone && this.checkIfFanzoneEnabled(this.fanzoneHelperService.selectedFanzone);
      });
    });
    this.cdRef.detectChanges();
  }

  /**
    * This method is used to check if Fanzone is enabled
    * @returns {void}
  */
  checkIfFanzoneEnabled(fanzone): void {
    const fanzoneStorage = this.fanzoneStorageService.get('fanzone');
    const [baseURL] = this.router.url.split('?');
    const isHomePage = (baseURL === '/') || (baseURL === '/home/featured');
    const isFootballPage = baseURL.includes('/sport/football/matches') || baseURL === '/sport/football';
    const showFanzoneBanner = isHomePage && fanzone.fanzoneConfiguration.homePage || isFootballPage && fanzone.fanzoneConfiguration.footballHome;
    if (fanzoneStorage && fanzoneStorage.teamId && fanzone && fanzone.active && showFanzoneBanner) {
      this.isFanzoneEnabled = true;
      this.cdRef.detectChanges();
      this.gtmData.eventDetails = fanzone.name;
      this.gtmService.push(this.gtmData.event,this.gtmData);
      this.fanzoneName = fanzone.name;
      this.fanzoneRoutingUrl = `/fanzone/sport-football/${this.fanzoneName}/${this.cmsService.getFanzoneRouteName(fanzone)}`;
      const bannerUrl = this.device.isMobile && !this.device.isTablet ? fanzone.launchBannerUrl : fanzone.fanzoneConfiguration.launchBannerUrlDesktop;
      this.getFanzoneBanner(bannerUrl);
    }
  }

  /**
   * fetch entry point banner
   * @return {void}
   */
  getFanzoneBanner(bannerUrl: string): void {
    this.getFanzoneBannerFromSiteCore().subscribe((response) => {
      if (response.length > 0) {
        const [teaserResponse] = response;
        this.siteCoreFanzone = teaserResponse.teasers ?? [];
        this.siteCoreFanzone.forEach((data) => {
          if (data.itemId === bannerUrl) {
            this.fanzoneBannerImage = data.backgroundImage.src;
          }
        });
        this.cdRef.detectChanges();
      }
    });
  }

  /**
   * fetch entry point banner from sitecore
   * @return {void}
   */
  getFanzoneBannerFromSiteCore(): Observable<any> {
    const APIOPTIONS: {
      [name: string]: string;
    } = {
      'prefix': '/en/coralsports'
    };
    return this.vanillaApiService.get(this.PATH, '', APIOPTIONS);
  }

  /**
   * push the data to gtm when i m in button clicked by user
   * @param fanzoneName {string}
   * @returns {any}
  */
  iMInClicked(fanzoneName: string): void {
    this.gtmData.eventLabel = 'click';
    this.gtmData.eventDetails = fanzoneName;
    this.gtmService.push(this.gtmData.event, this.gtmData);
  }

  ngOnDestroy() {
    this.pubSubService.unsubscribe(this.channelName);
  }
}
