import { Component, ChangeDetectionStrategy, ChangeDetectorRef } from '@angular/core';
import { FanzoneAppNowNextComponent } from '@app/fanzone/components/fanzoneNowNext/fanzone-now-next.component';
import { PubSubService } from '@app/core/services/communication/pubsub/pubsub.service';
import { FanzoneFeaturedService } from '@app/fanzone/services/fanzone-featured-ms.service';
import { FanzoneHelperService } from '@app/core/services/fanzone/fanzone-helper.service';
import { WsUpdateEventService } from '@app/core/services/wsUpdateEvent/ws-update-event.service';
import { FanzoneStorageService } from '@app/core/services/fanzone/fanzone-storage.service';

@Component({
  selector: 'fanzone-now-next',
  templateUrl: './fanzone-now-next.component.html',
  styleUrls: ['./fanzone-now-next.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class FanzoneNowNextComponent extends FanzoneAppNowNextComponent {

  constructor(protected fanzoneFeaturedService: FanzoneFeaturedService,
    protected pubsubService: PubSubService,
    protected changeDetectorRef: ChangeDetectorRef,
    protected fanzoneStorageService: FanzoneStorageService,
    fanzoneHelperService: FanzoneHelperService,
    wsupdateEventService: WsUpdateEventService) {
    super(fanzoneFeaturedService, pubsubService, changeDetectorRef, fanzoneStorageService, fanzoneHelperService,wsupdateEventService);
  }

}
