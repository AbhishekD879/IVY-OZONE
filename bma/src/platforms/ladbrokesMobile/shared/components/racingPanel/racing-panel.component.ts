import { Component } from '@angular/core';
import {
  RacingPanelComponent as CoralRacingPanelComponent
} from '@shared/components/racingPanel/racing-panel.component';

@Component({
  selector: 'racing-panel',
  templateUrl: 'racing-panel.component.html',
  styleUrls: ['./racing-panel.component.scss']
})
export class RacingPanelComponent extends CoralRacingPanelComponent {}
