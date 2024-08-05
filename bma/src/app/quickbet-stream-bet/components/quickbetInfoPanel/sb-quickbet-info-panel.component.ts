import { ChangeDetectorRef, Component, Input, OnInit } from '@angular/core';
import { QuickbetInfoPanelComponent } from '@app/quickbet/components/quickbetInfoPanel/quickbet-info-panel.component';
import { QuickbetNotificationService } from '@app/quickbet/services/quickbetNotificationService/quickbet-notification.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { Router } from '@angular/router';


@Component({
  selector: 'sb-quickbet-info-panel',
  templateUrl: 'sb-quickbet-info-panel.component.html',
  styleUrls: ['sb-quickbet-info-panel.component.scss']
})
export class SbQuickbetInfoPanelComponent extends QuickbetInfoPanelComponent implements OnInit {

  @Input() isBrandLadbrokes: boolean;
  maxPayoutMsg: string;

  constructor(
    quickbetNotificationService: QuickbetNotificationService,
    pubsub: PubSubService,
    router: Router,
    changeDetectorRef: ChangeDetectorRef,
  ) {
    super(quickbetNotificationService, pubsub, router, changeDetectorRef);
  }

  ngOnInit(){
    super.ngOnInit();
    this.quickbetNotificationService.snbMaxPayoutMsgSub.subscribe(maxPayoutMsg => {
      this.maxPayoutMsg = maxPayoutMsg;
    });
  }
}
