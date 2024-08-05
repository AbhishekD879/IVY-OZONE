import { ChangeDetectorRef, Component, OnInit, ViewChild } from '@angular/core';
import { Router } from '@angular/router';

import environment from '@environment/oxygenEnvConfig';

import { AbstractDialogComponent } from '@app/shared/components/oxygenDialogs/abstract-dialog';
import { DeviceService } from '@core/services/device/device.service';
import { GtmService } from '@app/core/services/gtm/gtm.service';
import { PubSubService } from '@app/core/services/communication/pubsub/pubsub.service';
import { TimeService } from '@app/core/services/time/time.service';
import { UserService } from '@app/core/services/user/user.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';

import { IDialogParams } from '@app/core/services/dialogService/dialog-params.model';
import { fanzoneRoutePath, SHOW_YOUR_COLORS } from '@app/fanzone/constants/fanzoneconstants';
import { fanzoneUserData, IDaysNotCompletedPopup, IThankYouPopup } from '@app/fanzone/models/fanzone-syc.model';
import { IFanzonePreferences } from '@app/fanzone/models/fanzone-preferences.model';
import { FanzoneSharedService } from '../../services/fanzone-shared.service';
import { FanzoneHelperService } from '@app/core/services/fanzone/fanzone-helper.service';
import { forkJoin, Observable } from 'rxjs';
import { map } from 'rxjs/internal/operators/map';
import { FanzoneStorageService } from '@app/core/services/fanzone/fanzone-storage.service';


@Component({
  selector: 'fanzone-select-your-team-dialog',
  templateUrl: './fanzone-select-your-team-dialog.component.html',
  styleUrls: ['./fanzone-select-your-team-dialog.component.scss']
})

export class FanzoneSelectYourTeamDialogComponent extends AbstractDialogComponent implements OnInit {

  @ViewChild('fanzoneSelectYourTeam', { static: true }) dialog;

  fanzonePopupData: IDialogParams;
  customTeamName: string = '';
  generic21stTeamName: string = '';
  thankYouPopup: boolean = false;
  customTeamNameError: boolean = false;
  userPreferencedata: fanzoneUserData = {};
  userJourneyCompletedData: fanzoneUserData;
  thankYouPopupData: IThankYouPopup;
  daysNotCompletedPopupData: IDaysNotCompletedPopup;
  preferences: IFanzonePreferences
  storageKey = 'fanzone';
  changeTeamTimePeriodMsg: string;
  interval: number;

  readonly CMS_UPLOADS_PATH: string = environment.CMS_ROOT_URI + environment.FIVEASIDE.svgImagePath;

  readonly tagName: string = SHOW_YOUR_COLORS.SYC_PAGE;

  constructor(
    protected device: DeviceService,
    protected gtmService: GtmService,
    protected fanzoneSharedService: FanzoneSharedService,
    protected pubSubService: PubSubService,
    protected router: Router,
    protected fanzoneStorageService: FanzoneStorageService,
    protected timeService: TimeService,
    protected userService: UserService,
    protected windowRef: WindowRefService,
    private changeDet: ChangeDetectorRef,
    protected fanzoneHelperService: FanzoneHelperService
  ) {
    super(device, windowRef);
  }

  /**
   * Method to execute on dialog open
   * returns {void}
   */
  open(): void {
    this.thankYouPopup = false;
    this.fanzonePopupData = { ...this.params };
    if (this.fanzonePopupData.teamId === SHOW_YOUR_COLORS.CUSTOM_TEAM_ID) {
      this.customTeamName = this.fanzonePopupData.teamName;
    }
    this.customTeamNameError = false;
    const { sycExitCTA, thankYouMsg, sycThankYouTitle, daysToChangeTeam, teamId } = this.fanzonePopupData;
    this.thankYouPopupData = {
      sycPopUpDescription: thankYouMsg,
      sycTitle: sycThankYouTitle,
      ctaSecondaryBtn: sycExitCTA,
      teamId: teamId,
      daysToChangeTeam: daysToChangeTeam
    }
    this.fanzoneHelperService.fanzoneTeamUpdate.subscribe(() => {
      this.changeOfTeamValidation();
    });
    this.fanzoneHelperService.selectedFanzoneUpdate.subscribe(() => {
      this.changeOfTeamValidation();
    })
    if ( !this.userService.status ) {
      super.open();
    } else if (this.userService.status && (this.fanzoneHelperService.fzDataAvailable || Object.keys(this.getUserData()).length)) {
      this.fanzoneHelperService.checkIfTeamIsRelegated().subscribe((isTeamRelegated) => {
        if (isTeamRelegated) {
          super.open();
        } else {
          this.changeOfTeamValidation();
        }
      });
    }
  }

  /**
   * Method to get time period change message
   * @returns observable string;
   */
  getTimePeriodChangeMessage(data: any, replaceKey: string): Observable<string> {
    const fanzoneInfo = this.fanzoneStorageService.get('fanzone');
    const subscriptionDate = fanzoneInfo && fanzoneInfo.subscriptionDate ? fanzoneInfo.subscriptionDate : '';
    return this.timeService.getHydraDaysDifference(subscriptionDate).pipe(map((date) => {
      if (fanzoneInfo && fanzoneInfo.subscriptionDate) {
        const remainingDays = this.fanzonePopupData.daysToChangeTeam - Math.floor(date);
        return data && data.replace(replaceKey, `<span class='font-weight-bold'>${remainingDays}</span>`);
      }
    }))
  }

  /**
   * Method to check if user data is available post login
   * @returns boolean
   */
  fzValidation(): boolean {
    if (!Object.keys(this.getUserData()).length || this.getUserData().hasOwnProperty('tempTeam')) {
      return false;
    }
    return true;
  }

  /**
   * Method to get change of team title
   * @param teamId - team id
   * @param sycTitle - title
   * @returns string
   */
  getChangeOfTeamTitle(teamId: string, sycTitle: string): string {
    return (teamId === SHOW_YOUR_COLORS.CUSTOM_TEAM_ID) ? sycTitle : SHOW_YOUR_COLORS.CHANGE_TEAM;
  }

  /**
   * Method to check team selection time exceeded
   */
  changeOfTeamValidation(): void {
    if (this.getUserData() && this.getUserData().isCustomResignedUser) {
      super.open();
      return;
    } 
    forkJoin({ userDaysExceeded: this.userSelectionDaysExceeded(), timePeriodChangeMsg: this.getTimePeriodChangeMessage(this.fanzonePopupData.changeTeamTimePeriodMsg, "${days}") }).subscribe((data) => {
      if (((this.userService.status && this.getUserData() &&
        ((this.getUserData().teamId && this.getUserData().teamId !== SHOW_YOUR_COLORS.CUSTOM_TEAM_ID) || (this.getUserData().teamId !== SHOW_YOUR_COLORS.CUSTOM_TEAM_ID && this.getUserData().isResignedUser)))
        && !data.userDaysExceeded)) {
        const { sycExitCTA, sycTitle, teamId } = this.fanzonePopupData;
        if (Object.keys(this.fanzonePopupData).length && sycExitCTA) {
          this.daysNotCompletedPopupData = {
            sycPopUpDescription: data.timePeriodChangeMsg,
            sycTitle: this.getChangeOfTeamTitle(teamId, sycTitle),
            ctaSecondaryBtn: sycExitCTA
          }
          this.thankYouPopup = true;
          this.fanzonePopupData = this.daysNotCompletedPopupData;
          super.open();
        }
      } else if(this.router.url.indexOf(`${fanzoneRoutePath}`) !== -1){
        super.open();
      }
    });
  }

  /**
   * Method to close dialog
   * returns {void}
   */
  closeDialog(): void {
    this.fanzonePopupData = {};
    super.closeDialog();
  }

  /**
   * Method to capture events in data layer
   * @param eventAction - button clicked
   * @param eventLabel - label
   */
  pushCachedEvents(eventLabel: string, teamName?: string, teamId?: string): void {
    const eventDetails = (teamId === SHOW_YOUR_COLORS.CUSTOM_TEAM_ID) ? this.customTeamName : teamName;
    const eventAction = (teamId === SHOW_YOUR_COLORS.CUSTOM_TEAM_ID) ? SHOW_YOUR_COLORS.GTA.FREE_TEXT_INPUT : SHOW_YOUR_COLORS.GTA.CONFIRMATION_SCREEN;
    const dataLayer = {
      event: SHOW_YOUR_COLORS.GTA.TRACK_EVENT,
      eventAction: eventAction,
      eventCategory: SHOW_YOUR_COLORS.GTA.SHOW_UR_COLORS,
      eventLabel: eventLabel,
      eventDetails: eventDetails ? eventDetails : null
    }
    this.gtmService.push(dataLayer.event, dataLayer)
  }

  /**
   * Method on Call to action 1 button click
   * @param ctaAction - message on  CTA button clicked 
   */
  ctaPrimaryBtnClick(ctaAction: string, teamName?: string, teamId?: string): void {
    if (ctaAction === SHOW_YOUR_COLORS.CTA_BUTTONS.SELECT_DIFFERENT_TEAM || ctaAction === SHOW_YOUR_COLORS.CTA_BUTTONS.EXIT) {
      this.pushCachedEvents(ctaAction, teamName, teamId);
      this.customTeamName = '';
      this.closeDialog();
    }
  }

  /**
   * Method on Call to action 2 button click
   * @param selectedTeam - tile selected
   * @param ctaAction - CTA button clicked
   * returns {void}
   */
  ctaSecondaryBtnClick(teamData: IDialogParams, ctaAction: string): void {
    this.customTeamNameError = false;
    this.pushCachedEvents(ctaAction, teamData.teamName, teamData.teamId);
    switch (ctaAction) {
      case SHOW_YOUR_COLORS.CTA_BUTTONS.EXIT:
        if (this.thankYouPopup && this.fanzonePopupData.teamId === SHOW_YOUR_COLORS.CUSTOM_TEAM_ID) {
          this.interval = this.windowRef.nativeWindow.setInterval(() =>{
            const route = this.fanzoneSharedService.getFanzoneRouteName(this.fanzoneHelperService.selectedFanzone);
            if (route) {
              this.router.navigateByUrl(`/fanzone/sport-football/${this.generic21stTeamName}/${route}`);
              this.interval && this.windowRef.nativeWindow.clearInterval(this.interval);
              this.closeDialog();
            }
          }, 1000);
          return;
        }
        this.closeDialog();
        break;
      case SHOW_YOUR_COLORS.CTA_BUTTONS.CONFIRM:
        if (teamData.teamId === SHOW_YOUR_COLORS.CUSTOM_TEAM_ID) {
          this.generic21stTeamName = teamData.genericTeamName;
          teamData.teamName = this.customTeamName;
          this.noSupportToTeam(teamData);
        } else {
          this.savePreferences(teamData);
        }
        break;
      case SHOW_YOUR_COLORS.CTA_BUTTONS.LOGIN:
        const selectedTeam = { teamId: teamData.teamId, teamName: this.customTeamName || teamData.teamName };
        if (teamData.teamId === SHOW_YOUR_COLORS.CUSTOM_TEAM_ID) { 
          selectedTeam["genericTeamName"] = teamData.genericTeamName;
        }
        this.fanzoneSharedService.appendToStorage({ tempTeam: selectedTeam });
        this.pubSubService.publish(this.pubSubService.API.OPEN_LOGIN_DIALOG, { moduleName: SHOW_YOUR_COLORS.FANZONE });
        break;
    }
  }

  /**
   * Method to execute when user selects i donot support any team tile for first time
   * @param selectedTeam - dialog params
   * returns {void}
   */
  noSupportToTeam(selectedTeam: IDialogParams): void {
    if (!this.checkIfTeamNameEntered(selectedTeam.teamId)) {
      this.thankYouPopup = true;
      this.fanzonePopupData = this.thankYouPopupData;
      this.savePreferences(selectedTeam);
    } else {
      this.customTeamNameError = true;
    }
  }

  /**
   * Method to save user selections
   * @param selectedTeam - selected team
   * returns {void}
   */
  savePreferences(selectedTeam): void {
    this.fanzoneSharedService.saveTeamOnPlatformOne(selectedTeam);
  }

  /**
   * get the user data
   * @returns {object} return user data stored in local storage or empty object
   * returns {void}
   */
  getUserData(): fanzoneUserData {
    return this.fanzoneStorageService.get(this.storageKey) || {};
  }

  /**
   * calculate the difference between user pref date and current date
   * @returns boolean observable
   */
  userSelectionDaysExceeded(): Observable<boolean> {
    return this.timeService.getHydraDaysDifference(this.getUserData().subscriptionDate).pipe(map((hydraDays) => {
      if (this.fanzonePopupData && this.fanzonePopupData.daysToChangeTeam && hydraDays && Math.ceil(hydraDays) > this.fanzonePopupData.daysToChangeTeam) {
        return true;
      }
      return false;
    }))
  }

  /**
   * Method to check if user entered a custom team name
   * @param selectedTeam - selected team
   * @returns boolean if a custom team name is entered
   */
  checkIfTeamNameEntered(selectedTeamId: string): boolean {
    return (!this.customTeamName.length && selectedTeamId === SHOW_YOUR_COLORS.CUSTOM_TEAM_ID) ? true : false;
  }

  /**
   * Method to update the custom team name
   * @param event - key up event
   * returns {void}
   */
  setCustomTeamName(event: Event): void {
    this.customTeamName = (event.target as HTMLButtonElement).value
    this.customTeamNameError = this.customTeamName.length ? false : true;
  }
}
