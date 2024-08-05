import { Component, OnInit, OnDestroy, ChangeDetectorRef } from '@angular/core';

import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { IQuickbetSelectionResponseModel } from '@app/quickbet/models/quickbet-selection-response.model';
import { ISystemConfig } from '@core/services/cms/models';
import { CmsService } from '@core/services/cms/cms.service';
import { RemoteBetslipService } from '@core/services/remoteBetslip/remote-betslip.service';

@Component({
  selector: 'quickbet-panel-wrapper',
  templateUrl: './quickbet-panel-wrapper.component.html'
})
export class QuickbetPanelWrapperComponent implements OnInit, OnDestroy {
  selection: IQuickbetSelectionResponseModel;
  quickbetShown: boolean;

  constructor(
    protected pubsub: PubSubService,
    protected changeDetectorRef: ChangeDetectorRef,
    protected cmsService: CmsService,
    protected remoteBsService: RemoteBetslipService
  ) {
    this.renderQuickbet = this.renderQuickbet.bind(this);
  }

  ngOnInit(): void {
    this.addListeners();
    this.cmsService.getSystemConfig().subscribe((config: ISystemConfig) => {
      const quickBetCmsConfig = config.quickBet || {};

      if (quickBetCmsConfig.EnableQuickBet) {
        // Check if session with RemoteBetslip MS should be restored for Quickbet Betslip
        this.remoteBsService.restoreSession();
      }
    });
  }

  addListeners() {
    this.pubsub.subscribe('QuickbetPanelWrapperComponent', this.pubsub.API.RENDER_QUICKBET_COMPONENT,
      this.renderQuickbet);
  }

  ngOnDestroy(): void {
    this.pubsub.unsubscribe('QuickbetPanelWrapperComponent');
  }

  protected renderQuickbet(selection: IQuickbetSelectionResponseModel): void {
    this.selection = selection;
    this.quickbetShown = true;
    this.changeDetectorRef.detectChanges();
  }
}
