import { IQuickbetRequestModel } from '@app/quickbet/models/quickbet-selection-request.model';
import { Injectable } from '@angular/core';
import { Subject, Observable } from 'rxjs';
import * as _ from 'underscore';

import environment from '@environment/oxygenEnvConfig';
import { WsConnectorService } from '../wsConnector/ws-connector.service';
import { SessionStorageService } from '../storage/session-storage.service';
import { TimeService } from '../time/time.service';
import { CommandService } from '../communication/command/command.service';
import { PubSubService } from '../communication/pubsub/pubsub.service';
import { IRemoteBetslipBet, IRemoteBetslipProviderConfig, remoteBetslipConstant } from './remote-betslip.constant';
import { IConstant } from '../models/constant.model';
import { GtmTrackingService } from '@core/services/gtmTracking/gtm-tracking.service';
import { ISystemConfig } from '@core/services/cms/models';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { FanzoneStorageService } from '../fanzone/fanzone-storage.service';
import { UserService } from '../user/user.service';

@Injectable()
export class RemoteBetslipService {

  timeoutId: any; // timeout
  private remoteBetslipConstant: IConstant;
  private generalConfig: IConstant;
  private pubsubEvents: IConstant;
  private connection;
  private sessionId: string;
  private handlersMap: IConstant;

  static get STORAGE_KEY(): string {
    return 'RemoteBS';
  }
  static set STORAGE_KEY(value: string) { }

  static get UPDATE_CHANNELS(): Array<string> {
    return ['sEVENT', 'sEVMKT', 'sSELCN'];
  }
  static set UPDATE_CHANNELS(value: Array<string>) { }
  constructor(
    WSConnector: WsConnectorService,
    private sessionStorage: SessionStorageService,
    private time: TimeService,
    private command: CommandService,
    private pubsub: PubSubService,
    private gtmTrackingService: GtmTrackingService,
    private cmsService: CmsService,
    private pubSubService: PubSubService,
    private windowRef: WindowRefService,
    private fanzoneStorageService: FanzoneStorageService,
    private user: UserService
  ) {
    const wsOptions = {
      path: '/quickbet',
      reconnectionDelay: 1000,
      timeout: 10000,
      reconnectionAttempts: 3
    };

    this.generalConfig = remoteBetslipConstant.general;
    this.remoteBetslipConstant = remoteBetslipConstant;
    this.connection = WSConnector.create(environment.REMOTEBETSLIPMS, wsOptions, 'quickbet-ms');

    // Map of WS response ids to pubsub events
    this.pubsubEvents = {
      [remoteBetslipConstant.ds.add.change]: pubsub.API.YOURCALL_SELECTION_UPDATE,
      [remoteBetslipConstant.byb.add.change]: pubsub.API.YOURCALL_SELECTION_UPDATE
    };
    this.sessionId = null;
    this.handlersMap = {};

    this.onInit();
  }

  get configs(): IConstant {
    return this.remoteBetslipConstant;
  }

  set configs(value: IConstant) { }

  /**
   * Performs session restore if stored session ID has valid TTL.
   * @private
   */
  restoreSession(): void {
    const { id, date, betTrace } = this.getSessionData();

    if (this.isSessionValid(date)) {
      const { success } = this.configs.sgl.add;

      this.gtmTrackingService.restoreTracking(betTrace);

      this.sessionId = id;
      this.addHandler(success, selection => {
        this.command.executeAsync(this.command.API.QUICKBET_RESTORE, [selection]);
      });
      this.connection.updateOptions({ query: { id } });
      this.connection.connect();
    } else {
      this.clearSession();
      this.connection.connect();
    }
  }

  /**
   * Sends request to remote betslip MS to retrieve selection data.
   * @param {Object} outcome
   * @param {Object=} config
   */
  addSelection(outcome: IQuickbetRequestModel, config: IRemoteBetslipProviderConfig = this.configs.sgl): Observable<IConstant> {
    const { request, success, error, change } = config.add;
    const result = new Subject();
    this.windowRef.nativeWindow.clearTimeout(this.timeoutId);

    const fzStorage = this.fanzoneStorageService.get('fanzone') || {};
    outcome.fanzoneTeamId = ''
    if (this.user.status) {
      outcome.fanzoneTeamId = Object.keys(fzStorage).length && fzStorage.teamId ? fzStorage.teamId : outcome.fanzoneTeamId = '';
    }

    this.addHandler(success, selection => {
      this.windowRef.nativeWindow.clearTimeout(this.timeoutId);
      if(!outcome.isStreamBet) {
        this.storeSession();
      }
      result.next(selection);
      result.complete();
    });
    this.addHandler(error, this.getErrorHandler(result));

    if (change && this.pubsubEvents[change]) {
      this.addHandler(change, data => this.pubsub.publish(this.pubsubEvents[change], data));
    }

    this.timeoutId = this.windowRef.nativeWindow.setTimeout(() => {
      this.clearSession();
      this.connection.removeOption('query');
      this.connection.disconnect();
      result.error({ error: 'timeout' });
      result.complete();
    }, 30000);

    this.connection.emit(request, outcome)
      .subscribe({ error: this.getErrorHandler(result) });

    return result;
  }

  /**
   * Sends request to remote betslip MS to remove added selection.
   * @param {Object=} config
   */
  removeSelection(config: IRemoteBetslipProviderConfig = this.configs.sgl): void {
    const requestId = config.remove.request;

    this.connection.emit(requestId);
  }

  /**
   * Sends request to remote betslip MS to place bet.
   * @param {Object} bet
   * @param {Object=} config
   */
  placeBet(
    bet: IRemoteBetslipBet,
    config: IRemoteBetslipProviderConfig = this.configs.sgl
  ): Observable<any> {
    const { request, success, error, overask, bir } = this.getConfig(config);
    const result = new Subject();
    let isBir = false;

    this.addHandler(success, (value: IConstant) => {
      result.next(this.addIsBirFlagToReceipt(value, isBir));
      result.complete();
      this.implicitBalanceRefresh(true);
    });
    this.addHandler(error, this.getErrorHandler(result, true));
    this.addHandler(overask, this.overAskHandler(result));
    this.addHandler(bir, (value: { confirmationExpectedAt: string, provider: string }) => {
      isBir = value.provider === 'OpenBetBir';
      const seconds = value.confirmationExpectedAt;
      this.pubSubService.publish(this.pubSubService.API.QUICKBET_COUNTDOWN_TIMER, seconds);
    });

    this.connection.emit(request, bet)
      .subscribe({ error: this.getErrorHandler(result, true) });

    return result;
  }

  /**
   * Connects to web socket
   * @private
   */
  connect() {
    return this.connection.connect();
  }

  /**
   * Disconnects from web socket.
   * @private
   */
  disconnect() {
    return this.connection.disconnect();
  }

  /**
   * Initializes all needed operations:
   *   - adds global handler for all messages from WS;
   *   - adds general handler for session and error messages;
   *   - performs session restoring if needed.
   * @private
   */
  private onInit(): void {
    this.connection.addAnyMessagesHandler(this.anyMessageHandler.bind(this));
    this.addGeneralHandlers();
  }

  /**
   * Checks if give session timestamp is less than 24 hours ago.
   * @param {number} date
   * @returns {boolean}
   * @private
   */
  private isSessionValid(date: string): boolean {
    return this.time.daysDifference(date) < 1;
  }

  /**
   * Retrieves MS's session ID and timestamp from session storage.
   * @return {Object}
   * @private
   */
  private getSessionData(): IConstant {
    return this.sessionStorage.get(RemoteBetslipService.STORAGE_KEY) || {};
  }

  /**
   * Stores session ID and timestamp to session storage.
   * @private
   */
  private storeSession(): void {
    const betTrace = this.gtmTrackingService.getTracking();
    const selectionData = this.sessionStorage.get(RemoteBetslipService.STORAGE_KEY);

    let data: IConstant = {
      id: this.sessionId,
      date: Date.now()
    };

    if (betTrace) {
      Object.assign(data, { betTrace });
    }

    if (selectionData) {
      data = { ...data, selectionData };
    }
    this.sessionStorage.set(RemoteBetslipService.STORAGE_KEY, data);
 }

  /**
   * Clears session information from session storage.
   * @private
   */
  private clearSession(): void {
    this.windowRef.nativeWindow.clearTimeout(this.timeoutId);
    this.sessionStorage.remove(RemoteBetslipService.STORAGE_KEY);
  }

  /**
   * Checks if message ID is of Live fs type.
   * @param {string} name
   * @return {boolean}
   * @private
   */
  private isLiveUpdate(name: string): boolean {
    return _.some(RemoteBetslipService.UPDATE_CHANNELS, channel => {
      return name.indexOf(channel) > -1;
    });
  }

  /**
   * Handler for general session confirmation message.
   * @param {string} options.id
   * @private
   */
  private onSessionInitHandler({ id }): void {
    this.sessionId = id;
    this.connection.updateOptions({ query: { id } });
  }

  /**
   * Handler for session cleareance message.
   * @private
   */
  private onSessionClearHandler(): void {
    this.clearSession();
  }

  /**
   * Handler for general 'ERROR' message.
   * @param {Object} error
   * @private
   */
  private onErrorHandler(error: IConstant) {
    console.warn('Remote Betslip MS session error', error);
    this.clearSession();
    this.connection.removeOption('query');
    this.connection.disconnect();
    this.connection.connect().subscribe(() => {
      this.pubsub.publish(this.pubsub.API.REMOTE_BS_RECONNECT);
    });
  }

  /**
   * Adds handler function for given ID or this of IDs.
   * @param {Array|number} ids
   * @param {Function} handler
   * @private
   */
  private addHandler(ids: string | string[], handler: Function): void {
    if (_.isArray(ids)) {
      _.each(ids, id => {
        this.handlersMap[id] = handler;
      });
    } else if (ids) {
      this.handlersMap[ids] = handler;
    }
  }

  /**
   * Adds general handlers for session and error messages.
   * @private
   */
  private addGeneralHandlers(): void {
    this.addHandler(this.generalConfig.sessionInit, this.onSessionInitHandler.bind(this));
    this.addHandler(this.generalConfig.sessionClear, this.onSessionClearHandler.bind(this));
    this.addHandler(this.generalConfig.error, this.onErrorHandler.bind(this));
  }

  /**
   * Global handler for all WS's messages.
   * @param {string} id
   * @param {Object} data
   * @private
   */
  private anyMessageHandler(id: string, data: IConstant): void {
    const handler = this.handlersMap[id];

    if (_.isFunction(handler)) {
      handler(data);
    } else if (this.isLiveUpdate(id)) {
      this.pubsub.publish(this.pubsub.API.QUICKBET_SELECTION_UPDATE, [id, data]);
    }
  }

  /**
   * Handler for overAsk response after PlaceBet
   * @private
   */
  private overAskHandler(result: Subject<IConstant>): Function {
    return data => {
      this.pubsub.publish(this.pubsub.API.REMOTE_BETSLIP_OVERASK_TRIGGERED, data);
      result.error({ data: { error: { description: 'overask', code: 'OVERASK' } } });
      result.complete();
      this.implicitBalanceRefresh(false);
    };
  }

  private getErrorHandler(subject: Subject<IConstant>, updateBalance: boolean = false): Function {
    return (error: IConstant) => {
      this.windowRef.nativeWindow.clearTimeout(this.timeoutId);
      subject.error(error);
      subject.complete();
      updateBalance && this.implicitBalanceRefresh(false);
    };
  }

  private implicitBalanceRefresh(success: boolean): void {
    this.cmsService.getSystemConfig()
      .subscribe((systemConfig: ISystemConfig) => {
        const balanceRefreshConfig = systemConfig.BalanceUpdate && (success ? systemConfig.BalanceUpdate.RemoteBetslipSuccess :
          systemConfig.BalanceUpdate.RemoteBetslipError);

        if (balanceRefreshConfig) {
          this.pubSubService.publish(this.pubSubService.API.IMPLICIT_BALANCE_REFRESH);
        }
      });
  }

  /**
   * Add BIR status to the receipt
   * @param {IConstant} value should have a receipt for adding isBir status
   * @param {boolean} isBir status of BIR
   * @returns {IConstant} modified value in case there is a receipt
   */
  private addIsBirFlagToReceipt(value: IConstant, isBir: boolean): IConstant {
    if (value.hasOwnProperty('data') && value.data.hasOwnProperty('receipt')) {
      value.data.receipt[0] = { ...value.data.receipt[0], isBir };
    }
    return value;
  }


  /** 
  * get request config based on market
  * @param {Object} config
  * @param {boolean} isLuckyDip
  * @returns { request, success, error, overask, bir } config
  */
  private getConfig(config) {
    return this.sessionStorage.get('LuckyDip') ? config.luckyDipPlaceBet : config.placeBet;
  }
}
