

import { Component } from '@angular/core';
import { RaceCardContentComponent } from '@app/lazy-modules/raceCard/raceCardContent/race-card-content.component';

@Component({
  selector: 'race-card-content',
  templateUrl: './race-card-content.component.html',
  styleUrls: ['../../../../../app/shared/components/raceCard/next-races.scss',
    '../../../../../app/shared/components/raceCard/race-card.component.scss',
    './race-card-content.component.scss']
})
export class LadbrokesRaceCardContentComponent extends RaceCardContentComponent {}
