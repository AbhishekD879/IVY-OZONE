import { Component, Input, ViewEncapsulation, OnInit } from '@angular/core';
import { CmsService } from '@app/core/services/cms/cms.service';
import { GtmService } from '@app/core/services/gtm/gtm.service';
import { ISystemConfig } from '@app/core/services/cms/models';
import { MAXPAY_OUT } from '@app/lazy-modules/maxpayOutErrorContainer/constants/maxpayout-error-container.constants';

@Component({
  selector: 'maxpayout-error-container',
  templateUrl: './maxpayout-error-container.component.html',
  styleUrls: ['./maxpayout-error-container.component.scss'],
  // eslint-disable-next-line
  encapsulation: ViewEncapsulation.None
})

export class MaxpayoutErrorContainerComponent implements OnInit {
  @Input() errorMsg: string;
  @Input() betType: string;
  link: string;
  click: string;
  gtmInfo: string[] = MAXPAY_OUT.eventAction;

  constructor(private cmsService: CmsService, protected gtmService: GtmService) {
    this.cmsService.getSystemConfig().subscribe((config: ISystemConfig) => {
      if (config?.maxPayOut) {
        this.link = config.maxPayOut.link;
        this.click = config.maxPayOut.click;
      }
    });
  }

  /**
   * @returns void
   */
  ngOnInit(): void {
    if (this.betType !== MAXPAY_OUT.eventLabel[3]) {
      this.sendGtmData(this.gtmInfo[1]);
    }
  }

  /**
   * GATracking for MaxPayOutError
   * @param  {string} Action
   * @returns void
   */
  sendGtmData(Action: string): void {
    const gtmData = {
      event: 'trackEvent',
      eventAction: Action,
      eventCategory: 'maximum returns',
      eventLabel: this.betType
    };
    this.gtmService.push(gtmData.event, gtmData);
  }

  /**
   * GATracking for Expand in MaxPayOutError
   * @returns void
   */
  expanded(): void {
    if (this.betType === MAXPAY_OUT.eventLabel[3] || this.betType === MAXPAY_OUT.eventLabel[2]) {
      this.sendGtmData(this.gtmInfo[2]);
    }
  }

}
