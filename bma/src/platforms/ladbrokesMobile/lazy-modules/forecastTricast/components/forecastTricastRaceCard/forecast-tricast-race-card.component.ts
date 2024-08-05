import { Component } from '@angular/core';

import {
  ForcastTricastRaceCardComponent as CoralForcastTricastRaceCardComponent
} from '@lazy-modules/forecastTricast/components/forecastTricastRaceCard/forecast-tricast-race-card.component';

@Component({
  selector: 'forecast-tricast-race-card',
  templateUrl: 'forecast-tricast-race-card.component.html',
  styleUrls: ['forecast-tricast-race-card.component.scss']
})
export class ForcastTricastRaceCardComponent extends CoralForcastTricastRaceCardComponent {}
