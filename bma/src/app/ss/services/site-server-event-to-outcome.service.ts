
import { from as observableFrom,  Observable } from 'rxjs';
import * as _ from 'underscore';
import { Injectable } from '@angular/core';
import { ISportEvent } from '@core/models/sport-event.model';
import { ISSRequestParamsModel } from '@core/models/ss-request-params.model';
import { BuildUtilityService } from '@core/services/buildUtility/build-utility.service';
import { SiteServerRequestHelperService } from '@core/services/siteServerRequestHelper/site-server-request-helper.service';
import { LoadByPortionsService } from '@ss/services/load-by-portions.service';
import { SimpleFiltersService } from '@ss/services/simple-filters.service';

@Injectable()
export class SiteServerEventToOutcomeService {

  constructor(
    private buildUtility: BuildUtilityService,
    private simpleFilters: SimpleFiltersService,
    private loadByPortions: LoadByPortionsService,
    private ssRequestHelper: SiteServerRequestHelperService
  ) { }

  /**
   * getEventToOutcomeForMarket()
   * @param {ISSRequestParamsModel} params
   * @returns {Promise<ISportEvent[]>}
   */
  getEventToOutcomeForMarket(params: ISSRequestParamsModel): Observable<ISportEvent[]> {
    const builder = (params.racingFormEvent || params.racingFormOutcome) ?
      this.buildUtility.buildEventsWithRacingForm :
      this.buildUtility.buildEvents,
      simpleFilters = [
        'isNotStarted',
        'eventIdEquals',
        'racingFormOutcome',
        'racingFormEvent',
        'siteChannels',
        'startTime',
        'endTime'
      ],
      filters = _.extend({}, _.pick(params, simpleFilters)),
      reqParams = { simpleFilters: this.simpleFilters.genFilters(filters) },
      ids = _.uniq(params.marketIds);

    return observableFrom(this.loadByPortions
      .get(data => this.ssRequestHelper.getEventsByMarkets(data), reqParams, 'marketIds', ids)
      .then(data =>  {
        return builder(data);
      }));
  }

  /**
   * getEventToOutcomeForOutcome()
   * @param {number[]} outcomesIds
   * @returns {Promise<ISportEvent[]>}
   */
  getEventToOutcomeForOutcome(outcomesIds: number[]): Promise<ISportEvent[]> {
    return this.loadByPortions
      .get(data => this.ssRequestHelper.getEventToOutcomeForOutcome(data), {}, 'outcomesIds', outcomesIds)
      .then(data => this.buildUtility.buildEventsWithExternalKeys(data))
      .then(data => this.buildUtility.buildEvents(data));
  }
}
