import { Injectable } from '@angular/core';

import { BYBBet } from '../../models/bet/byb-bet';

import { CoreToolsService } from '@core/services/coreTools/core-tools.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { UserService } from '@core/services/user/user.service';
import { FracToDecService } from '@core/services/fracToDec/frac-to-dec.service';
import { IOddsParams } from '../../models/odds-params.model';
import { IYourcallAccumulatorOddsResponse } from '@yourcall/models/yourcall-api-response.model';
import { IAccumulatorOdds } from '@yourcall/models/yourcall-dashboard-odds.model';
import { IYourcallSelection } from '@yourcall/models/selection.model';
import { YourCallEvent } from '@yourcall/models/yourcall-event';


@Injectable({ providedIn: 'root' })
export class BybHelperService {
  private ERROR_CODES: { [key: string]: string; } = {
    PRICE_CHANGED: 'PRICE_CHANGED',
    STAKE_HIGH: 'STAKE_HIGH',
    DEFAULT: 'DEFAULT',
    SERVICE_ERROR: 'SERVICE_ERROR',
    EVENT_STARTED: 'EVENT_STARTED'
  };

  constructor(
    private coreTools: CoreToolsService,
    private localeService: LocaleService,
    private userService: UserService,
    private fracToDecService: FracToDecService
  ) {

  }

  /**
   * Generate params (payload) object for request
   * @param selections
   * @param game
   * @returns {object}
   */
  buildOddsParams(selections: IYourcallSelection[], game: YourCallEvent): IOddsParams {
    const groupedMarketSelections: IYourcallSelection[] = selections.filter(selection => !selection.playerId);
    const playerSelections: IYourcallSelection[] = selections.filter(selection => selection.playerId);

    return {
      obEventId: game._obEventId,
      selectionIds: groupedMarketSelections.map((selection: IYourcallSelection) => selection.id),
      playerSelections: playerSelections.map((selection: IYourcallSelection) => {
        return {
          statId: selection.statisticId,
          playerId: selection.playerId,
          line: selection.value
        };
      })
    };
  }

  /**
   * Parse the odds value from response
   * @param response
   * @returns {Promise}
   */
  parseOddsValue(response: IYourcallAccumulatorOddsResponse): Promise<any> {
    const data: IAccumulatorOdds = (response && response.data) || null;

    return data && data.priceNum && data.priceDen
      ? Promise.resolve(this.fracToDecService.getFormattedValue(data.priceNum, data.priceDen))
      : Promise.reject({ data });
  }

  /**
   * Parse the odds value from response
   * @param error
   */
  parseOddsError(error: any): string {
    console.warn('BYB:calculateAccumulatorOdds error', error);
    return (this.coreTools.getOwnDeepProperty(error, 'data.responseMessage') || '')
      .replace(/[\[\]]+/g, '');
  }

  /**
   * Prepares object for add selection request
   * @param data
   * @return {{}}
   */
  createSelectionData(data: any): IOddsParams {
    const groupedMarketSelections = data.selections.filter(selectionsData => !selectionsData.selection.playerId);
    const playerSelections = data.selections.filter(selectionsData => selectionsData.selection.playerId);

    return {
      obEventId: data.game.obEventId,
      selectionIds: groupedMarketSelections.map(selectionsData => selectionsData.selection.id),
      playerSelections: playerSelections.map(selectionsData => {
        return {
          statId: selectionsData.selection.statisticId,
          playerId: selectionsData.selection.playerId,
          line: selectionsData.selection.value
        };
      })
    };
  }

  /**
   * Create instance of new Banach bet
   * @param betData
   * @return {BYBBet}
   */
  createBet(betData: any): BYBBet {
    return new BYBBet(betData);
  }

  /**
   * Handle Banach specific error codes
   * @param error
   * @return {*}
   */
  getPlaceBetErrorMsg(error: any): string {
    switch (error.subErrorCode) {
      case this.ERROR_CODES.PRICE_CHANGED:
        return this.localeService.getString('yourCall.priceChangeWarning');

      case this.ERROR_CODES.STAKE_HIGH:
        if (error.maxStake) {
          return this.localeService .getString('yourCall.stakeValueExceeded', {
            stake: error.maxStake,
            currency: this.userService.currencySymbol
          });
        }

        return this.localeService .getString('yourCall.stakeExceeded');
      case this.ERROR_CODES.SERVICE_ERROR:
        return this.localeService.getString('yourCall.timeoutError');
      case this.ERROR_CODES.DEFAULT:
        return this.localeService .getString('yourCall.generalPlaceBetError');

      case this.ERROR_CODES.EVENT_STARTED:
        return this.localeService .getString('yourCall.eventStartedError');

      default:
        return '';
    }
  }
}
