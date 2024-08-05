import { Component, Input, OnInit } from '@angular/core';

import { FiltersService } from '@core/services/filters/filters.service';
import { IOutcome, IToteOutcome } from '@core/models/outcome.model';
import { IMarket } from '@core/models/market.model';
import { ISportEvent } from '@core/models/sport-event.model';
import * as _ from 'underscore';

@Component({
  selector: 'forecast-tricast-race-card',
  templateUrl: 'forecast-tricast-race-card.component.html',
  styleUrls: ['forecast-tricast-race-card.component.scss']
})
export class ForcastTricastRaceCardComponent implements OnInit {
  @Input() outcomeEntity: IToteOutcome;
  @Input() marketEntity: IMarket;
  @Input() eventEntity: ISportEvent;

  isOutcomeCardAvailable: boolean;
  runnerNumberDisplay: boolean;
  outcomeName: string;

  constructor(
    protected filterService: FiltersService
  ) {}

  ngOnInit(): void {
    this.isOutcomeCardAvailable = !!(this.outcomeEntity && this.marketEntity && this.eventEntity);
    this.runnerNumberDisplay = this.isNumberNeeded(this.outcomeEntity)
      && !this.outcomeEntity.isFavourite;
    this.outcomeName = this.nameWithoutLineSymbol(this.outcomeEntity.name);
  }

  private nameWithoutLineSymbol(name: string): string {
    return this.filterService.removeLineSymbol(name);
  }

  private isNumberNeeded(outcome: IOutcome): boolean  {
    return (_.isUndefined(outcome.runnerNumber) || (outcome.runnerNumber && Number(outcome.runnerNumber) > 0));
  }
}
