import { Injectable } from '@angular/core';
import * as _ from 'underscore';

import { LoadByPortionsService } from '@app/ss/services/load-by-portions.service';
import { SiteServerRequestHelperService } from '@core/services/siteServerRequestHelper/site-server-request-helper.service';
import { FiltersService } from '@core/services/filters/filters.service';

import {
  IEventsIds, IRacingResult, IDividends, IFinalPositionResponse, INcastDividendResponse, IRuleDeductionResponse
} from '@sb/models/dividends.model';

@Injectable()
export class DividendsService {
  constructor(private loadByPortionsService: LoadByPortionsService,
              private filterService: FiltersService,
              private siteServerRequestHelperService: SiteServerRequestHelperService
  ) {}

  /**
   * Fetches dividends and invokes callback
   */
  fetch(eventsIds: Array<number>, callback: Function): void {
    this.loadByPortionsService.get((data: IEventsIds) => {
      return this.siteServerRequestHelperService.getRacingResultsForEvent(data, true);
      }, {}, 'eventsIds', eventsIds)
      .then((response: IRacingResult[]) => callback(this.mapEventIdsToDividends(response)));
  }

  /**
   * Maps RacingResultsForEvent server response for UI
   * Example of return value: {12345: {TC: 33, FC: 44}, ...} where 12345 - eventId
   */
  private mapEventIdsToDividends(rawServerResponse: IRacingResult[]): IDividends {
    return _.reduce(rawServerResponse, (prev, curr: IRacingResult) => {
      const dividends = this.getDividends(curr.racingResult.children);
      if (!_.isEmpty(dividends)) {
        prev[curr.racingResult.id] = dividends;
      }
      return prev;
    }, {});
  }

  private getDividends(children: Array<IFinalPositionResponse | INcastDividendResponse | IRuleDeductionResponse>):
    IFinalPositionResponse | INcastDividendResponse | IRuleDeductionResponse | {}  {
    return _.reduce(children, (prev: IFinalPositionResponse, curr: INcastDividendResponse):any => {
      if (curr && curr.ncastDividend) {
        prev[curr.ncastDividend.type] = this.filterService.setCurrency(curr.ncastDividend.dividend, '£');
      }
      return prev;
    }, {});
  }
}

