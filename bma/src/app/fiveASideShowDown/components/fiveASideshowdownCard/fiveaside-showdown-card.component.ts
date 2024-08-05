import { ChangeDetectorRef, Component, Input, OnDestroy, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { PubSubService } from '@app/core/services/communication/pubsub/pubsub.service';
import { CoreToolsService } from '@app/core/services/coreTools/core-tools.service';
import { IShowdownCard, IShowdownCardDetails, IShowdownCardSignPostings } from '@app/fiveASideShowDown/models/showdown-card.model';
import { FiveAsideLiveServeUpdatesService } from '@app/fiveASideShowDown/services/fiveaside-live-serve-updates.service';
import { FiveASideShowDownLobbyService } from '@app/fiveASideShowDown/services/fiveaside-show-down-lobby.service';
import { SHOWDOWN_CARDS, PUBSUB_API } from '@app/fiveASideShowDown/constants/constants';
import { GtmService } from '@app/core/services/gtm/gtm.service';
import environment from '@environment/oxygenEnvConfig';
import { WindowRefService } from '@app/core/services/windowRef/window-ref.service';
import { DomToolsService } from '@app/core/services/domTools/dom.tools.service';
import { ITeamColor } from '@app/fiveASideShowDown/models/team-color';
import { FiveasideLeaderBoardService } from '@app/fiveASideShowDown/services/fiveaside-leader-board.service';
import { LiveEventClockProviderService } from '@app/shared/components/liveClock/live-event-clock-provider.service';
import { TimeSyncService } from '@app/core/services/timeSync/time-sync.service';
import { IShowdownOptaUpdate } from '../../models/IShowdownOptaUpdate.model';
import { IEventDetails } from '../../models/show-down';

@Component({
  selector: 'fiveaside-showdown-card',
  template: ``
})

export class FiveASideShowdownCardComponent implements OnInit, OnDestroy {
  @Input() contestData: IShowdownCard;
  @Input() event: IEventDetails;
  @Input() categoryName: string;
  public contestDetails: IShowdownCardDetails;
  public componentId: string;
  public homeTeam: string;
  public awayTeam: string;
  public isMatchCompleted: boolean;
  public homeScore: string;
  public awayScore: string;
  public isScoresAvailable: boolean;
  public eventIsLive: boolean;
  public isMatchFT: boolean;
  public signPostingsInfo: IShowdownCardSignPostings;
  public isNoCommentaryAvailable = false;
  public ticketEntry: boolean = false;
  public userPrizeInfoAvailable: boolean = false;
  public teamColors: ITeamColor[] = [];
  public hasTeamImage: boolean;
  public timer: number;
  public isExtraTimePeriod: boolean;
  public isEventResulted: boolean;
  public staticMock;
  public staticMockScore;
  public staticMockEvent;
  readonly sponsorLogo = SHOWDOWN_CARDS.SPONSOR_LOGO;
  readonly voucherLogo = SHOWDOWN_CARDS.VOUCHER_LOGO;
  readonly SPONSOR_LOGO_BASE_PATH: string =
    environment.CMS_ROOT_URI + environment.FIVEASIDE.svgImagePath;
  readonly LAST_7_DAYS = SHOWDOWN_CARDS.LAST_7_DAYS;
  private readonly EXTRA_TIME_PERIODS: string[] = SHOWDOWN_CARDS.EXTRA_TIME_PERIODS;
  constructor(
    private pubSubService: PubSubService,
    private fiveASideShowDownLobbyService: FiveASideShowDownLobbyService,
    private fiveAsideLiveServeUpdatesService: FiveAsideLiveServeUpdatesService,
    private coreToolsService: CoreToolsService,
    private router: Router,
    protected gtmService: GtmService,
    protected windowRefService: WindowRefService,
    protected domToolsService: DomToolsService,
    protected showDownService: FiveasideLeaderBoardService,
    private timeSyncService: TimeSyncService,
    private liveEventClockProviderService: LiveEventClockProviderService,
    private changeDetectorRef: ChangeDetectorRef
  ) {
  }

  /**
   * Init method for component
   * @returns void
   */
  ngOnInit(): void {
    if (this.event && this.contestData) {
      if (this.event.clockData) {
        this.fiveAsideLiveServeUpdatesService.eventClockUpdate(this.event.clockData, this.event as any);
        this.createClockForEventForInit();
      }
      this.initShowdownCardDetails();
      this.registerLiveServeUpdateSubscriptions();
      this.changeDetectorRef.detectChanges();
    }
    this.domToolsService.scrollPageTop(0);
  }

  /**
   * Call the required init methods
   * @returns void
   */
  initShowdownCardDetails(): void {
    this.setEventLiveStatus();
    this.fiveASideShowDownLobbyService.setEventStateByStartDate(this.event, this.categoryName, this.isMatchFullTime);
    this.componentId = this.coreToolsService.uuid();
    this.initScoresFromEventComments();
    this.handleETClockUpdate();
    this.signPostingsInfo = this.fiveASideShowDownLobbyService.signPostingsPriority(this.contestData);
    this.contestDetails = this.fiveASideShowDownLobbyService.setContestSignPosting(this.contestData);
    this.initAssetManagementFlags();
  }

  /**
   * Init scores and team names from event
   * @returns void
   */
  initScoresFromEventComments(): void {
    const teamNames = this.fiveASideShowDownLobbyService.getTeamNameFromEventComments(this.event as any);
    this.homeTeam = teamNames['homeTeam'];
    this.awayTeam = teamNames['awayTeam'];
    this.isMatchCompleted = this.isMatchCompletedAndResulted();
    this.homeScore = this.event?.scores?.home?.score;
    this.awayScore = this.event?.scores?.away?.score;
    this.isScoresAvailable = this.isTeamScoresAvailable();
    this.isEventResulted = this.event?.regularTimeFinished;
  }

  /**
   * Update commentary availability status
   * @param  {ISportEvent} event
   * @returns void
   */
  updateEventCommentaryAvailability(event: IEventDetails): void {
    if (event && (event.started && !event.clock && !event.comments)) {
      this.isNoCommentaryAvailable = true;
    }
  }

  /**
   * Destroy method for component
   * @returns void
   */
  ngOnDestroy(): void {
    this.pubSubService.unsubscribe(this.componentId);
    this.windowRefService.nativeWindow.clearTimeout(this.timer);
  }

  /**
   * Navigate to leaderboard
   * @param  {string} id
   * @returns void
   */
  public gotoLeaderboard(id: string): void {
    this.showdownCardGATrack();
    this.router.navigate([SHOWDOWN_CARDS.LEADERBOARD_BASE_URL, id]);
  }

  /**
   * Checks if match time is half or full time
   * @returns {boolean}
   * @private
   */
  get isMatchPeriodStatus(): boolean {
    const clock = this.event?.clock;
    return clock && (clock.matchTime === 'HT' || clock.matchTime === 'PENS' || clock.matchTime === 'ET');
  }

  set isMatchPeriodStatus(value: boolean) { }

  /**
   * Check if match is FT or resulted (Completed)
   * @returns boolean
   */
  get isMatchFullTime(): boolean {
    const clock = this.event?.clock;
    this.isMatchFT = clock ? clock.matchTime === 'FT' : this.event?.regularTimeFinished;
    return this.isMatchFT;
  }

  set isMatchFullTime(value: boolean) { }

  /**
   * Returnn true if either match is FT or resulted
   * @returns boolean
   */
  get isMatchFTorResulted(): boolean {
    return this.isMatchFT || this.isEventResulted;
  }

  set isMatchFTorResulted(value: boolean) { }

  /**
   * Set Flags from asset manager
   * @param  {string} id
   * @returns void
   */
  private initAssetManagementFlags(): void {
    if (this.contestData.assets) {
      this.teamColors = this.contestData.assets;
      this.hasTeamImage = this.showDownService.hasImageForHomeAway(this.teamColors);
      this.teamColors = this.showDownService.setDefaultTeamColors(this.teamColors,
        [this.homeTeam, this.awayTeam]);
    }
  }

  /**
   * Register LiveServe update listeners and update event details
   * @returns void
   */
  private registerLiveServeUpdateSubscriptions(): void {
    this.pubSubService.subscribe(this.componentId, PUBSUB_API.SHOWDOWN_LIVE_SCORE_UPDATE, (update: IShowdownOptaUpdate) => {
      if (update && Number(this.event.id) === update.id && update.payload && update.payload.scores
        && update.payload.scores.home !== null && update.payload.scores.away != null) {
        const scoreUpdate = update.payload.scores;
        this.homeScore = scoreUpdate.home.score;
        this.awayScore = scoreUpdate.away.score;
        this.isScoresAvailable = this.isTeamScoresAvailable();
      }
    });
    this.pubSubService.subscribe(this.componentId, PUBSUB_API.SHOWDOWN_LIVE_CLOCK_UPDATE, (update: IShowdownOptaUpdate) => {
      if (update && Number(this.event.id) === update.id && update.payload) {
        this.fiveAsideLiveServeUpdatesService.eventClockUpdate(update.payload, this.event as any);
        this.createClockForEvent(update);
        this.handleETClockUpdate();
      }
    });
    this.pubSubService.subscribe(this.componentId, PUBSUB_API.SHOWDOWN_LIVE_EVENT_UPDATE, (update: IShowdownOptaUpdate) => {
      if (update && Number(this.event.id) === update.id && update.payload) {
        this.fiveAsideLiveServeUpdatesService.updateEventLiveData(this.event as any, update);
        this.setEventLiveStatus();
        this.setEventLiveStatusFromUpdate(update);
      }
    });
    this.pubSubService.subscribe(this.componentId, PUBSUB_API.SHOWDOWN_EVENT_STARTED, (eventId: string) => {
      if (eventId && Number(this.event.id) === Number(eventId)) {
        this.initEventStarted(this.event as any, Number(eventId));
        this.fiveASideShowDownLobbyService.setEventStateByStartDate(this.event);
        this.isMatchCompleted = this.isMatchCompletedAndResulted();
        this.isScoresAvailable = this.isTeamScoresAvailable();
        this.isEventResulted = this.event.regularTimeFinished;
        if (!this.isScoresAvailable) {
          this.homeScore = '0';
          this.awayScore = '0';
        }
      }
    });
  }

  /**
   * Handle ET during Extra Period
   * @returns void
   */
  private handleETClockUpdate(): void {
    if (this.event.clock) {
      this.isExtraTimePeriod = this.EXTRA_TIME_PERIODS.includes(this.event.clock.period_code);
    }
  }

  /**
   * Create clock for the inplay event if not available
   * @param  {ILiveServeUpd} update
   * @returns void
   */
  private createClockForEvent(update: IShowdownOptaUpdate): void {
    if (!this.event.clock && this.event.started) {
      const serverTimeDelta = this.timeSyncService.getTimeDelta();
      const clockData = update.payload as any;
      this.event.clock = this.liveEventClockProviderService.create(serverTimeDelta, clockData);
    }
  }

  /**
   * Create clock for the inplay event if not available
   * @param  {ILiveServeUpd} update
   * @returns void
   */
   private createClockForEventForInit(): void {
    if (!this.event.clock && this.event.started) {
      const serverTimeDelta = this.timeSyncService.getTimeDelta();
      const clockData = this.event.clockData;
      this.event.clock = this.liveEventClockProviderService.create(serverTimeDelta, clockData);
    }
  }

  /**
   * Method to handle event preplay to inplay
   * @param  {ISportEvent} event
   * @param  {number} eventId
   * @returns void
   */
  private initEventStarted(event: IEventDetails, eventId: number): void {
    if (event.started) {
      return;
    }
    event.started = true;
    this.eventIsLive = true;
  }

  /**
   * To check if match is completed and resulted
   * @returns boolean
   */
  private isMatchCompletedAndResulted(): boolean {
    return this.event && this.event.regularTimeFinished;
  }

  /**
   * Update event live status
   * @returns void
   */
  private setEventLiveStatus(): void {
    this.eventIsLive = this.event && this.event.started && !this.event.regularTimeFinished;
    if (this.event && this.event.regularTimeFinished) {
      this.pubSubService.publish(PUBSUB_API.SHOWDOWN_LIVE_EVENT_RESULTED, this.event.id);
    }
  }

  /**
   * Set Event Live status from LiveServe update
   * @param  {ILiveServeUpd} update
   * @returns void
   */
  private setEventLiveStatusFromUpdate(update: any): void {
    this.eventIsLive = update.payload.started && !update.payload.regular_time_finished; //regular_time_finished
    this.isEventResulted = update.payload.regular_time_finished;
  }

  /**
   * To check event scores available
   * @returns boolean
   */
  private isTeamScoresAvailable(): boolean {
    const homeScore = this.fiveASideShowDownLobbyService.isValidValue(this.homeScore);
    const awayScore = this.fiveASideShowDownLobbyService.isValidValue(this.awayScore);
    return homeScore && awayScore;
  }

  /**
   * Showdown Card GA tracking
   * @returns void
   */
  private showdownCardGATrack(): void {
    this.gtmService.push('trackEvent', {
      eventCategory: SHOWDOWN_CARDS.GA_TRACKING.eventCategory,
      eventAction: SHOWDOWN_CARDS.GA_TRACKING.eventAction,
      eventLabel: this.contestData.name,
      eventID: this.event.id
    });
  }
}
