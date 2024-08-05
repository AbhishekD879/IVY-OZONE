'use strict';

import { PoolBetsModel } from './pool-bets-model';

import { IPoolBet, IPoolBetLegPoolLegPart } from './../../models/pool-bet.model';
import { IFieldsControls } from './../../models/field-controls.model';

/**
 * Class for represent functionality for exacta bet model
 * @class
 */
export class ExPoolBetsModel extends PoolBetsModel {

  outcomeIds: string[];
  private _fieldsControls: IFieldsControls;
  private _totalStake: number;

  constructor(eventEntity, ip: string, poolType = 'EX') {
    super(eventEntity, ip, poolType);
    /**
     * @member {Object} with props as array witch should contain function which
     * can be added from some outside component
     */
    this._fieldsControls = {
      clearField: []
    };
    /**
     * @member {Number}
     */
    this._totalStake = 0;
  }

  /**
   * Create array with selected outcome ids
   * @param outcomeIds
   */
  changeValue(ids: string[]): void {
    this.outcomeIds = ids;
  }

  /**
   * Change stake value and refresh total stake amount
   * @param value
   */
  stakeValue(value: string): void {
    const number = value ? parseFloat(value).toFixed(2) : '0';
    this._totalStake = parseFloat(number);
  }

  /**
   * Clear bets by set all stakes values to 0, refresh total stake amount and clear fields
   */
  clearBets(): void {
    this._totalStake = 0;
    this.clearFields();
  }

  /**
   * Link to fieldsControls private property
   * @returns {Object}
   */
  get fieldsControls(): IFieldsControls {
    return this._fieldsControls;
  }
  set fieldsControls(value:IFieldsControls){}

  /**
   * @returns {Number}
   */
  get totalStake(): number {
    return this._totalStake;
  }
  set totalStake(value:number){}

  /**
   * @returns {Object} bet
   */
  get bet(): IPoolBet {
    return this.generateBet();
  }
  set bet(value:IPoolBet){}

  /**
   * Generate Bet with stake amount and stake per line with outcome id that ready to be placed
   * @param stake
   * @returns {Object}
   * @private
   */
  private generateBet(): IPoolBet {
    const bet = this.betModel;

    bet.betslip.stake.amount = this._totalStake;
    bet.bet[0].stake.stakePerLine = this._totalStake;
    bet.bet[0].stake.amount = this._totalStake;

    bet.leg[0].poolLeg.legPart = this.generateLegPart();

    return bet;
  }

  /**
   * Generate legPart array
   * @returns {Array}
   * @private
   */
  private generateLegPart(): IPoolBetLegPoolLegPart[] {
    const legPart = [];
    for (let i = 0; i < this.outcomeIds.length; i++) {
      const leg = this.betLegModel;
      leg.outcomeRef.id = this.outcomeIds[i];
      leg.places = i + 1;
      legPart.push(leg);
    }
    return legPart;
  }

  /**
   * Runs each clearField function that added from some outside component
   * @private
   */
  private clearFields(): void {
    this.fieldsControls.clearField.forEach(fn => fn());
  }
}
