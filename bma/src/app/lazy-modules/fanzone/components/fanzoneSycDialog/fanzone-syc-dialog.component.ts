import { Component, ViewChild } from '@angular/core';
import { AbstractDialogComponent } from '@shared/components/oxygenDialogs/abstract-dialog';
import { DeviceService } from '@core/services/device/device.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { UserService } from '@core/services/user/user.service';
import { Router } from '@angular/router';
import { IDialogParams } from '@app/core/services/dialogService/dialog-params.model';
import { TimeService } from '@app/core/services/time/time.service';
import * as fanzoneConst from '@lazy-modules/fanzone/fanzone.constant';
import { fanzoneUserData } from '@lazy-modules/fanzone/models/fanzone-syc.model';
import { GtmService } from '@app/core/services/gtm/gtm.service';
import { FanzoneSharedService } from '../../services/fanzone-shared.service';
import { SHOW_YOUR_COLORS } from '@app/fanzone/constants/fanzoneconstants';
import { forkJoin } from 'rxjs';
import { FanzoneStorageService } from '@app/core/services/fanzone/fanzone-storage.service';

@Component({
  selector: 'fanzone-syc-dialog',
  templateUrl: './fanzone-syc-dialog.component.html',
  styleUrls: ['./fanzone-syc-dialog.component.scss']
})

export class FanzoneSycDialogComponent extends AbstractDialogComponent {
  @ViewChild('fanzoneSycDialog', { static: true }) dialog;
  date: any;
  fanzonePopupData: IDialogParams;
  isImInClicked: boolean = false;
  isRemindMeLaterClicked: boolean = false;
  isDontShowMeAgainClicked: boolean = false;
  daysToChangeTeam: number;
  remindMeLaterDaysLeft: number;
  userKey: string = `setDate-${this.userService.username}`;
  readonly storageKey: string = fanzoneConst.storageKeyValue;
  data: fanzoneUserData = {};
  subscriptionTime: number;
  isRelegated?: boolean = false;
  gtmData = {
    event: fanzoneConst.GTM_DATA.TRACKEVENT,
    eventAction: fanzoneConst.GTM_DATA.EVENTACTION,
    eventCategory: fanzoneConst.GTM_DATA.EVENTCATEGORY,
    eventLabel: fanzoneConst.GTM_DATA.EVENTLABEL
  };

  constructor(
    device: DeviceService,
    windowRef: WindowRefService,
    private fanzoneStorageService: FanzoneStorageService,
    private userService: UserService,
    private router: Router,
    private timeService: TimeService,
    private gtmService: GtmService,
    private fanzoneSharedService: FanzoneSharedService,
  ) {
    super(device, windowRef);
  }

  /**
   * open SYC dialog box
   * @returns void
   */
  open(): void {
    this.fanzonePopupData = this.params;
    this.fanzoneSharedService.checkIfTeamIsRelegated().subscribe((teamRelegated: boolean) => {
      const fzStorage = this.fanzoneStorageService.get('fanzone');
      if (teamRelegated && fzStorage && Object.keys(fzStorage).length && fzStorage.teamId) {
        this.fetchRelegatedTeamInfo(fzStorage);
      } else if (fzStorage && fzStorage.isCustomResignedUser  && !fzStorage.hasOwnProperty('showSYCPopupOn')) {
        super.open();
      } else {
        this.fetchSYCInfo();
      }
    });
  }

  /**
   * Method to display SYC popup to a first time user
   */
  fetchSYCInfo(): void {
    const userData = this.getUserData() || {};
    if (userData.teamId && userData.teamId === SHOW_YOUR_COLORS.CUSTOM_TEAM_ID) {
      this.subscriptionTime = parseInt(this.fanzonePopupData.remindLaterHideDays);
      userData.showSYCPopupOn = this.fanzoneSharedService.addDaysToDate(userData.subscriptionDate, this.subscriptionTime);
    }
    forkJoin({ subscriptionDate: this.timeService.getHydraDaysDifference(userData.subscriptionDate), showSYCPopupOn: this.timeService.getHydraDaysDifference(userData.showSYCPopupOn) }).subscribe((data) => {
      if (!Object.keys(userData).length || (Object.keys(userData).length &&
        (
          (
            ((userData.isFanzoneExists === false && !userData.isResignedUser) ||
              (userData.isResignedUser && (data.subscriptionDate > this.fanzonePopupData.daysToChangeTeam))
            ) &&
            (!userData.showSYCPopupOn || (userData.showSYCPopupOn && data.showSYCPopupOn > 0))
          ) ||
          (((userData.teamId && userData.teamId === SHOW_YOUR_COLORS.CUSTOM_TEAM_ID) ||
            (!userData.teamId)) && userData.showSYCPopupOn && data.showSYCPopupOn > 0)
        )
      )) {
        this.gtmService.push(this.gtmData.event, this.gtmData);
        super.open();
      }
    })
  }

  /**
   * Method to display relegated popup to user
   */
  fetchRelegatedTeamInfo(fzStorage): void {
    this.fanzoneSharedService.isFanzoneConfigDisabled().subscribe((isFzConfigDisabled: boolean) => {
      if(!isFzConfigDisabled) {
        this.isRelegated = true;
        if (fzStorage && fzStorage.isFanzoneTeamRelegated && fzStorage.showRelegatedPopupOn && fzStorage.showRelegatedPopupOn.length) {
          this.timeService.getHydraDaysDifference(fzStorage.showRelegatedPopupOn).subscribe((daysDiff) => {
            if (daysDiff > 0) {
              this.gtmService.push(this.gtmData.event, this.gtmData);
              super.open();
            }
          })
        }
        else {
          this.gtmService.push(this.gtmData.event, this.gtmData);
          super.open();
        }
      }
    })
  }

  /**
   * checks which of the three(i'm in,remin me later,don't show me again) is clicked by userphom
   * @param {string} buttonClickValue 
   * @returns boolean
   */
  checkDialogButtonClick(buttonClickValue: string) {
    const gtmDataButtonClick = {
      event: fanzoneConst.GTM_DATA.TRACKEVENT,
      eventAction: buttonClickValue === fanzoneConst.IMIN ? "I'M IN" : buttonClickValue,
      eventCategory: fanzoneConst.GTM_DATA.EVENTCATEGORY,
      eventLabel: fanzoneConst.GTM_DATA.EVENTLABEL
    };
    this.gtmService.push(gtmDataButtonClick.event, gtmDataButtonClick);
    switch (buttonClickValue) {
      case fanzoneConst.IMIN:
        this.isImInClicked = true;
        break;
      case fanzoneConst.RemindMeLater:
        this.isRemindMeLaterClicked = true;
        break;
      case fanzoneConst.DontShowMeAgain:
        this.isDontShowMeAgainClicked = true;
        break;
    }
    this.closeSYCDialog();
  }

  /**
   * get the user data
   * @returns {object} return user data stored in local storage or empty object
   */
  getUserData(): fanzoneUserData {
    return this.fanzoneStorageService.get(this.storageKey) || {};
  }

  /**
    * save user preference/navigate and close the dialog
    * @returns void
    */
  closeSYCDialog(): void {
    if (!!this.userService.username) {
      if (this.isRemindMeLaterClicked) {
        const remindMeLaterDate = this.fanzoneSharedService.addDaysToCurrentDate(parseInt(this.params.remindLaterHideDays));
        const showPopupOn = this.isRelegated ? { isFanzoneTeamRelegated: true, showRelegatedPopupOn: remindMeLaterDate } : { ...this.getUserData(), showSYCPopupOn: remindMeLaterDate };
        this.fanzoneStorageService.set('fanzone', showPopupOn);
      } else if (this.isDontShowMeAgainClicked) {
        const showPopupOn = this.isRelegated ? { isFanzoneTeamRelegated: true, showRelegatedPopupOn: this.params.seasonEndDate } : { ...this.getUserData(), showSYCPopupOn: this.params.seasonEndDate };
        this.fanzoneStorageService.set('fanzone', showPopupOn);
      } else if (this.isImInClicked) {
        this.router.navigate(['/fanzone/sport-football/show-your-colours']);
      }
    }
    super.closeDialog();
  }
}
