import { Injectable } from '@angular/core';
import * as _ from 'underscore';
import { LocaleService } from '@core/services/locale/locale.service';

@Injectable({
  providedIn: 'root'
})
export class UkTotesBetRecognitionService {
  private recognizeWinBet: Function;
  private recognizePlaceBet: Function;
  private betTypeMapper: { [key: string]: Function };

  constructor(
    private locale: LocaleService
  ) {
    this.recognizeWinBet = _.partial(this.recognizeWinOrPlaceBet, _, 'oneSelectionWinBet', 'multipleSelectionsWinBet');
    this.recognizePlaceBet = _.partial(this.recognizeWinOrPlaceBet, _, 'oneSelectionPlaceBet', 'multipleSelectionsPlaceBet');
    this.betTypeMapper = {
      // UK tote
      UEXA: this.recognizeExactaBet.bind(this),
      UTRI: this.recognizeTrifectaBet.bind(this),
      UWIN: this.recognizeWinBet.bind(this),
      UPLC: this.recognizePlaceBet.bind(this),
      // International tote
      EX: this.recognizeExactaBet.bind(this),
      TR: this.recognizeTrifectaBet.bind(this),
      WN: this.recognizeWinBet.bind(this),
      PL: this.recognizePlaceBet.bind(this)
    };
  }

  recognizeBet(items, poolType: string = 'default'): string {
    const mapper = this.betTypeMapper[poolType];
    return typeof mapper === 'function' ? mapper(items) : (mapper || '');
  }

  /**
   * Recognizer function for exacta pools
   * @param {array} items - array of selections
   */
  private recognizeExactaBet(items): string {
    // Rule : two selections added (1st and 2nd)
    if (Object.keys(items).length === 2) {
      return this.locale.getString('uktote.strightExactaBet');
    }
    // Rule : two ANY selections(from any column) added
    if (items.any && items.any.length === 2) {
      return this.locale.getString('uktote.reverseExactaBet');
    }
    /* Rule : MORE than two ANY selections(from any column) added, calculation of combination number is:
        number_of_selections * (number_of_selections - 1)
     */
    if (items.any && items.any.length >= 3) {
      const length = items.any.length,
        combinationNumber = length * (length - 1);
      return this.locale.getString('uktote.combinationExactaBet', [combinationNumber]);
    }
    return '';
  }

  /**
   * Recognizer function for trifecta pools
   * @param {array} items - array of selections
   */
  private recognizeTrifectaBet(items): string {
    // Rule : 3 selections added (1st,2nd and 3rd)
    if (Object.keys(items).length === 3) {
      return this.locale.getString('uktote.strightTrifectaBet');
    }
    /* Rule : MORE than two ANY selections(from any column) added, calculation of combination number is:
        No of selections x next lowest number x (next lowest number-1)
     */
    if (items.any && items.any.length >= 3) {
      const length = items.any.length,
        combinationNumber = length * (length - 1) * (length - 2);
      return this.locale.getString('uktote.combinationTrifectaBet', [combinationNumber]);
    }
    return '';
  }

  private recognizeWinOrPlaceBet(items, oneSelectionTranslation, multipleSelectionsTranslation): string {
    if (!items.any || !items.any.length) {
      return '';
    }
    const translation = items.any.length > 1 ? multipleSelectionsTranslation : oneSelectionTranslation;
    return this.locale.getString(`uktote.${translation}`, [items.any.length]);
  }
}
