import { Component, Inject, ViewChild } from '@angular/core';
import { PlatformLocation } from '@angular/common';
import { Router } from '@angular/router';
import { MAT_LEGACY_DIALOG_DATA as MAT_DIALOG_DATA } from '@angular/material/legacy-dialog';
import { DeviceService } from '@core/services/device/device.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { AbstractDialogComponent } from '@shared/components/oxygenDialogs/abstract-dialog';
import { FreeRideOverlayComponent } from '@lazy-modules/freeRide/components/free-ride-overlay/free-ride-overlay.component';
import { FreeRideService } from '@lazy-modules/freeRide/services/freeRide.service';
import { IFreeRideCampaign, IOverlayData, ISplashPage } from '@lazy-modules/freeRide/models/free-ride';
import { FREE_RIDE_CONSTS, FREE_RIDE_DIALOG_CONSTS } from '@lazy-modules/freeRide/constants/free-ride-constants';
import environment from '@environment/oxygenEnvConfig';

@Component({
  selector: 'splash-popup',
  templateUrl: './splash-popup.component.html',
  styleUrls: ['splash-popup.component.scss']
})

export class SplashPopupComponent extends AbstractDialogComponent {
  @ViewChild('dialog', { static: true }) dialog: any;
  @ViewChild(FreeRideOverlayComponent) freeRide: FreeRideOverlayComponent;
  @Inject(MAT_DIALOG_DATA) public data: any;

  freeRideOverlay: HTMLElement;
  splashImg: string;
  freeRideImg: string;
  freeBetToken: string;
  isSoundChecked: boolean = true;
  splashInfo: ISplashPage;
  campaign: IFreeRideCampaign;
  FREERIDECONSTS = FREE_RIDE_CONSTS;
  cmsUri: string = environment.CMS_ROOT_URI;
  overLayFlag: boolean;
  campaignData: IOverlayData;

  constructor(
    device: DeviceService,
    windowRef: WindowRefService,
    loc: PlatformLocation,
    protected router: Router,
    public freeRideService: FreeRideService,
  ) {
    super(device, windowRef);
    loc.onPopState(() => this.closeSplashDialog());
  }

  /**
   * to open splash popup
   * @returns {void}
   */
  public open(): void {
    this.freeRideService.sendGTM('load', null);
    this.dialog.closeOnOutsideClick = false;
    super.open();
    this.windowRef.document.body.classList.add(FREE_RIDE_DIALOG_CONSTS.SPLASHPOPUP_MODEL_OPEN);
    ({ campaginDetails: this.campaign, splashInfo: this.splashInfo, freeBetToken: this.freeBetToken } = this.params.data);
    this.freeRideImg = `${this.cmsUri}${this.splashInfo.freeRideLogoUrl}`;
    this.splashImg = `${this.cmsUri}${this.splashInfo.splashImageUrl}`;
  }

  /**
   * to update value of checkbox
   * @param {boolean} value
   * @returns {void}
   */
  public toggle(value: boolean): void {
    this.isSoundChecked = !value;
    const eventLabel = this.isSoundChecked ? 'toggle on' : 'toggle off';
    this.freeRideService.sendGTM('overlay', eventLabel);
  }

  /**
   * to close splash popup and open overlay
   * @returns {void}
   */
  public goToFreeRideOverlay(): void {
    this.windowRef.document.body.classList.remove(FREE_RIDE_DIALOG_CONSTS.SPLASHPOPUP_MODEL_OPEN);
    super.closeDialog();
    this.freeRideOverlay = this.windowRef.document.querySelector(FREE_RIDE_CONSTS.FREE_RIDE_OVERLAY);
    this.overLayFlag = true;
    this.campaignData = {
      isSoundChecked: this.isSoundChecked,
      campaignInfo: this.campaign,
      splashInfo: this.splashInfo,
      freeBetToken: this.freeBetToken
    };
    this.freeRideService.sendGTM('overlay', this.splashInfo.buttonText);
  }

  freeRideClose() {
    this.overLayFlag = false;
    this.params.data.callClose(this.overLayFlag);
  }

  /**
   * to close splash popup
   * @returns {void}
   */
  public closeSplashDialog(): void {
    this.freeRideService.sendGTM('overlay', 'exit');
    this.params.data.callClose(false);
    super.closeDialog();
  }
}
