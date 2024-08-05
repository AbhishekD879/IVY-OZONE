import { Component, ElementRef, HostListener, ViewChild } from '@angular/core';
import { Router } from '@angular/router';
import { PlatformLocation } from '@angular/common';
import { forkJoin } from 'rxjs/internal/observable/forkJoin';
import { IDialogParams } from '@app/core/services/dialogService/dialog-params.model';
import * as fanzoneConst from '@lazy-modules/fanzone/fanzone.constant';
import environment from '@environment/oxygenEnvConfig';
import { AbstractDialogComponent } from '@shared/components/oxygenDialogs/abstract-dialog';
import { DeviceService } from '@core/services/device/device.service';
import { FanzoneSharedService } from '@app/lazy-modules/fanzone/services/fanzone-shared.service';
import { FanzoneStorageService } from '@app/core/services/fanzone/fanzone-storage.service';
import { TimeService } from '@app/core/services/time/time.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { ICmsEmailOptin, IEmailOptin } from '@app/lazy-modules/fanzone/models/fanzone-email-optin.model';
import { fanzoneEmailKey } from '@app/fanzone/constants/fanzoneconstants';

@Component({
  selector: 'fanzone-optin-email-dialog',
  templateUrl: './fanzone-optin-email-dialog.component.html',
  styleUrls: ['./fanzone-optin-email-dialog.component.scss']
})
export class FanzoneOptinEmailDialogComponent extends AbstractDialogComponent {
  @ViewChild('fanzoneOptinEmailDialog', { static: true }) dialog;
  fanzoneOptinCmsData: ICmsEmailOptin = {} as ICmsEmailOptin;
  optInData: IDialogParams;
  communicationUrl: string = environment.COMMUNICATION_URL;

  constructor(
    device: DeviceService,
    windowRef: WindowRefService,
    protected router: Router,
    protected fanzoneStorageService: FanzoneStorageService,
    protected fanzoneSharedService: FanzoneSharedService,
    private timeService: TimeService,
    private loc: PlatformLocation,
    private elementRef: ElementRef
  ) {
    super(device, windowRef);
    loc.onPopState(() => super.closeDialog());
  }

  @HostListener('document:click', ['$event'])
  @HostListener('document:touchend', ['$event'])
  clickOutside(event: MouseEvent): void {
    if (!this.elementRef.nativeElement.contains(event.target as HTMLElement)) {
      event.stopPropagation();
      super.closeDialog();
      this.fanzoneSharedService.showFanzoneGamesPopup(this.params.data.fanzoneDetailResponse);
    } 
  }

  /**
   * Open Optin Email dialog box
   * @returns void
   */
  open(): void {
    const fzOptinStorage = this.fanzoneStorageService.get(fanzoneEmailKey) || {};
    this.optInData = this.params.data;
    forkJoin({ optInCMSData: this.fanzoneSharedService.getFanzoneEmailOptin(), subscriptionDate: this.timeService.getHydraDaysDifference(fzOptinStorage.remindMeLaterPrefDate) }).subscribe((data) => {
      this.fanzoneOptinCmsData = data.optInCMSData[0];
      if (!this.optInData.email.selected && this.router && this.router.url && this.router.url.includes('fanzone')) {
        if (!(fzOptinStorage.remindMeLaterPrefDate) || (fzOptinStorage.remindMeLaterPrefDate && data.subscriptionDate && data.subscriptionDate > 0)) {
          super.open();
        } else {
          this.fanzoneSharedService.showFanzoneGamesPopup(this.optInData.fanzoneDetailResponse);
        }
      }
    });
  }

  /**
   * Method to save user selected details to platform when user clicks on remind me later / dont show me this again
   * @param request - details to be saved on platform
   */
  closePopupDialog(request: IEmailOptin): void {
    this.fanzoneSharedService.postEmailOptinDetails(request, true);
    if (this.device.isIos) {
      this.windowRef.document.body.classList.remove('ios-modal-opened');
      this.device.isWrapper && document.body.classList.remove('ios-modal-wrapper');
    }
    super.closeDialog();
    this.fanzoneSharedService.showFanzoneGamesPopup(this.optInData.fanzoneDetailResponse);
  }

  /**
   * Method to get remind me later count and days
   * @returns -IEmailRemindMeLater
   */
  getRemindMeLaterRequest(option: string): void {
    const fzOptinStorage = this.fanzoneStorageService.get(fanzoneEmailKey) || {};
    const rmlCount = fzOptinStorage && fzOptinStorage.remindMeLaterCount && (Number(fzOptinStorage.remindMeLaterCount) > 0) ? Number(fzOptinStorage.remindMeLaterCount) + 1 : 1;
    const rmlDays = Number(rmlCount) && Number(rmlCount) > 1 ? parseInt("30") : parseInt("14");
    const prefDays = (option === fanzoneConst.BUTTONS.dsme) ? this.fanzoneOptinCmsData && this.fanzoneOptinCmsData.seasonEndDate : this.fanzoneSharedService.addDaysToCurrentDate(rmlDays);
    Object.keys(fzOptinStorage).length && this.closePopupDialog({
      dontShowMeAgainPref: option === fanzoneConst.BUTTONS.dsme ? true : false,
      remindMeLaterPrefDate: `${this.timeService.formatByPattern(prefDays, 'yyyy-MM-ddTHH:mm:ss')}Z`,
      remindMeLaterCount: (option === fanzoneConst.BUTTONS.rml) ? rmlCount : fzOptinStorage.remindMeLaterCount
    });
  }

  /**
   * checks which of the three(Optin email, remin me later, don't show me again) is clicked by userphom
   * @param option - rml/dsme/optin
   */
  checkDialogButtonClick(option: string): void {
    switch (option) {
      case fanzoneConst.BUTTONS.optin:
        const location = this.windowRef.nativeWindow.location;
        const communicationPrefUrl = `${this.communicationUrl}${fanzoneConst.FZ_COMM_URL}${location.origin}${location.pathname}`;
        this.windowRef.nativeWindow.location.href = communicationPrefUrl;
        super.closeDialog();
        break;
      case fanzoneConst.BUTTONS.rml:
      case fanzoneConst.BUTTONS.dsme:
        this.getRemindMeLaterRequest(option);
        break;
      default:
        break;
    }
  }
}