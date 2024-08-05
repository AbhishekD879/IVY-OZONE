import { HttpClient } from '@angular/common/http';
import { Inject, Injectable } from '@angular/core';

import { CmsService as AppCmsService } from '@core/services/cms/cms.service';

import { PubSubService } from '@coreModule/services/communication/pubsub/pubsub.service';
import { CmsToolsService } from '@coreModule/services/cms/cms.tools';
import { DeviceService } from '@coreModule/services/device/device.service';
import { CoreToolsService } from '@coreModule/services/coreTools/core-tools.service';
import { NativeBridgeService } from '@coreModule/services/nativeBridge/native-bridge.service';
import { IInitialData } from '@coreModule/services/cms/models';
import { UserService } from '@coreModule/services/user/user.service';

import { CasinoLinkService } from '@coreModule/services/casinoLink/casino-link.service';
import { Observable } from 'rxjs';
import { IPromotionsList } from '@core/services/cms/models';
import { GRID_PROMOTION_CATEGORY_ID } from '@ladbrokesMobile/core/services/cms/cms.constants';
import { SegmentEventManagerService } from '@lazy-modules/segmentEventManager/service/segment-event-manager.service';
import { SegmentedCMSService } from '@app/core/services/cms/segmented-cms.service';
import { FanzoneStorageService } from '@app/core/services/fanzone/fanzone-storage.service';

@Injectable({providedIn:'root'})
export class CmsService extends AppCmsService {
  constructor(
    protected pubSubService: PubSubService,
    protected cmsToolsService: CmsToolsService,
    protected deviceService: DeviceService,
    protected httpClient: HttpClient,
    protected coreToolsService: CoreToolsService,
    protected fanzoneStorageService: FanzoneStorageService,
    protected casinoLinkService: CasinoLinkService,
    protected nativeBridgeService: NativeBridgeService,
    protected userService: UserService,
    protected segmentEventManagerService:SegmentEventManagerService,
    protected segmentedCMSService:SegmentedCMSService,
    @Inject('CMS_CONFIG') protected cmsInitConfig: Promise<IInitialData>
  ) {
    super(
      pubSubService,
      cmsToolsService,
      deviceService,
      httpClient,
      coreToolsService,
      fanzoneStorageService,
      casinoLinkService,
      nativeBridgeService,
      userService,
      segmentEventManagerService,
      segmentedCMSService,
      cmsInitConfig
    );
  }

  getRetailPromotions(): Observable<IPromotionsList> {
    return this.getPromotions(GRID_PROMOTION_CATEGORY_ID, true); // TODO: rename to retail after changes in cms.
  }
}
