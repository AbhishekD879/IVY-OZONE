import { Component } from '@angular/core';
import {
  RacingPanelComponent as LadbrokesRacingPanelComponent
} from '@ladbrokesMobile/shared/components/racingPanel/racing-panel.component';

@Component({
  selector: 'racing-panel',
  templateUrl: '../../../../ladbrokesMobile/shared/components/racingPanel/racing-panel.component.html',
  styleUrls: ['./racing-panel.component.scss']
})
export class RacingPanelComponent extends LadbrokesRacingPanelComponent {}
