import { Component, OnChanges, SimpleChanges, OnInit, Input } from '@angular/core';
import { RaceCardContentComponent as OxygenRaceCardComponent } from '@app/lazy-modules/raceCard/raceCardContent/race-card-content.component';

@Component({
  selector: 'race-card-inplay',
  templateUrl: './race-card-inplay.component.html',
  styleUrls: [
    './race-card-inplay.component.scss'    
  ]
})
export class RaceCardInplayComponent extends OxygenRaceCardComponent implements OnChanges, OnInit {
  @Input() viewFullRaceText: string;
  ngOnInit() {
    this.viewFullRaceText = this.locale.getString(this.viewFullRaceText);
    this.processOutcomes();
    this.generateEachWayTerms();
  }

  ngOnChanges(changes: SimpleChanges) {
    if(changes.raceData) {
      this.processOutcomes();
      this.generateEachWayTerms();
    }
  }
}
