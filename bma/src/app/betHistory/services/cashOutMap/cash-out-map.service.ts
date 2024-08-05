import { Injectable } from '@angular/core';
import * as _ from 'underscore';

import { BetHistoryApiModule } from '@betHistoryModule/bet-history-api.module';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { CashoutErrorMessageService } from '../cashoutErrorMessageService/cashout-error-message.service';
import { BetModelService } from '../betModelService/bet-model.service';
import { CashoutMapIndexService } from '../cashOutMapIndex/cashout-map-index.service';
import {
  CashOutLiveUpdatesSubscribeService
} from '@app/betHistory/services/cashOutLiveUpdatesSubscribeService/cashOutLiveUpdatesSubscribeService';

import { CashOutBetsMap } from '../../betModels/cashOutBetsMap/cash-out-bets-map.class';
import { IBetDetail } from '@app/bpp/services/bppProviders/bpp-providers.model';
import { BetHistoryMainService } from '@app/betHistory/services/betHistoryMain/bet-history-main.service';
import { LocaleService } from '@app/core/services/locale/locale.service';

/**
 * Service which provide fetching event functionality
 */
@Injectable({ providedIn: BetHistoryApiModule })
export class CashOutMapService {

  cashoutBetsMap: CashOutBetsMap;

  private readonly title = 'CashOutMapService';

  constructor(
    private pubSubService: PubSubService,
    private cashOutErrorMessage: CashoutErrorMessageService,
    private betModelService: BetModelService,
    private cashOutMapIndex: CashoutMapIndexService,
    private cashOutLiveUpdatesSubscribeService: CashOutLiveUpdatesSubscribeService,
    private betHistoryMainService: BetHistoryMainService,
    private localeService: LocaleService
  ) {
    this.init();
  }

  registerEvents(): void {
    this.pubSubService.subscribe(this.title, this.pubSubService.API.SESSION_LOGOUT, () => {
      this.cashoutBetsMap.mapState.isUserLogOut = true;
      this.cashoutBetsMap.reset(null);
    });

    this.pubSubService.subscribe(this.title, this.pubSubService.API.SUCCESSFUL_LOGIN, () => {
      this.cashoutBetsMap.mapState.isUserLogOut = false;
      this.cashoutBetsMap.reset(null);
    });
  }

  /**
   * Create cashoutBetsMap object from controller | mutable function
   * @param betsArr  {array}
   * @param currency {string}
   * @param currencySymbol {string}
   * @param fromWS {boolean} identifies whether bets are received from Cash Out WS
   * @returns {object}
   */
  createCashoutBetsMap(betsArr: IBetDetail[], currency: string, currencySymbol: string, fromWS: boolean = true): CashOutBetsMap {
    const map = this.cashoutBetsMap;

    let betsFromServer = betsArr,
      mergePredicate = null;
    if (!_.isEmpty(map)) {
      const idsForDeleteFromResponseBetArr = map.getBetsByCriterias({ inProgress: true });

      mergePredicate = function(item) {
        return item ? !item.isConfirmed : true;
      };

      betsFromServer = _.reject(betsArr, elm => {
        return idsForDeleteFromResponseBetArr.indexOf(elm.betId) !== -1;
      });
      map.deleteSuccessBets();
    }
    const updatedBets = this.cashoutBetsMap.createUpdatedCashoutBetsMap(betsFromServer, currency, currencySymbol, fromWS);

    map.extend(map, updatedBets, mergePredicate);
    map.deleteCompletedBets(updatedBets);

    this.cashoutBetsMap.mapState.isEmpty = this.cashoutBetsMap.isEmptyObj(map);

    // unsubscribe from the previous outcomes and subscribe for a new ones
    this.cashOutLiveUpdatesSubscribeService.addWatch(map);

    return map;
  }

  deleteCashOutBetOnTimeout(id: string, timeout: number): void {
    setTimeout(() => {
      this.cashoutBetsMap.deleteBets([id], null);
      this.cashoutBetsMap.mapState.isEmpty = this.isEmptyObj(this.cashoutBetsMap);
    }, timeout);
  }

  /**
   * Is object empty
   * @param obj {object}
   * @returns {boolean}
   */
  isEmptyObj(obj): boolean {
    for (const key in obj) {
      // hasOwnProperty doesn't work in Windows Phone
      if (Number(key)) {
        return false;
      }
    }
    return true;
  }

  /**
   * Init function for(callbacks, watchers, scope destroying)
   * @private
   */
  private init(): void {
    this.cashoutBetsMap = new CashOutBetsMap(this.cashOutMapIndex, this.betModelService, this.cashOutErrorMessage,
      this.betHistoryMainService, this.localeService);
    // set event name
    this.registerEvents();
  }
}
