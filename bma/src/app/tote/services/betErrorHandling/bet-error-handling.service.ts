import * as _ from 'underscore';
import { Injectable } from '@angular/core';
import { LocaleService } from '@core/services/locale/locale.service';
import { FiltersService } from '@core/services/filters/filters.service';
import { TOTE_CONFIG } from '@app/tote/tote.constant';
import { ToteBetSlipService } from '@app/tote/services/toteBetSlip/tote-bet-slip.service';

import { IPoolStake } from '@app/tote/models/pool-stake.model';
import { IPool } from '@app/tote/models/tote-event.model';
import {
  IOutcomeBetError,
  IStakeValidationState,
  ITotalStakeValidationState,
  IToteError,
  IToteErrorsMap
} from '@app/tote/services/betErrorHandling/tote-errors.model';
import { IToteOutcome } from '@app/tote/models/tote-outcome.model';

@Injectable()
export class BetErrorHandlingService {
  constructor(
    private locale: LocaleService,
    private filterService: FiltersService,
    private toteBetSlipService: ToteBetSlipService
  ) {}


  /**
   * Total stake error object
   *
   * @param  {[type]} pool       [description]
   * @param  {[type]} totalValue [description]
   * @return {[type]}            [description]
   */
  checkTotalStake(pool: IPool, totalValue: string): ITotalStakeValidationState {
    return {
      totalMax: this.isMaxValid(totalValue, pool.maxTotalStake),
      totalMin: this.isMinValid(totalValue, pool.minTotalStake),
      stakeIncrementFactor: this.isIncrementValid(totalValue, pool.stakeIncrementFactor)
    };
  }

  /**
   * Total stake error message
   */
  getTotalStakeErrorMsg(pool: IPool, totalStakeState: ITotalStakeValidationState, currency: string): string {
    const errorMessages = {
      totalMax: this.locale.getString(`tt.maxTotalStake`,
                                      { value: this.filterService.currencyPosition(pool.maxTotalStake, currency)}),
      totalMin: this.locale.getString(`tt.minTotalStake`,
                                      { value: this.filterService.currencyPosition(pool.minTotalStake, currency)}),
      stakeIncrementFactor: this.locale.getString(`tt.stakeIncrementFactor`,
                                                  { value: this.filterService.currencyPosition(pool.stakeIncrementFactor, currency)})
    };
    return errorMessages[_.findKey((totalStakeState as any), value => !!value)];
  }

  /**
   * Find errors in outcomes
   *
   * @param  {[type]}  eventData [description]
   * @return {Boolean}           [description]
   */
  isMarketsHasErrors(eventData: any): boolean {
    return eventData.markets[0].outcomes
      .map(outcome => {
        return outcome.error;
      })
      .some(item => {
        return _.has(item, 'type') && item.type === 'error';
      });
  }

  /**
   * @param {object} allErrors
   * @return {object}
   */
  generateServiceError(allErrors): {serviceError: IToteError} {
    // generate error object for general service error
    return {
      serviceError: {
        type: 'error',
        msg: allErrors[TOTE_CONFIG.TOTE_GENERAL_BET_ERROR_KEY.service]
      }
    };
  }

  /**
   * Generate event related error messages(suspension and event started errors)
   * @param {string} type
   * @return {object}
   */
  generateEventError(type: string): IToteError {
    return {
      type: 'error',
      msg: TOTE_CONFIG.TOTE_EVENT_RELATED_ERRORS[type]
    };
  }

  /**
   * @param {string} errorCode
   * @param {object} allErrors
   * @return {string}
   */
  generateOutcomeErrorMsg(errorCode: string, allErrors: IToteErrorsMap): string {
    if (_.has(allErrors, errorCode)) {
      // return custom msg for known sub error code
      return allErrors[errorCode];
    }
    // return general service error msg for unknown sub error codes
    return allErrors[TOTE_CONFIG.TOTE_GENERAL_BET_ERROR_KEY.bet];
  }

  /**
   * @param {object[]} failedBets
   * @param {object[]} eventData
   * @param {object} toteBetErrorsDescriptions
   */
  buildErrors(failedBets, eventData: any, toteBetErrorsDescriptions: IToteErrorsMap): any {
    // Detect if errors is custom or general
    const failedOutcomes = this.excludeOutcomeErrors(failedBets);
    if (_.has(failedOutcomes[0], 'serviceGenError')) {
      // Extend eventData with error object
      const serviceError = this.generateServiceError(toteBetErrorsDescriptions);
      eventData = _.extend(eventData, serviceError);
    } else {
      // Extend outcomes with error object
      eventData.markets[0].outcomes = this.extendOutcomeWithErrors(
        eventData.markets[0].outcomes,
        failedOutcomes,
        toteBetErrorsDescriptions
      );
    }
    return eventData;
  }

  /**
   * Creating pool stake error object
   *
   * @param  {object} eventData [description]
   * @param  {object} stakeState [description]
   * @return {}           [description]
   */
  buildPoolStakeError(eventData: any, stakeState: IPoolStake): void {
    const stakeObject = _.extend({}, this.validationState(stakeState), stakeState);

    eventData.markets[0].outcomes.forEach(item => {
      if (item.id === stakeObject.outcomeId && this.isRangeError(stakeObject)) {
        const errorKey = _.findKey(stakeObject, value => !!value);
        item.error = {
          type: 'error',
          msg: this.errorsMessages(errorKey, stakeObject)
        };
      }
    });
  }

  /**
   * Clear outcomes error properties
   * @param {object} eventData
   */
  clearBetErrors(eventData: any): void {
    eventData.markets[0].outcomes.forEach(outcome => {
      if (_.has(outcome, 'error')) {
        outcome.error = undefined;
      }
    });
  }

  /**
   * Clear outcomes error properties
   * @param {object} eventData
   * @param {string} outcomeId
   */
  clearLineBetErrors(eventData: any, outcomeId: string): void {
    eventData.markets[0].outcomes.forEach(outcome => {
      if (_.has(outcome, 'error')) {
        if (outcomeId === outcome.id) {
          outcome.error = undefined;
        }
      }
    });
  }

  /**
   * Checking if the increment follows the rules
   *
   * @param  {number}  value  Current value
   * @param  {number}  factor Increment factor
   * @return {Boolean}        true / false
   */
  private isIncrementValid(value: string, factor: string): boolean {
    const current = value ? Number(value) : 0;
    return Math.floor((Math.abs(current) * 100)) % Math.floor((Number(factor) * 100)) !== 0;
  }

  /**
   * Checking if the min value follows the rules
   *
   * @param  {number}  value    Number to check
   * @param  {number}  minStake Boundary value
   * @return {Boolean}          [description]
   */
  private isMinValid(value: string, minStake: string): boolean {
    return Number(minStake) > Number(value);
  }

  /**
   *  Checking if the max value follows the rules
   *
   * @param  {number}  value    Number to check
   * @param  {number}  maxStake Boundary value
   * @return {Boolean}          [description]
   */
  private isMaxValid(value: string, maxStake: string): boolean {
    return Number(maxStake) < Number(value);
  }

  /**
   * Checking if the one of the error occurred
   *
   * @param  {object}  state [description]
   * @return {Boolean}       [description]
   */
  private isRangeError(state: IPoolStake): boolean {
    return [state.minStakePerLine, state.maxStakePerLine, state.stakeIncrementFactor]
      .some(item => item) && Number(state.value) > 0;
  }

  /**
   * Validation state
   *
   * @param  {object} data [description]
   * @return {object}      [description]
   */
  private validationState(data: IPoolStake): IStakeValidationState {
    return {
      minStakePerLine: this.isMinValid(data.value, data.poolData.minStakePerLine),
      maxStakePerLine: this.isMaxValid(data.value, data.poolData.maxStakePerLine),
      stakeIncrementFactor: this.isIncrementValid(data.value, data.poolData.stakeIncrementFactor)
    };
  }

  /**
   * Getting translated string with value
   *
   * @param  {string} key  name of the error
   * @param  {object} data object with errors
   * @return {string}      transleted string with value
   */
  private errorsMessages(key: string, data: IPoolStake): string {
    return this.locale.getString(`tt.${key}`, {
      value: this.filterService.currencyPosition(data.poolData[key], this.toteBetSlipService.getCurrency(data.poolData.currencyCode))
    });
  }


  /**
   * Detect if errors is custom or general fetch errors and id's into build array of errors
   * @param {object[]} failedBets
   * @return {object[]} outcomesError
   */
  private excludeOutcomeErrors(failedBets): IOutcomeBetError[] {
    const outcomesError = [];

    failedBets.forEach(outcome => {
      if (_.has(outcome, 'error')) {
        // service error
        outcomesError.push({
          serviceGenError: outcome.code
        });
      }
      if (_.has(outcome, 'betError')) {
        if (_.has(outcome.betError[0], 'subErrorCode')) {
          outcomesError.push({
            // custom error for particular outcome
            id: outcome.leg[0].poolLeg.legPart[0].outcomeRef.id,
            subErrorCode: outcome.betError[0].subErrorCode
          });
        } else {
          // service error for particular outcome
          outcomesError.push({
            id: outcome.leg[0].poolLeg.legPart[0].outcomeRef.id,
            betGenError: outcome.betError[0].code
          });
        }
      }
    });
    return outcomesError;
  }

  /**
   * Extend outcomes data with error object
   * @param {object[]} outcomes
   * @param {object[]} failedOutcomes
   * @param {object} allErrors
   * @return {object[] | object}
   */
  private extendOutcomeWithErrors(outcomes: IToteOutcome[], failedOutcomes: IOutcomeBetError[], allErrors: IToteErrorsMap): IToteOutcome[] {
    outcomes.forEach(outcome => {
      failedOutcomes.forEach(failedOutcome => {
        if (failedOutcome.id === outcome.id) {
          // generate error for particular outcome
          if (_.has(failedOutcome, 'betGenError')) {
            // general error
            _.extend(outcome, {
              error: {
                type: 'error',
                msg: allErrors[TOTE_CONFIG.TOTE_GENERAL_BET_ERROR_KEY.bet]
              }
            });
          } else {
            // custom error
            _.extend(outcome, {
              error: {
                type: 'error',
                msg: this.generateOutcomeErrorMsg(failedOutcome.subErrorCode, allErrors)
              }
            });
          }
        }
      });
    });
    return outcomes;
  }
}

