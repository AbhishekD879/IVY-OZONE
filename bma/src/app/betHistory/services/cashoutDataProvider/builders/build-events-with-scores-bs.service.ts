import { Injectable } from '@angular/core';
import { from, of, Observable } from 'rxjs';
import { map } from 'rxjs/operators';

import * as _ from 'underscore';

import { BetHistoryApiModule } from '@betHistoryModule/bet-history-api.module';
import { SiteServerRequestHelperService } from '@core/services/siteServerRequestHelper/site-server-request-helper.service';
import { FiltersService } from '@core/services/filters/filters.service';
import { ISportEvent } from '@core/models/sport-event.model';

@Injectable({ providedIn: BetHistoryApiModule })
export class BuildEventsWithScoresBsService {
  // sport requires additional request to get scores
  private readonly scoresByAdditionalRequestSports: string[] = ['BADMINTON'];

  constructor(
    private ssRequestHelperService: SiteServerRequestHelperService,
    private filtersService: FiltersService
  ) {}

  build(event: ISportEvent): Observable<ISportEvent> {
    if (this.isSportWithScoresByRequest(event)) {
      return this.scoresExtension(event);
    } else {
      return of(event);
    }
  }

  private isSportWithScoresByRequest(event: ISportEvent): boolean {
    return _.contains(this.scoresByAdditionalRequestSports, event && event.categoryCode);
  }

  /**
   * Extend event data with scores by making additional call to SS
   * @param {object} event
   * @return {object} event
   */
  private scoresExtension(event: ISportEvent): Observable<ISportEvent> {
    return from(this.ssRequestHelperService.getCommentsByEventsIds({ eventsIds: event.id })).pipe(
      map(res => {
        const comments = res.SSResponse.children[0].event.children;

        if (_.isArray(comments) && comments.length) {
          const periods = _.filter(comments[0].eventPeriod.children, (el: any) => el.eventPeriod);
          const lastPeriod = _.max(periods, el => el.eventPeriod.periodIndex).eventPeriod.children;
          const current = _.sortBy(
            _.filter(lastPeriod, (el: any) => el.eventFact),
            el => el.eventFact.eventParticipantId
          );
          const scores = _.sortBy(
            _.filter(comments[0].eventPeriod.children, (el: any) => el.eventFact),
            el => el.eventFact.eventParticipantId
          );
          const participants = _.filter(comments, el => el.eventParticipant);

          event.comments = {
            teams: {
              home: {
                currentPoints: current[0].eventFact.fact,
                score: scores[0].eventFact.fact,
                name: this.filtersService.removeLineSymbol(participants[0].eventParticipant.name)
              },
              away: {
                currentPoints: current[1].eventFact.fact,
                score: scores[1].eventFact.fact,
                name: this.filtersService.removeLineSymbol(participants[1].eventParticipant.name)
              }
            }
          };
        }

        return event;
      }));
    }
}
