import { Component, OnInit } from '@angular/core';
import { RacingOutcomeResultedCardComponent } from '@racing/components/racingOutcomeResultedCard/racing-outcome-resulted-card.component';

@Component({
  selector: 'racing-outcome-resulted-card',
  templateUrl: 'racing-outcome-resulted-card.component.html',
  styleUrls: ['racing-outcome-resulted-card.scss']
})
export class LadbrokesRacingOutcomeResultedCardComponent extends RacingOutcomeResultedCardComponent implements OnInit {}
