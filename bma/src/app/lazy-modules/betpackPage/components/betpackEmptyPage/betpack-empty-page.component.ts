import { Component, Input, OnInit } from '@angular/core';
import { BetReceiptService } from '@app/betslip/services/betReceipt/bet-receipt.service';
import { StorageService } from '@app/core/services/storage/storage.service';
import { GtmService } from '@app/core/services/gtm/gtm.service';

@Component({
  selector: 'betpack-empty-page',
  templateUrl: './betpack-empty-page.component.html',
  styleUrls: ['./betpack-empty-page.component.scss'],
})
export class BetpackEmptyPageComponent implements OnInit {
  @Input() errorTitle?: string;
  @Input() errorMessage?: string;
  @Input() goToBettingLabel?: string;
  @Input() goBettingURL?: string;
  @Input() buttonEnable?: boolean;
  @Input() isReview?: boolean;


  cmsMessages: any;
  gtmSendData: string[] = ['bet bundles is empty', 'buy bet packs'];
  constructor(
    protected betReceiptService: BetReceiptService,
    protected storageService: StorageService,
    private gtmService: GtmService
  ) { }

  /**
  * @returns {void}
  */
  ngOnInit(): void {
    this.sendGtmData(this.gtmSendData[0]);
  }

  /**
  * GATracking
  * @param  {string} Action
  * @returns void
  */
  sendGtmData(data: string): void {
    const gtmData = {
      event: 'trackEvent',
      eventAction: this.isReview?'my bet bundles':'bet bundles',
      eventCategory: 'bet bundles marketplace',
      eventLabel: data.toLowerCase(),
    };
    this.gtmService.push(gtmData.event, gtmData);
  }
}