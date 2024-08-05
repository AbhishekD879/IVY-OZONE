import { Component, OnInit,  } from '@angular/core';
import {
  RightColumnWidgetComponent as CoralRightColumnWidgetItemComponent
} from '@app/lazy-modules/rightColumn/components/rightColumnWidget/right-column-widget.component';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { VisEventService } from '@core/services/visEvent/vis-event.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { RoutingState } from '@sharedModule/services/routingState/routing-state.service';
import { DeviceService } from '@core/services/device/device.service';
import { GermanSupportService } from '@core/services/germanSupport/german-support.service';
import { ActivatedRoute, Router } from '@angular/router';

@Component({
  selector: 'right-column-widget',
  styleUrls: ['right-column-widget.scss'],
  templateUrl: 'right-column-widget.component.html'
})
export class RightColumnWidgetComponent extends CoralRightColumnWidgetItemComponent implements OnInit {

  constructor(
    pubSubService: PubSubService,
    visEventService: VisEventService,
    windowRefService: WindowRefService,
    router: Router,
    routingState: RoutingState,
    route: ActivatedRoute,
    deviceService: DeviceService,
    private germanSupportService: GermanSupportService
  ) {
    super(
      pubSubService,
      visEventService,
      windowRefService,
      router,
      routingState,
      route,
      deviceService
    );
  }

  ngOnInit(): void {
    super.ngOnInit();
    this.filterNextRacesIfGermanCustomer();
    /* eslint-disable */
    // Unsubscribe in parent component
    this.pubSubService.subscribe(this.widgetColumn,
      [
        this.pubSubService.API.SUCCESSFUL_LOGIN, this.pubSubService.API.SESSION_LOGIN,
        this.pubSubService.API.SESSION_LOGOUT
      ], () => {
        this.filterNextRacesIfGermanCustomer();
      }
    );
    /* eslint-enable */
  }

  private filterNextRacesIfGermanCustomer(): void {
    if (this.germanSupportService.isGermanUser()) {
      this.widgets = (this.widgets as any).filter((widget) => {
        return widget.directiveName !== 'next-races';
      });
    }
  }
}
