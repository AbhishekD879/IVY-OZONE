import { Component, OnDestroy, ChangeDetectorRef, ChangeDetectionStrategy } from '@angular/core';
import { InplayWatchLivePageComponent
    as AppInplayWatchLivePageComponent } from '@app/inPlay/components/inplayWatchLivePage/inplay-watch-live-page.component';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { InplayMainService } from '@ladbrokesMobile/inPlay/services/inplayMain/inplay-main.service';
import { InplayConnectionService } from '@app/inPlay/services/inplayConnection/inplay-connection.service';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { Router } from '@angular/router';
import { InplaySubscriptionManagerService } from '@app/inPlay/services/InplaySubscriptionManager/inplay-subscription-manager.service';
import { InPlayStorageService } from '@ladbrokesMobile/inPlay/services/inplayStorage/in-play-storage.service';

@Component({
  selector: 'inplay-watch-live-page',
  templateUrl: '../../../../../app/inPlay/components/inplayWatchLivePage/inplay-watch-live-page.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush
})

export class InplayWatchLivePageComponent extends AppInplayWatchLivePageComponent implements OnDestroy {
  constructor(
    pubsubService: PubSubService,
    protected inplayMainService: InplayMainService,
    inPlayConnectionService: InplayConnectionService,
    cms: CmsService,
    router: Router,
    inplaySubscriptionManagerService: InplaySubscriptionManagerService,
    inplayStorageService: InPlayStorageService,
    protected changeDetectorRef: ChangeDetectorRef
  ) {
    super(
      pubsubService,
      inplayMainService,
      inPlayConnectionService,
      cms,
      router,
      inplaySubscriptionManagerService,
      inplayStorageService,
      changeDetectorRef
    );
  }

  ngOnDestroy(): void {
    this.pubsubService.unsubscribe(this.cSyncName);
    super.ngOnDestroy();
  }

  protected addEventListeners(): void {
    super.addEventListeners();

    this.pubsubService.subscribe(this.cSyncName, this.pubsubService.API.SESSION_LOGIN, () => {
      if (this.inplayMainService.isNewUserFromOtherCountry()) {
        this.reloadComponent();
        this.changeDetectorRef.detectChanges();
      }
    });
  }
}
