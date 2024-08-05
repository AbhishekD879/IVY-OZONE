import { Injectable } from '@angular/core';
import {
  IGamingHistoryResponse,
  ITotalSummary,
  IWalletTransaction
} from '@app/betHistory/models/gaming-history-response.model';
import { BetHistoryApiModule } from '@betHistoryModule/bet-history-api.module';
import { IBetHistoryAllSummary, IBetHistorySingleSummary } from '../../models/bet-win-history-summary.model';
import { BetHistoryMainService } from '@app/betHistory/services/betHistoryMain/bet-history-main.service';
import { AWSFirehoseService } from '@lazy-modules/awsFirehose/service/aws-firehose.service';
import { IAnalyticsParams } from '@lazy-modules/awsFirehose/model/analytics-params.model';

/**
 * Service which provide fetching bet & win summary
 */
@Injectable({ providedIn: BetHistoryApiModule })
export class BetHistorySummaryService {

  constructor(
    private awsService: AWSFirehoseService,
    private betHistoryMainService: BetHistoryMainService
  ) {  }

  /**
   * Forms the array IBetHistorySingleSummary[] from server response where the first item is total profit/loss summary
   * and the rest are tab related summaries like sports, lotto, pools
   * @param {IGamingHistoryResponse} data The server response data
   * @param {string[]} dataRefs The refs/keys related to switchers/tabs on the page which response data will be parsed
   * and filtered by
   * @returns {IBetHistoryAllSummary} The object collection of profit/loss info
   */
  getSummaryTotals(data: IGamingHistoryResponse, dataRefs: string[]): IBetHistoryAllSummary {
    return {
      allBetsGames: this.getAllTotals(data.summary, 'allBetsGames'),
      ...this.getSpecificTotals(data.walletTransactions, dataRefs)
    };
  }

  /**
   * Form IBetHistorySingleSummary as user's total summary of profit/loss got from response data
   * @param {ITotalSummary} summary The server response related type
   * @param {string} label The label for total summary
   * @returns {IBetHistorySingleSummary} The object of total profit/loss info
   */
  getAllTotals(summary: ITotalSummary, label: string): IBetHistorySingleSummary {
    return this.betHistoryMainService.calculateTotals(+summary.totalBets.amount, +summary.totalWins.amount, label);
  }

  /**
   * Create tab-related IBetHistorySingleSummary of profit/loss info for betTypes like sports, lotto, pools etc
   * @param {IWalletTransaction[]} wTrans The server response related type
   * @param {string[]} betTypes The refs/keys related to switchers/tabs on the page which response data will be parsed
   * and filtered by
   * @returns {IBetHistoryAllSummary} The object collection of profit/loss info
   */
  getSpecificTotals(wTrans: IWalletTransaction[], betTypes: string[]): IBetHistoryAllSummary {
    const accum = {}, res = {};

    // init accumulator, initial values
    betTypes.forEach((type: string) => {
      accum[type] = {
        win: 0,
        bet: 0,
        cancel: 0
      };
    });

    // summarize server data by actionTypes into accum object
    // for e.g. accum.sb.win = X, accum.lotto.bet = Y
    wTrans.forEach((trans: IWalletTransaction) => {
      const type = trans.actionType.split('_');
      if (accum[type[0]] && type[2] === 'cancel') {
        accum[type[0]][type[2]] += +trans.amount.amount;
      }
      if (!type[2] && accum[type[0]] && (type[1] === 'bet' || type[1] === 'win')) {
        accum[type[0]][type[1]] += +trans.amount.amount;
      }
    });

    // collect into result object by accum keys like { sb: IBetHistorySingleSummary, lotto: IBetHistorySingleSummary etc }
    Object.keys(accum).forEach(type => {
      res[type] = this.betHistoryMainService.calculateTotals(accum[type]['bet'] - accum[type]['cancel'], accum[type]['win'], type);
    });

    return res;
  }

  sendAwsData(awsObject: IAnalyticsParams): void {
    const getGamingHistoryId = 32012;
    awsObject.request.requestId = getGamingHistoryId;
    awsObject.requestEnd = new Date().getTime();
    awsObject.totalDuration = awsObject.requestEnd - awsObject.requestStart;
    this.awsService.addAction('RTS', awsObject);
  }
}
