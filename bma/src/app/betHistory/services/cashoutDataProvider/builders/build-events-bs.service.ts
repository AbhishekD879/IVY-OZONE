import * as _ from 'underscore';
import { Injectable } from '@angular/core';
import { ISportEvent } from '@core/models/sport-event.model';
import { IMarket } from '@core/models/market.model';
import { IOutcome } from '@core/models/outcome.model';
import { FiltersService } from '@core/services/filters/filters.service';
import { BetHistoryApiModule } from '@betHistoryModule/bet-history-api.module';

@Injectable({ providedIn: BetHistoryApiModule })
export class BuildEventsBsService {
  constructor(private filterService: FiltersService) { }

  build(eventsArray: ISportEvent[]): ISportEvent[] {
      _.each(eventsArray, eventEntity => {
        const isRacing: boolean = eventEntity.categoryId === '19' || eventEntity.categoryId === '21';
        eventEntity.id = Number(eventEntity.id);
        eventEntity.name = isRacing ? eventEntity.name : this.filterService.clearEventName(eventEntity.name);
        eventEntity.markets.forEach((marketEntity: IMarket) => {
          marketEntity.outcomes.forEach((outcomeEntity: IOutcome) => {
            outcomeEntity.price = _.clone(outcomeEntity.prices);
            delete outcomeEntity.prices;
          });
        });
      });

      return eventsArray;
  }
}
