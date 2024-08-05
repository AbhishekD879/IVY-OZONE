import { Component, Input, OnInit, OnChanges, SimpleChanges } from '@angular/core';

import { UkToteService } from '@uktote/services/ukTote/uk-tote.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';

import { ISportEvent } from '@core/models/sport-event.model';
import { IMarket } from '@core/models/market.model';
import { IOutcome } from '@core/models/outcome.model';
import { IUkToteLeg } from '@uktote/models/uk-tote-leg.model';
import { DeviceService } from '@core/services/device/device.service';
import { FracToDecService } from '@core/services/fracToDec/frac-to-dec.service';

@Component({
  selector: 'uk-tote-leg',
  templateUrl: 'uk-tote-leg.component.html'
})
export class UkToteLegComponent implements OnInit, OnChanges {

  @Input() toteLegVal: IUkToteLeg;
  @Input() isPoolBetSuspended: boolean;
  @Input() isUKorIRE: boolean;

  expandedSummary: boolean[] = [];
  marketOutcomes: IOutcome[] = [];
  market: IMarket;
  event: ISportEvent;
  raceTitle: string;
  outcomeSuspensionStatuses: boolean[];

  constructor(
    private ukToteService: UkToteService,
    protected deviceService: DeviceService,
    private fracToDecService: FracToDecService,
    private pubSubService: PubSubService
  ) {}

  ngOnInit() {
    this.initData();
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes.toteLegVal.currentValue && changes.toteLegVal.previousValue) {
      this.expandedSummary = [];
      this.initData();
    }
  }

  trackByOutcomes(index: number, outcome: IOutcome): string {
    return outcome.id;
  }

  /**
   * Process click to expand outcome icon
   * @param oIndex - index of outcome to expand
   */
  onExpandSummary(oIndex: number): void {
    if (!this.expandedSummary[oIndex]) {
      this.expandedSummary = [];
    }
    this.expandedSummary[oIndex] = !this.expandedSummary[oIndex];
  }

  /**
   * Process click to select outcome checkbox
   * @param {string} outcomeId - ID of outcome
   */
  selectOutcome(outcomeId: string): void {
    if (!this.toteLeg.isOutcomeSelected(outcomeId)) {
      this.toteLeg.selectOutcome(outcomeId);
    } else {
      this.toteLeg.deselectOutcome(outcomeId);
    }
    this.pubSubService.publish(this.pubSubService.API.UK_TOTE_LEG_UPDATED, this.toteLeg);
  }

  /**
   * Get tote leg
   * @returns {Object} - object of class toteBetLeg
   */
  private get toteLeg(): IUkToteLeg {
    return this.toteLegVal;
  }
  private set toteLeg(value:IUkToteLeg){}
  /**
   * Get Outcomes entity
   */
  private getMarketOutcomes(): IOutcome[] {
    return this.ukToteService.sortOutcomes(this.marketEntity ? this.marketEntity.outcomes : []);
  }

  /**
   * Get Market entity
   */
  private get marketEntity(): IMarket {
    return this.toteLeg && this.toteLeg.event && this.toteLeg.event.markets && this.toteLeg.event.markets[0];
  }
  private set marketEntity(value:IMarket){}

  /**
   * Get Event entity
   */
  private get eventEntity(): ISportEvent {
    return this.toteLeg && this.toteLeg.event;
  }
  private set eventEntity(value:ISportEvent){}

  /**
   * Set race title
   */
  private getRaceTitle(): string {
    return this.toteLeg.event ? this.ukToteService.getRaceTitle(this.toteLeg.event) : '';
  }

  /**
   * Check if outcome should be displayed as suspended
   * @param outcomeEntity - outcome entity
   * @returns {Boolean}
   */
  private checkIfOutcomeSuspended(outcomeEntity: IOutcome): boolean {
    const isWholeBetSuspended = this.isPoolBetSuspended || this.toteLeg.isSuspended;
    const isOutcomeSuspended = this.isOutcomeSuspended(outcomeEntity) && !outcomeEntity.nonRunner;
    return isWholeBetSuspended || isOutcomeSuspended;
  }

  private isOutcomeSuspended(outcome: IOutcome): boolean {
    return this.ukToteService.isOutcomeSuspended(outcome);
  }

  private initData(): void {
    this.marketOutcomes = this.getMarketOutcomes();
    this.market = this.marketEntity;
    this.event = this.eventEntity;
    this.event.isUKorIRE = this.isUKorIRE;
    this.raceTitle = this.getRaceTitle();
    this.outcomeSuspensionStatuses = this.marketOutcomes
      .map((outcome: IOutcome) => this.checkIfOutcomeSuspended(outcome));
  }
   /**
   * Convert odds format
   * @param priceNum {number}
   * @param priceDen {number}
   * @returns {*}
   * @private
   */
   fracToDec(priceNum: number, priceDen: number): string | number {
    return (priceNum && priceDen) ? this.fracToDecService.getFormattedValue(priceNum, priceDen) : (priceNum + '/' + priceDen);
  }
}
