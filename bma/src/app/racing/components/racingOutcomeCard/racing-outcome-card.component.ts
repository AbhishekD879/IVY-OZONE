import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { RaceOutcomeDetailsService } from '@core/services/raceOutcomeDetails/race-outcome-details.service';
import { FiltersService } from '@core/services/filters/filters.service';
import { IToteOutcome } from '@core/models/outcome.model';
import { IMarket } from '@core/models/market.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { horseracingConfig } from '@core/services/racing/config/horseracing.config';
import environment from '@environment/oxygenEnvConfig';
import { GtmService } from '@core/services/gtm/gtm.service';

@Component({
  selector: 'racing-outcome-card',
  templateUrl: 'racing-outcome-card.component.html',
  styleUrls: ['racing-outcome-card.component.scss']
})
export class RacingOutcomeCardComponent implements OnInit {
  @Input() outcomeEntity: IToteOutcome;
  @Input() marketEntity: IMarket;
  @Input() eventEntity: ISportEvent;
  @Input() showSummary: boolean;
  @Input() hideShowMore: boolean;
  @Input() outcomIndex: number;
  @Input() raceType?: string;
  @Input() isGreyhoundEdp: boolean;
  @Input() isUKorIRE:boolean;
  @Output() readonly expand: EventEmitter<number> = new EventEmitter<number>();
  @Input() toteTabName: string;

  isNumberNeeded: Function;
  isGenericSilk: Function;
  isGreyhoundSilk: Function;
  getSilkStyle: Function;
  isOutcomeCardAvailable: boolean;
  runnerNumberDisplay: boolean;
  isAntepostMarket: boolean;
  isSilkLoaded: boolean = false;
  spriteUrl: string | boolean;
  private readonly IMAGES_RACE_ENDPOINT: string = environment.IMAGES_RACE_ENDPOINT;

  constructor(
    public raceOutcomeData: RaceOutcomeDetailsService,
    protected filterService: FiltersService,
    protected gtmService: GtmService
  ) {
    /**
     * Check runner number needed
     * @param {Object} event
     * @param {Object} outcome
     * @returns {Boolean} true or false
     */
    this.isNumberNeeded = this.raceOutcomeData.isNumberNeeded;

    /**
     * Check generic silk needed
     * @param {Object} event
     * @param {Object} outcome
     * @returns {Boolean} true or false
     */
    this.isGenericSilk = this.raceOutcomeData.isGenericSilk;

    /**
     * Check GH silk needed
     * @param {Object} event
     * @param {Object} outcome
     * @returns {Boolean} true or false
     */
    this.isGreyhoundSilk = this.raceOutcomeData.isGreyhoundSilk;

    /**
     * Get Silk Image Style
     * @param {object} raceData
     * @param {object} outcomeEntity
     * @returns {background-image: string, background-position: string}
     */
    this.getSilkStyle = this.raceOutcomeData.getSilkStyle;
  }

  ngOnInit(): void {
    this.isOutcomeCardAvailable = !!(this.outcomeEntity && this.marketEntity && this.eventEntity);
    this.runnerNumberDisplay = this.isNumberNeeded(this.eventEntity, this.outcomeEntity)
      && !this.outcomeEntity.isFavourite;
    this.isAntepostMarket = this.getIsAntepostMarketStatus();
    this.spriteUrl = this.getSprites();
  }

  getSprites(): string | boolean {
    const racingIds = this.marketEntity.outcomes.filter(outcome => outcome.racingFormOutcome && outcome.racingFormOutcome.silkName)
      .map((outcome) => outcome.racingFormOutcome.silkName.split('.')[0]);
    return racingIds.length ? `${this.IMAGES_RACE_ENDPOINT}/${[...racingIds].sort((a, b) => a < b ? -1 : a > b ? 1 : 0)}` : this.isSilkLoaded = true;
  }

  onExpand(): void {
    if(!this.outcomeEntity.isFavourite && !this.outcomeEntity.nonRunner){
      this.expand.emit(this.outcomIndex);
    }
  }

  nameWithoutLineSymbol(name: string): string {
    return this.filterService.removeLineSymbol(name);
  }

  getDefaultSilk(eventEntity: ISportEvent, outcomeEntity: IToteOutcome): boolean {
    return !outcomeEntity.racingFormOutcome && eventEntity.sportId === horseracingConfig.config.request.categoryId;
  }

  nameWithoutNonRunner(name: string): string {
    return this.filterService.removenNonRunnerFromHorseName(name);
  }

  /**
   * Check for market with antepost flag
   * @returns {boolean}
   */
  private getIsAntepostMarketStatus(): boolean {
    return this.eventEntity &&
      this.eventEntity.markets &&
      this.eventEntity.markets[0] &&
      this.eventEntity.markets[0].isAntepost === 'true';
  }
}
