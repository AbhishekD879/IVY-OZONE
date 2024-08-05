import { Component } from '@angular/core';
import {
  RaceCardsControlsComponent as MobileRaceCardsControlsComponent
} from '@racing/components/raceCardControls/race-cards-controls.component';

@Component({
  selector: 'race-cards-controls',
  templateUrl: './race-cards-controls.component.html',
  styleUrls: [ './race-cards-controls.component.scss' ]
})
export class RaceCardsControlsComponent extends MobileRaceCardsControlsComponent {}
