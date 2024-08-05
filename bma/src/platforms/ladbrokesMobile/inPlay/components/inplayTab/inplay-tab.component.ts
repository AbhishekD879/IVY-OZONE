import { ChangeDetectorRef, Component, OnDestroy, ChangeDetectionStrategy } from '@angular/core';
import { InplayTabComponent as AppInplayTabComponent } from '@app/inPlay/components/inplayTab/inplay-tab.component';
import { InplayConnectionService } from '@app/inPlay/services/inplayConnection/inplay-connection.service';
import { InplayMainService } from '@ladbrokesMobile/inPlay/services/inplayMain/inplay-main.service';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { InPlayStorageService } from '@ladbrokesMobile/inPlay/services/inplayStorage/in-play-storage.service';
import { InplaySubscriptionManagerService } from '@app/inPlay/services/InplaySubscriptionManager/inplay-subscription-manager.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { AWSFirehoseService } from '@lazy-modules/awsFirehose/service/aws-firehose.service';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'inplay-tab',
  templateUrl: '../../../../../app/inPlay/components/inplayTab/inplay-tab.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush
})

export class InplayTabComponent extends AppInplayTabComponent implements OnDestroy {
  constructor(
    inPlayConnectionService: InplayConnectionService,
    protected inplayMainService: InplayMainService,
    cmsService: CmsService,
    inplayStorageService: InPlayStorageService,
    inplaySubscriptionManagerService: InplaySubscriptionManagerService,
    pubsubService: PubSubService,
    changeDetectorRef: ChangeDetectorRef,
    awsService: AWSFirehoseService,
    protected route: ActivatedRoute
  ) {
    super(
      inPlayConnectionService,
      inplayMainService,
      cmsService,
      inplayStorageService,
      inplaySubscriptionManagerService,
      pubsubService,
      changeDetectorRef,
      awsService,
      route
    );
  }

  addEventListeners(): void {
    super.addEventListeners();

    this.pubsubService.subscribe('inplay', this.pubsubService.API.SESSION_LOGIN, () => {
      if (this.inplayMainService.isNewUserFromOtherCountry()) {
        this.reloadComponent();
        this.changeDetectorRef.detectChanges();
      }
    });
  }

  ngOnDestroy(): void {
    this.pubsubService.unsubscribe('inplay');
    super.ngOnDestroy();
  }
}
