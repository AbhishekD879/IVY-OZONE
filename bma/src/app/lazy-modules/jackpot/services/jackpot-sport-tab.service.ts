import { of as observableOf,  Observable, throwError } from 'rxjs';

import { catchError, concatMap } from 'rxjs/operators';
import { Injectable } from '@angular/core';
import * as _ from 'underscore';

import { TimeSyncService } from '@core/services/timeSync/time-sync.service';
import { BppService } from '../../../bpp/services/bpp/bpp.service';
import { DeviceService } from '@core/services/device/device.service';
import { UserService } from '@core/services/user/user.service';
import { StorageService } from '@core/services/storage/storage.service';

import { IBetsResponse } from '@app/bpp/services/bppProviders/bpp-providers.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { IPoolEntity } from '@core/models/pool.model';
import { IOutcome } from '@core/models/outcome.model';
import { ClientUserAgentService } from '@core/services/clientUserAgent/client-user-agent.service';

@Injectable()
export class JackpotSportTabService {
  betsArray: string[] = [];

  constructor(
    private deviceService: DeviceService,
    private storageService: StorageService,
    private userService: UserService,
    private bppService: BppService,
    private clientUserAgentService: ClientUserAgentService,
    private timeSyncService: TimeSyncService
  ) {
    this.betsArray = this.storageService.get('footballJackpot') || [];
  }

  /**
   * Deletes all the bets
   */
  removeAllBets(): void {
    this.betsArray = [];
    this.storageService.set('footballJackpot', []);
  }

  /**
   * Deletes jackpot stake
   */
  removeStake(): void {
    this.storageService.set('footballJackpotStake', 1);
  }

  /**
   * Get Stake from Storage
   * @returns {number}
   */
  getStake(): number {
    return this.storageService.get('footballJackpotStake') || 1;
  }

  /**
   * Adds jackpot stake
   * @param {number} stake
   */
  addStake(stake: number): void {
    this.storageService.set('footballJackpotStake', stake);
  }

  /**
   * Gets outcomeId and checks whether it has already been made or not
   * @param {string} outcomeId
   * @returns {boolean}
   */
  isSelected(outcomeId: string): boolean {
    return this.betsArray.indexOf(outcomeId) !== -1;
  }

  /**
   * Deletes bet if it has been made and adds if not
   * @param {string} outcomeId
   * @param {ISportEvent} eventEntity
   */
  addBet(outcomeId: string, eventEntity: ISportEvent): void {
    const selected = this.isSelected(outcomeId);

    if (!selected) {
      eventEntity.selected++;
      this.betsArray.push(outcomeId);
    } else {
      eventEntity.selected--;
      this.betsArray.splice(this.betsArray.indexOf(outcomeId), 1);
    }

    this.storageService.set('footballJackpot', this.betsArray);
  }

  /**
   * Removes all previous bets and makes new ones for every of the events
   * @param {ISportEvent[]} initialData
   */
  makeLuckyDip(initialData: ISportEvent[]): void {
    let randomOutcome;

    this.removeAllBets();

    _.each(initialData, (item: ISportEvent) => {
      item.selected = 0;
      if (!item.unavailable) {
        // Gets random outcome with active status code
        randomOutcome = _.sample(_.reject(item.markets[0].outcomes, (outcome: IOutcome) => {
          return outcome.outcomeStatusCode === 'S';
        }));
        // Add random outcome to bet-slip
        this.addBet(randomOutcome.id, item);
      }
    });
  }

  /**
   * Place Jackpot Bet
   * @param {number} amount
   * @param {number} stakePerLine
   * @param {string[]} outcomeIds
   * @param {IPoolEntity} pool
   * @param {number} linesNumber
   * @returns {Observable<IBetsResponse>}
   */
  placeJackpotBet(amount: number, stakePerLine: number, outcomeIds: string[],
                  pool: IPoolEntity, linesNumber: number): Observable<IBetsResponse> {
    if (!this.userService.status) {
     return throwError({ code: 'NOT_LOGGEDIN' });
    } else if (+this.userService.sportBalance < amount) {
      return throwError({ code: 'INSUFFICIENT_FUNDS' });
    } else {
     return this.sentBetRequest(amount, stakePerLine, outcomeIds, pool, linesNumber);
    }
  }

  /**
   * Sort Jackpot Data
   * @param {ISportEvent[]} data
   * @returns {ISportEvent[]}
   */
  sortJackpotData(data: ISportEvent[]): ISportEvent[] {
    return _(data).chain().sortBy((event: ISportEvent) => {
      return event.name;
    }).sortBy((event: ISportEvent) => {
      return event.displayOrder;
    }).sortBy((event: ISportEvent) => {
      return event.typeDisplayOrder;
    }).sortBy((event: ISportEvent) => {
      return event.classDisplayOrder;
    }).sortBy((event: ISportEvent) => {
      return event.startTime;
    }).value();
  }

  /**
   * Send Bet Request
   * @param {number} amount
   * @param {number} stakePerLine
   * @param {string[]} outcomeIds
   * @param {IPoolEntity} pool
   * @param {number} linesNumber
   * @returns {Observable<IBetsResponse>}
   */
  private sentBetRequest(amount: number, stakePerLine: number, outcomeIds: string[],
                         pool: IPoolEntity, linesNumber: number): Observable<IBetsResponse> {
    const jackpotBet: IBetsResponse = {
      betslip: {
        clientUserAgent: this.clientUserAgentService.getId(),
        documentId: '1',
        stake: {
          amount: Number(amount).toFixed(2),
          stakePerLine: Number(stakePerLine).toFixed(2),
          currencyRef: { id: this.userService.currency }
        },
        slipPlacement: _.extend(
          { IPAddress: this.timeSyncService.ip },
          this.deviceService.channel
        ),
        betRef: [{
          documentId: '1'
        }]
      },
      bet: [{
        documentId: '1',
        betTypeRef: {
          id: pool.type
        },
        stake: {
          amount: Number(amount).toFixed(2),
          stakePerLine: Number(stakePerLine).toFixed(2),
          currencyRef: { id: this.userService.currency }
        },
        legRef: [{
          ordering: '1',
          documentId: '1'
        }],
        lines: { number: linesNumber }
      }],
      leg: [{
        documentId: '1',
        poolLeg: {
          poolRef: {
            id: pool.id
          },
          legPart: this.createOutcomesElements(outcomeIds)
        }
      }]
    };

    return (this.bppService.send('placeBet', jackpotBet) as Observable<IBetsResponse>).pipe(
      concatMap((response: IBetsResponse) => {
        const error = response.betError && response.betError[0];
        if (error) {
          return throwError({
            code: error.subErrorCode || error.code,
            errorDesc: error.errorDesc || error.subErrorCode
          });
        } else {
          return observableOf(response);
        }
      }), catchError(error => {
        return throwError({ code: error && error.message });
      }));
  }

  /**
   * Create outcomeRef element
   * @param {string[]} outcomeIds
   * @returns {{outcomeRef: {id: string}}[]}
   */
  private createOutcomesElements(outcomeIds: string[]): { outcomeRef: { id: string } }[] {
    return outcomeIds.map(id => {
      return { outcomeRef: { id } };
    });
  }
}
