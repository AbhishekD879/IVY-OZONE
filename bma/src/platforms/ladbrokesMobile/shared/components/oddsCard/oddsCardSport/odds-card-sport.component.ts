import { Component, OnInit, ViewEncapsulation, SimpleChanges } from '@angular/core';
import { OddsCardSportComponent as AppOddsCardSportComponent } from '@shared/components/oddsCard/oddsCardSport/odds-card-sport.component';
import { IScoreUpdateEventOptions } from '@core/models/update-options.model';
import { IReference } from '@core/models/live-serve-update.model';

@Component({
  selector: 'odds-card-sport',
  templateUrl: 'odds-card-sport.component.html',
  styleUrls: ['odds-card-sport.component.scss'],
  // eslint-disable-next-line
  encapsulation: ViewEncapsulation.None
})
export class OddsCardSportComponent extends AppOddsCardSportComponent implements OnInit {
  linkToEventPage: boolean | string;
  ifClockAllowed: boolean;
  isTeamNames: boolean;
  isPromotion: boolean;

  ngOnInit(): void {
    super.ngOnInit();

    this.linkToEventPage = this.goToEvent(true);
    this.ifClockAllowed = this.isClockAllowed();
    this.isTeamNames = !this.event.outcomeStatus && !!this.eventSecondName;
    if (!this.isEventStartedOrLive) {
      this.oddsLabel = this.oddsLabel.replace(',', '');
    }

    // Recalculate Scores & update component
    this.pubSubService.subscribe(`oddCardSport_${this.uniqueId}_${this.event.id}`,
      this.pubSubService.API.EVENT_SCORES_UPDATE, (options: IScoreUpdateEventOptions) => {
        if (this.event.id === options.event.id) {
          this.watchGroupHandler();
        }
      });
    // also on MOVE_EVENT_TO_INPLAY
    this.pubSubService.subscribe(`oddCardSport_${this.uniqueId}_${this.event.id}`,
    this.pubSubService.API.MOVE_EVENT_TO_INPLAY, (options: IReference) => {
        if (this.event.id === options.id) {
          this.watchGroupHandler();
        }
      });
  }

  ngOnChanges(changes: SimpleChanges): void {
    super.ngOnChanges(changes);
    if (!this.isEventStartedOrLive && this.oddsLabel) {
      this.oddsLabel = this.oddsLabel.replace(',', '');
    }
  }
}
