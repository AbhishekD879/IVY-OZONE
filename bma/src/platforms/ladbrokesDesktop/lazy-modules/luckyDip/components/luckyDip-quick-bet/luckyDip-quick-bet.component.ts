import { Component, Input, Output, EventEmitter } from '@angular/core';
import { LUCKY_DIP_CONSTANTS } from '@lazy-modules/luckyDip/constants/lucky-dip-constants';
import { DialogService } from '@core/services/dialogService/dialog.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { ILuckyDipFieldsConfig, ILuckyDipRemoteBetSlipSelection } from '@lazy-modules/luckyDip/models/luckyDip';

@Component({
  selector: 'lucky-dip-qb',
  templateUrl: './luckyDip-quick-bet.component.html',
  styleUrls: ['luckyDip-quick-bet.component.scss']
})

export class LadsDeskLuckyDipBetSelectionComponent  {
  @Input() selectionDataLd: ILuckyDipRemoteBetSlipSelection;
  @Input() luckyDipMarketName:string;
  @Input() luckyDipCmsData: ILuckyDipFieldsConfig;
  @Output() readonly placedBet: EventEmitter<any> = new EventEmitter();
  isLuckyDip: boolean = true;
  tag = LUCKY_DIP_CONSTANTS.DESK_LDIP_TAG;
  
  constructor(
    public pubsub: PubSubService,
    public dialogService: DialogService) {
  }

  /**
   * Method to handle output events from parent
   * @returns {void}
   */
  handleLuckyDipEvents(event): void {
    if (event.output === LUCKY_DIP_CONSTANTS.PLACE_BET_FN) {
      this.pubsub.publish(this.pubsub.API.MY_BET_PLACED_LD, event.value);
      this.placedBet.emit(event.value);
    }
    else if (event.output === LUCKY_DIP_CONSTANTS.CLOSE_PANEL_FN) {
      this.dialogService.closeDialog(DialogService.API.splashModal);
    }
  }

  /**
   * set tag for ld desktop disable quickbet
   * @returns {void}
   */
  setTagforLd(): void {
    this.tag = LUCKY_DIP_CONSTANTS.DESK_LDIP_TAG;
  }
}
