import { Component, Input, OnInit } from '@angular/core';

import { RaceOutcomeDetailsService } from '@core/services/raceOutcomeDetails/race-outcome-details.service';
import { FiltersService } from '@core/services/filters/filters.service';
import { IOutcome } from '@core/models/outcome.model';
import { LocaleService } from '@core/services/locale/locale.service';
import { ISilkStyleModel } from '@core/services/raceOutcomeDetails/silk-style.model';
import { FracToDecService } from '@core/services/fracToDec/frac-to-dec.service';
import { IRacingMarket } from '@core/models/racing-market.model';
import { IRacingEvent } from '@core/models/racing-event.model';

@Component({
  selector: 'racing-outcome-resulted-card',
  templateUrl: 'racing-outcome-resulted-card.component.html',
  styleUrls: ['racing-outcome-resulted-card.scss']
})
export class RacingOutcomeResultedCardComponent implements OnInit {
  @Input() outcomeEntity: IOutcome;
  @Input() marketEntity: IRacingMarket;
  @Input() eventEntity: IRacingEvent;
  @Input() raceType: string;
  @Input() nonRunners: IOutcome[];
  @Input() unPlaced: IOutcome;

  isNumberNeeded: boolean;
  isGreyhoundSilk: boolean;
  silkStyle: ISilkStyleModel;
  isOutcomeCardAvailable: boolean;
  runnerNumberDisplay: boolean;
  oddsFormat: boolean = true;
  runnerName: string;
  outcomePositionSufx: string;
  oddsPrice: string = '';

  constructor(
    private raceOutcomeDetailsService: RaceOutcomeDetailsService,
    private filterService: FiltersService,
    private fracToDecService: FracToDecService,
    private localeService: LocaleService
  ) {}

  ngOnInit(): void {
    this.isOutcomeCardAvailable = !!(this.outcomeEntity && this.marketEntity && this.eventEntity);
    this.runnerNumberDisplay = this.raceOutcomeDetailsService.isNumberNeeded(this.eventEntity, this.outcomeEntity)
      && !this.outcomeEntity.isFavourite;
    this.runnerName = this.getRunnerName();
    this.isGreyhoundSilk = this.raceOutcomeDetailsService.isGreyhoundSilk(this.eventEntity, this.outcomeEntity);
    if (this.outcomeEntity.racingFormOutcome && this.outcomeEntity.racingFormOutcome.silkName) {
      if (!this.nonRunners && !this.unPlaced) {
        this.silkStyle = this.raceOutcomeDetailsService.getSilkStyle(this.marketEntity, this.outcomeEntity, '0');
      }else if(!this.nonRunners && this.unPlaced){
        this.silkStyle = this.raceOutcomeDetailsService.getSilkStyle(this.unPlaced, this.outcomeEntity, '0');
      } else {
        this.silkStyle = this.raceOutcomeDetailsService.getSilkStyle(this.nonRunners, this.outcomeEntity,  '0');
      }
    }
    if (this.outcomeEntity.results) {
      this.outcomePositionSufx = this.getPositionWithSuffix();
      const price = this.outcomeEntity.results;
      this.oddsPrice = <string>this.fracToDecService.getFormattedValue(price.priceNum, price.priceDen);
    }
  }

  private nameWithoutLineSymbol(name: string): string {
    return this.filterService.removeLineSymbol(name);
  }

  /**
  * get position
  */
  private getPositionWithSuffix(): string {
    const pos = this.outcomeEntity.results.position;
    if(pos == 0){
    const Rcode = this.outcomeEntity.results.resultCode;
       if(Rcode === "L" || Rcode === "0"){
         return '-'
       }
       else{
         return Rcode ? Rcode : '-';
       }
    }
    else{
     return pos ?
      `${pos}${this.localeService.getString((this.filterService.numberSuffix(pos)))}` : '-';
    }
  }

  private getRunnerName(): string {
    const prefix = this.raceType && this.raceType.toLowerCase() === 'horse_racing'
    && !this.outcomeEntity.isFavourite && this.outcomeEntity.runnerNumber ? `${this.outcomeEntity.runnerNumber} - ` : '';
    return `${prefix}${this.nameWithoutLineSymbol(this.outcomeEntity.name)}`;
  }
}
