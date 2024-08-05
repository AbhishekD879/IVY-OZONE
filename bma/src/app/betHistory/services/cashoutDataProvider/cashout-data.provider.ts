import {
  of as observableOf,
  from as observableFrom,
  forkJoin,
  Observable,
  throwError
} from 'rxjs';

import { switchMap, catchError, map } from 'rxjs/operators';
import * as _ from 'underscore';
import { Injectable } from '@angular/core';

import { BetHistoryApiModule } from '@betHistoryModule/bet-history-api.module';
import { DeviceService } from '@core/services/device/device.service';
import { BppService } from '@app/bpp/services/bpp/bpp.service';
import { LoadByPortionsService } from '@app/ss/services/load-by-portions.service';
import { SiteServerService } from '@core/services/siteServer/site-server.service';
import { SiteServerRequestHelperService } from '@core/services/siteServerRequestHelper/site-server-request-helper.service';

import { BuildEventsBsService } from './builders/build-events-bs.service';
import { BuildEventsWithScoresAndClockBsService } from './builders/build-events-with-scores-and-clock-bs.service';
import { BuildEventsWithScoresBsService } from './builders/build-events-with-scores-bs.service';

import { ISportEvent } from '@core/models/sport-event.model';
import {
  IBet,
  IBetDetail,
  ICashoutBetRequest,
  ICashoutBetResponse,
  IReadBetRequest,
  IReadBetResponse,
  IResponseTransGetBetDetail,
  IResponseTransGetBetDetails,
  IResponseTransGetBetsPlaced
} from '@app/bpp/services/bppProviders/bpp-providers.model';
import { ICashoutRawComments } from './builders/build-events-with-scores-and-clock-bs.service.models';
import { IRawCashOutBetReqParams } from '../../models/cashout-data-provider.model';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { AWSFirehoseService } from '@lazy-modules/awsFirehose/service/aws-firehose.service';

@Injectable({ providedIn: BetHistoryApiModule })
export class CashoutDataProvider {
  constructor(
    private pubSubService: PubSubService,
    private deviceService: DeviceService,
    private bppService: BppService,
    private loadByPortionsService: LoadByPortionsService,
    private ssService: SiteServerService,
    private ssRequestHelperService: SiteServerRequestHelperService,
    private buildEventsBsService: BuildEventsBsService,
    private buildEventsWithScoresAndClockBsService: BuildEventsWithScoresAndClockBsService,
    private buildEventsWithScoresBsService: BuildEventsWithScoresBsService,
    private awsService: AWSFirehoseService
  ) {}

  /**
   * Get some bets with cashOut param by cash out ids
   *
   * @param {array} idArray
   * @param {boolean} isForLiveUpdate
   * @param {boolean} showErrorPopup
   * @returns {*}
   */
  getBet(idArray: string[], isForLiveUpdate: boolean = false, showErrorPopup: boolean = true): Observable<IBetDetail[]> {
    const req = {
      betId: idArray,
      returnPartialCashoutDetails: 'Y',
      forLiveUpdate: isForLiveUpdate
    };
    return (this.bppService.send('getBetDetail', req) as Observable<IResponseTransGetBetDetail>).pipe(
      map(data => data.response.respTransGetBetDetail.bet),
      catchError(error => {
        const analyticsParams = {
          betId: idArray[0],
          showErrorPopup: showErrorPopup,
          error: error
        };
        this.awsService.addAction('cashout=>UI_Message=>(bpp)Unavailable=>getBet', analyticsParams);
        if (error && showErrorPopup) {
          this.bppService.showErrorPopup('cashOutError');
        }

        return throwError(error);
      }));
  }

  /**
   * Get market ids from outcome ids
   *
   * @param ids {Array} // [123,234,345,456]
   * @param customParams {object}
   * @return {Array}
   */
  getEventsByOutcomesIds(ids: string[], customParams = {}): Observable<ISportEvent[]> {
    const params = {
      outcomesIds: ids,
      includeUndisplayed: true,
      racingFormOutcome: true,
      ...customParams
    };
    return observableFrom(this.ssService.getEventsByOutcomeIds(params)).pipe(
      map(data => this.buildEventsBsService.build(data)),
      switchMap((e: ISportEvent[]) => {
        // TODO: (BMA-48577): buildEventsWithScoresBsService.build and this.loadScoresAndClock can make
        // TODO: additional call ssRequestHelperService.getCommentsByEventsId for Badminton event
        const eventsObservables = e.map(event => this.buildEventsWithScoresBsService.build(event));
        return forkJoin(eventsObservables);
      }),
      switchMap(data => this.loadScoresAndClock(data)),
      catchError(error => {
        console.warn('Error while getting Event from SS (siteServerFactoryBs.getEventsByOutcomesIds)');
        return throwError(error);
      }));
  }

  /**
   * Get placed bets
   *
   * @param eventId
   * @returns {promise}
   */
  getPlacedBets(eventId: number): Observable<IBet[]> {
    if (eventId) {
      return (this.bppService.send('getBetsPlaced', { eventId }) as Observable<IResponseTransGetBetsPlaced>).pipe(
        // OpenBet added validation of eventId: if it is not numeric value, internal server error is thrown
        map(res => res.response.respTransGetBetsPlaced && res.response.respTransGetBetsPlaced.bets),
        catchError(error => {
          this.awsService.addAction('cashout=>UI_Message=>(bpp)Unavailable=>getPlacedBets');
          this.bppService.showErrorPopup('cashOutError');
          return throwError(error);
      }));
    } else {
      return observableOf();
    }
  }

  /**
   * Get all bets with cashOut param
   * @param {boolean} showErrorPopup
   * @returns {promise}
   */
  getCashOutBets(showErrorPopup: boolean = true): Observable<IBetDetail[]> {
    const req = {
      cashoutBets: 'Y',
      status: 'A',
      returnPartialCashoutDetails: 'Y',
      filter: 'Y'
    };

    return (this.bppService.send('getBetDetails', req) as Observable<IResponseTransGetBetDetails>).pipe(
      map(data => data.response.respTransGetBetDetails.bets),
      catchError(error => {
        if (showErrorPopup) {
          this.awsService.addAction('cashout=>UI_Message=>(bpp)Unavailable=>getCashOutBets');
          this.bppService.showErrorPopup('cashOutError');
        }

        return throwError(error);
      }));
  }

  /**
   * Make cash out request for outcome
   *
   * @param data {object}
   * @returns {promise}
   */
  makeCashOutRequest(data: IRawCashOutBetReqParams): Observable<ICashoutBetResponse> {
    return (this.bppService.send('cashoutBet', this.generateCashOutBetReqParams(data)) as Observable<ICashoutBetResponse>).pipe(
      catchError(error => {
        const analyticsParams = {
          betId: data.betId,
          cashOutAmount: data.cashOutAmount,
          partialCashOutAmount: data.partialCashOutAmount,
          partialCashOutPercentage: data.partialCashOutPercentage,
          currency: data.currency,
          error: error
        };
        this.awsService.addAction('cashout=>UI_Message=>(bpp)Unavailable=>makeCashOutRequest', analyticsParams);
        return this.handleError(error);
      }));
  }

  /**
   * Make cash out makeReadBet request for outcome
   *
   * @param betId {string}
   * @returns {promise}
   */
  makeReadBetRequest(betId: string, reqData: IRawCashOutBetReqParams): Observable<IReadBetResponse | any[]> {
    return (this.bppService.send('readBet', this.generateReadBetReqParams(betId)) as Observable<IReadBetResponse>).pipe(
      map(data => data || []),
      catchError(error => {
        const analyticsParams = {
          betId: reqData.betId,
          cashOutAmount: reqData.cashOutAmount,
          partialCashOutAmount: reqData.partialCashOutAmount,
          partialCashOutPercentage: reqData.partialCashOutPercentage,
          currency: reqData.currency,
          error: error
        };
        this.awsService.addAction('cashout=>UI_Message=>(bpp)Unavailable=>makeReadBetRequest', analyticsParams);
        return this.handleError(error);
      }));
  }

  private handleError(error): Observable<any> {
    if (this.deviceService.isMobile) {
      this.pubSubService.publish(this.pubSubService.API.RELOAD_CASHOUT);
    }

    this.bppService.showErrorPopup('cashOutError');
    return throwError(error);
  }

  /**
   * Create object for cashOut request
   *
   * @param data {object}
   * @returns {object}
   */
  private generateCashOutBetReqParams(data: IRawCashOutBetReqParams): ICashoutBetRequest {
    return {
      betRef: {
        id: data.betId,
        provider: 'OpenBetSports'
      },
      channelRef: this.deviceService.channel.channelRef,
      cashoutValue: {
        amount: data.cashOutAmount,
        partialCashoutAmount: data.partialCashOutAmount || null,
        partialCashoutPercentage: data.partialCashOutPercentage || null,
        currencyRef: {
          id: data.currency
        }
      }
    };
  }

  /**
   * Create object for readBet request
   *
   * @param betId {string}
   * @returns {object}
   */
  private generateReadBetReqParams(betId: string): IReadBetRequest {
    return {
      betRef: [{
        id: betId,
        provider: 'OpenBetCashoutDelay'
      }]
    };
  }

  private isScoresAndClockAvailable(event: ISportEvent): boolean {
    return event && _.has(event, 'isStarted');
  }

  /**
   * loadScoresAndClock from SS comments for BIP events and build them with events
   *
   * @param events
   * @returns {*}
   */
  private loadScoresAndClock(events: ISportEvent[]): Observable<ISportEvent[]> {
    const eventsIds = events.filter(this.isScoresAndClockAvailable)
                            .map(eventEntity => eventEntity.id);

    return this.getCommentsByEvents(eventsIds).pipe(
      map(result => {
        return { events, comments: result };
      }),
      map(data => this.buildEventsWithScoresAndClockBsService.build(data)));
  }

  /**
   * Returns comments for given events
   *
   * @param {Array} eventsIds
   * @return {Observable} events with comments like {eventId: commentsObj, ...}
   */
  private getCommentsByEvents(eventsIds: number[]): Observable<ICashoutRawComments> {
    const request = this.ssRequestHelperService.getCommentsByEventsIds.bind(this.ssRequestHelperService);

    return observableFrom(
      this.loadByPortionsService.get(request, {}, 'eventsIds', eventsIds)
    ).pipe(
      map(result => {
        // get only events with comments and format like {eventId: commentsObj, ...}
        return _.object(_.map(_.filter(result, obj => {
          return obj.event.children;
        }), obj => {
          return [obj.event.id, obj.event.children];
        }));
      }));
  }
}
