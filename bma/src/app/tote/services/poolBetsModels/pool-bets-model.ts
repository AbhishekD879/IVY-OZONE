import * as _ from 'underscore';
import { BET_TEMPLATE } from './bet-template';

import { IToteEvent } from '../../models/tote-event.model';
import { IPoolBet, IPoolBetLegPoolLegPart } from '../../models/pool-bet.model';

/**
 * Class for generating general bet model
 * @class
 */
export class PoolBetsModel {

  eventEntity: IToteEvent;
  private poolType: string;
  private poolId: string;

  constructor(eventEntity, private ip: string, poolType) {
    /**
     * @member {Object} int tote event
     */
    this.eventEntity = eventEntity;
    /**
     * @member {String} int tote event
     */
    this.poolType = poolType;
    /**
     * @member {Number} int tote event
     */
    this.poolId = _.findWhere(this.eventEntity.pools, { poolType: this.poolType }).id;
  }

  /**
   * Return model of bet template and pool id with pool type assigned to it
   * @returns {Object} bet template
   */
  get betModel(): IPoolBet {
    BET_TEMPLATE.betslip.slipPlacement.IPAddress = this.ip;
    const betModel = JSON.parse(JSON.stringify(BET_TEMPLATE));

    betModel.bet[0].betTypeRef.id = this.poolType;
    betModel.leg[0].poolLeg.poolRef.id = this.poolId;

    return betModel;
  }
  set betModel(value:IPoolBet){}

  /**
   * @returns {{outcomeRef: {id: string}}}
   */
  get betLegModel(): IPoolBetLegPoolLegPart {
    return {
      outcomeRef: {
        id: ''
      }
    };
  }
  set betLegModel(value:IPoolBetLegPoolLegPart){}

  /**
   * @returns {{outcomeId: string, numericValue: number}}
   */
  get stakeModel(): {outcomeId: string, numericValue: number} {
    return {
      outcomeId: '',
      numericValue: 0
    };
  }
  set stakeModel(value:{outcomeId: string, numericValue: number}){}
}
