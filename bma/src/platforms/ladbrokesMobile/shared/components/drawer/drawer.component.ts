import { Component, ChangeDetectorRef, ChangeDetectionStrategy } from '@angular/core';

import { DrawerComponent } from '@shared/components/drawer/drawer.component';

import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { DomToolsService } from '@coreModule/services/domTools/dom.tools.service';
import { DeviceService } from '@core/services/device/device.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';

@Component({
  selector: 'drawer',
  templateUrl: './drawer.component.html',
  styleUrls: ['./drawer.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class LadbrokesDrawerComponent extends DrawerComponent {
  constructor(
    protected windowRefService: WindowRefService,
    protected domToolsService: DomToolsService,
    protected deviceService: DeviceService,
    protected changeDetector: ChangeDetectorRef,
    protected pubSubService: PubSubService
  ) {
    super(
      windowRefService,
      domToolsService,
      deviceService,
      changeDetector,
      pubSubService
    );
  }

  closeClick(): void {
    super.closeClick();
  }

  overlayClick(): void {
    super.overlayClick();
  }
}
