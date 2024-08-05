import { Component, Input, OnInit } from '@angular/core';
import { OddsCardSportComponent } from '@coralDesktop/shared/components/oddsCard/oddsCardSport/odds-card-sport.component';

@Component({
  selector: 'odds-card-inplay',
  templateUrl: 'odds-card-inplay.component.html'
})

export class OddsCardInplayComponent implements OnInit {
  @Input() gtmModuleTitle?: string;
  @Input() oddsCard: OddsCardSportComponent;
  @Input() isFootballCoupon?: boolean;

  oddsScoreDataSnooker:string[][];
  ngOnInit() {
    if (this.oddsCard) {
      if (this.oddsCard.isDarts){
        this.oddsCard.oddsScores.home = this.oddsCard.eventComments?.teams.home.score;
      }
      if (this.oddsCard.isSnooker){
        this.oddsScoreDataSnooker = [[null, ...this.oddsCard.eventList]];
      }
    }
  }
}
