import { Injectable } from '@angular/core';
import { GET_DATA_MESSAGES } from '../../constants/messages';
import { Subject } from 'rxjs';
import * as _ from 'underscore';

import { InplayConnectionService } from '../inplayConnection/inplay-connection.service';

import { ISportEventData } from '../../models/module-data-item.model';
import { IRequestParams } from '../../models/request.model';
import { IDataTypes } from '@app/inPlay/services/inplayData/inplay-data.model';
import { InplayApiModule } from '@app/inPlay/inplay-api.module';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import environment from '@environment/oxygenEnvConfig';

@Injectable({
  providedIn: InplayApiModule
})
export class InplayDataService {
  loadDataTimeout: number;
  MATCH_RESULT_MARKET_IDENTIFICATOR: string = 'MR';
  FOOTBALL_MARKETS_TO_MODIFY = ['To Qualify', 'Penalty Shoot Out Winner', 'Penalty Shoot-Out Winner'];

  dataTypes: IDataTypes = {
    ribbon: {
      requestMessage: GET_DATA_MESSAGES.RIBBON.REQUEST_MESSAGE,
      buildResponseMessage() {
        return GET_DATA_MESSAGES.RIBBON.RESPONSE_MESSAGE;
      }
    },
    structure: {
      requestMessage: GET_DATA_MESSAGES.STRUCTURE.REQUEST_MESSAGE,
      buildResponseMessage() {
        return GET_DATA_MESSAGES.STRUCTURE.RESPONSE_MESSAGE;
      }
    },
    ls_structure: {
      requestMessage: GET_DATA_MESSAGES.LS_STRUCTURE.REQUEST_MESSAGE,
      buildResponseMessage() {
        return GET_DATA_MESSAGES.LS_STRUCTURE.RESPONSE_MESSAGE;
      }
    },
    sports: {
      requestMessage: GET_DATA_MESSAGES.SPORT.REQUEST_MESSAGE,
      buildResponseMessage(data) {
        return `${GET_DATA_MESSAGES.SPORT.RESPONSE_MESSAGE}::${data.categoryId}::${data.topLevelType}`;
      },
      additionalRequestParams: {
        emptyTypes: 'Yes',
        autoUpdates: 'No'
      }
    },
    competition: {
      requestMessage: GET_DATA_MESSAGES.COMPETITION.REQUEST_MESSAGE,
      buildResponseMessage(data) {
        const responseMessage = GET_DATA_MESSAGES.COMPETITION.RESPONSE_MESSAGE;

        if (data.marketSelector) {
          // eslint-disable-next-line max-len
          return `${responseMessage}::${data.categoryId}::${data.topLevelType}::${data.marketSelector}::${data.typeId}`;
        }

        return `${GET_DATA_MESSAGES.COMPETITION.RESPONSE_MESSAGE}::${data.categoryId}::${data.topLevelType}::${data.typeId}`;
      }
    },
    virtuals: {
      requestMessage: GET_DATA_MESSAGES.VIRTUALS.REQUEST_MESSAGE,
      buildResponseMessage() {
        return GET_DATA_MESSAGES.VIRTUALS.RESPONSE_MESSAGE;
      }
    }
  };

  constructor(
    private windowRefService: WindowRefService,
    private inPlayConnectionService: InplayConnectionService
  ) { }

  /**
   * Load data via websockets
   * @param {string} dataType
   * @param {object} loadParams
   * @returns {deferred} - promise, resolved after getting response message.
   */
  loadData<T>(dataType: string, loadParams: IRequestParams = {}): Subject<T> {
    let dataResolved = false;
    const loadDataPromiseTimeout = 30000;
    const isOnceTimeLitener = true;
    const requestMessage = this.dataTypes[dataType] && this.dataTypes[dataType].requestMessage;
    const responseMessage = this.dataTypes[dataType] && this.dataTypes[dataType].buildResponseMessage(loadParams);
    let emitParams = loadParams;
    const subject: Subject<T> = new Subject();

    if (this.loadDataTimeout) {
      clearTimeout(this.loadDataTimeout);
    }

    // hardcoded Sport request params. will be removed in future microservice releases, then should be removed here.
    if (this.dataTypes[dataType] && this.dataTypes[dataType].additionalRequestParams) {
      emitParams = _.extend({}, loadParams, this.dataTypes[dataType].additionalRequestParams);
    }

    if (requestMessage && responseMessage) {
      this.inPlayConnectionService.addEventListener(responseMessage, wsData => {
        // for competition response and only for football
        // when no market selector or "main market" market selector
        // modify main markets template view (home/away => home/draw/away)
        if (responseMessage.match(/::\d+$/) &&
                parseInt(loadParams.categoryId, 10)  === parseInt(environment.CATEGORIES_DATA.footballId, 10) &&
                   (!loadParams.marketSelector || loadParams.marketSelector === 'Main Market') && loadParams.modifyMainMarkets) {
          this.modifyMainMarkets(wsData);
        }

        subject.next(wsData);
        subject.complete();
        dataResolved = true;
      }, isOnceTimeLitener);

      this.inPlayConnectionService.emitSocket(requestMessage, emitParams);

      this.loadDataTimeout = this.windowRefService.nativeWindow.setTimeout(() => {
        if (!dataResolved) {
          subject.error(`error data. response ${responseMessage} was not resolved`);
          subject.complete();
          this.inPlayConnectionService.setConnectionErrorState(true);
        }
      }, loadDataPromiseTimeout);
    }

    return subject;
  }

  /**
   * To qualify and Penalty markets have "home/away" type,
   * but we need to show all sections with "home/draw/away" odds card header.
   * thats why we need to emulate MatchResult market.
   * @param wsData
   */
  modifyMainMarkets(wsData: ISportEventData[]): void {
    _.forEach(wsData, event => {
      // each event has only one market
      const market = event.markets[0];

      if (market && _.contains(this.FOOTBALL_MARKETS_TO_MODIFY, market.templateMarketName)) {
        market.marketMeaningMinorCode = this.MATCH_RESULT_MARKET_IDENTIFICATOR;
        market.dispSortName = this.MATCH_RESULT_MARKET_IDENTIFICATOR;
      }
    });
  }
}
