import { Component, ChangeDetectorRef, Input } from '@angular/core';
import { Location } from '@angular/common';

import { LocaleService } from '@core/services/locale/locale.service';
import { GtmService } from '@core/services/gtm/gtm.service';
import { RemoteBetslipService } from '@core/services/remoteBetslip/remote-betslip.service';
import { CommandService } from '@core/services/communication/command/command.service';
import { DialogService } from '@core/services/dialogService/dialog.service';
import { InfoDialogService } from '@coreModule/services/infoDialogService/info-dialog.service';
import { DeviceService } from '@core/services/device/device.service';
import { NativeBridgeService } from '@core/services/nativeBridge/native-bridge.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { QuickbetService } from '@app/quickbet/services/quickbetService/quickbet.service';
import { QuickbetOveraskService } from '@app/quickbet/services/quickbetOveraskService/quickbet-overask.service';
import { QuickbetDataProviderService } from '@app/core/services/quickbetDataProviderService/quickbet-data-provider.service';

import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { GtmTrackingService } from '@core/services/gtmTracking/gtm-tracking.service';
import { QuickbetDepositService } from '@quickbetModule/services/quickbetDepositService/quickbet-deposit.service';
import { UserService } from '@core/services/user/user.service';
import { RendererService } from '@shared/services/renderer/renderer.service';
import { QuickbetNotificationService } from '@app/quickbet/services/quickbetNotificationService/quickbet-notification.service';
import { SessionStorageService } from '@core/services/storage/session-storage.service';
import { RacingPostTipService } from '@app/lazy-modules/racingPostTip/service/racing-post-tip.service';
import { AWSFirehoseService } from '@lazy-modules/awsFirehose/service/aws-firehose.service';
import { ArcUserService } from '@app/lazy-modules/arcUser/service/arcUser.service';
import { QuickbetComponent } from '@app/quickbet/components/quickbet/quickbet.component';
import { IMarket } from '@core/models/market.model';
import { StorageService } from '@core/services/storage/storage.service';
import { BetslipService } from '@app/betslip/services/betslip/betslip.service';
import { ScorecastDataService } from '@app/core/services/scorecastData/scorecast-data.service';
@Component({
  selector: 'sb-quickbet',
  templateUrl: 'sb-quickbet.component.html'
})
export class SbQuickbetComponent extends QuickbetComponent {
@Input() isStreamAndBet?: boolean;
@Input() market: IMarket;
@Input() categoryName: string;
@Input() eventName: string;

  constructor( locale: LocaleService,
     pubsub: PubSubService,
     gtm: GtmService,
     quickbetService: QuickbetService,
     remoteBsService: RemoteBetslipService,
     quickbetOverAskService: QuickbetOveraskService,
     command: CommandService,
     dialogService: DialogService,
     infoDialogService: InfoDialogService,
     device: DeviceService,
     nativeBridgeService: NativeBridgeService,
     location: Location,
     quickbetDataProviderService: QuickbetDataProviderService,
     rendererService: RendererService,
     windowRef: WindowRefService,
     gtmTrackingService: GtmTrackingService,
     quickbetDepositService: QuickbetDepositService,
     quickbetNotificationService: QuickbetNotificationService,
     awsService: AWSFirehoseService,
     changeDetectorRef: ChangeDetectorRef,
     userService: UserService,
     sessionStorage: SessionStorageService,
     racingPostTipService: RacingPostTipService,
     arcUserService: ArcUserService,
     protected storageService: StorageService,
     protected betslipService:BetslipService,
     protected scorecastDataService: ScorecastDataService
    ) 
     {
       super(locale, pubsub, gtm, quickbetService, remoteBsService, quickbetOverAskService, command,
        dialogService, infoDialogService, device, nativeBridgeService, location, quickbetDataProviderService,
        rendererService, windowRef, gtmTrackingService, quickbetDepositService, quickbetNotificationService,
        awsService, changeDetectorRef, userService, sessionStorage, racingPostTipService, arcUserService, storageService, betslipService, scorecastDataService);
        this.tag = 'SbQuickbet';
        
      this.addSelectionHandler = this.addSelectionHandler.bind(this);
}

ngOnInit() {
  super.ngOnInit();
  this.pubsub.subscribe(this.tag, this.pubsub.API.ADD_TO_QUICKBET, this.addSelectionHandler);
  this.placeBetListener();
  this.selection && this.addSelectionHandler(this.selection);
  this.quickbetService.quickBetOnOverlayCloseSubj.subscribe((qbStatusMsg: string) => {
    if(qbStatusMsg === 'fullscreen exit') {
      this.closePanel();
    }
  });
}

  /**
   * closes the bet stream and bet quick bet
   */
  closePanel(): void {
    if (this.device.isOnline()) {
      super.closePanel(false);
      this.pubsub.publish(this.pubsub.API.REMOVE_FROM_SB_QUICKBET);
    } else {
      this.infoDialogService.openConnectionLostPopup();
    }
  }

  ngOnDestroy(): void {
    this.pubsub.unsubscribe(this.tag);
    // this.removeSubscribers(); TODO: chk this if needed to be commented?
  }
  
}
