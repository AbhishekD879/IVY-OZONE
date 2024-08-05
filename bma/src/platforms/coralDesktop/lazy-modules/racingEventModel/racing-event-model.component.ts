import { DesktopRacingEventModelComponent } from '@app/lazy-modules/racingEventModel/racing-event-model.component';
import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  templateUrl: 'racing-event-model.component.html',
  selector: 'racing-event-model',
  styleUrls: ['racing-event-model.component.scss'],
  // eslint-disable-next-line
  encapsulation: ViewEncapsulation.None
})
export class CoralDesktopRacingEventModelComponent extends DesktopRacingEventModelComponent { 
  isCoralDesktopRaceControls:boolean = true;
}
