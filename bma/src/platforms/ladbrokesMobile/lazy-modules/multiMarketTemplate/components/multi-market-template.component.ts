import { Component, OnInit, SimpleChanges } from '@angular/core';
import {
  MultiMarketTemplateComponent
} from '@app/lazy-modules/multiMarketTemplate/components/multi-market-template.component';
import { IScoreUpdateEventOptions } from '@core/models/update-options.model';
import { IReference } from '@core/models/live-serve-update.model';
@Component({
  selector: 'multi-market-template',
  templateUrl: 'multi-market-template.component.html',
  styleUrls: ['multi-market-template.component.scss']
})
export class LadsMobileMultiMarketTemplateComponent extends MultiMarketTemplateComponent implements OnInit {
  linkToEventPage: boolean | string;
  ifClockAllowed: boolean;
  isTeamNames: boolean;
  isPromotion: boolean;
  ngOnInit(): void {
    this.linkToEventPage = this.goToEvent(true);
    super.ngOnInit();
    this.ifClockAllowed = this.isClockAllowed();
    this.isTeamNames = !this.event.outcomeStatus && !!this.eventSecondName;
    if (!this.isEventStartedOrLive) {
      this.oddsLabel = this.oddsLabel.replace(',', '');
    }
    // Recalculate Scores & update component
    this.pubSubService.subscribe(`oddCardSport_${this.uniqueId}_${this.event.id}`,
      this.pubSubService.API.EVENT_SCORES_UPDATE, (options: IScoreUpdateEventOptions) => {
        if (this.event.id === options.event.id) {
          if(options.event.comments){
            this.event.comments = JSON.parse(JSON.stringify(options.event.comments));
            this.watchGroupHandler();
          }
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