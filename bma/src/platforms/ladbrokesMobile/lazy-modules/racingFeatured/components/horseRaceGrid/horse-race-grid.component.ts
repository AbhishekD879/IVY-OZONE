import { Component } from '@angular/core';
import { HorseRaceGridComponent } from '@app/lazy-modules/racingFeatured/components/horseRaceGrid/horse-race-grid.component';


@Component({
  selector: 'horse-race-grid',
  templateUrl: './horse-race-grid.component.html'
})

export class LadbrokesHorseRaceGridComponent extends HorseRaceGridComponent {}
