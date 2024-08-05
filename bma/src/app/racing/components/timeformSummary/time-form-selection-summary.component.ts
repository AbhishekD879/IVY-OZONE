import { Component, Input, OnInit } from '@angular/core';

import { GtmService } from '@core/services/gtm/gtm.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { IOutcome } from '@core/models/outcome.model';
import { TimeFormBaseComponent } from '@racing/components/timeformSummary/time-form-base';

@Component({
  selector: 'timeform-selection-summary',
  templateUrl: './time-form-selection-summary.html'
})
export class TimeFormSelectionSummaryComponent extends TimeFormBaseComponent implements OnInit {

  @Input() outcome: IOutcome;

  constructor(
    protected gtmService: GtmService,
    protected locale: LocaleService,
  ) { super(gtmService, locale); }

  ngOnInit() {
    this.summaryText = this.outcome.timeformData ? this.outcome.timeformData.oneLineComment : '';
    super.ngOnInit();
  }
}
