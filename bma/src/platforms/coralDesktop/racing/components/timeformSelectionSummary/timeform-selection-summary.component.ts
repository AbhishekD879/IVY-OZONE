import { Component, ViewEncapsulation } from '@angular/core';
import { TimeFormSelectionSummaryComponent } from '@racing/components/timeformSummary/time-form-selection-summary.component';

@Component({
  selector: 'timeform-selection-summary',
  templateUrl: './timeform-selection-summary.component.html',
  styleUrls: ['timeform-selection-summary.component.scss'],
  // eslint-disable-next-line
  encapsulation : ViewEncapsulation.None

})
export class DesktopTimeFormSelectionSummaryComponent extends TimeFormSelectionSummaryComponent {}
