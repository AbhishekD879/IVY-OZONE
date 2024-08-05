import { InPlayStorageService as AppInPlayStorageService } from '@app/inPlay/services/inplayStorage/in-play-storage.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { WsUpdateEventService } from '@core/services/wsUpdateEvent/ws-update-event.service';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { RoutingState } from '@sharedModule/services/routingState/routing-state.service';
import { Injectable } from '@angular/core';
import { InplayApiModule } from '@app/inPlay/inplay-api.module';
import { GermanSupportInPlayService } from '@ladbrokesMobile/core/services/germanSupportInPlay/german-support-inplay.service';
import { IRibbonData } from '@app/inPlay/models/ribbon.model';
import { IStructureCache } from '@app/inPlay/models/structure.model';

@Injectable({
  providedIn: InplayApiModule
})
export class InPlayStorageService extends AppInPlayStorageService {
  static ngInjectableDef = undefined;

  constructor(
    windowRef: WindowRefService,
    pubsubService: PubSubService,
    wsUpdateEventService: WsUpdateEventService,
    cmsService: CmsService,
    routingState: RoutingState,
    private germanSupportInPlayService: GermanSupportInPlayService
  ) {
    super(
      windowRef,
      pubsubService,
      wsUpdateEventService,
      cmsService,
      routingState
    );
  }

  updateRibbonData(ribbonData: IRibbonData): void {
    ribbonData.items = this.germanSupportInPlayService.getGeFilteredRibbonItemsForInPlay(ribbonData.items);
    super.updateRibbonData(ribbonData);
  }

  onStructureUpdate(structureData: IStructureCache): void {
    this.germanSupportInPlayService.applyFiltersToStructureData(structureData.data);
    super.onStructureUpdate(structureData);
  }

  outdateRibbonCache() {
    this.ribbonCache.lastUpdated -= this.intervals.ribbonCache;
  }
}
