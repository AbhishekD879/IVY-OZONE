import { from as observableFrom, of as observableOf,  Observable } from 'rxjs';

import { switchMap, map, catchError } from 'rxjs/operators';
import * as _ from 'underscore';
import { Injectable } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

import { BetHistoryApiModule } from '@betHistoryModule/bet-history-api.module';
import { UserService } from '@core/services/user/user.service';
import { SessionService } from '@authModule/services/session/session.service';

import { IBet, IBetDetail, IBetDetailLeg } from '@app/bpp/services/bppProviders/bpp-providers.model';
import { CashoutMapIndexService } from '@betHistoryModule/services/cashOutMapIndex/cashout-map-index.service';
import { CashoutDataProvider } from '@betHistoryModule/services/cashoutDataProvider/cashout-data.provider';
import { CashOutMapService } from '@betHistoryModule/services/cashOutMap/cash-out-map.service';
import { ICashoutMapItem } from '@betHistoryModule/models/cashout-map-item.model';

/**
 * Service which provide fetching event functionality
 */
@Injectable({ providedIn: BetHistoryApiModule })
export class BetsIntegrationService {
  constructor(
    private userService: UserService,
    private sessionService: SessionService,
    private cashoutMapIndexService: CashoutMapIndexService,
    private cashoutDataProvider: CashoutDataProvider,
    private cashOutMapService: CashOutMapService,
    private route: ActivatedRoute
  ) {}

  /**
   * Return cash out bets ids and placed bets (except already cash outed) for certain event
   * @param eventId
   * @param cashoutBetsArray
   * @param placedBetsArray
   * @return {{cashoutIds: Array, placedBets: Array}}
   */
  getBetsForEvent(eventId: number,
                  cashoutBetsArray: IBetDetail[],
                  placedBetsArray: IBetDetail[]): Observable<{ cashoutIds: ICashoutMapItem[], placedBets: IBetDetail[] }> {
    const placedBets = [];
    let cashoutIds = [];

    if (this.userService.isInShopUser()) {
      return observableOf({ cashoutIds, placedBets });
    }

    return Observable.create((observer) => {
      if (this.cashoutBetsHasEvent(eventId, cashoutBetsArray)) {
        this.cashOutMapService.createCashoutBetsMap(cashoutBetsArray, this.userService.currency, this.userService.currencySymbol, false);
        cashoutIds = this.cashoutMapIndexService.event[eventId];
      }

      _.each(placedBetsArray, (bet: IBetDetail) => {
        if (bet.cashoutStatus !== 'BET_CASHED_OUT') {
          placedBets.push(bet);
        }
      });

      observer.next({ cashoutIds, placedBets });
      observer.complete();
    });
  }

  getPlacedBets(eventId: number): Observable<IBetDetail[] | null> {
    if (!this.isSport() || this.userService.isInShopUser()) {
      return observableOf(null);
    }
    return observableFrom(this.sessionService.whenProxySession()).pipe(
      switchMap(() => {
        return this.getPlacedBetsWithCasOutDetails(eventId);
      }),
      map((bets: IBetDetail[]) => {
        return bets;
      }),
      catchError(() => observableOf(null)));
  }

  getCashOutBets(): Observable<IBetDetail[] | null> {
    if (!this.isSport() || this.userService.isInShopUser()) {
      return observableOf(null);
    }
    return observableFrom(this.sessionService.whenProxySession()).pipe(
      switchMap(() => {
        return this.cashoutDataProvider.getCashOutBets();
      }),
      map((bets: IBetDetail[]) => {
        return bets;
      }),
      catchError(() => observableOf(null)));
  }

  /**
   * Extend placed bets with cash out properties with help of getBetDetail request
   * @param placedBets
   * @returns {Promise<Object>}
   * @private
   */
  private extendPlacedBetsWithCashOutDetails(placedBets: IBet[]): Observable<IBetDetail[] | null> {
    if (_.isEmpty(placedBets)) {
      return observableOf(null);
    }
    return this.cashoutDataProvider.getBet(_.pluck(placedBets, 'betId'));
  }

  /**
   * Check whether is any of bets belongs to event
   * @param eventId
   * @param bets
   * @returns {boolean}
   * @private
   */
  private cashoutBetsHasEvent(eventId: number, bets: IBetDetail[] | IBetDetailLeg[]): boolean {
    return !_.isEmpty(bets) && _.some(bets, (item: IBetDetail | IBetDetailLeg) => {
      if (_.has(item, 'part')) {
        return Number((item as IBetDetailLeg).part[0].eventId) === eventId;
      }

      if (_.has(item, 'leg')) {
        return this.cashoutBetsHasEvent(eventId, (item as IBetDetail).leg);
      }

      return false;
    });
  }

  /**
   * get placed bets and modify them with cash out properties
   * @param eventId
   * @returns {Promise<Object>}
   */
  private getPlacedBetsWithCasOutDetails(eventId: number): Observable<IBetDetail[] | null> {
    return this.cashoutDataProvider.getPlacedBets(eventId).pipe(
      switchMap((data: IBet[]) => {
        return this.extendPlacedBetsWithCashOutDetails(data);
      }));
  }

  /**
   * Check if current rout is a sport
   * @return {boolean}
   * @private
   */
  private isSport(): boolean {
    return _.indexOf(['horseracing', 'greyhound'], this.route.snapshot.params['sport']) === -1;
  }
}
