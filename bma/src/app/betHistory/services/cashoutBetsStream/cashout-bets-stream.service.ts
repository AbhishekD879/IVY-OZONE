import { throwError, Observable } from 'rxjs';
import { Injectable } from '@angular/core';
import { catchError, finalize, map, shareReplay } from 'rxjs/operators';

import { BetHistoryApiModule } from '@betHistoryModule/bet-history-api.module';
import { BppService } from '@app/bpp/services/bpp/bpp.service';
import { CashoutDataProvider } from '../cashoutDataProvider/cashout-data.provider';
import { CashoutWsConnectorService } from '@betHistoryModule/services/cashoutWsConnector/cashout-ws-connector.service';
import { IBetDetail } from '@app/bpp/services/bppProviders/bpp-providers.model';
import { CashOutLiveServeUpdatesService } from '@betHistoryModule/services/cashOutLiveServeUpdatesService/cashOutLiveServeUpdatesService';
import { ICashOutBet } from '@betHistoryModule/models/bet-history-cash-out.model';
import * as _ from 'underscore';
import { ICashoutBet } from '@app/betHistory/models/bet-history-bet.model';
import { AWSFirehoseService } from '@lazy-modules/awsFirehose/service/aws-firehose.service';

@Injectable({ providedIn: BetHistoryApiModule })
export class CashoutBetsStreamService {
  cashoutBetsObservable: Observable<IBetDetail[]>;

  constructor(
    private bppService: BppService,
    private cashoutDataProvider: CashoutDataProvider,
    private cashoutWsConnectorService: CashoutWsConnectorService,
    private awsService: AWSFirehoseService,
    private cashOutLiveServeUpdatesService: CashOutLiveServeUpdatesService
  ) {}

  /**
   * Get some bets with cashOut param by cash out ids
   *
   * @param idArray {array}
   * @param isForLiveUpdate {boolean}
   * @returns {*}
   */
  getCashoutBet(idArray: string[], isForLiveUpdate: boolean = false): Observable<IBetDetail[]> {
    return this.cashoutDataProvider.getBet(idArray, isForLiveUpdate, false).pipe(
      map((result: IBetDetail[]) => {
        const betToUpdate = _.isArray(result) ? result[0] : result;

        if (betToUpdate) {
          this.cashOutLiveServeUpdatesService.updateBetDetails(betToUpdate as ICashOutBet, Date.now(), null, true);
        }

        return result;
      }),
      catchError(error => {
        if (error) {
          this.bppService.showErrorPopup('cashOutError');
        }

        this.awsService.addAction('cashout=>getCashoutBet=>error', { error });

        return throwError(error);
      })
    );
  }

  /**
   * Get all bets with cashOut param
   * @returns {promise}
   */
  getCashoutBets(): Observable<IBetDetail[]> {
    if (!this.cashoutBetsObservable) {
      this.cashoutBetsObservable = this.cashoutWsConnectorService.streamBetDetails().pipe(
        catchError(error => {
          this.bppService.showErrorPopup('cashOutError');
          this.awsService.addAction('cashout=>getCashoutBets=>error', { error });
          return throwError(error);
        }),
        shareReplay(1),
        finalize(() => {
          this.cashoutBetsObservable = null;
        })
      );
    }

    return this.cashoutBetsObservable;
  }

  updateCashedOutBet(bet: ICashoutBet): void {
    this.cashoutWsConnectorService.updateBet(bet);
  }

  /**
   * If enabled in CMS - opens cashout bet updates event stream.
   */
  openBetsStream(): Observable<IBetDetail[]> {
    return this.cashoutWsConnectorService.streamBetDetails();
  }

  /**
   * Closes cashout bet updates event stream.
   */
  closeBetsStream(): void {
    this.cashoutWsConnectorService.closeStream();
  }

  /**
   * Clear bets observable from Cash out page
   */
  clearCashoutBetsObservable(): void {
    this.cashoutBetsObservable = null;
  }
}
