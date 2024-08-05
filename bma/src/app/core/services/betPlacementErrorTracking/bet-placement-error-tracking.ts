import { Injectable } from '@angular/core';
import { Location } from '@angular/common';
import * as _ from 'underscore';

import { IMultipleBet } from '../../models/multiple-bet.model';
import { ISingleBet } from '../../models/single-bet.model';
import { GtmService } from '../gtm/gtm.service';
import { IBetError, IErrorsType, IGtmBetErrors } from './bet-placement-error-tracking.model';
import { CommandService } from '@core/services/communication/command/command.service';
import { ITrackEvent } from '@core/services/gtm/models';

@Injectable()
export class BetPlacementErrorTrackingService {

  private betPlacementErrorStatic: ITrackEvent & { [key: string]: string };

  constructor(private gtmService: GtmService, private command: CommandService, private location: Location) {
    this.betPlacementErrorStatic = {
      event: 'trackEvent',
      eventCategory: 'betslip',
      eventAction: 'place bet',
      eventLabel: 'failure'
    };

    this.sendBetSlip = this.sendBetSlip.bind(this);
  }

  // TODO: migration. Find an external model for additional errors, comes from Betslip.
  /**
   * Send collected errors info to gtm service
   * @param {ISingleBet[]} singles
   * @param {IMultipleBet[]} multiples
   * @param {array} errors
   * @param {string} globalErrorCode
   * @param {string} globalErrorMsg
   * @param {IErrorsType} errorsType
   */
  sendBetSlip(singles: ISingleBet[],
    multiples: IMultipleBet[],
    errors: any[],
    globalErrorCode: string = null,
    globalErrorMsg: string = null,
    errorsType: IErrorsType): void {
    const betsErrors = this.gatherAllBetsErrors(singles, multiples),
      betsErrorsObject = this.genErrorObject(betsErrors, globalErrorCode, globalErrorMsg, errorsType, errors),
      gtmData = Object.assign({}, this.betPlacementErrorStatic, betsErrorsObject, {
        location: this.location.path()
      });

    this.command.executeAsync(this.command.API.GET_LIVE_STREAM_STATUS, undefined, false).then(streamData => {
      if (streamData) {
        _.extend(gtmData, {
          streamActive: streamData.streamActive,
          streamID: streamData.streamID
        });
      }
      this.gtmService.pushBetPlacementErrorInfo(gtmData);
    });
  }

  /**
   * Send collected lotto errors info to gtm service
   * @param errorCode
   * @param errorMessage
   */
  sendLotto(errorCode: string, errorMessage: string): void {
    this.sendAsCategory('Lotto', errorCode, errorMessage);
  }

  /**
   * Send collected Football Jackpot errors info to gtm service
   * @param errorCode
   * @param errorMessage
   */
  sendJackpot(errorCode: string, errorMessage: string): void {
    this.sendAsCategory('Football', errorCode, errorMessage);
  }

  /**
   * Extracts Error Data for bet
   * @param bet
   * @returns {void|*}
   */
  private extractErrorData(bet: ISingleBet | IMultipleBet): IBetError {
    const betLegs = bet.Bet.legs,
      freeBetsAmount = bet.stake.freeBetAmount,

      // legs - selections data in bet legs
      betSelectionsInfo = betLegs.reduce((currLeg, l) => {
        // parts - selection data in leg parts
        return l.parts.reduce((curr, p) => {
          const outcomeDetails = p.outcome.details,
            isBetInPlay = !!(outcomeDetails.info.isStarted && outcomeDetails.isMarketBetInRun);
          curr.betCategory.push(outcomeDetails.info.sport);
          curr.betInPlay.push(isBetInPlay);
          return curr;
        }, currLeg);
      }, { betCategory: [], betInPlay: [] });

    return Object.assign({}, {
      errorCode: bet.error || bet.Bet.error,
      errorMessage: bet.errorMsg || bet.Bet.errorMsg,
      betType: bet.type,
      isFreeBets: !!freeBetsAmount
    }, betSelectionsInfo);
  }

  /**
   * gathers errors from bets array
   * @param {ISingleBet[] | IMultipleBet[]} betList
   * @returns {Array}
   */
  private gatherBetsErrors(betList: Array<ISingleBet | IMultipleBet>): IBetError[] {
    const betsWithErrors = [];

    _.forEach(betList, bet => {
      betsWithErrors.push(this.extractErrorData(bet));
    });

    return betsWithErrors;
  }

  /**
   * gathers All Bets Errors
   * @param singles
   * @param multiples
   * @returns {*[]}
   */
  private gatherAllBetsErrors(singles: ISingleBet[], multiples: IMultipleBet[]): IBetError[] {
    // do not check bets for errors when global error exists
    // gather bets selection info only
    const singlesErrors = this.gatherBetsErrors(singles),
      multiplesErrors = this.gatherBetsErrors(multiples);
    return [...singlesErrors, ...multiplesErrors];
  }

  /**
   * generates bonusBet value for error
   * @param {array} errorsArray
   * @returns {boolean}
   */
  private genBonusBet(errorsArray): string {
    return _.contains(_.pluck(errorsArray, 'isFreeBets'), true) ? 'true' : 'false';
  }

  /**
   * process Error String string to string format
   * @param {string} text
   * @returns {string}
   */
  private processErrorString(text: string = ''): string {
    return text.toString().replace(/_/g, ' ')
      .toLowerCase();
  }

  /**
   * generates error type for errorCode and errorMessage
   * @param {array} errorsArr
   * @param {array} globalErrorsArr
   * @param {string} type
   * @returns {string}
   */
  private genErrorType(errorsArr: IBetError[],
    globalErrorsArr: any[],
    type: string): string {
    return globalErrorsArr.length > 1 ? 'multiple errors' : this.processErrorString(errorsArr[0][type] || globalErrorsArr[0].code);
  }

  /**
   * generate error object ready to be send to gtm
   * @param {array} errors
   * @param {boolean} errCode
   * @param {boolean} errMsg
   * @param {object} errorsType
   * @param {object} globalErrors
   * @returns {{errorCode: string, errorMessage: string, betType: string, betCategory: string, betInPlay: string, bonusBet: boolean}}
   */
  private genErrorObject(errors: IBetError[],
    errCode: string,
    errMsg: string,
    errorsType: IErrorsType,
    globalErrors: any[]): IGtmBetErrors {
    return {
      errorCode: errCode ? this.processErrorString(errCode) : this.genErrorType(errors, globalErrors, 'errorCode'),
      errorMessage: errMsg ? this.processErrorString(errMsg) : this.genErrorType(errors, globalErrors, 'errorMessage'),
      bonusBet: this.genBonusBet(errors)
    };
  }

  /**
   * Sends data to gtm service with info about given category.
   * @param {string} category
   * @param {string} errorCode
   * @param {string} errorMessage
   */
  private sendAsCategory(category: string, errorCode: string, errorMessage: string): void {
    const gtmData: IGtmBetErrors = Object.assign({}, this.betPlacementErrorStatic, {
      errorCode: this.processErrorString(errorCode),
      errorMessage: this.processErrorString(errorMessage),
      betType: 'Single',
      betCategory: category,
      betInPlay: 'No',
      bonusBet: 'false'
    });

    this.gtmService.pushBetPlacementErrorInfo(gtmData);
  }
}
