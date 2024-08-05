import { Component, OnInit, OnDestroy, Input } from '@angular/core';
import { BigCompetitionsSpecialsService } from '@app/bigCompetitions/services/bigCompetitionsSpecials/big-competitions-specials-service';
import { ITypeSegment } from '@app/inPlay/models/type-segment.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';

@Component({
  selector: 'competition-specials-overview',
  templateUrl: 'competition-specials-overview.component.html'
})
export class CompetitionSpecialsOverviewComponent implements OnInit, OnDestroy {
  @Input() moduleConfig;

  showLimit: number;
  initialData: ITypeSegment[] & ISportEvent[];
  openMarketTabs: boolean[];
  eventsBySections: ITypeSegment[];
  viewAllUrl: string;
  inner: boolean;

  constructor(
    private bigCompetitionsSpecialsService: BigCompetitionsSpecialsService,
    private pubSubService: PubSubService
  ) {
    this.inner = true;
    this.showLimit = 10;
    this.openMarketTabs = [];
  }

  ngOnInit(): void {
    this.initialData = this.moduleConfig.events;
    this.viewAllUrl = this.moduleConfig.specialModuleData && this.moduleConfig.specialModuleData.linkUrl || this.moduleConfig.linkUrl;
    this.eventsBySections = this.bigCompetitionsSpecialsService.getEventsBySections(this.initialData);

    this.pubSubService.subscribe(`CompetitionSpecialsOverviewComponent${this.moduleConfig.id}`,
      this.pubSubService.API.DELETE_EVENT_FROM_CACHE,
        eventId => {
        (this.initialData as ITypeSegment[]) = this.bigCompetitionsSpecialsService.removeEvent(this.eventsBySections, eventId);
      });
  }

  ngOnDestroy(): void {
    this.pubSubService.unsubscribe(`CompetitionSpecialsOverviewComponent${this.moduleConfig.id}`);
  }
}
