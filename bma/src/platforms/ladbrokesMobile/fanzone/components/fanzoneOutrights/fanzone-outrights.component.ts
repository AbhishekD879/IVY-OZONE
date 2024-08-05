import { Component, ChangeDetectorRef } from '@angular/core';
import { FanzoneAppOutrightsComponent } from '@app/fanzone/components/fanzoneOutrights/fanzone-outrights.component';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { ChannelService } from '@app/core/services/liveServ/channel.service';
import { CacheEventsService } from '@app/core/services/cacheEvents/cache-events.service';
import { UpdateEventService } from '@app/core/services/updateEvent/update-event.service';
import { FanzoneAppModuleService } from '@app/fanzone/services/fanzone-module.service';
import { FanzoneHelperService } from '@app/core/services/fanzone/fanzone-helper.service';
import { FiltersService } from '@core/services/filters/filters.service';
import { GtmService } from '@app/core/services/gtm/gtm.service';
import { DomSanitizer } from '@angular/platform-browser';
import { DeviceService } from '@core/services/device/device.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { DomToolsService } from '@coreModule/services/domTools/dom.tools.service';
import { PlatformLocation } from '@angular/common';

@Component({
  selector: 'fanzone-outrights',
  templateUrl: './fanzone-outrights.component.html',
  styleUrls: ['../../../../../app/fanzone/components/fanzoneOutrights/fanzone-outrights.component.scss']
})
export class FanzoneOutrightsComponent extends FanzoneAppOutrightsComponent {

  constructor(
    public pubSubService: PubSubService,
    public changeDetectorRef: ChangeDetectorRef,
    protected channelService: ChannelService,
    public cacheEventsService: CacheEventsService,
    public updateEventService: UpdateEventService,
    protected fanzoneModuleService: FanzoneAppModuleService,
    protected fanzoneHelperService: FanzoneHelperService,
    protected filtersService: FiltersService,
    protected gtmService: GtmService,
    protected device: DeviceService,
    protected sanitizer: DomSanitizer,
    protected windowRefService: WindowRefService,
    protected domToolsService: DomToolsService,
    loc: PlatformLocation
    ) {
    super(
      pubSubService,
      changeDetectorRef,
      channelService,
      cacheEventsService,
      updateEventService,
      fanzoneModuleService,
      fanzoneHelperService,
      filtersService,
      gtmService,
      device,
      sanitizer,
      windowRefService,
      domToolsService,
      loc
    );
  }
}