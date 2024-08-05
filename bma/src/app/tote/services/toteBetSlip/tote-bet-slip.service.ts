import { map } from 'rxjs/operators';
import { Injectable } from '@angular/core';

import { Observable, of } from 'rxjs';
import { TOTE_CONFIG } from '../../tote.constant';

import { WinPoolBetsModel } from '../poolBetsModels/wn.model';
import { PlacePoolBetsModel } from '../poolBetsModels/pl.model';
import { ShowPoolBetsModel } from '../poolBetsModels/sh.model';
import { ExPoolBetsModel } from '../poolBetsModels/ex.model';
import { TrPoolBetsModel } from '../poolBetsModels/tr.model';

import { UserService } from '@core/services/user/user.service';
import { DeviceService } from '@core/services/device/device.service';
import { BppService } from '@app/bpp/services/bpp/bpp.service';
import { ToteBetReceiptService } from '../toteBetReceipt/tote-bet-receipt.service';
import { TimeSyncService } from '@core/services/timeSync/time-sync.service';

import { IToteEvent } from './../../models/tote-event.model';
import { IPoolBet, IPoolBetsModels } from './../../models/pool-bet.model';
import { ClientUserAgentService } from '@core/services/clientUserAgent/client-user-agent.service';

@Injectable()
export class ToteBetSlipService {

  private poolBetsModels: any;

  constructor(
    private user: UserService,
    private device: DeviceService,
    private bppService: BppService,
    private toteBetReceipt: ToteBetReceiptService,
    private clientUserAgentService: ClientUserAgentService,
    private timeSyncService: TimeSyncService
  ) {
    /**
     * Object with link to poolBetsModels
     * @type {{WN: WinPoolBetsModel}}
     * @private
     */
    this.poolBetsModels = {
      WN: WinPoolBetsModel,
      PL: PlacePoolBetsModel,
      SH: ShowPoolBetsModel,
      EX: ExPoolBetsModel,
      TR: TrPoolBetsModel
    };
  }

  /**
   * @param {string} poolName
   * @param {Object} eventEntity
   * @returns {undefined || _poolBetsModels}, _poolBetsModels - poll type instance
   */
  getPoolBetsInstance(poolName: string, eventEntity: IToteEvent): IPoolBetsModels {
    if (this.poolBetsModels[poolName]) {
      return new this.poolBetsModels[poolName](eventEntity, this.timeSyncService.ip);
    }
    return undefined;
  }

  /**
   * Pacing bets from poolBetsInstance bets array by making request to bet placement proxy
   * @param poolBetsInstance
   * @returns {Observable}
   */
  placeBets(poolBetsInstance): Observable<any> {
    const bet = poolBetsInstance && poolBetsInstance.bet;

    if (bet) {
      this.extendWithDetails(bet);

      const serviceName = poolBetsInstance.BPPService || 'placeBet';

      return (this.bppService.send(serviceName, bet) as Observable<any>).pipe(
        map(res => this.toteBetReceipt.betReceiptBuilder(poolBetsInstance.eventEntity, res))
      );
    }

    return of([]);
  }

  /**
   * Returns currency symbol according to currency in pool (e.g. 'HKD')
   * @param currency
   * @returns {String}
   */
  getCurrency(currency: string): string {
    return TOTE_CONFIG.currecySymbols[currency] || currency;
  }

  isUserLoggedIn(): boolean {
    return this.user.status;
  }

  /**
   * Assign user details to bet
   * @param {Object} bet
   * @private
   */
  private addUserDetails(bet: IPoolBet): void {
    bet.betslip.stake.currencyRef.id = this.user.currency;
    bet.bet[0].stake.currencyRef.id = this.user.currency;
  }

  /**
   * Assign device details to bet
   * @param {Object} bet
   * @private
   */
  private addDeviceDetails(bet: IPoolBet): void {
    bet.betslip.clientUserAgent = this.clientUserAgentService.getId();
    bet.betslip.slipPlacement.channelRef = this.device.channel.channelRef;
  }

  /**
   * Extend bet or bets with user and device details
   * @param {Object} bet
   * @private
   */
  private extendWithDetails(bet: IPoolBet): void {
    if (bet.requests && bet.requests.length) {
      this.extendArray(bet.requests);
    } else {
      this.extendBet(bet);
    }
  }

  /**
   * Extend each bet objects in array
   * @param {Array} betsArray
   * @private
   */
  private extendArray(betsArray: IPoolBet[]): void {
    betsArray.forEach(bet => this.extendBet(bet));
  }

  /**
   * Extend bet object with user and device details
   * @param bet
   * @private
   */
  private extendBet(bet: IPoolBet): void {
    this.addUserDetails(bet);
    this.addDeviceDetails(bet);
  }
}



