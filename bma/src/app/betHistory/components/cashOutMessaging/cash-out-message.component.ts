import { Component, ComponentFactoryResolver, Input } from '@angular/core';
import { DeviceService } from '@core/services/device/device.service';
import { InfoDialogService } from '@coreModule/services/infoDialogService/info-dialog.service';
import { DialogService } from '@core/services/dialogService/dialog.service';
import { CashOutPopUpComponent } from '@app/betHistory/components/cashOutMessaging/cashOutPopUp/cash-out-popup.component';
import { CmsService } from '@app/core/services/cms/cms.service';
import { GtmService } from '@app/core/services/gtm/gtm.service';
import { CASHOUT_GTM ,GTM_DATA,SUSPENSION, MESSAGE_LIMIT } from '@app/betHistory/components/cashOutMessaging/cash-out-message.constants';

@Component({
  selector: 'cash-out-message',
  templateUrl: './cash-out-message.component.html'
})
export class CashOutMessageComponent {
  @Input() gaTrackDetails: Map<string, string>;
  @Input() isMarketLevelDisabled: boolean;
  @Input() isEventLevelDisabled: boolean;
  cashOutMessage: string = '';
  findOut: string = '';
  private cashOutCmsMsg: string = '';

  constructor(
    private device: DeviceService,
    private infoDialog: InfoDialogService,
    private dialogService: DialogService,
    private componentFactoryResolver: ComponentFactoryResolver,
    private cmsService: CmsService,
    private gtmService: GtmService
  ) {
    this.cmsService.getSystemConfig().subscribe((config) => {
      if (config && config.cashOutMessaging) {
        this.findOut = config.cashOutMessaging.findOut;
        this.cashOutCmsMsg = config.cashOutMessaging.cashOutMessage;
        this.cashOutMessage = this.formCashOutMsg(this.cashOutCmsMsg);
      }
    });
  }
  /**
   * to open pop up box
   * @returns {void}
   */
  openCashOutPopUp(): void {
    if (!this.device.isOnline()) {
      this.infoDialog.openConnectionLostPopup();
    } else {
      const componentFactory = this.componentFactoryResolver.resolveComponentFactory(CashOutPopUpComponent);
      this.dialogService.openDialog(DialogService.API.cashOutPopUp, componentFactory, true, {
        data: {
          eventName: [...this.gaTrackDetails.keys()],
          suspension: this.isEventLevelDisabled ? SUSPENSION.eventCashoutSuspension : SUSPENSION.marketCashoutSuspension
        }
      });
    }
  }

  /**
   * open dialog box to display the suspended events name
   * @returns void
   */
  dialogOpen(): void {
      this.sendGTMData();
      this.openCashOutPopUp();
  }

  /**
   * Sends data to GA tracking
   * @returns void
   */
  private sendGTMData(): void {
    const data = this.isMarketLevelDisabled?  CASHOUT_GTM.senarioTwo :  CASHOUT_GTM.senarioOne;
    const gtmData = {
      event: GTM_DATA.TRACKEVENT,
      eventAction: GTM_DATA.LINK_CLICK,
      eventCategory: GTM_DATA.CASHOUT_MESSAGING,
      eventLabel: data.eventLabel,
      eventDetails: data.eventDetails
    };
    this.gtmService.push(gtmData.event, gtmData);
  }

  /**
   * to limit the string size
   * @param msg {string}
   * @returns string
   */
  private formCashOutMsg(msg: string): string {
    return msg.length > MESSAGE_LIMIT ?
    `${msg.substring(0, MESSAGE_LIMIT)}...` : msg;
  }
}
