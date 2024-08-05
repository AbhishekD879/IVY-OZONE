import {  Component } from '@angular/core';
import { RendererService } from '@app/shared/services/renderer/renderer.service';
import { DeviceService } from '@app/core/services/device/device.service';
import { WindowRefService } from '@app/core/services/windowRef/window-ref.service';
import { trigger, transition, style, animate, state, keyframes } from '@angular/animations';
import { FiveASideEntryInfoService } from '@fiveASideShowDownModule/services/fiveaside-entryInfo-handler.service';
import {FiveASideEntryListOverlayComponent
    as AppFiveASideEntryListOverlayComponent
} from '@app/fiveASideShowDown/components/fiveASideEntry/fiveASideEntryListOverlay/fiveaside-entrylist-overlay.component';
import { PubSubService } from '@app/core/services/communication/pubsub/pubsub.service';
import { CoreToolsService } from '@app/core/services/coreTools/core-tools.service';
@Component({
  selector: 'fiveaside-entrylist-overlay',
  templateUrl: './fiveaside-entrylist-overlay.component.html',
  styleUrls: ['./fiveaside-entrylist-overlay.component.scss'],
  animations:[trigger('overlay', [
    state('in', style({ transform: 'translateY(0)' })),
    transition('void => *', [
      animate(
        300,
        keyframes([
          style({ opacity: 1, transform: 'translateY(800px)', offset: 0 }),
          style({ opacity: 1, transform: 'translateY(400px)', offset: 0.5 }),
          style({ opacity: 1, transform: 'translateY(0)', offset: 1.0 })
        ])
      )
    ])
  ])]
})
export class FiveASideEntryListOverlayComponent extends AppFiveASideEntryListOverlayComponent {
  constructor(protected fiveASideEntryInfoService: FiveASideEntryInfoService,
    protected rendererService: RendererService,protected coreToolsService: CoreToolsService,
    protected windowRef: WindowRefService, protected deviceService: DeviceService,protected pubsub:PubSubService) {
      super(fiveASideEntryInfoService,rendererService,coreToolsService,windowRef,deviceService,pubsub);
  }
  /**
   * get the parent element to make the overlay sit on the parent
   * @returns void
   */
  getBody(): void {
    this.homeBody = this.windowRef.document.querySelector('fiveaside-live-leader-board');
  }
}
