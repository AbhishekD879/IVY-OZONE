import { Component } from '@angular/core';
import {
  LadbrokesRaceCardsControlsComponent as LadbrokesMobileRaceCardsControlsComponent
} from '@ladbrokesMobile/racing/components/race-cards-controls/race-cards-controls.component';

@Component({
  selector: 'race-cards-controls',
  templateUrl: './race-cards-controls.component.html',
  styleUrls: [ './race-cards-controls.component.scss' ]
})
export class LadbrokesRaceCardsControlsComponent extends LadbrokesMobileRaceCardsControlsComponent {}
