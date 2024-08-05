import { Component, OnInit, OnDestroy, Input } from '@angular/core';
import { BigCompetitionsSpecialsService } from '@app/bigCompetitions/services/bigCompetitionsSpecials/big-competitions-specials-service';
import { ITypeSegment } from '@app/inPlay/models/type-segment.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';

@Component({
  selector: 'competition-specials',
  templateUrl: 'competition-specials.component.html'
})
export class CompetitionSpecialsComponent implements OnInit, OnDestroy {
  @Input() moduleConfig;

  showLimit: number;
  initialData: ITypeSegment[] & ISportEvent[];
  openMarketTabs: boolean[];
  eventsBySections: ITypeSegment[];

  constructor(
    private bigCompetitionsSpecialsService: BigCompetitionsSpecialsService,
    private pubSubService: PubSubService
  ) {
    this.showLimit = 10;
    this.openMarketTabs = [];
    this.eventsBySections = [];
  }

  ngOnInit(): void {
    this.initialData = this.moduleConfig.events;
    this.eventsBySections = this.bigCompetitionsSpecialsService.getEventsBySections(this.initialData);

    this.pubSubService.subscribe(
      `CompetitionSpecialsComponent${this.moduleConfig.id}`,
      this.pubSubService.API.DELETE_EVENT_FROM_CACHE,
        eventId => {
        (this.initialData as ITypeSegment[]) = this.bigCompetitionsSpecialsService.removeEvent(this.eventsBySections, eventId);
      });
  }

  ngOnDestroy(): void {
    this.pubSubService.unsubscribe(`CompetitionSpecialsComponent${this.moduleConfig.id}`);

  }
}
