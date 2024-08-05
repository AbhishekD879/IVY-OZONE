import { Injectable } from '@angular/core';
import * as _ from 'underscore';

import { BetHistoryApiModule } from '@betHistoryModule/bet-history-api.module';
import { FracToDecService } from '@core/services/fracToDec/frac-to-dec.service';
import { betHistoryConstants } from '../../constants/bet-history.constant';
import { IYourCallBetStatuses } from '../../models/your-call-bet-statuses.model';

/**
 * Service which provide fetching event functionality
 */
@Injectable({ providedIn: BetHistoryApiModule })
export class YourCallHistoryBetBuilderService {
  // Set YC bet statuses
  readonly ycBetStatuses: IYourCallBetStatuses = betHistoryConstants.ycBetStatuses;

  constructor(
    private fracToDecService: FracToDecService
  ) {}

  /**
   * Extend YourCall bet with needed data to show in history
   */
  extendHistoryBet(historyBet: any, ycBet: any): any {
    // Set YourCall flag and status
    _.extend(historyBet, { ycBet: true, ycStatus: ycBet.data[0].status });
    // Set some of params
    const fracOdds = this.fracToDecService.decToFrac(ycBet.data[0].odds);
    const numAndDenArr = fracOdds.split('/');
    const betResult = this.getYCBetStatus(ycBet.data[0].status);
    const betConfirmed = betResult === '-' ? 'N' : 'Y';
    // YC bets is always a Single
    historyBet.betType.code = 'SGL';
    historyBet.betType.name = 'Single';
    const eventName = `${ycBet.data[0].events[0].game1.homeTeam.title} v ${ycBet.data[0].events[0].game1.visitingTeam.title}`;

    // Extend 'leg' properties with needed data
    historyBet.leg[0] = {
      legType: {
        code: 'W'
      },
      legSort: {
        code: '--'
      },
      part: [{
        outcome: [{
          name: this.parseOutcomeName(historyBet.manualBetDetail[0].description),
          event: {
            id: '',
            name: eventName,
            startTime: ycBet.data[0].events[0].game1.date
          },
          eventType: ycBet.data[0].events[0].type,
          eventClass: {
            name: ''
          },
          eventCategory: {
            id: ''
          },
          market: {
            name: '#YourCall'
          },
          result: {
            confirmed: betConfirmed,
            value: betResult,
            places: ''
          }
        }],
        price: [{
          priceType: {
            code: 'L'
          },
          priceNum: numAndDenArr[0],
          priceDen: numAndDenArr[1],
          priceDecimal: ycBet.data[0].odds
        }]
      }]
    };

    // Calculate potential payout
    const potentialPayout = {
      potentialPayout: [
        {
          value: this.calculateEstReturns(ycBet.data[0].odds, ycBet.data[0].amount)
        }
      ]
    };
    // Extend with potentialPayout data
    _.extend(historyBet, potentialPayout);
    return historyBet;
  }

  /**
   * Calculate potentialPayout (est. returns)
   * @param {array} odds
   * @param {number} stake
   */
  private calculateEstReturns(odds: any, stake: number): string {
    return (odds && stake) ? ((parseFloat(odds) * stake).toFixed(2)) : 'N/A';
  }

  /**
   * Parse outcome name, substitute 'and' with comma if present
   * and make all names after comma started with capital letter
   * @param {string} outcomesName
   */
  private parseOutcomeName(outcomesName: string): string {
    // It possible that one or two spaces could be before 'and'
    const fixedName: string = outcomesName.replace('  and ', ' and ');
    let namesArr: string[] = fixedName.split(' and ');
    namesArr = _.flatten(
      _.map(namesArr, (name: string) => name.split(', '))
    );
    namesArr = _.map(namesArr, (name: string) => name.charAt(0).toUpperCase() + name.slice(1));
    return namesArr.join(', ');
  }

  /**
   * Set status of the YC bet.
   * @param {number} status
   * @return {string} e.g. 'W'
   */
  private getYCBetStatus(status: number): string {
    switch (true) {
      case (status === this.ycBetStatuses.won):
        return 'W'; // won
      case (status === this.ycBetStatuses.lost):
        return 'L'; // lost
      case (status === this.ycBetStatuses.void1):
      case (status === this.ycBetStatuses.void2):
        return 'V'; // void
      default :
        return '-'; // pending
    }
  }

}
