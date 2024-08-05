import { Injectable } from '@angular/core';
import { from as observableFrom, Observable, Subject, throwError } from 'rxjs';

import { BetHistoryApiModule } from '@app/betHistory/bet-history-api.module';
import { UserService } from '@core/services/user/user.service';
import { CashOutLiveServeUpdatesService } from '@app/betHistory/services/cashOutLiveServeUpdatesService/cashOutLiveServeUpdatesService';
import { IBetDetail } from '@app/bpp/services/bppProviders/bpp-providers.model';
import { CommandService } from '@core/services/communication/command/command.service';
import { WsConnectorService } from '@core/services/wsConnector/ws-connector.service';
import { WsConnector } from '@core/services/wsConnector/ws-connector';
import * as _ from 'underscore';
import environment from '@environment/oxygenEnvConfig';
import { IConstant } from '@core/services/models/constant.model';
import { catchError, map, takeUntil } from 'rxjs/operators';
import {
  ISocketCashoutUpdateMessage,
  ICashoutSocketBets,
  ICashoutSocketBetUpdate,ICashoutSocketEventUpdate,ISocketTwoUpMessage
} from '@app/betHistory/models/cashout-socket.model';
import { ICashOutBet } from '@app/betHistory/models/bet-history-cash-out.model';
import { ICashoutBet } from '@app/betHistory/models/bet-history-bet.model';
import { AWSFirehoseService } from '@lazy-modules/awsFirehose/service/aws-firehose.service';

import { IDateRangeObject } from '@app/betHistory/models/date-object.model';
import { IDatePickerDate, IDatePickerDates } from '@app/betHistory/models/date-picker-date.model';
import { TimeService } from '@core/services/time/time.service';
@Injectable({ providedIn: BetHistoryApiModule })
export class CashoutWsConnectorService {
  private readonly moduleName = 'cashout';
  private readonly CASHOUT_MS_ENDPOINT: string = environment.CASHOUT_MS;

  private connection: WsConnector;

  private eventHandlers = new Map<string, Function>();
  private connectionStateHandlers = new Map<string, Function>();

  private betDetails$ = new Subject<IBetDetail[]>();
  private disconnected$ = new Subject();

  private subscribers: number = 0;

  private unauthorised = false;
  private unknownErrorReconnectAttempts = 3;
  private pageScrollCallBack: Function;

  pagingToken: string;
  token: string;
  startDate: IDatePickerDate;
  endDate: IDatePickerDate;

  constructor(private wsConnectorService: WsConnectorService,
    private user: UserService,
    private cashOutLiveServeUpdatesService: CashOutLiveServeUpdatesService,
    private commandService: CommandService,
    private awsService: AWSFirehoseService,
    private timeService: TimeService
  ) { }

  /**
   * Opens cashout bets events stream and updates subscriptions amount
   * @returns {Observable}
   */
  streamBetDetails(): Observable<IBetDetail[]> {
    this.subscribers++;
    this.reconnect();
    return this.betDetails$.asObservable();
  }

  updateBet(bet: ICashoutBet): void {
    this.connection.emit('updateBet', { betId: bet.betId, updateType: 'cashedOut' });
  }
  getConnection() {
    return this.connection;
  }
  /**
   * Removes subscriber from the listeners of cashout web socket stream and closes connection if needed.
   */
  closeStream() {
    if (this.subscribers-- === 1) {
      this.closeConnection();
    }
  }

  /**
   * return the today minus default days formatted start/end dates
   */
  getDateObject(): IDateRangeObject {
    const defaultDays: number = this.timeService.oneDayInMiliseconds * 29;
    const startDate: number = new Date().getTime() - defaultDays;
    this.startDate = { value: new Date(startDate) };
    this.endDate = { value: new Date() };
    return this.formatDateByPattern(this.startDate.value, this.endDate.value);
  }

  /**
   * returns the formatted start/end dates
   */
  private formatDateByPattern(startDate: Date, endDate: Date): IDateRangeObject {
    return {
      startDate: this.timeService.formatByPattern(startDate, 'yyyy-MM-dd 00:00:00'),
      endDate: this.timeService.formatByPattern(endDate, 'yyyy-MM-dd 23:59:59')
    };
  }

  /**
   * gets the formatted date object
   */
  getFormattedDateObject(): IDatePickerDates {
    const dateObject = this.getDateObject();
    this.startDate = { value: new Date(dateObject.startDate.replace(" ", "T")) };
    this.endDate = { value: new Date(dateObject.endDate.replace(" ", "T")) };
    return { startDate: this.startDate, endDate: this.endDate };
  }

  /**
   * Creates connection with cashout socket for initial bets, bet and cashout value live updates.
   */
  private createConnection(): WsConnector {
    const dateObject = this.getDateObject();
    const queryparams = `&detailLevel=DETAILED&fromDate=${dateObject.startDate}&toDate=${dateObject.endDate}&group=BET&pagingBlockSize=20&settled=N`;

    const params = {
      path: '/socket.io',
      timeout: 10000,
      reconnectionAttempts: 10,
      reconnectionDelay: 1000
    };

    this.connection = this.wsConnectorService.create(
      `${this.CASHOUT_MS_ENDPOINT}:8443/?token=${this.user.bppToken}${queryparams}`,
      params,
      this.moduleName
    );

    this.awsService.addAction('cashoutUpdates->createConnection', {
      bppToken: `${this.user.bppToken}`.substr(0, 7),
    });

    return this.connection;
  }

  /**
   * returns websocket connection observable for initial 20 bets
   */
  dateChangeBet(startDate: IDatePickerDate = null, endDate: IDatePickerDate = null): Observable<IBetDetail[]> {
    const dateObject: IDateRangeObject = startDate && endDate ? this.formatDateByPattern(startDate.value, endDate.value) : this.getDateObject();
    this.connection.emit('initialBets',
      {
        detailLevel: 'DETAILED',
        pagingBlockSize: '20',
        token: this.user.bppToken,
        fromDate: dateObject.startDate,
        toDate: dateObject.endDate,
        group: 'BET',
        settled: 'N'
      });
    return this.betDetails$.asObservable();
  }

  /**
   * returns websocket connection observable for next 20 bets
   */
  nextCashoutBet(pageScrollCallBack: Function = null): void {
    this.pageScrollCallBack = null;
    if (this.pagingToken) {
      this.connection.emit('nextBets',
        {
          detailLevel: 'DETAILED',
          blockSize: '20',
          pagingToken: this.pagingToken,
          token: this.user.bppToken
        });
      this.pageScrollCallBack = pageScrollCallBack;
    }
  }

  private createConnectionAndInitHandlers() {
    this.createConnection();
    this.initEventHandlers();
    this.initStateHandlers();
  }

  /**
   * Closes connection with cashout socket
   */
  private closeConnection(): void {
    if (this.connection) {
      this.connection.disconnect();
      this.connection = null;
      this.disconnected$.next(null);
      this.disconnected$.complete();
      this.disconnected$ = new Subject();
    }
  }

  /**
   * Re-creates new connection with cashout web socket
   */
  private reconnect(): WsConnector {
    this.closeConnection();
    this.createConnectionAndInitHandlers();
    this.connection.connect();
    return this.connection;
  }

  private initEventHandlers() {
    this.eventHandlers.set('initial', this.initialEventHandler.bind(this));
    this.eventHandlers.set('betUpdate', this.betUpdateEventHandler.bind(this));
    this.eventHandlers.set('cashoutUpdate', this.cashoutUpdateEventHandler.bind(this));
    this.eventHandlers.set('nextBetsUpdate', this.nextPageCashoutDataEventHandler.bind(this));
    this.eventHandlers.set('payoutUpdate', this.payoutUpdateEventHandler.bind(this));
    this.eventHandlers.set('eventUpdate', this.eventUpdateEventHandler.bind(this));
    this.eventHandlers.set('twoUpUpdate', this.twoUpUpdateEventHandler.bind(this));
    this.connection.addAnyMessagesHandler(this.handleMessage.bind(this));    

  }

  private initStateHandlers() {
    this.connectionStateHandlers.set('connect', () => {
      this.trackConnectionState('connected');
    });

    if (this.connection) {
      this.connection.state$
        .pipe(takeUntil(this.disconnected$))
        .subscribe(this.handleConnectionStateChange.bind(this));
    }
  }

  /**
   * method to trigger callback function and load bets for new set of bets
   */
  private nextPageCashoutDataEventHandler(update: any): void {
    if (update && update['paging']) {
      this.pagingToken = update['paging'].token;
      update.pageToken = this.pagingToken;
      if (this.pageScrollCallBack) {
        this.pageScrollCallBack(update, true);
      }
    } else {
      this.trackUpdatesError('PAGE_UPDATE_TYPE_RES', update);
    }
  }

  private handleConnectionStateChange(state: string) {
    const handler = this.connectionStateHandlers.get(state);
    if (typeof handler !== 'function') {
      console.error('Unknown socket error');
      return;
    }

    handler();
  }

  private handleMessage(messageName: string, body: any) {
    const handler = this.eventHandlers.get(messageName);
    if (typeof handler !== 'function') {
      console.error('Unknown socket message: ', messageName);
      this.trackUpdatesError('unknownSocketMessage', { messageName, body });
      return;
    }

    handler(body);
  }

  private initialEventHandler(update: ICashoutSocketBets) {
    if (update && _.isArray(update.bets)) {
      this.pagingToken = update['paging'].token;
      this.betDetails$.next(update.bets);
      this.betDetails$.complete();
      this.betDetails$ = new Subject<IBetDetail[]>();
    } else {
      this.trackUpdatesError('initial', update);

      if (this.isUnathorisedError(update)) {
        // Reconnect to BPP and create new connection with updated BPP token
        this.handleUnauthorisedError()
          .subscribe(() => {
            this.unauthorised = false;
          }, () => {
            this.throwBetDetailsError();
          });
      } else if (update.error.code === 'UNKNOWN_SERVICE_ERROR' && this.unknownErrorReconnectAttempts) {
        this.unknownErrorReconnectAttempts--;
        this.reconnect();
      } else {
        this.closeConnection();
        this.throwBetDetailsError();
      }
    }
  }
  private eventUpdateEventHandler(update: ICashoutSocketEventUpdate) {
    if (update && update.event) {
      this.cashOutLiveServeUpdatesService.updateEventDetail(update.event);
    } else {
      this.trackUpdatesError('eventUpdate', update);

    }
  }  
  
  private twoUpUpdateEventHandler(update: ISocketTwoUpMessage) {
    if (update && update.twoUp) {
      this.cashOutLiveServeUpdatesService.update2UpSelection(update.twoUp);
    } else {
      this.trackUpdatesError('twoUpUpdate', update);
    }
  }

  private betUpdateEventHandler(update: ICashoutSocketBetUpdate) {
    if (update && update.bet) {
      this.cashOutLiveServeUpdatesService.updateBetDetails(update.bet, Date.now(), null, true);
    } else {
      this.trackUpdatesError('betUpdate', update);

      // Reconnect to BPP and create new connection with updated BPP token
      if (this.isUnathorisedError(update)) {
        this.handleUnauthorisedError()
          .subscribe(() => {
            this.unauthorised = false;

            // replace "initial" message handler
            this.eventHandlers.set('initial', this.handleBetsUpdate);
          });
      }
    }
  }

  private handleBetsUpdate(update: ICashoutSocketBets): void {
    if (update && _.isArray(update.bets)) {
      _.each(update.bets, (bet: IBetDetail) => {
        this.cashOutLiveServeUpdatesService.updateBetDetails(bet as ICashOutBet, Date.now());
      });
    } else {
      this.trackUpdatesError('betUpdateReconnect', update);
    }
  }

  private cashoutUpdateEventHandler(update: ISocketCashoutUpdateMessage) {
    if (update && update.cashoutData) {
      this.cashOutLiveServeUpdatesService.applyCashoutValueUpdate(update.cashoutData);
    } else {
      this.trackUpdatesError('cashoutUpdate', update);
    }
  }
  private payoutUpdateEventHandler(update: any) {
    (update && update.length > 0) ?
      this.cashOutLiveServeUpdatesService.updatePayoutDetails(update) :
      this.trackUpdatesError('payoutUpdate', update)
  }
  private trackUpdatesError(channel: string, errorData: IConstant): void {
    this.awsService.addAction(`cashoutUpdates->error->${channel}`, {
      data: errorData
    });
  }

  private trackConnectionState(state: string, data?: any) {
    this.awsService.addAction(`cashoutConnection->${state}`, { data });
  }

  private isUnathorisedError(update: ICashoutSocketBets | ICashoutSocketBetUpdate| ICashoutSocketEventUpdate): boolean {
    return !this.unauthorised && _.has(update, 'error') && update.error.code === 'UNAUTHORIZED_ACCESS';
  }

  private handleUnauthorisedError(): Observable<void> {
    this.unauthorised = true;

    return observableFrom(this.commandService.executeAsync(this.commandService.API.BPP_AUTH_SEQUENCE)).pipe(
      map(() => {
        this.reconnect();
      }),
      catchError((error: string) => {
        this.trackUpdatesError('bppReconnect', { error });
        this.closeConnection();
        return throwError(error);
      })
    );
  }

  private throwBetDetailsError() {
    this.betDetails$.error([]);
    this.betDetails$.complete();
    this.betDetails$ = new Subject<IBetDetail[]>();
  }
}
