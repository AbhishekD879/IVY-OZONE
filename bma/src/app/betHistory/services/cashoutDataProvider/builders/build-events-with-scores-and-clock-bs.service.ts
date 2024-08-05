import * as _ from 'underscore';
import { Injectable } from '@angular/core';
import { CommentsService } from '@core/services/comments/comments.service';

import { ISportEvent } from '@core/models/sport-event.model';
import { ICashoutRawComments } from './build-events-with-scores-and-clock-bs.service.models';
import { BetHistoryApiModule } from '@betHistoryModule/bet-history-api.module';
import { ScoreParserService } from '@core/services/scoreParser/score-parser.service';


@Injectable({ providedIn: BetHistoryApiModule })
export class BuildEventsWithScoresAndClockBsService {

  constructor(
    private commentsService: CommentsService,
    private scoreParser: ScoreParserService
  ) { }

  build(data: { events: ISportEvent[], comments: ICashoutRawComments }): ISportEvent[] {
    this.addComments(data.events, data.comments);
    this.addClock(data.events, data.comments);

    return data.events;
  }

  /**
   * Parse comments and add them to event
   *
   * @param {Array} events - events to extend
   * @param {Object} rawComments - raw comments data for events, {eventId: data, ...}
   * @returns {Array} eventsArray - events with additional data
   */
  private addComments(events: ISportEvent[], rawComments: ICashoutRawComments): ISportEvent[] {
    _.each(events, (event: ISportEvent) => {
      const sportCommentsParser = this.commentsService[`${event.categoryCode.toLowerCase()}InitParse`];
      if (rawComments[event.id] && sportCommentsParser) {
        event.comments = sportCommentsParser(rawComments[event.id]);
        this.commentsService.extendWithScoreType(event, event.categoryCode);
      } else {
        const scoreInfo = this.scoreParser.parseTypeAndScores(event.originalName, event.categoryCode);
        this.commentsService.extendWithScoreInfo(event, scoreInfo);
      }
    });

    return events;
  }

  /**
   * Parse comments and add needed clock data to event
   *
   * @param {Array} events - events to extend
   * @param {Object} rawComments - raw comments data for events, {eventId: data, ...}
   * @returns {Array} eventsArray - events with additional data
   */
  private addClock(events: ISportEvent[], rawComments: ICashoutRawComments): ISportEvent[] {
    _.each(events, (event: ISportEvent) => {
      if (rawComments[event.id]) {
        const categoryCode: string = event.categoryCode.toLowerCase();
        const parser: Function = this.commentsService[`${categoryCode}ClockInitParse`];

        if (parser) {
          _.extend(event, parser(rawComments[event.id],
            event.categoryCode.toLowerCase(), event.startTime, event.responseCreationTime));
        }
      }
    });

    return events;
  }
}
