import { Component } from '@angular/core';

import {
  RacingEventsComponent as CoralRacingEventsComponent
} from '@app/lazy-modules/racingFeatured/components/racingEvents/racing-events.component';

@Component({
  selector: 'racing-events',
  templateUrl: './racing-events.component.html'
})
export class RacingEventsComponent extends CoralRacingEventsComponent {}
