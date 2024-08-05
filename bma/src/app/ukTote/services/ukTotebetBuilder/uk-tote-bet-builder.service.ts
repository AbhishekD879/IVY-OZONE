import { Injectable } from '@angular/core';

import { IUkTotePoolBet, IUkTotePoolOptions } from './../../models/tote-pool.model';
import { IOutcome } from '@core/models/outcome.model';
import { UkToteService } from '@uktote/services/ukTote/uk-tote.service';
import { UkTotesBetRecognitionService } from '../ukTotesbetRecognition/uk-totes-bet-recognition.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { TotePotBet } from '@uktote/models/totePotBet/tote-pot-bet';
import { Subject, Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class UkToteBetBuilderService {

  betModel: TotePotBet;
  pool: IUkTotePoolBet;
  poolType: string;

  private isMultipleLegsBet: boolean;
  private ukToteItems: IOutcome[] = [];
  private ukToteBetName: string;
  private ukTotePoolId: number;
  private isMultipleLegsBetSubject = new Subject<boolean>();

  constructor(
    private pubsub: PubSubService,
    private betRecognitionService: UkTotesBetRecognitionService,
    private ukToteService: UkToteService
  ) {}

  get isMultipleLegsBet$(): Observable<boolean> {
    return this.isMultipleLegsBetSubject.asObservable();
  }
  set isMultipleLegsBet$(value:Observable<boolean>){}

  /**
   * Get items
   * @returns {Array}
   */
  get items(): IOutcome[] {
    return this.ukToteItems;
  }
  set items(value:IOutcome[]){}

  /**
   * Get items
   * @returns {string}
   */
  get betName(): string {
    return this.ukToteBetName;
  }
  set betName(value:string){}

  /**
   * Get items
   * @returns {number}
   */
  get poolId(): number {
    return this.ukTotePoolId;
  }
  set poolId(value:number){}

  /**
   * Clear the betbuilder
   */
  clear(outcomeId?: string): void {
    if (this.isMultipleLegsBet) {
      this.betModel.clear();
    } else {
      this.ukToteItems = [];
    }
    this.pubsub.publishSync(this.pubsub.API.CLEAR_BETBUILDER, outcomeId);
    this.pubsub.publishSync(this.pubsub.API.BETBUILDER_UPDATED);
  }

  /**
   * add/update selections in betbuilder
   * @params {array | object} items - selections, could be array or object
   */
  add(options: IUkTotePoolOptions): void {
    this.isMultipleLegsBet = this.ukToteService.isMultipleLegsToteBet(options.poolType);
    this.handleMultipleLegsBetChange();
    if (this.isMultipleLegsBet) {
      this.ukToteItems = [];
      this.betModel = options.betModel as TotePotBet;
    } else {
      this.betModel = undefined;
      this.pool = options.currentPool;
      this.poolType = this.pool && this.pool.poolType;
      this.ukTotePoolId = this.pool && this.pool.id;
      this.ukToteBetName = this.betRecognitionService.recognizeBet(options.betModel, options.poolType);
      this.ukToteItems = options.betModel as IOutcome[];
    }
    this.pubsub.publishSync(this.pubsub.API.BETBUILDER_UPDATED);
  }

  /**
   * Check if bet builder should be shown
   * @returns Boolean
   */
  checkIfShouldShow(): boolean {
    let shouldBeShown;
    if (this.isMultipleLegsBet) {
      shouldBeShown = this.betModel && this.betModel.checkIfSomeLegFilled();
    } else {
      shouldBeShown = Object.keys(this.items).length > 0 || this.items.length > 0;
    }
    return shouldBeShown;
  }

  /**
   * Calculates total stake
   * @param {Number} stakePerLine - stake per line
   * @returns {Number} calculated total stake
   */
  getTotalStake(stakePerLine: number): number {
    return stakePerLine ? this.betModel.numberOfLines * stakePerLine : 0;
  }

  private handleMultipleLegsBetChange(): void {
    if (this.isMultipleLegsBetSubject.observers.length) {
      this.isMultipleLegsBetSubject.next(this.isMultipleLegsBet);
    }
  }
}
