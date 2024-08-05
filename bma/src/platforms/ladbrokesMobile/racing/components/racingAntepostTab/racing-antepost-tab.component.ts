import { Component } from '@angular/core';
import { RacingAntepostTabComponent } from '@racing/components/racingAntepostTab/racing-antepost-tab.component';
import { ISportEvent } from '@core/models/sport-event.model';
import { FiltersService } from '@core/services/filters/filters.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { RacingService } from '@coreModule/services/sport/racing.service';
import { RoutingHelperService } from '@core/services/routingHelper/routing-helper.service';
import { EventTimeService } from '@ladbrokesMobile/racing/services/event-time.service';
import { PubSubService } from '@app/core/services/communication/pubsub/pubsub.service';
import { SessionStorageService } from '@app/core/services/storage/session-storage.service';
import { GtmService } from '@core/services/gtm/gtm.service';
import { DeviceService } from '@app/core/services/device/device.service';

@Component({
  selector: 'racing-antepost-tab',
  templateUrl: 'racing-antepost-tab.component.html'
})
export class LadbrokesRacingAntepostTabComponent extends RacingAntepostTabComponent {
  constructor(
    public filterService: FiltersService,
    public locale: LocaleService,
    public racingService: RacingService,
    public routingHelperService: RoutingHelperService,
    public sessionStorageService: SessionStorageService,
    public pubSubService: PubSubService,
    private eventTimeService: EventTimeService,
    public gtm: GtmService,
    public deviceService: DeviceService
  ) {
    super(filterService, locale, racingService, routingHelperService, sessionStorageService, pubSubService, gtm, deviceService);
  }
  getDate(event: ISportEvent): string {
    return this.eventTimeService.getDate(event);
  }
}
