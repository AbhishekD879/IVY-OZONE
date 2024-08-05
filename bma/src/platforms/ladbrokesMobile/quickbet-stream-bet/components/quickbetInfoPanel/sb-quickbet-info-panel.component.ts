import { ChangeDetectorRef, Component, Input } from '@angular/core';
import { QuickbetNotificationService } from '@app/quickbet/services/quickbetNotificationService/quickbet-notification.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { Router } from '@angular/router';
import { LadbrokesQuickbetInfoPanelComponent } from '@ladbrokesMobile/quickbet/components/quickbetInfoPanel/quickbet-info-panel.component';

@Component({
  selector: 'sb-quickbet-info-panel',
  templateUrl: '../../../../../app/quickbet-stream-bet/components/quickbetInfoPanel/sb-quickbet-info-panel.component.html',
  styleUrls: ['../../../../../app/quickbet-stream-bet/components/quickbetInfoPanel/sb-quickbet-info-panel.component.scss']
})
export class SbQuickbetInfoPanelComponent extends LadbrokesQuickbetInfoPanelComponent {

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
