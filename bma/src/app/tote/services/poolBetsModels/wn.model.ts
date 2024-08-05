import * as _ from 'underscore';
import { PoolBetsModel } from './pool-bets-model';

import { IToteEvent } from '../../models/tote-event.model';
import { IOutcome } from '@core/models/outcome.model';
import { IPoolBet } from '../../models/pool-bet.model';
import { IFieldsControls } from '../../models/field-controls.model';

interface IStakesMap {
  [key: string]: IStakesMapObj;
}

interface IStakesMapObj {
  numericValue: number;
  outcomeId: string;
}

/**
 * Class for represent functionality for WN bet model
 * @class
 */
export class WinPoolBetsModel extends PoolBetsModel {

  eventEntity: IToteEvent;
  BPPService: string;
  private stakesMap: IStakesMap;
  private _fieldsControls: IFieldsControls;
  private _totalStake: number;

  constructor(eventEntity, ip: string, poolType = 'WN') {
    super(eventEntity, ip, poolType);
    /**
     * @member {String} custom placeBet service on Bet Placement
     * Proxy side (bpp - PIROZHOK_API), service should be added to
     * submodules/bpp/scripts/services/bppServices.js
     */
    this.BPPService = 'placeWinPoolBet';
    /**
     * @member {Object} stakes map
     */
    this.stakesMap = this.generateStakesMap(this.eventEntity.markets[0].outcomes);
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
   * Change stake value and refresh total stake amount
   * @param value
   * @param outcomeId
   */
  changeValue(obj: { value: string; outcomeId: string}): void {
    const number = obj.value ? parseFloat(obj.value).toFixed(2) : '0';
    this.setStake(obj.outcomeId, parseFloat(number));
    this.refreshTotalStake();
  }

  /**
   * clear bets by set all stakes values to 0, refresh total stake amount and clear fields
   */
  clearBets(): void {
    _.each(this.stakesMap, (stake: IStakesMapObj, outcomeId: string) => {
      this.setStake(outcomeId, 0);
    });

    this.refreshTotalStake();
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
   * @returns {Array} of bets are ready to be placed
   */
  get bet(): { requests: IPoolBet[] } {
    const betsArray = _.toArray(this.stakesMap)
      .filter(stake => this.filterZeroStake(stake))
      .map(stake => this.generateBet(stake));

    return {
      requests: betsArray
    };
  }
  set bet(value:{ requests: IPoolBet[] }){}

  /**
   * Generate Bet with stake amount and stake per line with outcome id that ready to be placed
   * @param stake
   * @returns {Object}
   * @private
   */
  private generateBet(stake): IPoolBet {
    const bet = this.betModel,
      leg = this.betLegModel;

    bet.betslip.stake.amount = stake.numericValue;
    bet.bet[0].stake.stakePerLine = stake.numericValue;
    bet.bet[0].stake.amount = stake.numericValue;

    leg.outcomeRef.id = stake.outcomeId;

    bet.leg[0].poolLeg.legPart.push(leg);

    return bet;
  }

  /**
   * @param outcomesArray
   * @returns {Object} with stakes
   * @private
   */
  private generateStakesMap(outcomesArray: IOutcome[]): IStakesMap {
    const map = {};
    outcomesArray.forEach(outcome => {
      map[outcome.id] = this.stakeModel;
      map[outcome.id].outcomeId = outcome.id;
    });
    return map;
  }

  /**
   * Runs each clearField function that added from some outside component
   * @private
   */
  private clearFields(): void {
    this._fieldsControls.clearField.forEach(fn => fn());
  }

  /**
   * Calculates each stake numericValue to sum and assign it to total stake private property
   * @private
   */
  private refreshTotalStake(): void {
    let stakesSum = 0;

    _.each(this.stakesMap, (stake: IStakesMapObj) => {
      stakesSum += stake.numericValue;
    });

    this._totalStake = stakesSum;
  }

  /**
   * Set stakes to stake in the stake map
   * @param outcomeId
   * @param number
   * @private
   */
  private setStake(outcomeId: string, number: number): void {
    this.stakesMap[outcomeId].numericValue = number;
  }

  /**
   * @param stake
   * @returns {number}
   * @private
   */
  private filterZeroStake(stake): number {
    return Number(stake.numericValue);
  }
}
