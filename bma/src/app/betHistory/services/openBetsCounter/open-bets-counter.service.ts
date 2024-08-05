import { Injectable } from '@angular/core';
import { from as observableFrom, Subscription, BehaviorSubject, Observable, Subject } from 'rxjs';
import { mergeMap, takeUntil } from 'rxjs/operators';

import { BetHistoryApiModule } from '@app/betHistory/bet-history-api.module';

import { IBetCount, IFilteredPageBets } from '@app/betHistory/models/bet-history.model';
import { IOpenBetsCount } from '@app/bpp/services/bppProviders/bpp-providers.model';

import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { UserService } from '@core/services/user/user.service';
import { SessionService } from '@authModule/services/session/session.service';
import { BetHistoryMainService } from '@app/betHistory/services/betHistoryMain/bet-history-main.service';
import { AuthService } from '@authModule/services/auth/auth.service';

@Injectable({ providedIn: BetHistoryApiModule })
export class OpenBetsCounterService {
  filter: string = '';

  readonly betType: string = 'open';
  readonly maxOpenBetsCount: number = 20;

  protected loadDataSub: Subscription;
  private readonly NAME: string = 'BetsCounter';
  private openBetsCount$: BehaviorSubject<IOpenBetsCount> = new BehaviorSubject<IOpenBetsCount>({
    count: 0,
    moreThanTwenty: false
  });
  private destroyed$ = new Subject();
  constructor(
    protected pubsub: PubSubService,
    private userService: UserService,
    protected sessionService: SessionService,
    private betHistoryMainService: BetHistoryMainService,
    private authService: AuthService
  ) {
    this.pubsub.subscribe(this.NAME, this.pubsub.API.BETS_COUNTER_PLACEBET, this.handleMyBetsCounter.bind(this));
    this.pubsub.subscribe(this.NAME, this.pubsub.API.BETS_COUNTER_CASHOUT_BET, this.handleCashoutBet.bind(this));
    this.pubsub.subscribe(this.NAME, this.pubsub.API.BETS_COUNTER_OPEN_BETS, this.handleBetsCunterOpenBets.bind(this));
    this.pubsub.subscribe(this.NAME, this.pubsub.API.SESSION_LOGOUT, this.handleLogOut.bind(this));
  }

  init(): Observable<IOpenBetsCount> {
    this.authService.sessionLoggedIn
      .pipe(
        mergeMap((): Observable<any> => {
          return observableFrom(this.sessionService.whenUserSession());
        }),
        takeUntil(this.destroyed$)
      )
      .subscribe(() => {
        this.loadData();
      });

    return this.getOpenBetsCount();
  }

  unsubscribeBetsCounter(): void {
    this.pubsub.unsubscribe(this.NAME);
    this.destroyed$.next(null);
    this.destroyed$.complete();
  }

  protected loadData(): void {
    if (this.userService.isInShopUser()) {
      this.openBetsCount$.next({ count: 0, moreThanTwenty: false });
      return;
    }

    if (this.loadDataSub) {
      this.loadDataSub.unsubscribe();
    }

    this.loadDataSub = observableFrom(this.sessionService.whenProxySession())
      .pipe(mergeMap(() => this.betHistoryMainService.getBetsCountForYear(this.filter, this.betType)))
      .subscribe((data: IBetCount) => {
        data && this.openBetsCount$.next(
          data.betCount.includes('+') ?
            { count: this.maxOpenBetsCount, moreThanTwenty: true } :
            { count: +data.betCount, moreThanTwenty: false }
        );
      });
  }

  private handleBetsCunterOpenBets(pageBets: IFilteredPageBets): void {
    const pageBetsData = pageBets.data;
    if (pageBetsData && pageBetsData.bets) {
      const openSportBets = pageBetsData.bets.length;
      const betsPageToken = pageBetsData.pageToken;
      if (pageBets.filter === 'bet') {
        this.openBetsCount$.next({
          count: openSportBets <= this.maxOpenBetsCount ? openSportBets : this.maxOpenBetsCount,
          moreThanTwenty: openSportBets > this.maxOpenBetsCount || !!(betsPageToken && betsPageToken.length)
        });
      }
    }
  }

  private getOpenBetsCount(): Observable<IOpenBetsCount> {
    return this.openBetsCount$.asObservable();
  }

  private handleCashoutBet(): void {
    const currentValue = this.openBetsCount$.getValue();

    if (currentValue.moreThanTwenty) {
      this.loadData();
    } else
    if (currentValue.count) {
      this.decreaseCount(currentValue.count);
    }
  }

  private decreaseCount(currentValue: number): void {
    this.openBetsCount$.next({ count: currentValue - 1, moreThanTwenty: false });
  }

  private handleMyBetsCounter(amountBet: number = 1): void {
    const openBetsCount = this.openBetsCount$.getValue().count + amountBet;

    this.openBetsCount$.next({
      count: openBetsCount <= this.maxOpenBetsCount ? openBetsCount : this.maxOpenBetsCount,
      moreThanTwenty: openBetsCount > this.maxOpenBetsCount
    });
  }

  private handleLogOut(): void {
    if (this.loadDataSub) {
      this.loadDataSub.unsubscribe();
    }
    this.openBetsCount$.next({ count: 0, moreThanTwenty: false });
  }
}
