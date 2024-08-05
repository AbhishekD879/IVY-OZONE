import { Component, Input, OnDestroy, OnInit } from '@angular/core';
import { IBCModule } from '../../services/bigCompetitions/big-competitions.model';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { BigCompetitionsService } from '../../services/bigCompetitions/big-competitions.service';
import { BigCompetitionsLiveUpdatesService } from '../../services/bigCompetitionsLiveUpdates/big-competitions-live-updates.service';
import { IBigCompetitionSportEvent } from '../../models/big-competitions.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { SportsConfigService } from '@sb/services/sportsConfig/sports-config.service';
import { ISportInstance, ISportConfig } from '@core/services/cms/models';

@Component({
  selector: 'competition-next-events, competition-next-events-individual',
  templateUrl: 'competition-next-events.component.html'
})
export class CompetitionNextEventsComponent implements OnInit, OnDestroy {
  @Input() moduleConfig: IBCModule;

  events: IBigCompetitionSportEvent[] = [];
  moduleId: string;
  moduleViewType: string;
  categoryId: string | number;
  isExpanded: boolean = true;
  sportConfig: ISportConfig;

  constructor(private pubSubService: PubSubService,
              private bigCompetitionsService: BigCompetitionsService,
              private bigCompetitionLiveUpdatesService: BigCompetitionsLiveUpdatesService,
              private sportsConfigService: SportsConfigService) {
  }

  ngOnInit(): void {
    this.moduleId = `competitionModule-${this.moduleConfig.id}`;
    this.moduleViewType = 'list';
    this.categoryId = this.bigCompetitionsService.activeCategoryId;

    this.sportsConfigService.getSportByCategoryId(Number(this.categoryId)).subscribe((sportInstance: ISportInstance) => {
      this.sportConfig = sportInstance.sportConfig;
    });

    // Filter events without outcomes
    this.moduleConfig.events = this.moduleConfig.events.filter(e =>
      !!(e.markets.length && e.markets[0].outcomes.length)
    );

    this.events = this.getSortedEvents(this.moduleConfig.events);
    this.bigCompetitionsService.addOutcomeMeaningMinorCode(this.events);
    this.subscribeForLiveUpdates();
  }

  ngOnDestroy(): void {
    this.pubSubService.unsubscribe(this.moduleId);
  }

  /**
   * Subscribe/unsubscribe live updates for competition events(Live Serve MS) when accordion is expanded/collapsed
   */
  accordionHandler(): void {
    this.isExpanded = !this.isExpanded;

    if (this.isExpanded) {
      this.subscribeOnExpand();
    } else {
      this.unsubscribeOnCollapse(this.moduleConfig.events);
    }
  }

    /**
   * Check how to display events in the module
   * @returns {boolean}
   */
     get isListView(): boolean {
      return this.moduleViewType === 'list';
    }
    set isListView(value:boolean){}
    /**
     * Check how to display events in the module
     * @returns {boolean}
     */
    get isCardView(): boolean {
      return this.moduleViewType === 'card';
    }
    set isCardView(value:boolean){}

  /**
   * Performs subscription for live updates and update events.
   */
  private subscribeForLiveUpdates(): void {
    // Remove event which become live from next events list
    this.pubSubService.subscribe(this.moduleId, this.pubSubService.API.MOVE_EVENT_TO_INPLAY, event => {
      this.removeEventEntity(event);
    });

    this.pubSubService.subscribe(this.moduleId, this.pubSubService.API.LIVE_SERVE_MS_UPDATE, () => {
      setTimeout(() => {
        this.bigCompetitionLiveUpdatesService.removeEventEntity(this.events);
        this.bigCompetitionLiveUpdatesService.removeEventEntity(this.moduleConfig.events);
        this.events = [...this.events];
      });
    });
  }

  /**
   * Remove event from events list when live update received from LS MS; unsubscribe from LS updates
   * @param event - event should be updated
   * @private
   */
  private removeEventEntity(event: IBigCompetitionSportEvent): void {
    const index: number = this.events.findIndex( e => Number(e.id) === Number(event.id));

    if (index > -1) {
      this.events = this.events.filter((e:IBigCompetitionSportEvent, i:number) => i !== index);
      this.moduleConfig.events.splice(index, 1);
      this.unsubscribeOnCollapse([event]);
    }
  }

  /**
   * Subscribe to Live Serve on expand
   * @private
   */
  private subscribeOnExpand(): void {
    this.bigCompetitionLiveUpdatesService.subscribe(this.moduleConfig.events);
  }

  /**
   * Unsubscribe to Live Serve on collapse
   * @private
   */
  private unsubscribeOnCollapse(events: ISportEvent[]): void {
    this.bigCompetitionLiveUpdatesService.unsubscribe(events);
  }

  /**
   * returns function that compares items by corresponding property values
   * @param propertyName
   */
  private getComparatorByProperty(propertyName: string): Function {
    return ((a, b) => {
      return a[propertyName] === b[propertyName] ? 0 : (a[propertyName] < b[propertyName] ? -1 : 1);
    });
  }

  /**
   * sorts by startTime, if startTime is equal than sort by displayOrder, if displayOrder is equal than sort by names
   * @param events
   */
  private getSortedEvents(events: IBigCompetitionSportEvent[]): IBigCompetitionSportEvent[] {
    return [...events].sort(this.getComparatorByProperty('name') as any)
      .sort(this.getComparatorByProperty('displayOrder') as any)
      .sort(this.getComparatorByProperty('startTime') as any);
  }

}
