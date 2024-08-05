import { Component, ChangeDetectionStrategy, ChangeDetectorRef } from '@angular/core';
import { InplayPageComponent as AppInplayPageComponent } from '@app/inPlay/components/inplayPage/inplay-page.component';
import { InplayConnectionService } from '@app/inPlay/services/inplayConnection/inplay-connection.service';
import { InplayMainService } from '@ladbrokesMobile/inPlay/services/inplayMain/inplay-main.service';
import { InPlayStorageService } from '@ladbrokesMobile/inPlay/services/inplayStorage/in-play-storage.service';
import { RoutingState } from '@sharedModule/services/routingState/routing-state.service';
import { ActivatedRoute, Router } from '@angular/router';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';

@Component({
  selector: 'inplay-page',
  templateUrl: './inplay-page.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush
})

export class InplayPageComponent extends AppInplayPageComponent {
  constructor(
    inPlayConnectionService: InplayConnectionService,
    protected inPlayMainService: InplayMainService,
    protected inplayStorageService: InPlayStorageService,
    router: Router,
    route: ActivatedRoute,
    routingState: RoutingState,
    protected pubsubService: PubSubService,
    changeDetector: ChangeDetectorRef
  ) {
    super(
      inPlayConnectionService,
      inPlayMainService,
      inplayStorageService,
      router,
      route,
      routingState,
      pubsubService,
      changeDetector
    );
  }

  protected addEventListeners(): void {
    super.addEventListeners();

    /* eslint-disable-next-line */
    this.pubsubService.subscribe(this.tagName, this.pubsubService.API.SESSION_LOGIN, () => {
      if (this.inPlayMainService.isNewUserFromOtherCountry()) {
        this.inplayStorageService.outdateRibbonCache();
        this.reloadComponent();
        this.changeDetector.detectChanges();
      }
    });
  }
}
