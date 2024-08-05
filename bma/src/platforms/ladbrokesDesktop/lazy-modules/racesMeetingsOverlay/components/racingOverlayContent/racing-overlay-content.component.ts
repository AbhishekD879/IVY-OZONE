import { Component, OnChanges, OnInit } from '@angular/core';

import { RacingOverlayContentComponent } from '@app/lazy-modules/racesMeetingsOverlay/components/racingOverlayContent/racing-overlay-content.component';
@Component({
  selector: 'racing-overlay-content',
  templateUrl: './racing-overlay-content.component.html',
  styleUrls: ['./racing-overlay-content.component.scss']

})
export class LadbrokesDesktopRacingOverlayContentComponent extends RacingOverlayContentComponent implements OnInit, OnChanges {

}
