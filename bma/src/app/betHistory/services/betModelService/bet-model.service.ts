import { Injectable } from '@angular/core';
import * as _ from 'underscore';

import { IBet, IPotentialPayout } from '@app/bpp/services/bppProviders/bpp-providers.model';
import { IBetHistoryPart } from '../../models/bet-history.model';

import { FiltersService } from '@core/services/filters/filters.service';
import { TimeService } from '@core/services/time/time.service';
import { BetHistoryApiModule } from '@betHistoryModule/bet-history-api.module';

/**
 * Service which provide fetching event functionality
 */
@Injectable({ providedIn: BetHistoryApiModule })
export class BetModelService {

  constructor(
    private timeService: TimeService,
    private filtersService: FiltersService,
  ) {}

  /**
   * Returns string which contains bet time according to user time zone:
   * if bet was set today, bet time is returned in hh:mm format,
   * day and month in format dd/mm are returned otherwise
   *
   * @param date
   * @returns {string}
   */
  getBetTimeString(date: string): string {
    const userTimeZoneBetDate = this.timeService.getLocalDateFromString(date),
      betHours = userTimeZoneBetDate.getHours(),
      betMinutes = userTimeZoneBetDate.getMinutes(),
      betDay = userTimeZoneBetDate.getDate(),
      betMonth = userTimeZoneBetDate.getMonth(),
      betYear = userTimeZoneBetDate.getFullYear(),
      today = new Date(),
      isBetSetToday = today.getDate() === betDay && today.getMonth() === betMonth &&
        today.getFullYear() === betYear;

    return isBetSetToday ? `${this.changeStringFormat(betHours)}:${this.changeStringFormat(betMinutes)}`
      : `${this.changeStringFormat(betDay)}/${this.changeStringFormat(betMonth + 1)}`;
  }

  /**
   * Gets potential payout for cash out bet object
   * @param bet {object}
   * @returns {*}
   */
  getPotentialPayout(bet: IBet): string | IPotentialPayout |  IPotentialPayout[] {
    const potentialPayout = Number(bet.potentialPayout),
      lastTermChange = _.last(bet.betTermsChange);
    if (lastTermChange && lastTermChange.potentialPayout) {
      return lastTermChange.potentialPayout.value;
    }

    if (potentialPayout || potentialPayout === 0) {
      return bet.potentialPayout;
    }

    return 'N/A';
  }

  /**
   * Creates outcome name with handicapValueDec value, if present
   * @params{object} outcome
   * @returns{string} name
   */
  createOutcomeName(parts: IBetHistoryPart[]): IBetHistoryPart[] {
    _.forEach(parts, (part: IBetHistoryPart) => {
      if (part.eventInfo && part.handicap) {
        part.description = part.description + this.filtersService.makeHandicapValue((part.handicap as string), part.outcome);
      }
    });
    return parts;
  }

  /**
   * Changes string format in the way if str value is less than 10, zero is added
   *
   * @param str
   * @returns {string}
   */
  private changeStringFormat(str: number): string {
    return `${str < 10 ? '0' : ''}${str}`;
  }
}
