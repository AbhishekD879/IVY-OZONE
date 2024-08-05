import { Component, Input, OnInit, OnDestroy, ViewEncapsulation } from '@angular/core';
import { RoutingHelperService } from '@core/services/routingHelper/routing-helper.service';
import { SportTabsService } from '@sb/services/sportTabs/sport-tabs.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { SlpSpinnerStateService } from '@core/services/slpSpinnerState/slpSpinnerState.service';

import { ISportEvent } from '@core/models/sport-event.model';
import { ITypeSegment } from '@app/inPlay/models/type-segment.model';
import { GamingService } from '@app/core/services/sport/gaming.service';

@Component({
  selector: 'outrights-sport-tab',
  templateUrl: 'outrights-sport-tab.component.html',
  styleUrls: ['outrights-sport-tab.component.scss'],
  // eslint-disable-next-line
  encapsulation: ViewEncapsulation.None
})
export class OutrightsSportTabComponent implements OnInit, OnDestroy {
  @Input() sport: GamingService;
  @Input() display: string;
  
  eventsBySections: ITypeSegment[] = [];
  isResponseError: boolean = false;
  isLoaded: boolean = false;

  constructor(
    private sportTabsService: SportTabsService,
    private pubsubService: PubSubService,
    private routingHelper: RoutingHelperService,
    private slpSpinnerStateService: SlpSpinnerStateService
  ) {}

  ngOnInit(): void {

    this.loadOutrightData();

    this.pubsubService.subscribe('OutrightsSportTabComponent', this.pubsubService.API.DELETE_EVENT_FROM_CACHE, eventId => {
      this.sportTabsService.deleteEvent(eventId, this.eventsBySections);
    });
  }

  ngOnDestroy(): void {
    this.pubsubService.unsubscribe('OutrightsSportTabComponent');
  }

  trackById(index: number, value: ITypeSegment) {
    return value.typeId;
  }

  /**
   * Redirects to event details page
   * @param event
   * @returns {*}
   */
  eventURL(event: ISportEvent): string {
    return this.routingHelper.formEdpUrl(event);
  }

  /**
   * Load Outright Data
   */
  public loadOutrightData(): void {
    this.isLoaded = false;
    this.isResponseError = false;

    this.sport.getByTab(this.display).then((events: ISportEvent[]) => {
      this.eventsBySections = events && events.length ? this.sportTabsService.eventsBySections(events, this.sport) : [];
      this.isResponseError = false;
    }).catch(error => {
      this.isResponseError = true;
      console.warn('Outrights Data:', error && error.error || error);
    }).finally(() => {
      this.isLoaded = true;
      this.slpSpinnerStateService.handleSpinnerState();
    });
  }
}
