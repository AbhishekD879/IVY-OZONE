import { Component, Input, OnInit } from '@angular/core';

import { RacingOutcomeCardComponent } from '@racing/components/racingOutcomeCard/racing-outcome-card.component';

import { RaceOutcomeDetailsService } from '@core/services/raceOutcomeDetails/race-outcome-details.service';
import { FiltersService } from '@core/services/filters/filters.service';
import { GtmService } from '@core/services/gtm/gtm.service';

@Component({
  selector: 'racing-outcome-card',
  templateUrl: 'racing-outcome-card.component.html',
  styleUrls: ['racing-outcome-card.component.scss'],
})
export class LadbrokesRacingOutcomeCardComponent  extends RacingOutcomeCardComponent implements OnInit {
  @Input() isNotRacingSpecials: boolean;
  @Input() isGreyhoundEdp: boolean;
  @Input() isUKorIRE:boolean;

  getOutcomeClass: Function;
  isGroupSilkNeeded: Function;

  isNotGreyhoundSpecials: boolean;

  constructor(
    public raceOutcomeData: RaceOutcomeDetailsService,
    protected filterService: FiltersService,
    protected gtmService: GtmService
  ) {
    super(raceOutcomeData, filterService, gtmService);

    /**
     * Returns true if odds/even, outside/inside market
     * @param {object} outcomeEntity
     * @returns {String}
     */
    this.getOutcomeClass = this.raceOutcomeData.getOutcomeClass;

    /**
     * Returns true if Odds/Even, Outside/Inside market
     * @param {object} outcomeEntity
     * @returns {Boolean}
     */
    this.isGroupSilkNeeded = this.raceOutcomeData.isGroupSilkNeeded;
  }

  ngOnInit(): void {
    super.ngOnInit();
    this.isNotGreyhoundSpecials = this.isNotRacingSpecials || !this.isGreyhoundEdp;
  }
}
