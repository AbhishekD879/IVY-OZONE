import { ChangeDetectorRef, Component, ComponentFactoryResolver, OnDestroy, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { forkJoin } from "rxjs";

import environment from '@environment/oxygenEnvConfig';

import { FanzoneSelectYourTeamDialogComponent } from '@app/lazy-modules/fanzone/components/fanzoneSelectYourTeamDialog/fanzone-select-your-team-dialog.component';

import { CmsService } from '@app/core/services/cms/cms.service';
import { DeviceService } from '@app/core/services/device/device.service';
import { DialogService } from '@app/core/services/dialogService/dialog.service';
import { FanzoneSharedService } from '@app/lazy-modules/fanzone/services/fanzone-shared.service';
import { GtmService } from '@app/core/services/gtm/gtm.service';
import { LocaleService } from '@app/core/services/locale/locale.service';
import { PubSubService } from '@app/core/services/communication/pubsub/pubsub.service';
import { StorageService } from '@app/core/services/storage/storage.service';
import { UserService } from '@app/core/services/user/user.service';

import { IFanzoneSyc } from '@app/fanzone/models/fanzone-syc.model';
import { fanzone, SHOW_YOUR_COLORS, userData } from '@app/fanzone/constants/fanzoneconstants';
import { FanzoneDetails } from '@app/fanzone/models/fanzone.model';
import { ITeamAsset } from '@app/lazy-modules/fanzone/models/fanzone-team-asset.model';
import { RoutingState } from '@sharedModule/services/routingState/routing-state.service';
import { TimeService } from '@app/core/services/time/time.service';
import { FanzoneStorageService } from '@app/core/services/fanzone/fanzone-storage.service';

@Component({
  selector: 'fanzone-select-your-team',
  templateUrl: './fanzone-select-your-team.component.html'
})
export class FanzoneSelectYourTeamAppComponent implements OnInit, OnDestroy {

  currentlyClickedCardIndex: number;
  assets: string[] = [];
  ctrlName: string = SHOW_YOUR_COLORS.FANZONE;
  customTeam: string = '';
  genericTeamName: string = '';
  fanzoneData: FanzoneDetails[] = [];
  fanzonePopupData: IFanzoneSyc;
  iDonotSupportAnyTeam: string;
  isUserLoggedIn: boolean = false;
  noTeamSupport: boolean = false;
  colorsData: ITeamAsset[];

  readonly storageKey = SHOW_YOUR_COLORS.FANZONE_SYT_POPUP;
  readonly CMS_UPLOADS_PATH: string = environment.CMS_ROOT_URI + environment.FIVEASIDE.svgImagePath;

  constructor(
    protected cmsService: CmsService,
    protected componentFactoryResolver: ComponentFactoryResolver,
    protected deviceService: DeviceService,
    protected dialogService: DialogService,
    protected fanzoneSharedService: FanzoneSharedService,
    protected gtmService: GtmService,
    protected localeService: LocaleService,
    protected pubSubService: PubSubService,
    protected route: Router,
    protected routingState: RoutingState,
    protected storageService: StorageService,
    protected userService: UserService,
    protected timeService: TimeService,
    protected changeDetectorRef: ChangeDetectorRef,
    protected fanzoneStorageService: FanzoneStorageService) {
  }

  ngOnInit(): void {
    this.iDonotSupportAnyTeam = this.localeService.getString('app.iDonotSupportAnyTeam');
    this.isUserLoggedIn = this.userService.status;
    this.getPopupData();
    // When user logs in post team / no team to support selected
    this.pubSubService.subscribe(this.ctrlName,
      [
        this.pubSubService.API.SUCCESSFUL_LOGIN, this.pubSubService.API.SESSION_LOGIN
      ], () => {
        this.getPreLoginInfo();
      }
    );
  }

  /**
   * Method to get temp team info selected by user pre-login
   */
  private getPreLoginInfo() {
    this.isUserLoggedIn = this.userService.status;
    const teamSelection = JSON.parse(JSON.stringify(this.fanzoneStorageService.get(this.storageKey)));
    if (teamSelection) {
      if (teamSelection.teamId) {
        this.teamJourneyAlreadyFinished(teamSelection.teamId);
      }
      if (teamSelection.tempTeam && teamSelection.tempTeam.teamId && teamSelection.tempTeam.teamId === SHOW_YOUR_COLORS.CUSTOM_TEAM_ID) {
        this.customTeam = teamSelection.tempTeam.teamName;
        this.genericTeamName = teamSelection.tempTeam.genericTeamName;
        delete teamSelection.tempTeam;
        this.fanzoneStorageService.set(fanzone, teamSelection);
        this.onNoTeamSupportSelection(this.genericTeamName);
      } else if (teamSelection.tempTeam && teamSelection.tempTeam.teamId) {
        this.getTeamDetails(teamSelection.tempTeam.teamName);
      }
    }
  }

  /**
   * Method to highlight prevous journey selected team
   * @param teamId - team id
   */
  teamJourneyAlreadyFinished(id) {
    if (id === SHOW_YOUR_COLORS.CUSTOM_TEAM_ID) {
      this.noTeamSupport = true;
      this.currentlyClickedCardIndex = undefined;
    } else {
      this.fanzoneData.forEach((team, index) => {
        if (team.teamId && team.teamId === id) {
          this.currentlyClickedCardIndex = index;
          this.noTeamSupport = false;
        }
      })
    }
    this.changeDetectorRef.detectChanges();
  }

  /**
   * Method to get the show your colors information from CMS
   * returns {void}
   */
  getPopupData(): void {
    forkJoin({ fzData: this.fanzoneSharedService.getSpecialPagesDataCollection(), fanzoneDetail: this.cmsService.getFanzone() }).subscribe((data) => {
      const [first] = data.fzData;
      this.fanzonePopupData = first;
      this.fanzoneData = data.fanzoneDetail.filter(fanzoneDet => fanzoneDet.active);
      data.fanzoneDetail.forEach((fanzoneAssetObj) => {
        if (fanzoneAssetObj.assetManagementLink) {
          this.assets.push(fanzoneAssetObj.assetManagementLink);
        }
      })
      if (this.checkIfUserLoginFirstTime()) {
        this.getPreLoginInfo();
      }
      const SYCPreviousData = JSON.parse(JSON.stringify(this.fanzoneStorageService.get(this.storageKey)));
      if (this.isUserLoggedIn && SYCPreviousData) {
        this.teamJourneyAlreadyFinished(SYCPreviousData.teamId);
      }
      this.cmsService.getTeamsColors(this.assets, SHOW_YOUR_COLORS.FOOTBALL_SPORT_ID).subscribe((colorInfo: ITeamAsset[]) => {
        this.colorsData = colorInfo;
        this.getAssetData();
      });
    });
  }

  /**
   * Method to check if user logged in for first
   * @returns - boolean
   */
  checkIfUserLoginFirstTime(): boolean {
    return this.storageService.get(userData) && this.storageService.get(userData).firstLogin;
  }

  /**
   * Method to get the selected team index before login
   * @param teamAsset - name of the selected team
   * returns {void}
   */
  getTeamDetails(teamAssetName: string): void {
    this.fanzoneData.forEach((team, index) => {
      if (team.name === teamAssetName) {
        this.onTeamSelection(team, index);
      }
    })
  }

  /**
   * Method to get the associated team for fanzones
   * returns {void}
   */
  getAssetData(): void {
    this.fanzoneData.forEach((fanzoneAsset: FanzoneDetails) => {
      this.colorsData.forEach((team: ITeamAsset) => {
        if (fanzoneAsset.assetManagementLink.toUpperCase() === team.teamName.toUpperCase()) {
          fanzoneAsset.asset = team;
        }
      })
    });
  }

  /**
   * Method to capture events in data layer
   * @param eventAction - button clicked
   * @param eventLabel - label
   */
  pushCachedEvents(eventAction: string, eventLabel: string): void {
    const dataLayer = {
      event: SHOW_YOUR_COLORS.GTA.TRACK_EVENT,
      eventAction: eventAction,
      eventCategory: SHOW_YOUR_COLORS.GTA.SHOW_UR_COLORS,
      eventLabel: eventLabel
    }
    this.gtmService.push(dataLayer.event, dataLayer)
  }



  /**
   * Method to get the popup description for desktop
   * @param teamName : name of team
   * @returns string;
   */
  getPopupDescriptionForDesktop(stringToReplace: string, teamName: string, days: number): string {
    return stringToReplace.replace("${team}", `<span class='font-weight-bold'>${teamName}</span>`).replace("${days}", `<span class='font-weight-bold'>${days}</span>`);
  }


  /**
   * Method to open team selected dialog
   * @param selectedTeam - selected fanzone team
   * @param index - index of selected team
   * returns {void}
   */
  onTeamSelection(selectedTeam: FanzoneDetails, index?: number): void {
    this.currentlyClickedCardIndex = index;
    this.noTeamSupport = false;
    this.changeDetectorRef.detectChanges();
    const { sycConfirmTitle, sycChangeCTA, sycLoginCTA, sycExitCTA, sycConfirmCTA, sycConfirmMsgDesktop, sycConfirmMsgMobile, sycPreLoginTeamSelectionMsg, daysToChangeTeam, changeTeamTimePeriodMsg } = this.fanzonePopupData;
    const msgDesktop = this.getPopupDescriptionForDesktop(sycConfirmMsgDesktop, selectedTeam.name, daysToChangeTeam);
    const msgMobile = this.getPopupDescriptionForDesktop(sycConfirmMsgMobile, selectedTeam.name, daysToChangeTeam);
    const selectedTeamData = {
      sycTitle: sycConfirmTitle,
      ctaPrimaryBtn: this.getMessageUserLogin(sycChangeCTA.toUpperCase(), sycExitCTA.toUpperCase()),
      ctaSecondaryBtn: this.getMessageUserLogin(sycConfirmCTA.toUpperCase(), sycLoginCTA.toUpperCase()),
      sycTeam: selectedTeam,
      sycPopUpDescription: this.getMessageUserLoginDevice(msgDesktop, msgMobile, sycPreLoginTeamSelectionMsg),
      teamName: selectedTeam.name,
      changeTeamTimePeriodMsg: changeTeamTimePeriodMsg,
      sycExitCTA: sycExitCTA,
      teamId: selectedTeam.teamId,
      daysToChangeTeam: daysToChangeTeam
    }
    const teamSelection = JSON.parse(JSON.stringify(this.fanzoneStorageService.get(this.storageKey)));
    if (teamSelection && teamSelection.tempTeam) {
      delete teamSelection.tempTeam;
      this.fanzoneStorageService.set(fanzone, teamSelection);
    }
    this.pushCachedEvents(SHOW_YOUR_COLORS.GTA.SELECT, selectedTeam.name);
    this.dialogService.openDialog(SHOW_YOUR_COLORS.DIALOG_NAME.TEAM_CONFIRMATION, this.componentFactoryResolver.resolveComponentFactory(FanzoneSelectYourTeamDialogComponent), true, selectedTeamData);
  }

  /**
   * Method to get messages based on user login status and device
   * @param msgDesktop - popup text message for desktop
   * @param sycConfirmMsgMobile -  popup text message for mobile
   * @param sycPreLoginTeamSelectionMsg - popup text message when user not logged in
   * @returns- string
   */
  getMessageUserLoginDevice(msgDesktop: string, sycConfirmMsgMobile: string, sycPreLoginTeamSelectionMsg: string): string {
    return this.isUserLoggedIn ? this.deviceService.isDesktop ? msgDesktop : sycConfirmMsgMobile : sycPreLoginTeamSelectionMsg;
  }

  /**
   * Method to get messages based on user login status
   * @param text1 - user message when logged in
   * @param text2 - user message when not logged in
   * @returns string
   */
  getMessageUserLogin(text1: string, text2: string): string {
    return this.isUserLoggedIn ? text1 : text2;
  }

  /**
   * Method to open dialog when user selects i dont support any team tile
   * returns {void}
   */
  onNoTeamSupportSelection(teamName: string): void {
    this.noTeamSupport = true;
    this.currentlyClickedCardIndex = undefined;
    this.changeDetectorRef.detectChanges();
    const { customTeamNameText, sycExitCTA, thankYouMsg, sycThankYouTitle, sycConfirmCTA, sycLoginCTA, sycPreLoginNoTeamSelectionMsg, sycNoTeamSelectionTitle, daysToChangeTeam, remindLaterHideDays, changeTeamTimePeriodMsg } = this.fanzonePopupData;
    const noSupportToTeam = {
      sycPopUpDescription: this.getMessageUserLogin(customTeamNameText, sycPreLoginNoTeamSelectionMsg),
      sycTitle: sycNoTeamSelectionTitle,
      ctaPrimaryBtn: sycExitCTA.toUpperCase(),
      ctaSecondaryBtn: this.getMessageUserLogin(sycConfirmCTA.toUpperCase(), sycLoginCTA.toUpperCase()),
      teamName: this.customTeam ,
      genericTeamName: teamName,
      thankYouMsg: thankYouMsg,
      sycThankYouTitle: sycThankYouTitle,
      teamId: SHOW_YOUR_COLORS.CUSTOM_TEAM_ID,
      changeTeamTimePeriodMsg: changeTeamTimePeriodMsg,
      sycExitCTA: sycExitCTA,
      daysToChangeTeam: daysToChangeTeam,
      remindLaterHideDays: remindLaterHideDays
    }
    this.pushCachedEvents(SHOW_YOUR_COLORS.GTA.SELECT, SHOW_YOUR_COLORS.GTA.I_DONT_SUPPORT);
    this.dialogService.openDialog(SHOW_YOUR_COLORS.DIALOG_NAME.NO_SUPPORT_TO_TEAM, this.componentFactoryResolver.resolveComponentFactory(FanzoneSelectYourTeamDialogComponent), true, noSupportToTeam);
  }

  /**
   * Method to unsubscribe 
   * returns {void}
   */
  ngOnDestroy(): void {
    this.pubSubService.unsubscribe(this.ctrlName);
  }
}