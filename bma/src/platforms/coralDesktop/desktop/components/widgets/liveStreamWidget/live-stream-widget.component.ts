import { Component, Input, OnDestroy, OnInit, ViewEncapsulation } from '@angular/core';
import * as _ from 'underscore';
import { ISportEvent } from '@core/models/sport-event.model';
import { IMarket } from '@core/models/market.model';
import { FiltersService } from '@core/services/filters/filters.service';
import { UserService } from '@core/services/user/user.service';
import { RoutingHelperService } from '@core/services/routingHelper/routing-helper.service';
import { LiveStreamWidgetService } from '@desktop/components/widgets/liveStreamWidget/liveStreamWidgetService/live-stream-widget.service';
import { SportEventHelperService } from '@core/services/sportEventHelper/sport-event-helper.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { IScores } from '@desktop/models/live-stream-widget.model';
import { IOutcome } from '@core/models/outcome.model';
import { ITeams } from '@core/models/teams.model';
import { AbstractOutletComponent } from '@shared/components/abstractOutlet/abstract-outlet.component';
import { InplayHelperService } from '@coralDesktop/inPlay/services/inPlayHelper/inplay-helper.service';
import { Subscription } from 'rxjs';

@Component({
  selector: 'live-stream-widget',
  templateUrl: './live-stream-widget.component.html',
  styleUrls: ['./live-stream-widget.component.scss'],
  // eslint-disable-next-line
  encapsulation : ViewEncapsulation.None
})
export class LiveStreamWidgetComponent extends AbstractOutletComponent implements OnInit, OnDestroy {
  @Input() categoryId: number;
  @Input() sportName: string;

  isExpanded: boolean = true;
  isLoggedIn: boolean;
  widgetTitle: string = 'Watch Live';
  widgetMoreLink: string = '/live-stream';
  widgetMoreTitle: string = 'View All Live Streaming Events';

  event: ISportEvent;
  outcomes: IOutcome[];
  teams: ITeams;
  scores: IScores[];
  category: string = '';
  edpUrl: string;

  private isFirstTimeCollapsed: boolean = false;
  private deletedEventIds: number[] = [];
  private readonly title = 'liveStreamWidget';
  private dataSubscription: Subscription;

  constructor(
    private pubSubService: PubSubService,
    private sportEventHelperService: SportEventHelperService,
    private liveStreamWidgetService: LiveStreamWidgetService,
    private routingHelperService: RoutingHelperService,
    private userService: UserService,
    private filtersService: FiltersService,
    private inplayHelperService: InplayHelperService
  ) {
    super();
  }

  ngOnInit(): void {
    this.isLoggedIn = this.userService.status;
    this.pubSubService.subscribe(this.title, this.pubSubService.API.SET_PLAYER_INFO, user => (this.isLoggedIn = user.status));
    this.pubSubService.subscribe(this.title, this.pubSubService.API.DELETE_SELECTION_FROMCACHE,
      (updateData: { selectionId: string; marketId: string; eventId: string; }) => this.handleSelectionDeletion(updateData));

    this.pubSubService.subscribe(this.title, this.pubSubService.API.DELETE_EVENT_FROM_CACHE, (eventId: number) => {
      if (this.notCurrentOrDeletedEvent(eventId)) {
        return;
      }
      this.deletedEventIds.push(eventId);
      this.reloadComponent();
    });

    this.pubSubService.subscribe(this.title, this.pubSubService.API.RELOAD_IN_PLAY, () => {
      this.reloadComponent();
    });

    this.getLiveStreamEvents();
  }

  ngOnDestroy(): void {
    this.dataSubscription && this.dataSubscription.unsubscribe();

    this.pubSubService.unsubscribe(this.title);
    if (this.event) {
      this.inplayHelperService.unsubscribeForLiveUpdates([this.event]);
    }
    this.event = null;
  }

  trackById(index: number, outcome: IOutcome): string {
    return outcome && outcome.id ? `${outcome.id}_${index}` : index.toString();
  }

  /**
   * Get Live Stream Events Data
   */
  getLiveStreamEvents(): void {
    this.dataSubscription = this.liveStreamWidgetService.getData(this.categoryId, this.sportName, this.deletedEventIds)
      .subscribe((event: ISportEvent) => {
        this.hideSpinner();
        if (!event) {
          this.toggleWidgetVisibility(false);
          return;
        }
        this.event = event;
        this.toggleWidgetVisibility(true);
        this.initStreamViewData();
      }, (error: string) => console.warn(error));
  }

  /**
   * send GTM tracking, collapse accordion
   */
  sendCollapseGTM(): void {
    if (this.isFirstTimeCollapsed) {
      return;
    }
    this.liveStreamWidgetService.sendGTM('collapse', this.sportName);
    this.isFirstTimeCollapsed = true;
  }

  /**
   * send GTM tracking, view all
   */
  sendViewAllGTM(): void {
    this.liveStreamWidgetService.sendGTM('view all', this.sportName);
  }

  /**
   * send GTM tracking, play button
   */
  sendPlayGTM(): void {
    this.liveStreamWidgetService.sendGTM('play', this.sportName);
  }

  /**
   * send GTM tracking, register link
   */
  sendRegisterGTM(event): void {
    if (event.target.tagName === 'A') {
      this.liveStreamWidgetService.sendGTM('register link', this.sportName);
    }
  }

  /**
   * Get score for team
   * @return {string}
   */
  getOddsScore(): string {
    const teamA = this.sportEventHelperService.getOddsScore(this.event, 'teamA');
    const teamB = this.sportEventHelperService.getOddsScore(this.event, 'teamB');
    return `${teamA} - ${teamB}`;
  }

  /**
   * Returns current points for team
   * @returns {string}
   */
  getCurrentOddsScore(): string {
    const teamA = this.sportEventHelperService.getEventCurrentPoints(this.event, 'teamA');
    const teamB = this.sportEventHelperService.getEventCurrentPoints(this.event, 'teamB');
    return `${teamA} - ${teamB}`;
  }

  /**
   * Check if event type is tennis
   * @returns {boolean}
   */
  isTennis(): boolean {
    return this.category === 'Tennis';
  }

  /**
   * Get Sets Scores
   * @param setScores
   * @returns {string}
   */
  getSetsScores(setScores: IScores): string {
    const teamA = setScores[this.teams.player_1.id];
    const teamB = setScores[this.teams.player_2.id];
    return teamA && teamB ? `${teamA} - ${teamB}` : '';
  }

  /**
   * Check if event is live
   * @returns {boolean}
   */
  isLive(): boolean {
    return this.sportEventHelperService.isLive(this.event) && !this.isHalfTime() && !this.isClock() && !this.getSetIndex();
  }

  /**
   * Check if event has Half Time
   * @returns {*|boolean}
   */
  isHalfTime(): boolean {
    return this.sportEventHelperService.isHalfTime(this.event);
  }

  /**
   * Check if event has clock;
   * @returns {boolean}
   */
  isClock(): boolean {
    return this.sportEventHelperService.isClockAllowed(this.event) && !this.isHalfTime();
  }

  /**
   * Show login dialog
   */
  openLoginDialog(): void {
    this.liveStreamWidgetService.sendGTM('login link', this.sportName);
    this.pubSubService.publish(this.pubSubService.API.OPEN_LOGIN_DIALOG, { moduleName: 'livestream' });
  }

  /**
   * Build string of set number (Example: Set 1)
   * @returns {string}
   */
  getSetIndex(): string {
    return this.sportEventHelperService.getTennisSetIndex(this.event);
  }

  /**
   * Get Header to Odds Button
   * @param {Number} minorCode
   * @param {Number} $index
   * @returns {string}
   */
  getOddsHeader(minorCode: number, $index: number): string {
    const index = minorCode - 1 || $index;
    const headTitles = (this.liveStreamWidgetService.findOddsHeader(
      this.market,
      this.category,
      false)  as string).split(',');

    return headTitles[index];
  }

  /**
   * Checks if odds button should be shown
   * @param {Number} index of odds button
   * @returns {boolean}
   */
  isShowOddButton(index: number): boolean {
    const columns: any = this.liveStreamWidgetService.findOddsHeader(this.market, this.category, true);
    const columns2 = columns && columns.columns2;
    const columns3 = columns && columns.columns3;
    return (((!columns2 || (columns2 && index !== 1)) && columns3) || (!columns3 && index !== 1));
  }

  /**
   * Check if Cashout is enabled for event
   * @returns {Boolean}
   */
  isCashOutEnabled(): boolean {
    return this.sportEventHelperService.isCashOutEnabled(this.event);
  }

  get market(): IMarket | null {
    return (this.event && this.event.markets && this.event.markets.length) ? this.event.markets[0] : null;
  }

  set market(value: IMarket | null){}

  private notCurrentOrDeletedEvent(eventId: number): boolean {
    return (this.event && this.event.id !== eventId) || this.deletedEventIds.includes(eventId);
  }

  private toggleWidgetVisibility(showWidget: boolean): void {
    this.pubSubService.publish(this.pubSubService.API.WIDGET_VISIBILITY, { liveStream: showWidget });
  }

  private handleSelectionDeletion(updateData: { selectionId: string; marketId: string; eventId: string; }): void {
    if (this.event && this.event.id === +updateData.eventId) {
      const outcomeIndex = (this.outcomes || []).findIndex(outcome => outcome && outcome.id === updateData.selectionId);

      if (outcomeIndex >= 0) {
        this.outcomes[outcomeIndex] = undefined;
      }
    }
  }

  private initStreamViewData(): void {
    this.category = this.event.categoryName;
    this.teams = this.event.comments && this.event.comments.teams;
    this.edpUrl = `/${this.routingHelperService.formEdpUrl(this.event)}/all-markets/watch-live`;
    this.scores = this.event.comments && _.toArray(this.event.comments.setsScores);
    this.outcomes = this.sortOutcomes();
  }

  /**
   * Get sorted outcomes
   * @returns {IOutcome[]}
   */
  private sortOutcomes(): IOutcome[] {
    const outcomes = this.market && this.market.outcomes;
    if (outcomes && outcomes.length > 0) {
      return _.map(this.filtersService.groupBy(outcomes,
        'correctedOutcomeMeaningMinorCode'), value => value[0]);
    }
  }
}
