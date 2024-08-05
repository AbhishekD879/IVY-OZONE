import { Component, OnDestroy, OnInit, Input } from '@angular/core';
import { ActivatedRoute, Params } from '@angular/router';
import { ICountDownTimer } from '@app/core/services/time/time-service.model';
import { TimeService } from '@app/core/services/time/time.service';
import { AbstractOutletComponent } from '@app/shared/components/abstractOutlet/abstract-outlet.component';
import { UserService } from '@core/services/user/user.service';
import { FiveasideLeaderBoardService } from '@fiveASideShowDownModule/services/fiveaside-leader-board.service';
import { IEventDetails, IShowDown, IShowDownResponse } from '@app/fiveASideShowDown/models/show-down';
import { IPrize } from '@app/fiveASideShowDown/models/IPrize';
import { of, Subscription } from 'rxjs';
import { concatMap } from 'rxjs/operators';
import { FiveASidePreHeaderService } from '@app/fiveASideShowDown/services/fiveaside-pre-header.service';
import { kickOutFlag } from '@app/fiveASideShowDown/constants/fiveaside-pre-leader-board.enum';
import { LocaleService } from '@core/services/locale/locale.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { ITeamColor } from '@app/fiveASideShowDown/models/team-color';
import { EVENTSTATUS, LEADERBOARD_WIDGET, PUBSUB_API } from '@app/fiveASideShowDown/constants/constants';
import { IWelcomeOverlay } from '@app/fiveASideShowDown/models/welcome-overlay';
import { WindowRefService } from '@app/core/services/windowRef/window-ref.service';
import { FiveAsideLiveServeUpdatesSubscribeService } from '@app/fiveASideShowDown/services/fiveaside-live-serve-updates-subscribe.service';
import { FiveASideCmsService } from '@app/fiveASideShowDown/services/fiveaside-cms.service';
import { LiveServConnectionService } from '@app/core/services/liveServ/live-serv-connection.service';
import { CONTEST_STATUSES } from '@app/fiveASideShowDown/components/fiveASideRulesEntryArea/fiveaside-rules-entry-area.constant';
import { NavigationService } from '@core/services/navigation/navigation.service';
@Component({
  selector: 'fiveaside-pre-leader-board',
  templateUrl: './fiveaside-pre-leader-board.component.html'
})
export class FiveASidePreLeaderBoardComponent extends AbstractOutletComponent implements OnInit, OnDestroy {
  @Input() leaderboardData: IShowDown;
  showOverlay: boolean;
  showDown: IShowDown;
  public prizePoolData: IPrize;
  public contentDescription: string;
  public clockTime: ICountDownTimer;
  public dateTime: string;
  public homeName: string;
  public awayName: string;
  public flagHomeIcon: string;
  public flagAwayIcon: string;
  public kickOut: string = kickOutFlag.KO_FLAG;
  public dateTimeMonth: string;
  readonly eventstatus: string = EVENTSTATUS.PRE;
  public teamColors: ITeamColor[];
  public hasTeamImage: boolean;
  public showTutorialOverlay: boolean = true;
  public isOverlayEnabled: boolean = false;
  public isWelcomeOverlaySeen: boolean = false;
  public currentOverlay: string = 'PREEVENT';
  public preEventData: IWelcomeOverlay;
  public channels: string[] = [];
  private eventEntity: IEventDetails;
  private routeSubscriber: Subscription;
  private contestSubscriber: Subscription;
  private prizesSubscriber: Subscription;
  private contestId: string;
  private readonly title = 'FiveASidePreLeaderBoard';
  public readonly contestStatus = CONTEST_STATUSES.pre;

  constructor(
    private timeService: TimeService,
    private route: ActivatedRoute,private pubSubService:PubSubService,
    private fiveASidePreHeaderService: FiveASidePreHeaderService, private userService: UserService,
    private leaderBoardService: FiveasideLeaderBoardService, private localeService: LocaleService,
    private cmsService: FiveASideCmsService,
    private windowRef: WindowRefService,
    private subscriberService: FiveAsideLiveServeUpdatesSubscribeService,
    private liveServConnectionService: LiveServConnectionService,
    private navigationService: NavigationService
    ) {
    super();
  }

  /**
   * OnInit function for the component
   */
  ngOnInit(): void {
    this.showSpinner();
    this.subscribeToLiveUpdates();
    this.routeSubscriber = this.route.params
      .pipe(
        concatMap((param: Params) => {
          if (param.id) {
            this.contestId = param.id;
            // this.fetchPrizePoolData(param.id);
            // this.getContestInformation();
            this.decodeInitialData();
            this.getWelcomeOverlayCMS();
            if (this.checkForDisplayed()) {
              this.isWelcomeOverlaySeen = true;
            }
            this.showTutorialOverlay = this.checkForWelcome();
          }
          return of({});
        })
      ).subscribe();
    this.postLoginTrigger();
    this.reloadComponentData();
  }
  /**
   * ngOnDestroy function for the component
   * @returns {void}
   */
  ngOnDestroy(): void {
    this.routeSubscriber && this.routeSubscriber.unsubscribe();
    this.prizesSubscriber && this.prizesSubscriber.unsubscribe();
    this.contestSubscriber && this.contestSubscriber.unsubscribe();
    this.pubSubService.unsubscribe(this.title);
    this.unsubscribeLiveServeConnection();
    this.removeFocusListner();
  }

  /**
   * Triggers when user comes back from offline to online
   * @returns {void}
   */
   private reloadComponentData(): void {
    this.pubSubService.subscribe(this.title, this.pubSubService.API.RELOAD_COMPONENTS, () => {
      this.liveServConnectionService.connect()
        .subscribe(() => {
          this.showSpinner();
          this.ngOnDestroy();
          this.ngOnInit();
        });
    });
  }

  /**
   * To open live serve connection and subscribe to channels
   * @returns {void}
   */
  private openLiveServConnection(): void {
    const eventId: string = this.eventEntity.id.toString();
    this.channels = this.subscriberService.createChannels([eventId]);
    this.subscriberService.openLiveServeConnectionForUpdates(this.channels);
  }

  /**
   * To Subscribe to live serve updates
   * @returns {void}
   */
  private subscribeToLiveUpdates(): void {
    this.pubSubService.subscribe(this.title, PUBSUB_API.SHOWDOWN_EVENT_STARTED, (eventId: string) => {
      if (eventId && Number(this.eventEntity.id) === Number(eventId)) {
        this.pubSubService.publish(PUBSUB_API.LEADERBOARD_EVENT_STARTED);
      }
    });
  }

  /**
   * To Unsubscribe to channels and close liveserve connection
   * @return {void}
   */
  private unsubscribeLiveServeConnection(): void {
    const eventId: string = this.eventEntity.id.toString();
    this.channels = this.subscriberService.createChannels([eventId]);
    this.subscriberService.unSubscribeLiveServeConnection(this.channels);
  }

  /**
   * Scenario: When User Logged in first time to refresh the Data
   * @returns void
   */
  private postLoginTrigger(): void {
    this.pubSubService.subscribe(this.title, this.pubSubService.API.SUCCESSFUL_LOGIN, () => {
      this.getContestInformation();
    });
  }

  /**
   * Fetch the initial data to show in leaderboard header during pre-event
   * @param {string} contestId
   */
  private fetchInitialData(): void {
    if (this.showDown && this.showDown.description) {
      this.contentDescription = this.showDown.description;
    }
    if (this.showDown && this.showDown.eventDetails) {
      this.eventEntity = this.showDown.eventDetails;
      const eventStartTime: Date = new Date(this.eventEntity.startTime);
      if (this.fiveASidePreHeaderService.checkForMatchDay(eventStartTime)) {
        const currentDate = new Date();
        const diffSeconds: number = this.fiveASidePreHeaderService.getTimeDifference(eventStartTime, currentDate);
        this.clockTime = this.timeService.countDownTimerForHours(diffSeconds);
        this.windowRef.nativeWindow.localStorage.setItem('fiveasideStartTime', this.eventEntity.startTime);
        this.focusListner();
      } else {
        this.dateTime = this.timeService.getDateTimeFormat(eventStartTime);
        this.dateTimeMonth = this.timeService.getFullDateTimeFormatSufx(eventStartTime);
      }
      this.formTeamName();
    }
  }

  private focusHandler(): void {
    const startTimeField: string = this.windowRef.nativeWindow.localStorage.getItem('fiveasideStartTime');
    const eventStartTime: Date = new Date(startTimeField);
      if (this.fiveASidePreHeaderService.checkForMatchDay(eventStartTime)) {
        const currentDate = new Date();
        const diffSeconds: number = this.fiveASidePreHeaderService.getTimeDifference(eventStartTime, currentDate);
        this.clockTime = this.timeService.countDownTimerForHours(diffSeconds);
      }
  }

  private focusListner(): void {
    this.windowRef.nativeWindow.addEventListener('focus', this.focusHandler.bind(this));
  }

  /**
   * remove scroll Listeners
   * @returns {void}
   */
   private removeFocusListner(): void {
    this.windowRef.nativeWindow.removeEventListener('focus', this.focusHandler);
  }

  /**
   * To decode initial contest information received from leaderboard component
   * @returns {void}
   */
  private decodeInitialData() {
    this.showDown = this.leaderboardData;
    this.prizePoolData = this.leaderboardData.prizeMap;
    this.hideSpinner();
    this.showDown.events = this.showDown.eventDetails;
    if(!this.showDown.display) {
      this.navigationService.openRouterUrl(LEADERBOARD_WIDGET.LOBYY_URL, true);
    }
    this.fetchInitialData();
    this.openLiveServConnection();
    this.cmsService.getTeamsColors([this.homeName, this.awayName], '16')
    .subscribe((response: ITeamColor[]) => {
      this.teamColors = response;
      this.hasTeamImage = this.leaderBoardService.hasImageForHomeAway(this.teamColors);
      this.teamColors = this.leaderBoardService.setDefaultTeamColors(this.teamColors,
        [this.homeName, this.awayName]);
    }, () => {
      this.showError();
      this.navigationService.openRouterUrl(LEADERBOARD_WIDGET.LOBYY_URL, true);
    });
  }

  /**
   * To get contest information
   * @returns {void}
   */
  private getContestInformation(): void {
    const userName: string = this.userService.username;
    const bppToken: string = this.userService.bppToken;
    this.leaderBoardService.getContestInformationById(this.contestId, userName, bppToken)
      .subscribe((response: IShowDownResponse) => {
        this.leaderboardData = response.contest;
        this.decodeInitialData();
      });
  }

  /**
   * Forming team flag name from team name
   * @param { string } name
   * @returns { string }
   */
  private formFlagName(name: string): string {
    const teamName: string = name.toLowerCase().split(' ').join('_');
    return this.localeService.getString('fs.flagIcon', {teamName});
  }

  /**
   * Forming team from event response
   * @returns {void}
   */
  private formTeamName(): void {
    const eventName: string = this.eventEntity.name.replace(/[|,]/g, '');
    [this.homeName, this.awayName] = eventName.split(/ v | vs | - /);
    this.flagHomeIcon = this.formFlagName(this.homeName);
    this.flagAwayIcon = this.formFlagName(this.awayName);
  }

  /**
   * To fetch welcome overlay from CMS
   * @returns {void}
   */
  private getWelcomeOverlayCMS(): void {
    this.cmsService.getWelcomeOverlay().subscribe((response: IWelcomeOverlay) => {
      this.preEventData = response;
      if (this.preEventData) {
        this.isOverlayEnabled = this.preEventData.overlayEnabled;
      }
    }, (error) => {
      console.warn(error);
    });
  }

  private checkForDisplayed(): boolean {
    return this.windowRef.nativeWindow.localStorage.getItem('showdownOverlay') &&
    !this.windowRef.nativeWindow.localStorage.getItem('preEventOverlay');
  }

  private checkForWelcome(): boolean {
    return !this.windowRef.nativeWindow.localStorage.getItem('showdownOverlay') &&
    !this.windowRef.nativeWindow.localStorage.getItem('preEventOverlay');
  }
}
