import { Component } from '@angular/core';
import { GreyhoundFutureTabComponent } from '@racing/components/greyhound/greyhoundFutureTab/greyhound-future-tab.component';
import { EventTimeService } from '@ladbrokesMobile/racing/services/event-time.service';
import { FiltersService } from '@core/services/filters/filters.service';
import { EventService } from '@sb/services/event/event.service';
import { RoutingHelperService } from '@core/services/routingHelper/routing-helper.service';
import { ISportEvent } from '@core/models/sport-event.model';
import { GtmService } from '@core/services/gtm/gtm.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { SessionStorageService } from '@core/services/storage/session-storage.service';
import { DeviceService } from '@core/services/device/device.service';

@Component({
  selector: 'greyhound-future-tab',
  templateUrl: 'greyhound-future-tab.component.html'
})

export class LadbrokesGreyhoundFutureTabComponent extends GreyhoundFutureTabComponent {
  constructor(
    public filterService: FiltersService,
    public eventService: EventService,
    public routingHelperService: RoutingHelperService,
    private eventTimeService: EventTimeService,
    protected sessionStorageService: SessionStorageService,
    protected pubSubService: PubSubService,
    protected gtmService: GtmService,
    protected deviceService: DeviceService
  ) {
    super(filterService, eventService, routingHelperService, sessionStorageService, pubSubService, gtmService, deviceService);
  }

  public getRaceTimeView(event: ISportEvent): string {
    return this.eventTimeService.getDate(event);
  }
}
