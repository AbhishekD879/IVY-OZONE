import { Injectable } from '@angular/core';
import { IResponseFooterEntity } from '@core/models/response-footer-entity.model';
import { ISportEventEntity } from '@core/models/sport-event-entity.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { ISSResponseEntity } from '@core/models/ss-response-entity.model';
import * as _ from 'underscore';

@Injectable()
export class SiteServerUtilityService {

  constructor() {
    /**
     * Context bindings
     * It's needed here because context losses in such functions, like "_.partial(Fn1, Fn2, ...)"
     */
    this.stripResponse = this.stripResponse.bind(this);
  }

  /**
   * filterEventsWithPrices()
   * @param {ISportEvent[]} events
   * @returns {ISportEvent[]}
   */
  filterEventsWithPrices(events: ISportEvent[]): ISportEvent[] {
    return events.filter(event => {
      return event.markets && event.markets.some(market => {
        return market.outcomes && market.outcomes.some(outcome => {
          return !!(outcome.prices && outcome.prices.length);
        });
      });
    });
  }

  /**
   * stripResponse()
   * @param {ISSResponseEntity} data
   * @returns {ISportEventEntity[]}
   */
  stripResponse(data: ISSResponseEntity): any {
    const arr = data.SSResponse && data.SSResponse.children && data.SSResponse.children.slice() || [],
      responseFooter = arr.pop();

    return this.addResponseCreationTime(arr, responseFooter);
  }

  queryService(service: Function, params) {
    return service(params).then(this.stripResponse);
  }

  /**
   * addResponseCreationTime()
   * @param {ISportEventEntity[]} eventEntities
   * @param {IResponseFooterEntity} responseFooter
   * @returns {ISportEventEntity[]}
   */
  addResponseCreationTime(eventEntities: ISportEventEntity[], responseFooter: IResponseFooterEntity): ISportEventEntity[] {
    _.each(eventEntities, objectEntity => {
      objectEntity[Object.keys(objectEntity)[0]].responseCreationTime = responseFooter.responseFooter.creationTime;
    });

    return eventEntities;
  }
}
