import { Injectable } from '@angular/core';
import { ILiveServeUpd } from '@app/core/models/live-serve-update.model';
import { ISportEvent } from '@app/core/models/sport-event.model';
import { FiveASideShowDownLobbyService } from '@app/fiveASideShowDown/services/fiveaside-show-down-lobby.service';
import { FiveASideShowDownApiModule } from '@app/fiveASideShowDown/fiveASideShowDown-api.module';
import { CommentsService } from '@app/core/services/comments/comments.service';
import { ScoreParserService } from '@app/core/services/scoreParser/score-parser.service';
import { SportEventHelperService } from '@app/core/services/sportEventHelper/sport-event-helper.service';
import { IShowdownOptaPayload, IShowdownOptaUpdate } from '../models/IShowdownOptaUpdate.model';
import { IEventDetails } from '../models/show-down';


/**
 * Service to update event details with Liveserve updates
 */
@Injectable({
  providedIn: FiveASideShowDownApiModule
})
export class FiveAsideLiveServeUpdatesService {

  constructor(
    private fiveASideShowDownLobbyService: FiveASideShowDownLobbyService,
    private commentsService: CommentsService,
    private scoreParserService: ScoreParserService,
    private sportEventHelperService: SportEventHelperService
  ) { }

  /**
   * Update event comments with Liveserve update
   * @param  {ISportEvent} event
   * @param  {ILiveServeUpd} update
   * @returns void
   */
  updateEventComments(event: ISportEvent, update: ILiveServeUpd): void {
    // To be removed later
    // this.fiveASideShowDownLobbyService.eventCommentsUpdate(update.payload, event);
  }

  /**
   * Create Event comments when no comments are present in event
   * @param  {IShowdownOptaPayload} scoreboardData
   * @param  {ISportEvent} event
   * @returns void
   */
  createEventScoreComments(scoreboardData: IShowdownOptaPayload, event: ISportEvent): void {
    const methodName = `${event.categoryCode.toLowerCase()}UpdateExtend`;
    const extender = this.commentsService[methodName];
    const scoreType = this.scoreParserService.getScoreType(event.categoryId);

    if (!event.comments && extender && scoreType) {
      if (this.sportEventHelperService.isTennis(event)) {
        event.comments = { teams: { player_1: { id: `${event.id}` }, player_2: { id: `${event.id}` } } };
      } else {
        event.comments = { teams: { home: { eventId: event.id }, away: { eventId: event.id } } };
      }
      event.scoreType = scoreType;
      this.commentsService.updateSportScores(event.comments, scoreboardData);
    }
  }

  /**
   * Update event clock with Liveserve update
   * @param  {IPayload} payload
   * @param  {ISportEvent} event
   * @returns void
   */
  eventClockUpdate(payload: IShowdownOptaPayload, event: IEventDetails): void {
    if (payload && Number(payload.ev_id) === Number(event.id) && event.clock) {
      event.clock.refresh(payload);
    }
  }

  /**
   * Update event details and dateTime with Liveserve update
   * @param  {ISportEvent} event
   * @param  {IShowdownOptaUpdate} update
   * @returns void
   */
  updateEventLiveData(event: IEventDetails, update: IShowdownOptaUpdate): void {
    event.isResulted = update.payload.regular_time_finished;
    event.regularTimeFinished = update.payload.regular_time_finished;
    this.fiveASideShowDownLobbyService.setEventStateByStartDate(event);
  }

  /**
   * Update event clock with Liveserve update
   * @param  {IShowdownOptaUpdate} update
   * @param  {ISportEvent} event
   * @returns void
   */
  updateClock(event: IEventDetails, update: IShowdownOptaUpdate): void {
    const payload: IShowdownOptaPayload = update.payload;
    if (payload && Number(payload.ev_id) === Number(event.id) && event.clock) {
      event.clock.refresh(payload);
    }
  }
}
