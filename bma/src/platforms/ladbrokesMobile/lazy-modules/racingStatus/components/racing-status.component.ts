import { Component } from '@angular/core';
import {
  RacingStatusComponent as CoralRacingStatusComponent
} from '@lazy-modules/racingStatus/components/racing-status.component';

@Component({
  selector: 'racing-status',
  templateUrl: 'racing-status.component.html',
  styleUrls: ['./racing-status.component.scss']
})
export class RacingStatusComponent extends CoralRacingStatusComponent {}

