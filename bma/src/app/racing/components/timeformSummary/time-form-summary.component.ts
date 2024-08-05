import { Component, Input, OnInit } from '@angular/core';
import { GtmService } from '@core/services/gtm/gtm.service';
import { TimeFormBaseComponent } from '@racing/components/timeformSummary/time-form-base';
import { LocaleService } from '@core/services/locale/locale.service';

@Component({
  selector: 'timeform-summary',
  templateUrl: './time-form-summary.html'
})
export class TimeFormSummaryComponent extends TimeFormBaseComponent implements OnInit {

  @Input() summary: any; // timeFormData

  constructor(
    protected gtmService: GtmService,
    protected locale: LocaleService,
  ) { super(gtmService, locale); }

  ngOnInit(): void {
    this.summaryText = this.summary.verdict;
    super.ngOnInit();
  }

  /**
   * winnerPrediction()
   * @returns {string}
   */
  get winnerPrediction() {
    return this.summary.winnerPrediction ? this.summary.winnerPrediction.greyHoundFullName : '';
  }
  set winnerPrediction(value:any){}

  /**
   * setPositionClass()
   * @param {string} positionPrediction
   * @returns {string}
   */
  setPositionClass(positionPrediction: string): string {
    return `position-${positionPrediction}`;
  }
}
