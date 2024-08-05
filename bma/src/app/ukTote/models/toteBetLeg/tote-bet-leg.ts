import { IOutcome } from '@core/models/outcome.model';
import { ISportEvent } from '@core/models/sport-event.model';
import * as _ from 'underscore';

export class ToteBetLeg {

  name: string;
  linkedMarketId;
  outcomesMap: { [key: string]: IOutcome; };
  filled: boolean = false;
  isSuspended: boolean;
  private selectedOutcomesIds = [];
  private readonly SUSPENDED_STATUS_CODE: string = 'S';

  constructor(
    public index,
    public marketId,
    private eventEntity: ISportEvent,
    private ukToteService
  ) {
    this.index = index;
    this.name = `Leg ${index + 1}`;
    if (!this.event) {
      return;
    }
    this.linkedMarketId = this.event.markets.length && this.event.markets[0].linkedMarketId;
    this.outcomesMap = this.generateOutcomesMap();
    this.updateSuspendedStatus();
  }

  get event(): ISportEvent {
    return this.eventEntity;
  }
  set event(value:ISportEvent){}

  /**
   * Get count of selected outcomes
   * @returns {number}
   */
  get selectionsCount(): number {
    return this.selectedOutcomesIds.length;
  }
  set selectionsCount(value:number){}

  /**
   * Get selected outcomes
   */
  get selectedOutcomes(): IOutcome[] {
    const selectedOutcomes = _.map(this.selectedOutcomesIds, outcomeId => this.outcomesMap[outcomeId]);
    return this.ukToteService.sortOutcomes(selectedOutcomes);
  }
  set selectedOutcomes(value:IOutcome[]){}


  /**
   * Update suspended status of leg and outcomes
   */
  updateSuspendedStatus(): void {
    this.isSuspended = this.isEventSuspended() || this.isMarketSuspended() || this.isEventResulted();
    if (this.isSuspended) {
      this.clear();
    } else {
      this.filterSelectedOutcomes();
    }
  }

  /**
   * Updates filled property of object
   */
  updateFilledStatus(): void {
    this.filled = !!this.selectedOutcomesIds.length;
  }

  /**
   * Add outcome Id to array of selected Outcomes
   * @param {string} outcomeId - Id of selected outcome
   */
  selectOutcome(outcomeId: string): void {
    this.selectedOutcomesIds = this.selectedOutcomesIds.concat(outcomeId);
    this.updateFilledStatus();
  }

  /**
   * Remove outcome Id to array of selected Outcomes
   * @param {string} outcomeId
   */
  deselectOutcome(outcomeId: string): void {
    this.selectedOutcomesIds = _.without(this.selectedOutcomesIds, outcomeId);
    this.updateFilledStatus();
  }

  /**
   * Checks whether outcome with ID - outcomeId is selected
   * @param {string} outcomeId
   * return {Boolean}
   */
  isOutcomeSelected(outcomeId: string): boolean {
    return _.contains(this.selectedOutcomesIds, outcomeId);
  }

  /**
   * Remove all selections from the leg
   */
  clear(): void {
    this.selectedOutcomesIds = [];
    this.updateFilledStatus();
  }

  /**
   * Generates object which is dictionary of outcome ids and outcomes
   * @returns {Object}
   * @private
   */
  private generateOutcomesMap(): { [key: string]: IOutcome; } {
    if (!this.event) {
      return {};
    }
    const outcomesMap = {};
    _.forEach(this.event.markets[0].outcomes, (outcome: IOutcome) => {
      outcomesMap[outcome.id] = outcome;
    });
    return outcomesMap;
  }

  /**
   * Check if event suspended
   * @returns {Boolean}
   * @private
   */
  private isEventSuspended(): boolean {
    return this.event && this.event.eventStatusCode === this.SUSPENDED_STATUS_CODE;
  }

  /**
   * Check if market suspended
   * @returns {Boolean}
   * @private
   */
  private isMarketSuspended(): boolean {
    return this.event && this.event.markets && this.event.markets[0].marketStatusCode === this.SUSPENDED_STATUS_CODE;
  }

  /**
   * Check if event is resluted
   * @returns {Boolean}
   * @private
   */
  private isEventResulted(): boolean {
    return this.event && this.event.isResulted;
  }

  /**
   * Check whether provided outcome has suspended status
   * @param {Object} outcome - outcome entity
   * @returns {boolean}
   */
  private isOutcomeSuspended(outcome: IOutcome): boolean {
    return outcome.outcomeStatusCode === this.SUSPENDED_STATUS_CODE;
  }

  /**
   * Deselect suspended outcomes
   * @private
   */
  private filterSelectedOutcomes(): void {
    _.forEach(this.selectedOutcomesIds, outcomeId => {
      if (this.isOutcomeSuspended(this.outcomesMap[outcomeId])) {
        this.deselectOutcome(outcomeId);
      }
    });
    this.updateFilledStatus();
  }
}
