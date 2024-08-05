import { Component, Input, OnInit } from '@angular/core';

import { RacingOutcomeCardComponent } from '@app/racing/components/racingOutcomeCard/racing-outcome-card.component';

import { RaceOutcomeDetailsService } from '@app/core/services/raceOutcomeDetails/race-outcome-details.service';
import { FiltersService } from '@app/core/services/filters/filters.service';
import { GtmService } from '@core/services/gtm/gtm.service';

@Component({
  selector: 'racing-outcome-card',
  templateUrl: 'racing-outcome-card.component.html',
  styleUrls: ['racing-outcome-card.component.scss'],
})
export class LadbrokesDesktopRacingOutcomeCardComponent extends RacingOutcomeCardComponent implements OnInit {
  @Input() isNotRacingSpecials: boolean;
  @Input() isGreyhoundEdp: boolean;

  getOutcomeClass: Function;
  isGroupSilkNeeded: Function;
  courseDistanceWinners: string[] = [];

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

  ngOnInit() {
    super.ngOnInit();
    if (this.outcomeEntity.racingFormOutcome && this.outcomeEntity.racingFormOutcome.courseDistanceWinner) {
      this.courseDistanceWinners = this.outcomeEntity.racingFormOutcome.courseDistanceWinner.split(',');
    }
  }
  isFlagsDisp(BFlag, tabname) {
    return tabname === 'UTRI' &&  (BFlag ? this.courseDistanceWinners.length>=1 : this.courseDistanceWinners.length>1);
  }
}
