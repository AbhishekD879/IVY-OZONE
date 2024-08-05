import { InplayMainService as LadbrokesInplayMainService } from '@ladbrokesMobile/inPlay/services/inplayMain/inplay-main.service';
import { Injectable } from '@angular/core';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { InplayDataService } from '@app/inPlay/services/inplayData/inplay-data.service';
import { InPlayStorageService } from '@ladbrokesDesktop/inPlay/services/inplayStorage/in-play-storage.service';
import { InplaySubscriptionManagerService } from '@app/inPlay/services/InplaySubscriptionManager/inplay-subscription-manager.service';
import { TimeSyncService } from '@core/services/timeSync/time-sync.service';
import { LiveEventClockProviderService } from '@shared/components/liveClock/live-event-clock-provider.service';
import { CashOutLabelService } from '@core/services/cashOutLabel/cash-out-label.service';
import { Location } from '@angular/common';
import { UserService } from '@core/services/user/user.service';
import { StorageService } from '@core/services/storage/storage.service';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { IsPropertyAvailableService } from '@sb/services/isPropertyAvailable/is-property-available.service';
import { CommentsService } from '@core/services/comments/comments.service';
import { ActivatedRoute, Router } from '@angular/router';
import { RoutingState } from '@sharedModule/services/routingState/routing-state.service';
import { InplayApiModule } from '@app/inPlay/inplay-api.module';
import { SportsConfigService } from '@sb/services/sportsConfig/sports-config.service';
import { GermanSupportInPlayService } from '@ladbrokesMobile/core/services/germanSupportInPlay/german-support-inplay.service';

@Injectable({
  providedIn: InplayApiModule
})
export class InplayMainService extends LadbrokesInplayMainService {
  static ngInjectableDef = undefined;

  constructor(
    pubSubService: PubSubService,
    inPlayDataService: InplayDataService,
    inPlayStorageService: InPlayStorageService,
    inPlaySubscriptionManagerService: InplaySubscriptionManagerService,
    timeSyncService: TimeSyncService,
    liveEventClockProviderService: LiveEventClockProviderService,
    cashOutLabelService: CashOutLabelService,
    location: Location,
    userService: UserService,
    storageService: StorageService,
    cmsService: CmsService,
    windowRef: WindowRefService,
    isPropertyAvailableService: IsPropertyAvailableService,
    commentsService: CommentsService,
    router: Router,
    routingState: RoutingState,
    route: ActivatedRoute,
    sportsConfigService: SportsConfigService,
    germanSupportInPlayService: GermanSupportInPlayService) {
    super(
      pubSubService,
      inPlayDataService,
      inPlayStorageService,
      inPlaySubscriptionManagerService,
      timeSyncService,
      liveEventClockProviderService,
      cashOutLabelService,
      location,
      userService,
      storageService,
      cmsService,
      windowRef,
      isPropertyAvailableService,
      commentsService,
      router,
      routingState,
      route,
      sportsConfigService,
      germanSupportInPlayService
    );
  }
}