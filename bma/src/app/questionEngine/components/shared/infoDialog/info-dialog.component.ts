import { Component, ViewChild } from '@angular/core';

import { DeviceService } from '@core/services/device/device.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { RendererService } from '@sharedModule/services/renderer/renderer.service';
import { NavigationService } from '@core/services/navigation/navigation.service';
import { InformationDialogComponent } from '@sharedModule/components/informationDialog/information-dialog.component';
import { GtmService } from '@core/services/gtm/gtm.service';

@Component({
  selector: 'info-dialog',
  templateUrl: './info-dialog.component.html',
  styleUrls: ['./info-dialog.component.scss']
})

export class InfoDialogComponent extends InformationDialogComponent {
  @ViewChild('infoDialog', { static: true }) dialog;

  constructor(
    deviceService: DeviceService,
    rendererService: RendererService,
    windowRef: WindowRefService,
    pubSubService: PubSubService,
    navigationService: NavigationService,
    gtmService: GtmService
  ) {
    super(deviceService, rendererService, windowRef, pubSubService, navigationService, gtmService);
  }
}
