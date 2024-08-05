import { InPlayStorageService
    as LadbrokesInPlayStorageService } from '@ladbrokesMobile/inPlay/services/inplayStorage/in-play-storage.service';
import { Injectable } from '@angular/core';
import { InplayApiModule } from '@app/inPlay/inplay-api.module';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { WsUpdateEventService } from '@core/services/wsUpdateEvent/ws-update-event.service';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { RoutingState } from '@sharedModule/services/routingState/routing-state.service';
import { GermanSupportInPlayService } from '@ladbrokesMobile/core/services/germanSupportInPlay/german-support-inplay.service';

@Injectable({
  providedIn: InplayApiModule
})
export class InPlayStorageService extends LadbrokesInPlayStorageService {
  static ngInjectableDef = undefined;

  constructor(
    windowRef: WindowRefService,
    pubsubService: PubSubService,
    wsUpdateEventService: WsUpdateEventService,
    cmsService: CmsService,
    routingState: RoutingState,
    germanSupportInPlayService: GermanSupportInPlayService
  ) {
    super(
      windowRef,
      pubsubService,
      wsUpdateEventService,
      cmsService,
      routingState,
      germanSupportInPlayService
    );
  }
}
