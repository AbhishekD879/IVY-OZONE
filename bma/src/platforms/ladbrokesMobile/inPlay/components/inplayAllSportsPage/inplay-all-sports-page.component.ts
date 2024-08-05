import { Component, OnDestroy, ChangeDetectionStrategy, ChangeDetectorRef } from '@angular/core';
import { InplayAllSportsPageComponent as
    AppInplayAllSportsPageComponent } from '@app/inPlay/components/inplayAllSportsPage/inplay-all-sports-page.component';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { InplayMainService } from '@ladbrokesMobile/inPlay/services/inplayMain/inplay-main.service';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { InplayConnectionService } from '@app/inPlay/services/inplayConnection/inplay-connection.service';

@Component({
  selector: 'inplay-all-sports-page',
  templateUrl: '../../../../../app/inPlay/components/inplayAllSportsPage/inplay-all-sports-page.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush
})

export class InplayAllSportsPageComponent extends AppInplayAllSportsPageComponent implements OnDestroy {
  constructor(
    pubsubService: PubSubService,
    protected inplayMainService: InplayMainService,
    cms: CmsService,
    inPlayConnectionService: InplayConnectionService,
    changeDetector: ChangeDetectorRef
  ) {
    super(
      pubsubService,
      inplayMainService,
      cms,
      inPlayConnectionService,
      changeDetector
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
        this.changeDetector.detectChanges();
      }
    });
  }
}
