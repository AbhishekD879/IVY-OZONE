import { ChangeDetectorRef, Component, OnDestroy, OnInit, Input } from '@angular/core';
import { WindowRefService } from '@app/core/services/windowRef/window-ref.service';
import { RendererService } from '@app/shared/services/renderer/renderer.service';
import { PubSubService } from '@app/core/services/communication/pubsub/pubsub.service';
import { IPageYOffset, Time, LIVE_EVENT_VALUE } from '@app/fiveASideShowDown/constants/enums';
import { ActivatedRoute } from '@angular/router';
import { FiveAsideLiveServeUpdatesService } from '@app/fiveASideShowDown/services/fiveaside-live-serve-updates.service';
import { CoreToolsService } from '@app/core/services/coreTools/core-tools.service';
import { IEventDetails, IShowDown, IShowDownResponse } from '@app/fiveASideShowDown/models/show-down';
import { FiveASideShowDownLobbyService } from '@app/fiveASideShowDown/services/fiveaside-show-down-lobby.service';
import { FiveasideLeaderBoardService } from '@app/fiveASideShowDown/services/fiveaside-leader-board.service';
import {
  FiveAsideLiveServeUpdatesSubscribeService
} from '@app/fiveASideShowDown/services/fiveaside-live-serve-updates-subscribe.service';
import { UserService } from '@app/core/services/user/user.service';
import { LocaleService } from '@app/core/services/locale/locale.service';
import { IEntrySummaryInfo } from '@app/fiveASideShowDown/models/entry-information';
import {
  GTM_RULES_DATA, LIVESERVELISTNERS, LIVE_OVERLAY, LIVE_SERVE_KEY,
  PUBSUB_API, EVENTSTATUS, LEADERBOARD_WIDGET
} from '@app/fiveASideShowDown/constants/constants';
import { ITeamColor } from '@app/fiveASideShowDown/models/team-color';
import { GtmService } from '@app/core/services/gtm/gtm.service';
import { IWelcomeOverlay } from '@app/fiveASideShowDown/models/welcome-overlay';
import { Subscription } from 'rxjs';
import { FiveASideCmsService } from '@app/fiveASideShowDown/services/fiveaside-cms.service';
import { LiveServConnectionService } from '@app/core/services/liveServ/live-serv-connection.service';
import { DeviceService } from '@core/services/device/device.service';
import { AbstractOutletComponent } from '@app/shared/components/abstractOutlet/abstract-outlet.component';
import { AWSFirehoseService } from '@app/lazy-modules/awsFirehose/service/aws-firehose.service';
import { TimeSyncService } from '@app/core/services/timeSync/time-sync.service';
import { LiveEventClockProviderService } from '@app/shared/components/liveClock/live-event-clock-provider.service';
import { ILeaderboardData } from '../../models/leader-board';
import { NavigationService } from '@core/services/navigation/navigation.service';
import { IShowdownOptaUpdate } from '../../models/IShowdownOptaUpdate.model';

@Component({
  selector: 'fiveaside-live-leader-board',
  templateUrl: './fiveaside-live-leader-board.component.html'
})
export class FiveASideLiveLeaderBoardComponent extends AbstractOutletComponent implements OnInit, OnDestroy {
  @Input() leaderboardData: IShowDown;
  public event: IEventDetails;
  public isHalfTime: boolean;
  public isFullTime: boolean;
  public homeName: string;
  public awayName: string;
  public homeScore: string;
  public awayScore: string;
  public eventId: number;
  public eventArray: string[];
  public componentId: string;
  public updateState: string = '';
  public flagHomeIcon: string;
  public flagAwayIcon: string;
  public eventIsLive: boolean | string;
  public isScoresAvailable: boolean;
  public channelsList: string[];
  public isNoCommentaryAvailable: boolean = false;
  public contestInfo: IShowDown;
  public events: IEventDetails;
  public myEntries: Array<IEntrySummaryInfo> = [];
  public userEntries: Array<IEntrySummaryInfo> = [];
  public entryIdList: string[];
  public dataLoading: boolean = true;
  public offSetPValue: number = IPageYOffset.offSetPValue;
  public offSetValue: number = IPageYOffset.offSetValue;
  public slideContent: HTMLElement;
  public listeners = LIVESERVELISTNERS;
  public leaderboardVal: string = '';
  readonly halfTime: string = Time.HALF_TIME;
  readonly fullTime: string = Time.FULL_TIME;
  readonly eventStatus: string = EVENTSTATUS.LIVE;
  public teamColors: ITeamColor[];
  public hasTeamImage: boolean;
  public initialRecordsCopy: Array<IEntrySummaryInfo> = [];
  public showOverlay: boolean;
  public showLiveOverlay: boolean;
  public welcomeCard: IWelcomeOverlay;
  public liveManualTutorial: boolean;
  public isMyEntriesLoaded: boolean = false;
  public showServiceMessage: boolean = false;
  public staticMock;
  public staticMockScore;
  public staticMockEvent;
  private lbrIdList: string[];
  private contestId: string;
  private channel: string;
  private leaderboardChannel: string;
  private emitKey: string = LIVE_SERVE_KEY.MYENTRIES;
  private ldrbrdEmitKey: string = LIVE_SERVE_KEY.LDRBRD;
  private initialAllRecords: Array<IEntrySummaryInfo> = [];
  private timeOutListener: number;
  private readonly subscribeForUpdates: string = 'subscribeshowdown';
  private interval: number;
  private leaderBoardUpdates: string;
  private updatedLeaderBoardEntries: Array<IEntrySummaryInfo> = [];
  private isLeaderboardLoaded: boolean = false;
  private isOverlayLoaded: boolean = false;
  private liveOverlaySeen: boolean = false;
  private welcomeOverlaySeen: boolean = false;
  private isLoginUpdate: boolean = false;
  private myUserEntries: Array<IEntrySummaryInfo> = [];
  private leaderbaordLimitSubscription: Subscription;


  constructor(
    protected windowRefService: WindowRefService,
    protected rendererService: RendererService,
    protected showDownService: FiveasideLeaderBoardService,
    protected fiveAsideLiveServeUpdatesSubscribeService: FiveAsideLiveServeUpdatesSubscribeService,
    protected pubSub: PubSubService,
    protected fiveAsideLiveServeUpdatesService: FiveAsideLiveServeUpdatesService,
    protected coreToolsService: CoreToolsService,
    protected route: ActivatedRoute,
    protected fiveASideShowDownLobbyService: FiveASideShowDownLobbyService,
    protected userService: UserService,
    private localeService: LocaleService,
    private cmsService: FiveASideCmsService,
    private gtmService: GtmService,
    private changeDetectorRef: ChangeDetectorRef,
    private liveServConnectionService: LiveServConnectionService,
    private deviceService: DeviceService,
    private awsService: AWSFirehoseService,
    private liveEventClockProviderService: LiveEventClockProviderService,
    private timeSyncService: TimeSyncService,
    private navigationService: NavigationService
  ) {
    super();
  }

  ngOnInit(): void {
    this.componentId = this.coreToolsService.uuid();
    this.contestId = this.route.snapshot.params.id;
    this.setScrollListeners();
    this.getLiveupdatesubscription();
    this.loginTrigger();
    // this.fetchInitialDataOfEvent();
    this.decodeInitialData();
    this.getInitialLiveOverlayData();
    this.liveOverlaySeen = this.windowRefService.nativeWindow.localStorage.getItem(LIVE_OVERLAY.OVERLAY);
    this.welcomeOverlaySeen = this.windowRefService.nativeWindow.localStorage.getItem(LIVE_OVERLAY.WELCOME_OVERLAY);
    this.reloadComponent();
  }

  ngOnDestroy(): void {
    this.initialRecordsCopy = [];
    this.removeScrollListeners();
    this.pubSub.unsubscribe(this.componentId);
    this.unsubscribeForLiveServeConnection();
    this.unSubscribeChannel(this.leaderboardChannel, this.leaderboardUpdateHandler);
    this.leaderbaordLimitSubscription && this.leaderbaordLimitSubscription.unsubscribe();
  }
  /**
   * Post Login Trigger MyEntries
   * @returns void
   */
  loginTrigger(): void {
    this.pubSub.subscribe(this.componentId, this.pubSub.API.SUCCESSFUL_LOGIN, () => {
      this.isLoginUpdate = true;
      this.pubSub.publish(PUBSUB_API.PUBLISH_LEADERBOARD);
      this.leaderboardChannel = `${this.ldrbrdEmitKey}::${this.contestId}::0`;
      this.unSubscribeChannel(this.leaderboardChannel, this.leaderboardUpdateHandler.bind(this));
      this.getInitialLeaderBoardData();
    });
  }
  /**
   * InitialEntrySummary
   * @param  { Array<IEntrySummaryInfo> } initialData
   * @returns void
   */
  initialEntrySummary(initialData: Array<IEntrySummaryInfo>): void {
    this.myEntries = initialData;
    this.myUserEntries = initialData;
    this.isMyEntriesLoaded = true;
    this.getLiveOverlayData();
    if (this.isLoginUpdate) {
      this.myEntriesFilter();
    }
    this.awsService.addAction('MYENTRY=>LIVE', { entries: this.myEntries });
  }

  /**
   * create channels and open Live Serv Connection
   * @returns {void}
   */
  openLiveServConnection(): void {
    this.channelsList = this.fiveAsideLiveServeUpdatesSubscribeService.createChannels(this.eventArray);
    this.fiveAsideLiveServeUpdatesSubscribeService.openLiveServeConnectionForUpdates(this.channelsList);
  }

  /**
   * getInitialLeaderBoardData to get initial leaderboard entries with contestId
   * @returns void
   */
  getInitialLeaderBoardData(): void {
    const contestId: string = this.route.snapshot.params.id;
    this.dataLoading = true;
    this.leaderboardChannel = `${this.ldrbrdEmitKey}::${contestId}::${this.userService.username ? `${this.userService.username}::${this.userService.bppToken}` : 0}`;
    this.unSubscribeChannel(this.leaderboardChannel, this.leaderboardUpdateHandler.bind(this));
    this.fiveAsideLiveServeUpdatesSubscribeService.openLiveServeInitialDataEntryInformation(this.leaderboardChannel, this.leaderboardUpdateHandler.bind(this), this.subscribeForUpdates);
  }

  /**
   * unsubscribe For Live Serve Connection updates
   * @returns void
   */
  unsubscribeForLiveServeConnection(): void {
    this.channelsList = this.fiveAsideLiveServeUpdatesSubscribeService.createChannels(this.eventArray);
    this.fiveAsideLiveServeUpdatesSubscribeService.unSubscribeLiveServeConnection(this.channelsList);
  }

  /**
   * scrollHandler for animation expand and collapse the header area
   * @returns {void}
   */
  scrollHandler(): void {
    if (this.deviceService.isMobile) {
      const headerAreaScroll: HTMLElement = this.windowRefService.document.querySelector('.header-area-scroll');
      this.slideContent = this.windowRefService.document.querySelector('.over-all-height');
      if (headerAreaScroll && this.windowRefService.nativeWindow.pageYOffset > this.offSetPValue) {
        const diff =
          (this.windowRefService.nativeWindow.pageYOffset - this.offSetPValue) > this.offSetValue ?
            this.offSetValue : (this.windowRefService.nativeWindow.pageYOffset - this.offSetPValue);
        this.rendererService.renderer.setStyle(headerAreaScroll, 'display', 'initial');
        this.rendererService.renderer.setStyle(headerAreaScroll, 'top', `${diff}px`);
        this.rendererService.renderer.setStyle(headerAreaScroll, 'position', 'fixed');
      }
      if (headerAreaScroll && this.windowRefService.nativeWindow.pageYOffset <= this.offSetPValue) {
        this.rendererService.renderer.setStyle(headerAreaScroll, 'top', '-38px');
        this.rendererService.renderer.setStyle(headerAreaScroll, 'display', 'none');
      }
      if (this.slideContent && this.windowRefService.nativeWindow.pageYOffset > (this.slideContent.offsetHeight - this.offSetPValue)) {
        this.rendererService.renderer.setStyle(headerAreaScroll, 'display', 'none');
      }
    }
  }

  /**
   * initial scores and clock updates form the event comments
   * @returns {void}
   */
  initScoresFromEventComments(): void {
    if (this.event && this.event.scores) {
      this.homeName = this.event.scores.home.name;
      this.awayName = this.event.scores.away.name;
      this.homeScore = this.event.scores.home.score;
      this.awayScore = this.event.scores.away.score;
    }
    this.homeScore = this.homeScore || '0';
    this.awayScore = this.awayScore || '0';
    this.isMatchCompletedAndResulted();
    const eventName: string = this.event.name.replace(/[|,]/g, ''); // A v B
    [this.homeName, this.awayName] = eventName.split(/ v | vs | - /);
    this.flagHomeIcon = this.formFlagName(this.homeName);
    this.flagAwayIcon = this.formFlagName(this.awayName);
    this.isScoresAvailable = this.isTeamScoresAvailable();
    this.isHalfTime = this.isHalftime(this.event);
  }

  /**
   * Clock Update full/halfTime
   * @returns {void}
   */
  onClockUpdate(): void {
    this.isHalfTime = this.isHalftime(this.event);
    this.isFullTime = this.isFulltime(this.event);
  }

  /**
   * check if Match is Completed And Resulted
   * @returns {boolean}
   */
  isMatchCompletedAndResulted(): boolean {
    return this.event.isResulted && this.event.regularTimeFinished;
  }

  /**
   * set Event Live Status
   * @returns {void}
   */
  setEventLiveStatus(): void {
    this.eventIsLive = this.event.started && !this.event.regularTimeFinished;
  }

  /**
   * is Team Scores Available
   * @returns {boolean}
   */
  isTeamScoresAvailable(): boolean {
    return !!(this.homeScore && this.awayScore);
  }

  /**
   * check for the event commentary availabiltiy
   * @param  {ISportEvent} event
   * @returns {void}
   */
  updateEventCommentaryAvailability(event: IEventDetails): void {
    if (event && (event.started && !event.clock && !event.comments)) {
      this.isNoCommentaryAvailable = true;
    }
  }

  /**
   * leaderboard update handler is used to set initial data live for leader board and listen to subsequent changes
   * @param  { IEntrySummaryInfo } initialData
   * @returns void
   */
  leaderboardUpdateHandler(leaderboardData: ILeaderboardData): void {
    if(leaderboardData.ertFlag){
      this.pubSub.publish(PUBSUB_API.LEADERBOARD_EVENT_RESULTED);
    }
    if (this.initialRecordsCopy && this.initialRecordsCopy.length > 0) {
      this.shuffle(leaderboardData);
    } else {
      this.initialLbrEntries(leaderboardData);
    }
    if (leaderboardData.myEntries && leaderboardData.myEntries.length > 0) {
      this.pubSub.publish(PUBSUB_API.LEADERBOARD_UPDATE, { update: leaderboardData.myEntries });
    }
  }

  /**
   * initialLbrEntries is used to set initial data live for leader board
   * @param  { IEntrySummaryInfo } initialData
   * @returns void
   */
  initialLbrEntries(initialData: ILeaderboardData): void {
    if (initialData.myEntries && initialData.myEntries.length > 0) {
      this.initialEntrySummary(initialData.myEntries);
    }
    this.initialRecordsCopy = [];
    this.windowRefService.nativeWindow.clearInterval(this.timeOutListener);
    this.windowRefService.nativeWindow.clearInterval(this.interval);
    this.interval = null;
    this.timeOutListener = null;
    this.initialAllRecords = [];
    this.isLeaderboardLoaded = true;
    this.addAWSLog(initialData.leaderboard);
    this.getLiveOverlayData();
    this.initialAllRecords = initialData.leaderboard ? initialData.leaderboard.slice() : [];
    this.myEntriesFilter();
    this.myUserEntries = initialData.myEntries ? initialData.myEntries : [];
    this.myEntries = initialData.myEntries ? initialData.myEntries : [];
    this.userEntries = initialData.leaderboardUserEntries ? initialData.leaderboardUserEntries : [];
    this.timeOutListener = this.windowRefService.nativeWindow.setInterval(() => {
      const count: number = this.initialRecordsCopy.length;
      for (let index = count; index < count + LIVE_EVENT_VALUE.UPDATE_COUNT; index++) {
        if (this.initialAllRecords[index] && this.initialAllRecords) {
          this.initialRecordsCopy.push(this.initialAllRecords[index]);
          this.dataLoading = false;
          if (this.initialRecordsCopy.length === this.initialAllRecords.length) {
            if (this.myUserEntries.length !== LIVE_EVENT_VALUE.INITIAL_COUNT) {
              this.myEntriesFilter();
            }
            this.windowRefService.nativeWindow.clearInterval(this.timeOutListener);
          }
        }
      }
      this.leaderboardVal = this.validateLeaderBoardRecords(this.initialAllRecords.length);
    }, LIVE_EVENT_VALUE.TIME_INTERVAL);
  }

  /**
   * shuffle the records with delta and call change order
   * @param  { IEntrySummaryInfo } initialData
   * @returns void
   */
  shuffle(updatedLeaderBoardEntries: ILeaderboardData): void {
    this.updatedLeaderBoardEntries = [];
    this.updatedLeaderBoardEntries = updatedLeaderBoardEntries.leaderboard ? updatedLeaderBoardEntries.leaderboard.slice() : [];
    this.windowRefService.nativeWindow.clearInterval(this.timeOutListener);
    this.windowRefService.nativeWindow.clearInterval(this.interval);
    this.interval = null;
    this.timeOutListener = null;
    const updateDeltaTime = this.initDeltaTime();
    const processedDeltaIds = [];
    const updatedDeltaId = [];
    const initialRecordId = [];
    if (this.initialAllRecords.length > 0) {
      this.initialRecordsCopy = this.initialAllRecords;
    }
    updatedLeaderBoardEntries.leaderboard.forEach((entry: IEntrySummaryInfo) => {
      updatedDeltaId.push(entry.id);
    });
    this.leaderboardVal = this.validateLeaderBoardRecords(this.updatedLeaderBoardEntries.length);
    const initialDeltaIdsLen = updatedDeltaId.length;
    this.initialRecordsCopy.forEach((entry: IEntrySummaryInfo) => {
      initialRecordId.push(entry.id);
    });
    if (updatedLeaderBoardEntries.myEntries) {
      this.myUserEntries = updatedLeaderBoardEntries.myEntries;
      this.myEntries = updatedLeaderBoardEntries.myEntries;
      this.isMyEntriesLoaded = true;
    } else {
      this.myUserEntries = [];
      this.myEntries = [];
    }
    this.userEntries = updatedLeaderBoardEntries.leaderboardUserEntries ? updatedLeaderBoardEntries.leaderboardUserEntries : [];
    this.deltaRecordUpdatesCallBack(() => {
      updatedDeltaId.every((id) => {
        const matchedDeltaEntry = updatedLeaderBoardEntries.leaderboard.find(leaderBoardEntry => leaderBoardEntry && leaderBoardEntry.id === id);
        const matchedInitialEntry = this.initialRecordsCopy.find(leaderBoardEntry => leaderBoardEntry && leaderBoardEntry.id === id);
        if (initialRecordId.indexOf(id) !== -1 && matchedInitialEntry && matchedDeltaEntry &&
          typeof matchedDeltaEntry.index !== 'undefined' && typeof matchedInitialEntry.index !== 'undefined') { 

          this.changeOrder(matchedInitialEntry.index, matchedDeltaEntry.index, matchedDeltaEntry);
        } else if (matchedDeltaEntry && typeof matchedDeltaEntry.index !== 'undefined') {
          this.changeOrder(matchedDeltaEntry.index, matchedDeltaEntry.index, matchedDeltaEntry);
        }
        processedDeltaIds.push(id);
        const deltaIndex = updatedDeltaId.indexOf(id);
        updatedDeltaId.splice(deltaIndex, 1);
        if (initialDeltaIdsLen === processedDeltaIds.length) {
          this.initialRecordsCopy = [...this.initialRecordsCopy.reduce((map, obj) => map.set(obj.id, obj), new Map()).values()];
          this.initialAllRecords = this.initialRecordsCopy.slice();
          return false;
        }
      });
    }, updateDeltaTime, this.updatedLeaderBoardEntries.length);
    this.dataLoading = false;
  }

  /**
   * checks for the records
   * @param  { string } entryId
   * @returns boolean
   */
  checkIfRecordExist(entryId: string): boolean {
    return this.updatedLeaderBoardEntries && this.updatedLeaderBoardEntries.length > 0 ?
      this.updatedLeaderBoardEntries.findIndex(updatedEntry => (updatedEntry.id === entryId)) > -1 : true;
  }

  /**
   * change order to shift indexes
   * @param previuosIndex { number }
   * @param updatedIndex { number }
   * @param updateEntry { IEntrySummaryInfo }
   */
  changeOrder(previuosIndex: number, updatedIndex: number, updateEntry?: IEntrySummaryInfo): void {
    if (typeof previuosIndex !== 'undefined' && typeof updatedIndex !== 'undefined') {
      if (previuosIndex === updatedIndex && updateEntry) {
        this.initialRecordsCopy[previuosIndex] = updateEntry;
        this.updateState = 'sameUpdate';
      } else {
        const previousRankedIndex = this.initialRecordsCopy[previuosIndex].rankedIndex;
        const newIndex = this.initialRecordsCopy[updatedIndex];
        this.initialRecordsCopy[updatedIndex] = this.initialRecordsCopy[previuosIndex];
        this.initialRecordsCopy[previuosIndex] = newIndex;
        this.initialRecordsCopy[previuosIndex].index = previuosIndex;
        this.initialRecordsCopy[previuosIndex].rankedIndex = previousRankedIndex;
        this.initialRecordsCopy[updatedIndex] = updateEntry;
        this.updateState = 'swapping';
      }
      this.changeDetectorRef.detectChanges();
    }
  }
  /**
   * @returns void
   * Triggers when user comes back from offline to online
   */
  reloadComponent(): void {
    this.pubSub.subscribe(this.componentId, this.pubSub.API.RELOAD_COMPONENTS, () => {
      this.liveServConnectionService.closeConnection();
      this.liveServConnectionService.connect()
        .subscribe(() => {
          this.dataLoading = true;
          this.ngOnDestroy();
          this.ngOnInit();
        });
    });
  }

  /**
   * Get Initial Live Overlay data to display button
   * @returns void
   */
  getInitialLiveOverlayData(): void {
    this.cmsService.getWelcomeOverlay().subscribe((response: IWelcomeOverlay) => {
      this.welcomeCard = response;
    }, (error) => {
      console.warn(error);
    });
  }

  /**
   * showOverlay on clicking Rules button and Ga track
   * @returns {void}
   */
  showOverlayFunction(): void {
    this.showOverlay = true;
    const gtmData = GTM_RULES_DATA;
    this.gtmService.push('trackEvent', gtmData);
  }

  /**
   * Method for live event tutorial
   * @returns void
   */
  triggerLiveTutorial(): void {
    this.cmsService.getWelcomeOverlay().subscribe((response: IWelcomeOverlay) => {
      const trackingObj = LIVE_OVERLAY.TUTORIAL_GA_TRACKING;
      this.gtmService.push('trackEvent', trackingObj);
      this.welcomeCard = response;
      this.isOverlayLoaded = true;
      this.initWelcomeOverlay(this.welcomeCard.overlayEnabled); this.liveManualTutorial = true;
      this.showLiveOverlay = false;
      this.changeDetectorRef.detectChanges();
      this.showLiveOverlay = true;
    }, (error) => {
      console.warn(error);
    });
  }

  /**
   * To unsubscribe to all the channels
   * @param {string} channel
   * @param {function} handler
   * @returns {void}
   */
  private unSubscribeChannel(channel: string, handler: Function) {
    if (channel) {
      this.fiveAsideLiveServeUpdatesSubscribeService.unSubscribeShowDownChannels([channel], handler);
    }
  }
  /**
   *
   * @returns record update time
   */
  private initDeltaTime() {
    const deltaCount = this.updatedLeaderBoardEntries.length;
    return deltaCount > 50 ? (1 / deltaCount) * 10000 : (1 / deltaCount) * 1000;
  }

  /**
   * myEntriesFilter to filter the userentries based on lbrentries
   * @returns {void}
   */
  private myEntriesFilter(): void {
    this.entryIdList = this.myUserEntries.map(({ id }) => id);
    this.pubSub.publish(PUBSUB_API.PUBLISH_LEADERBOARD);
  }

  /**
   * run loop till delta updates records is completed
   * @param callback { function }
   * @param delay { number }
   * @param repetitions { number }
   */
  private deltaRecordUpdatesCallBack(callback: Function, delay: number, repetitions: number): void {
    let count: number = 0;
    this.interval = this.windowRefService.nativeWindow.setInterval(() => {
      callback();
      if (++count === repetitions) {
        // to remove stale records
        this.initialRecordsCopy.forEach((record) =>{
          record.hidden = !this.checkIfRecordExist(record.id);
        });
        this.windowRefService.nativeWindow.clearInterval(this.interval);
      }
    }, delay);
  }

  /**
   * Checks if match time is half time
   * @param  {ISportEvent} event
   * @returns boolean
   */
  private isHalftime(event: IEventDetails): boolean {
    const eventClock = event.clock;
    return !!eventClock && eventClock.matchTime === Time.HALF_TIME;
  }

  /**
   * Checks if match time is full time
   * @param  {ISportEvent} event
   * @returns boolean
   */
  private isFulltime(event: IEventDetails): boolean {
    const eventClock = event.clock;
    return !!eventClock && eventClock.matchTime === Time.FULL_TIME;
  }

  /**
   * subscribe for the live updates from score clock eventchannels
   * @returns {void}
   */
  private getLiveupdatesubscription(): void {
    this.pubSub.subscribe(this.componentId, PUBSUB_API.SHOWDOWN_LIVE_SCORE_UPDATE, (updates: IShowdownOptaUpdate) => {
      if (updates && Number(this.event.id) === updates.id && updates.payload && updates.payload.scores
        && updates.payload.scores.home !== null && updates.payload.scores.away != null) {
        const scoreUpdate = updates.payload.scores;
        this.homeScore = scoreUpdate.home.score;
        this.awayScore = scoreUpdate.away.score;
        this.isScoresAvailable = this.isTeamScoresAvailable();
      }
    });
    this.pubSub.subscribe(this.componentId, PUBSUB_API.SHOWDOWN_LIVE_CLOCK_UPDATE, (updates: IShowdownOptaUpdate) => {
      if (updates && Number(this.event.id) === updates.id && updates.payload) {
        this.fiveAsideLiveServeUpdatesService.eventClockUpdate(updates.payload, this.event as any);
        this.onClockUpdate();
        this.createClockUpdate(updates);
        this.changeDetectorRef.detectChanges();
      }
    });
    this.pubSub.subscribe(this.componentId, PUBSUB_API.SHOWDOWN_LIVE_EVENT_UPDATE, (updates: IShowdownOptaUpdate) => {
      if (updates && Number(this.event.id) === updates.id && updates.payload) {
        this.fiveAsideLiveServeUpdatesService.updateEventLiveData(this.event as any, updates);
        this.setEventLiveStatus();
        this.onClockUpdate();
      }
    });
  }
  /**
   * check Commentary to be called for Event
   * @param  {ISportEvent} event
   * @returns {boolean}
   */
  private checkCommentaryToBeCalledForEvent(event: IEventDetails): boolean {
    return !(event.clock || event.comments) && !this.isNoCommentaryAvailable;
  }

  /**
   * To decode initial contest information received from leaderboard component
   * @returns {void}
   */
  private decodeInitialData(): void {
    this.contestInfo = this.leaderboardData;
    if (!this.contestInfo.display) {
      this.navigationService.openRouterUrl(LEADERBOARD_WIDGET.LOBYY_URL, true);
    }
    this.showServiceMessage = this.contestInfo.enableServiceMsg;
    this.initContestDetails();
    this.cmsService.getTeamsColors([this.homeName, this.awayName], '16').subscribe((response: ITeamColor[]) => {
        this.teamColors = response;
        this.hasTeamImage = this.showDownService.hasImageForHomeAway(this.teamColors);
        this.teamColors = this.showDownService.setDefaultTeamColors(this.teamColors,
          [this.homeName, this.awayName]);
      },
      () => {
        this.showError();
        this.navigationService.openRouterUrl(LEADERBOARD_WIDGET.LOBYY_URL, true);
      });
  }

  /**
   * fetch Initial Data Of Event
   * @returns {void}
   */
  private fetchInitialDataOfEvent(): void {
    const contestId: string = this.route.snapshot.params.id;
    const username: string = this.userService.username;
    const bppToken: string = this.userService.bppToken;
    this.showDownService.getContestInformationById(contestId, username, bppToken)
      .subscribe((response: IShowDownResponse) => {
        this.leaderboardData = response.contest;
        this.decodeInitialData();
      });
  }

  /**
   * to get the initial contest Details for the entry
   */
  private initContestDetails() {
    this.events = this.contestInfo.eventDetails;
    this.event = this.events;
    this.eventId = this.contestInfo.eventDetails.id;
    if (this.checkCommentaryToBeCalledForEvent(this.event)) {
      if (this.event.clockData) {
        this.fiveAsideLiveServeUpdatesService.eventClockUpdate(this.event.clockData, this.event as any);
        this.createClockForEventFromInit();
      }
      //this.fiveASideShowDownLobbyService.addScoresAndClockForEvents(this.events);
      this.event = this.events;
      this.eventArray = [this.eventId.toString()];
      this.initScoresFromEventComments();
      this.updateEventCommentaryAvailability(this.event);
      this.setEventLiveStatus();
    }
    this.changeDetectorRef.detectChanges();
    this.unsubscribeForLiveServeConnection();
    this.openLiveServConnection();
    this.onClockUpdate();
    this.getInitialLeaderBoardData();
  }


  /**
   * create a clock initially
   * @returns {void}
   */
  private createClockForEventFromInit(): void {
    if (!this.event.clock && this.event.started) { //
      const serverTimeDelta = this.timeSyncService.getTimeDelta();
      const clockData = this.event.clockData;
      this.event.clock = this.liveEventClockProviderService.create(serverTimeDelta, clockData);
    }
  }

  /**
   * form the Flag Name
   * @param  {string} name
   * @returns string
   */
  private formFlagName(name: string): string {
    const teamName: string = name.toLowerCase().split(' ').join('_');
    return this.localeService.getString('fs.flagIcon', { teamName });
  }

  /**
   * set scroll Listeners
   * @returns {void}
   */
  private setScrollListeners(): void {
    this.windowRefService.nativeWindow.document.addEventListener('scroll', this.scrollHandler.bind(this));
  }

  /**
   * remove scroll Listeners
   * @returns {void}
   */
  private removeScrollListeners(): void {
    this.windowRefService.nativeWindow.document.removeEventListener('scroll', this.scrollHandler.bind(this));
  }

  /**
   * Init Live Tutorial data
   * @returns void
   */
  private getLiveOverlayData(): void {
    this.liveOverlaySeen = this.windowRefService.nativeWindow.localStorage.getItem(LIVE_OVERLAY.OVERLAY);
    this.welcomeOverlaySeen = this.windowRefService.nativeWindow.localStorage.getItem(LIVE_OVERLAY.WELCOME_OVERLAY);
    if ((!this.welcomeOverlaySeen || !this.liveOverlaySeen) && this.isMyEntriesLoaded
      && this.isLeaderboardLoaded && !this.isOverlayLoaded) {
      this.cmsService.getWelcomeOverlay().subscribe((response: IWelcomeOverlay) => {
        this.welcomeCard = response;
        this.isOverlayLoaded = true;
        this.initWelcomeOverlay(this.welcomeCard.overlayEnabled);
      }, (error) => {
        console.warn(error);
      });
    }
  }

  /**
   * Display welcome overlay handler
   * @param  {boolean} overlayEnabled
   */
  private initWelcomeOverlay(overlayEnabled: boolean) {
    this.liveOverlaySeen = this.windowRefService.nativeWindow.localStorage.getItem(LIVE_OVERLAY.OVERLAY);
    this.welcomeOverlaySeen = this.windowRefService.nativeWindow.localStorage.getItem(LIVE_OVERLAY.WELCOME_OVERLAY);
    if (overlayEnabled) {
      if (this.welcomeOverlaySeen && !this.liveOverlaySeen) {
        this.liveManualTutorial = false;
        this.showLiveOverlay = true;
      } else if (!this.welcomeOverlaySeen) {
        this.showLiveOverlay = true;
      }
    }
  }

  /**
   * Checking the length of initial data
   * @param {number} length
   * @returns string
   */
  private validateLeaderBoardRecords(length: number): string {
    return length < 100 ? `${length}` : '100';
  }
  /**
   * Adds AWS Log
   * @param {Array<IEntrySummaryInfo>} initialData
   * @returns void
   */
  private addAWSLog(initialData: Array<IEntrySummaryInfo>): void {
    if (initialData) {
      this.awsService.addAction('SHOWDOWN=>INITIAL_LEADERBOARD_COUNT', { count: initialData.length });
    }
  }

  /**
   * Create clock for the inplay event if not available
   * @param  {IShowdownOptaUpdate} update
   * @returns void
   */
  private createClockUpdate(update: IShowdownOptaUpdate): void {
    if (!this.event.clock) {
      const serverTimeDelta = this.timeSyncService.getTimeDelta();
      const clockData = update.payload as any;
      this.event.clock = this.liveEventClockProviderService.create(serverTimeDelta, clockData);
    }
  }

}
