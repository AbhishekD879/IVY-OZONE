import { ComponentFactoryResolver, Inject, Injectable } from "@angular/core";
import { CmsService } from "@app/core/services/cms/cms.service";
import { catchError, map } from 'rxjs/operators';
import { PubSubService } from '@app/core/services/communication/pubsub/pubsub.service';
import { CmsToolsService } from '@app/core/services/cms/cms.tools';
import { DeviceService } from '@app/core/services/device/device.service';
import { CoreToolsService } from '@app/core/services/coreTools/core-tools.service';
import { CasinoLinkService } from '@app/core/services/casinoLink/casino-link.service';
import { NativeBridgeService } from '@app/core/services/nativeBridge/native-bridge.service';
import { UserService } from '@app/core/services/user/user.service';
import { IInitialData, ISystemConfig } from '@app/core/services/cms/models';
import { SegmentEventManagerService } from '@lazy-modules/segmentEventManager/service/segment-event-manager.service';
import { SegmentedCMSService } from '@app/core/services/cms/segmented-cms.service';
import { HttpClient, HttpResponse } from "@angular/common/http";
import { WindowRefService } from "@app/core/services/windowRef/window-ref.service";
import { AsyncScriptLoaderService } from "@app/core/services/asyncScriptLoader/async-script-loader.service";
import { IFanzoneSyc } from '@lazy-modules/fanzone/models/fanzone-syc.model';
import { Observable, of } from "rxjs";
import { Fanzone, gtmTackingKeys } from '@app/fanzone/constants/fanzonePreferenceConstants';
import { GtmService } from '@app/core/services/gtm/gtm.service';
import { VanillaApiService } from '@app/vanillaInit/services/vanillaApi/vanilla-api.service';
import { Router } from "@angular/router";
import { DialogService } from "@app/core/services/dialogService/dialog.service";
import { FanzoneNotificationComponent } from "@app/lazy-modules/fanzone/components/fanzoneNotification/fanzone-notification.component";
import { FanzoneGamesDialogComponent } from "@app/lazy-modules/fanzone/components/fanzoneGamesDialog/fanzone-games-dialog.component";
import { FanzoneGameLaunchDialogComponent } from "@app/lazy-modules/fanzone/components/fanzoneGameLaunchDialog/fanzone-game-launch-dialog.component";
import { IFanzoneData, IFanzonePreferences } from "@app/fanzone/models/fanzone-preferences.model";
import { IFanzoneGamesSignPostingData, IFanzoneGamesPopupData } from "@app/fanzone/models/fanzone-games.model";

import { TimeService } from "@app/core/services/time/time.service";
import { FANZONE, SHOW_YOUR_COLORS, UNSUBSCRIBE_CUSTOM_TEAM_ID, fanzoneEmailKey } from "@app/fanzone/constants/fanzoneconstants";
import { FanzoneHelperService } from "@app/core/services/fanzone/fanzone-helper.service";
import { FanzoneDetails } from "@app/fanzone/models/fanzone.model";
import { FanzoneStorageService } from "@app/core/services/fanzone/fanzone-storage.service";
import { ISiteCoreTeaserFromServer } from "@app/core/models/aem-banners-section.model";
import { FZ_POST_MAPPER } from "@app/lazy-modules/fanzone/fanzone.constant";
import { FanzoneGamesService } from "@app/fanzone/services/fanzone-games.service";
import { ICmsEmailOptin, ICommunicationSettings, IEmailOptin } from "@app/lazy-modules/fanzone/models/fanzone-email-optin.model";

@Injectable()
export class FanzoneSharedService extends CmsService {
  readonly PATH: string = FANZONE.desktopPath;
  constructor(protected fanzoneStorageService: FanzoneStorageService,
    protected pubsub: PubSubService,
    protected cmsTools: CmsToolsService,
    protected device: DeviceService,
    protected http: HttpClient,
    protected coreToolsService: CoreToolsService,
    protected casinoDecoratorService: CasinoLinkService,
    protected nativeBridgeService: NativeBridgeService,
    protected userService: UserService,
    protected segmentEventManagerService: SegmentEventManagerService,
    protected segmentedCMSService: SegmentedCMSService,
    protected windowRefService: WindowRefService,
    protected asyncScriptLoaderService: AsyncScriptLoaderService,
    @Inject('CMS_CONFIG') protected cmsInitConfigPromise: Promise<IInitialData>,
    private gtmService: GtmService,
    private router: Router,
    private dialogService: DialogService,
    private timeService: TimeService,
    private vanillaApiService: VanillaApiService,
    private componentFactoryResolver: ComponentFactoryResolver,
    private fanzoneHelperService: FanzoneHelperService,
    private fanzoneGamesService: FanzoneGamesService) {
    super(pubsub, cmsTools, device, http, coreToolsService, fanzoneStorageService,
      casinoDecoratorService, nativeBridgeService, userService,
      segmentEventManagerService, segmentedCMSService, cmsInitConfigPromise);
  }

  getSpecialPagesDataCollection(): Observable<IFanzoneSyc[]> {
    return this.getData(`fanzone-syc`)
      .pipe(
        map((data: HttpResponse<IFanzoneSyc[]>) => data.body)
      )
  }

  /**
   * Method to get the date on which popup should open
   * @param days - number of days from today
   * @returns - future date as per calculation
   */
  addDaysToCurrentDate(days): Date {
    const futureDate = new Date();
    futureDate.setDate(futureDate.getDate() + parseInt(days));
    return futureDate;
  }

  /**
   * Method to save user selected team information on storage
   * @param selectedTeam - team info
   * @param communication - communication preferences
   * @param navigateTo - navigate to
   */
  saveTeamOnPlatformOne(selectedTeam?: IFanzoneData, comm?: string[], navigateTo?: string): void {
    this.saveUserFanzoneTeam(selectedTeam, comm).subscribe(() => {
      selectedTeam = this.getSelectedTeam(selectedTeam);
      if (selectedTeam.teamId !== SHOW_YOUR_COLORS.CUSTOM_TEAM_ID && !navigateTo) {
        if (this.getFanzoneInfo().isFanzoneExists && this.device.isWrapper) {
          this.showNotifications(true);
        } else {
          this.showNotifications(false);
        }
      }
      const { teamId, teamName } = selectedTeam;
      const fzData = this.fanzoneStorageService.get('fanzone');
      const subscriptionDate = comm ? fzData.subscriptionDate : this.timeService.getSuspendAtTime();
      const isFanzoneExists = this.isTeamSelection(teamId);
      const isResignedUser = false;
      if (fzData && fzData.teamId !== 'FZ001' && fzData.showSYCPopupOn) {
        delete fzData.showSYCPopupOn;
        this.fanzoneStorageService.set('fanzone', fzData);
      }
      const communication = comm ? comm : fzData.communication;
      this.appendToStorage({ teamId, teamName, subscriptionDate, communication, isFanzoneExists, isResignedUser }, true);
      if (navigateTo && navigateTo.length) this.router.navigate([`${navigateTo}`]);
    }, (error: any) => {
      console.log('FAILED TO SAVE TEAM ON PALTFORM', error);
    })
  }
  /**
   * Method to add days to current date
   * @param date - current date
   * @param days - number of days to be added
   * @returns - future date
   */
  addDaysToDate(date: string, days: number): string {
    const futureDate = new Date(date);
    futureDate.setDate(futureDate.getDate() + days);
    return futureDate.toString();
  }

  /**
   * Method to check if a valid team
   * @param teamId - id of team
   * @returns - boolean
   */
  isTeamSelection(teamId: string): boolean {
    return teamId !== SHOW_YOUR_COLORS.CUSTOM_TEAM_ID ? true : false;
  }

  /**
   * Method to get stored fanzone information from local storage
   * @returns - local storage data
   */
  getFanzoneInfo(): IFanzoneData {
    return this.fanzoneStorageService.get(Fanzone) || {};
  }

  /**
   * Method to check if a fanzone team is relegated
   * @returns - Observable boolean
   */
  checkIfTeamIsRelegated(): Observable<boolean> {
    return this.fanzoneHelperService.checkIfTeamIsRelegated();
  }

  /**
   * Method to check if the ios device is black listed
   * @returns - Observable: true/false
   */
  isIosBlackListedDevice(): Observable<boolean> {
    return this.getSystemConfig().pipe(map((config: ISystemConfig) => {
        const appMenuProperties = config.GamingEnabled;
        if (this.device.isWrapper && this.device.isIos && this.fanzoneHelperService.appBuildVersion && appMenuProperties.iosVersionBlackList
          && appMenuProperties.iosVersionBlackList.includes(this.fanzoneHelperService.appBuildVersion)) {
          return true;
        }
        return false;
      }
    ));
  }

  /**
   * Method to save user selected fanzone team to vanilla
   * @param selectedTeam - team data
   * @param commPref -communication preferences
   * @returns - empty object
   */
  saveUserFanzoneTeam(selectedTeam?: IFanzoneData, commPref?: string[]): any {
    const APIOPTIONS: {
      [name: string]: string;
    } = {
      'prefix': '/en/coralsports'
    };
    selectedTeam = this.getSelectedTeam(selectedTeam);

    const payload = this.getPayload(selectedTeam, commPref);

    return this.vanillaApiService.post('perferencecenter/football', payload, APIOPTIONS);
  }

  /**
   * Method to save user Eamil Optin Mock to vanilla
   * @returns - empty object
   */
  saveEmailOptinData(payload: IEmailOptin): Observable<any> {
    const APIOPTIONS: {
      [name: string]: string;
    } = {
      'prefix': '/en/coralsports'
    };
    return this.vanillaApiService.post('perferencecenter/emailOptin', payload, APIOPTIONS);
  }

  /**
   * Method to send updated data to platform
   * @param payload - user updated fields.
   * @param fanzoneUser - is user a fanzone subscribed user
   */
  postEmailOptinDetails(payload, fanzoneUser: boolean): void {
    const request =  {
      "fanzoneUser": fanzoneUser,
      "requestData": this.getEmailPayload(payload)
    };
    this.saveEmailOptinData(request).subscribe(() => {
      const fanzoneEmail = this.fanzoneStorageService.get(fanzoneEmailKey);
      const info = {...payload , ...{fanzoneUser: fanzoneUser}}
      this.fanzoneStorageService.set(fanzoneEmailKey, {...fanzoneEmail, ...info});
    });
  }

  /**
   * Method to construct POST payload using the mapper
   * @param payload - keys and values
   * @returns - payload.
   */
  getEmailPayload(payload): any {
    const requestData = [];
    Object.entries(payload).forEach(([key, value]) => {
      requestData.push({key: FZ_POST_MAPPER[key], value: value})
    });
    return requestData;
  }

  /**
   * Method to save user selected fanzone team to vanilla
   * @param selectedTeam - team data
   * @param commPref -communication preferences
   * @returns - payload
   */
  getPayload(selectedTeam?: IFanzoneData, commPref?: string[]): any {
    const selectedTeamPayload = {
      category: "football",
      preferences: [
        {
          key: "TEAM_ID",
          value: selectedTeam.teamId
        },
        {
          key: "TEAM_NAME",
          value: selectedTeam.teamName
        }
      ]
    }
    const preferencePayload = {
      category: "football",
      preferences: [
        { key: "COMM_PREFERENCES", value: JSON.stringify(commPref) }
      ]
    }
    return commPref ? preferencePayload : selectedTeamPayload;
  }
  /**
   * Method to check if selected team exists or get data from storage
   * @param selectedTeam - team selected
   * @returns - team
   */
  getSelectedTeam(selectedTeam: IFanzoneData): IFanzoneData {
    return Object.keys(selectedTeam).length ? selectedTeam : this.getFanzoneInfo();
  }

  /**
  * Method to add info fanzone info to storage
  * @param object - IFanzoneData
  */
  appendToStorage(object: IFanzoneData, isCustomResignedUser?: boolean): void {
    const fanzoneData = this.getFanzoneInfo();
    const fanzoneInfoData = { ...fanzoneData, ...object };
    if (fanzoneInfoData && fanzoneInfoData.hasOwnProperty('isCustomResignedUser') && isCustomResignedUser) {
      delete fanzoneInfoData['isCustomResignedUser'];
    }
    this.fanzoneStorageService.set('fanzone', fanzoneInfoData);
    this.fanzoneHelperService.PublishFanzoneData();
  }

  /**
   * Method to resign a user from fanzone
   */
  resignFanzone() {
    const userData = this.fanzoneStorageService.get('fanzone');
    if (userData.teamId && userData.teamId === SHOW_YOUR_COLORS.CUSTOM_TEAM_ID) {
      this.saveUserFanzoneTeam({
        teamId: UNSUBSCRIBE_CUSTOM_TEAM_ID
      }).subscribe(() => {
        this.successfulDeleteFanzoneTeam();
      });
    } else {
      this.deleteFanzonePreferences().subscribe(() => {
        this.successfulDeleteFanzoneTeam();
      }, error => {
        console.error(error)
      })
    }
  }

  successfulDeleteFanzoneTeam() {
    const userData = this.fanzoneStorageService.get('fanzone');
    if (userData) {
      if (userData.teamId && userData.teamId === SHOW_YOUR_COLORS.CUSTOM_TEAM_ID) {
        userData.isCustomResignedUser = true;
      }
      userData.isResignedUser = true;
      userData.isFanzoneExists = false;
      delete userData.teamId;
      delete userData.teamName;
      delete userData.communication;
      this.fanzoneStorageService.set('fanzone', userData);
      this.pubsub.publish(this.pubsub.API.FANZONE_DATA, <FanzoneDetails>{});
      this.router.navigate(['']);
      this.pushCachedEvents(gtmTackingKeys.confirm);
    }
  }

  /**
   * Method to unsubscribe fanzone
   * @returns observable
   */
  deleteFanzonePreferences(): Observable<any> {
    const APIOPTIONS: {
      [name: string]: string;
    } = {
      'prefix': '/en/coralsports'
    };
    const payload = {
      category: "football",
      preferenceKeys: ['TEAM_ID', 'TEAM_NAME', 'COMM_PREFERENCES'],
    }
    return this.vanillaApiService.post('perferencecenter/deletefootball', payload, APIOPTIONS);
  }

  /**
  * Method to capture events in data layer for GA tracking
  * @param eventLabel - label of event
  */
  pushCachedEvents(eventLabel?: string, eventDetails?: string, eventCategory?: string): void {
    const dataLayer = {
      event: gtmTackingKeys.trackEvent,
      eventAction: gtmTackingKeys.preferenceCentre,
      eventCategory: eventCategory || gtmTackingKeys.fanzone,
      eventLabel: eventLabel,
      eventDetails: eventDetails
    }
    this.gtmService.push(dataLayer.event, { ...dataLayer });
  }

  /**
   * Method to load preference centre / notification dialog
   * @param showToggle - boolean to show/hide fanzone subscribe toggle
   * @returns - void
   */
  showNotifications(showToggle?: boolean) {
    this.getFanzonePreferences().subscribe((data: IFanzonePreferences[]) => {
      const preferences = data[0];
      this.pushCachedEvents();
      const navigationFromSYC = { showToggle: showToggle };
      if (this.device.isWrapper) {
        const stateData = { ...preferences, ...navigationFromSYC };
        this.router.navigate(['/fanzone/sport-football/preference-centre'], { state: { data: stateData } });
        return;
      }
      const componentFactory = this.componentFactoryResolver.resolveComponentFactory(FanzoneNotificationComponent);
      this.dialogService.openDialog('NYT', componentFactory, true, { ...preferences, ...{ showToggle: showToggle } });
    })
  }

  /**
   * Method to show Fanzone Games popup
   * @param {}
   * @returns - void
   */
  showGamesPopup() {
    this.getFanzoneNewGamePopupContent().subscribe((data: IFanzoneGamesPopupData[]) => {
      const componentFactory = this.componentFactoryResolver.resolveComponentFactory(FanzoneGamesDialogComponent);
      this.dialogService.openDialog('GAMES', componentFactory, true, data[0]);
    })
  }

   /**
   * Method to show Fanzone Game launch in popup
   * @param {}
   * @returns - void
   */
  showGameLaunchPopup(gameDetails) {
    const componentFactory = this.componentFactoryResolver.resolveComponentFactory(FanzoneGameLaunchDialogComponent);
    this.dialogService.openDialog('GAMES-LAUNCH', componentFactory, true, gameDetails);
  }

  /**
   * Method to get fanzone information from CMS
   * @returns - IFanzonePreferences
   */
  getFanzonePreferences() {
    return this.getData(`fanzone-preference-center`)
      .pipe(
        map((data: any) => data.body)
      ).pipe(
        catchError(() => of([]))
      );
  }

  /**
   * Get email optin data from CMS
   * @returns - ICmsEmailOptin
   */
  getFanzoneEmailOptin(): Observable<ICmsEmailOptin[]> {
    return this.getData('fanzone-optin-email')
      .pipe(
        map((fzData: HttpResponse<any[]>) => fzData.body)
      );
  }
  
  /**
   * Method to get user communication settings details
   * @returns Observable
   */
  getUserCommunicationSettings(): Observable<ICommunicationSettings> {
    const APIOPTIONS: {
      [name: string]: string;
    } = {
      'prefix': '/en/coralsports'
    };
    return this.vanillaApiService.get('perferencecenter/communicationsettings', '', APIOPTIONS);
  }
  /**
   * fetch fanzone teaser images from sitecore
   * @returns - ISiteCoreTeaserFromServer
   */
  getFanzoneBannerFromSiteCore(): Observable<ISiteCoreTeaserFromServer[]> {
    const APIOPTIONS: {
      [name: string]: string;
    } = {
      'prefix': '/en/coralsports'
    };
    return this.vanillaApiService.get(this.PATH, '', APIOPTIONS);
  }

  /**
   * Method to get fanzone new signposting information from CMS
   * @returns - IFanzoneGamesSignPostingData[]
   */
  getFanzoneNewSignPosting(): Observable<IFanzoneGamesSignPostingData[]>{
    return this.getData(`fanzone-new-signposting`)
      .pipe(
        map((data: HttpResponse<IFanzoneGamesSignPostingData[]>) => data.body)
      ).pipe(
        catchError(() => of([]))
      );
  }

  /**
   * Method to get fanzone new gaming popup content from CMS
   * @returns - IFanzoneGamesPopupData[]
   */
  getFanzoneNewGamePopupContent(): Observable<IFanzoneGamesPopupData[]> {
    return this.getData(`fanzone-new-gaming-pop-up`)
      .pipe(
        map((data: HttpResponse<IFanzoneGamesPopupData[]>) => data.body)
      ).pipe(
        catchError(() => of([]))
      );
  }
  /**
   * Shows fanzone games popup if user is visited for first time
   * @param {}
   * @returns { void }
   */
  showFanzoneGamesPopup(fanzoneDetailResponse: FanzoneDetails): void {
    this.isIosBlackListedDevice().subscribe((isIosBlackListedDevice: boolean) => {
      if (fanzoneDetailResponse.fanzoneConfiguration.showGames && !this.fanzoneGamesService.getNewFanzoneGamesPopupSeen() && !isIosBlackListedDevice) {
        this.showGamesPopup();
      }
    });
  }

   /**
    * Method to check user subscribed to custom team
    * returns {boolean}
    */
   isSubscribedToCustomTeam() {
    const fanzoneTeam = this.fanzoneStorageService.get('fanzone');
    return fanzoneTeam && fanzoneTeam.teamId === SHOW_YOUR_COLORS.CUSTOM_TEAM_ID;
  }
}