import { Component, ChangeDetectorRef, ChangeDetectionStrategy } from '@angular/core';
import { InplaySingleSportPageComponent
    as AppInplaySingleSportPageComponent } from '@app/inPlay/components/inplaySingleSportPage/inplay-single-sport-page.component';
import { InplayMainService } from '@ladbrokesMobile/inPlay/services/inplayMain/inplay-main.service';
import { InplaySubscriptionManagerService } from '@app/inPlay/services/InplaySubscriptionManager/inplay-subscription-manager.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { InplayConnectionService } from '@app/inPlay/services/inplayConnection/inplay-connection.service';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { DeviceService } from '@core/services/device/device.service';
import { ActivatedRoute, Router } from '@angular/router';
import { AWSFirehoseService } from '@lazy-modules/awsFirehose/service/aws-firehose.service';
import { SportsConfigService } from '@app/sb/services/sportsConfig/sports-config.service';

@Component({
  selector: 'inplay-single-sport-page',
  templateUrl: '../../../../../app/inPlay/components/inplaySingleSportPage/inplay-single-sport-page.component.html',
  styleUrls: ['../../../../../app/inPlay/components/inplaySingleSportPage/inplay-single-sport-page.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})

export class InplaySingleSportPageComponent extends AppInplaySingleSportPageComponent {
  constructor(
    protected inplayMainService: InplayMainService,
    inplaySubscriptionManagerService: InplaySubscriptionManagerService,
    pubsubService: PubSubService,
    inPlayConnectionService: InplayConnectionService,
    route: ActivatedRoute,
    cms: CmsService,
    router: Router,
    deviceService: DeviceService,
    awsService: AWSFirehoseService,
    changeDetectorRef: ChangeDetectorRef,
    sportsConfigService: SportsConfigService
  ) {
    super(
      inplayMainService,
      inplaySubscriptionManagerService,
      pubsubService,
      inPlayConnectionService,
      route,
      cms,
      router,
      deviceService,
      awsService,
      changeDetectorRef,
      sportsConfigService
    );
  }

  protected showContent(): void {
    /* eslint-disable-next-line */
    this.pubsubService.subscribe(this.cSyncName, this.pubsubService.API.SESSION_LOGIN, () => {
      if (this.inplayMainService.isNewUserFromOtherCountry()) {
        this.reloadComponent();
        this.changeDetectorRef.detectChanges();
      }
    });
    super.showContent();
    this.changeDetectorRef.detectChanges();
  }
}
