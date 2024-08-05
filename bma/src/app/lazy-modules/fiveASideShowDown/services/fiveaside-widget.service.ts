import { Injectable } from '@angular/core';
import { FiveASideShowDownApiModule } from '@app/fiveASideShowDown/fiveASideShowDown-api.module';
import { ILeaderBoardWidget } from '@lazy-modules/fiveASideShowDown/models/leader-board-widget';
import { FiveasideRulesEntryAreaService } from '@app/fiveASideShowDown/services/fiveaside-rules-entry-area.service';
import { FiveASideShowDownLobbyService } from '@app/fiveASideShowDown/services/fiveaside-show-down-lobby.service';
import { Time } from '@app/fiveASideShowDown/constants/enums';
import { IEventDetails, IShowDown } from '@app/fiveASideShowDown/models/show-down';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { PUBSUB_API } from '@app/fiveASideShowDown/constants/constants';
import { TimeSyncService } from '@app/core/services/timeSync/time-sync.service';
import { LiveEventClockProviderService } from '@app/shared/components/liveClock/live-event-clock-provider.service';
import { FiveAsideLiveServeUpdatesService } from '@app/fiveASideShowDown/services/fiveaside-live-serve-updates.service';
import { ILiveClock } from '@app/core/models/live-clock.model';
import { IShowdownOptaUpdate } from '@root/app/fiveASideShowDown/models/IShowdownOptaUpdate.model';

@Injectable({
  providedIn: FiveASideShowDownApiModule
})
export class FiveasideWidgetService {

  constructor(private lobbyService: FiveASideShowDownLobbyService,
    private rulesService: FiveasideRulesEntryAreaService,
    private pubSub: PubSubService,
    private timeSyncService: TimeSyncService,
    private liveEventClockProviderService: LiveEventClockProviderService,
    private fiveAsideLiveServeUpdatesService: FiveAsideLiveServeUpdatesService
    ) { }

  /**
   * To Get Event Live Status
   * @param {ISportEvent} event
   * @param {ILeaderBoardWidget} widget
   * @returns {void}
   */
  getEventLiveStatus(event: IEventDetails, widget: ILeaderBoardWidget): void {
    widget.isLive = event.started && !event.regularTimeFinished;
    if (event.regularTimeFinished) {
      this.pubSub.publish(PUBSUB_API.SHOWDOWN_LIVE_EVENT_RESULTED, event.id.toString());
    }
  }

  /**
   * To Set score and clock data from comments
   * @param {ISportEvent} eventEntity
   * @param {ILeaderBoardWidget} widget
   * @returns {void}
   */
  setScoresFromEventComments(eventEntity: IEventDetails, widget: ILeaderBoardWidget, update?: IShowdownOptaUpdate): void {
    if (update) {
      this.fiveAsideLiveServeUpdatesService.createEventScoreComments(update.payload, eventEntity as any);
    }
    const teamNames: {[key:string]: string} = this.lobbyService.getTeamNameFromEventComments(eventEntity as any);
    widget.homeTeam = teamNames.homeTeam;
    widget.awayTeam = teamNames.awayTeam;
    widget.homeIcon = this.rulesService.formFlagName(teamNames.homeTeam);
    widget.awayIcon = this.rulesService.formFlagName(teamNames.awayTeam);
    widget.isResulted = this.getEventResultedStatus(eventEntity);
    widget.homeScore = this.getTeamScore(eventEntity, 'home');
    widget.awayScore = this.getTeamScore(eventEntity, 'away');
    widget.hasTeamScores = this.hasTeamScores(widget.homeScore, widget.awayScore);
    this.clockUpdate(eventEntity, widget);
  }

  /**
   * To Set score from Opta update
   * @param  {IEventDetails} eventEntity
   * @param  {ILeaderBoardWidget} widget
   * @param  {IShowdownOptaUpdate} update?
   * @returns void
   */
  setScoresFromOptaUpdate(eventEntity: IEventDetails, widget: ILeaderBoardWidget, update?: IShowdownOptaUpdate): void {
    if (update.payload.scores && update.payload.scores.home !== null && update.payload.scores.away != null) {
      const scoreUpdate = update.payload.scores;
      widget.homeScore = scoreUpdate.home.score;
      widget.awayScore = scoreUpdate.away.score;
      widget.hasTeamScores = this.hasTeamScores(widget.homeScore, widget.awayScore);
    }
  }

  /**
   * To build leaderboards data with socres and clock
   * @param {IEventContest[]} leaderBoards
   * @param {string[]} events
   * @returns {void}
   */
  buildLeaderBoardData(leaderBoards: IShowDown[], events: string[]): void {
    leaderBoards.forEach((widget: IShowDown, index: number) => {
      if (widget.eventDetails && widget.eventDetails.id) {
        widget.active = this.setActiveWidget(index);
        events.push(widget.eventDetails.id.toString());
        if (widget.eventDetails.clockData) {
          this.fiveAsideLiveServeUpdatesService.eventClockUpdate(widget.eventDetails.clockData, widget.eventDetails as any);
          this.createClockWithClockData(widget.eventDetails);
        }
      }
    });
  }

  /**
   * Handler for clock update
   * @param {ISportEvent} eventEntity
   * @param {ILeaderBoardWidget} widget
   * @returns {void}
   */
  clockUpdate(eventEntity: IEventDetails, widget: ILeaderBoardWidget, update?: IShowdownOptaUpdate): void {
    const eventClock = eventEntity.clock;
    if (eventClock) {
      widget.isHalfTime = eventClock.matchTime === Time.HALF_TIME;
      widget.isFullTime = eventClock.matchTime === Time.FULL_TIME;
    }
    if (update) {
      this.createClockForEventEntity(eventEntity, update);
    }
  }

  /**
   * Creation of clock with clock data initially
   * @param  {IEventDetails} eventDetails
   * @returns void
   */
  private createClockWithClockData(eventDetails: IEventDetails): void {
    if (!eventDetails.clock && eventDetails.started) {
      const serverTimeDelta = this.timeSyncService.getTimeDelta();
      const clockData = eventDetails.clockData;
      eventDetails.clock = this.liveEventClockProviderService.create(serverTimeDelta, clockData);
    }
  }

  /**
   * To create clock for the event when clock is not present
   * @param  {ISportEvent} eventEntity
   * @param  {IShowdownOptaUpdate} update
   * @returns void
   */
  private createClockForEventEntity(eventEntity: IEventDetails, update: IShowdownOptaUpdate): void {
    if (!eventEntity.clock && eventEntity.started) {
      const serverTimeDelta: number = this.timeSyncService.getTimeDelta();
      const clockData: ILiveClock = this.liveServeUpdatetoClockDataMapper(update);
      eventEntity.clock = this.liveEventClockProviderService.create(serverTimeDelta, clockData);
    }
  }

  /**
   * Transform sCLOCK update payload to clock data
   * @param  {IShowdownOptaUpdate} update
   * @returns ILiveClock
   */
  private liveServeUpdatetoClockDataMapper(update: IShowdownOptaUpdate): ILiveClock {
    const clockData = {} as ILiveClock;
    if (update.payload) {
      clockData.ev_id = Number(update.payload.ev_id);
      clockData.clock_seconds = update.payload.clock_seconds;
      clockData.last_update = update.payload.last_update;
      clockData.last_update_secs = update.payload.last_update_secs;
      clockData.offset_secs = update.payload.offset_secs;
      clockData.period_code = update.payload.period_code;
      clockData.sport = update.payload.sport;
      clockData.start_time_secs = update.payload.start_time_secs;
      clockData.state = update.payload.state;
      clockData.period_index = update.payload.period_index;
      return clockData;
    }
    return null;
  }

  /**
   * To Set active Widget
   * @param {number} index
   * @returns {boolean}
   */
  private setActiveWidget(index: number): boolean {
    return index === 0;
  }

  /**
   * To fetch event resulted status
   * @param {ISportEvent} eventEntity
   * @returns {boolean}
   */
  private getEventResultedStatus(eventEntity: IEventDetails): boolean {
    return eventEntity.regularTimeFinished;
  }

  /**
   * To check if team has scored
   * @param {string} homeScore
   * @param {string} awayScor
   * @returns {boolean}
   */
  private hasTeamScores(homeScore: string, awayScore: string): boolean {
    return !!(homeScore && awayScore);
  }

  /**
   * To fetch team score if exists
   * @param {ISportEvent} event
   * @param {string} team
   * @returns {string}
   */
  private getTeamScore(event: IEventDetails, team: string): string {
    if (event && event.scores) {
      return event.scores[team].score;
    }
    return null;
  }
}
