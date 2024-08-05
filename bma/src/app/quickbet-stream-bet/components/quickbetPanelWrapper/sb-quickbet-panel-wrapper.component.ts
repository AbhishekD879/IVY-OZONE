import { Component, OnDestroy, ChangeDetectorRef, Input } from '@angular/core';
import { QuickbetPanelWrapperComponent } from '@app/shared/components/quickbetPanelWrapper/quickbet-panel-wrapper.component';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { CmsService } from '@core/services/cms/cms.service';
import { RemoteBetslipService } from '@core/services/remoteBetslip/remote-betslip.service';
import { IMarket } from '@core/models/market.model';

@Component({
  selector: 'sb-quickbet-panel-wrapper',
  templateUrl: 'sb-quickbet-panel-wrapper.component.html'
})
export class SbQuickbetPanelWrapperComponent extends QuickbetPanelWrapperComponent implements OnDestroy {
  
  @Input() market: IMarket;
  @Input() categoryName: string;
  @Input() eventName: string;

  
  tagName = 'SbQuickbetPanelWrapperComponent';

  constructor(
    protected pubsub: PubSubService,
    protected changeDetectorRef: ChangeDetectorRef,
    protected cmsService: CmsService,
    protected remoteBsService: RemoteBetslipService
  ) {
    super(pubsub, changeDetectorRef, cmsService, remoteBsService);
  }

  addListeners() {
    this.pubsub.subscribe(this.tagName, this.pubsub.API.RENDER_QUICKBET_COMPONENT,
      this.renderQuickbet);
  }

  ngOnDestroy(): void {
    this.pubsub.unsubscribe(this.tagName);
  }

}
