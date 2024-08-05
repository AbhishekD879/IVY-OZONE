import { Component, ViewEncapsulation } from '@angular/core';
import { RaceTimerComponent as AppRaceTimerComponent } from '@shared/components/raceTimer/race-timer.component';

@Component({
  selector: 'race-timer',
  styleUrls: ['./race-timer.component.scss'],
  templateUrl: '../../../../../app/shared/components/raceTimer/race-timer.component.html',
  encapsulation :ViewEncapsulation.None
})
export class RaceTimerComponent extends AppRaceTimerComponent {}
