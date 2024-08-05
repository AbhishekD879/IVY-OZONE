import {  Component, Input, OnInit } from '@angular/core';
import { CmsService } from '@app/core/services/cms/cms.service';
import { LocaleService } from '@app/core/services/locale/locale.service';
import { IPromotionLite } from '@app/core/services/cms/models/promotion/promotion-lite.model';
import { ExistNewUserService } from '@app/core/services/existNewUser/exist-new-user.service';
import { IPromotionLiteList } from '@app/core/services/cms/models';
import { GtmService } from '@app/core/services/gtm/gtm.service';
import { PubSubService } from '@app/core/services/communication/pubsub/pubsub.service';
@Component({
  selector: 'twoup-blurbmsg',
  templateUrl: './twoup-signposting-blurbmsg.component.html',
  styleUrls: ['./twoup-signposting-blurbmsg.component.scss']
})
export class TwoUpSignPostingBlurbMsgComponent implements OnInit{

  @Input() marketName;
  twoUpMarketPromotionData: IPromotionLite;
  twoUpMarketName: string;
  gtaEventName: string;

  constructor(private cmsService: CmsService,
    private locale: LocaleService,
    private existNewUserService: ExistNewUserService,
    private gtm: GtmService,
    private pubSubService: PubSubService) {
   }

  ngOnInit() {
    this.twoUpMarketName = this.locale.getString('bma.twoUpMarketName');
    this.cmsService.getSignpostingPromotionsLight().subscribe((promos: IPromotionLiteList | any) => {
      promos.promotions = this.existNewUserService.filterExistNewUserItems(promos.promotions, false);
      this.twoUpMarketPromotionData = promos.promotions.find(res => res.templateMarketName && res.templateMarketName === this.twoUpMarketName);
    });
    this.pubSubService.subscribe('twoUpTracking', this.pubSubService.API.TWO_UP_TRACKING, (data) => {
      if (data.marketName.includes('2Up')) {
        this.sendGtmData(data);
      }
    });
  }

  sendGtmData(data: any): void {
    const twoUp = this.locale.getString('bma.twoUp');
    const trackEvents = {
      categoryEvent: 'promotions',
      labelEvent: data.marketName,
      actionEvent: 'click',
      positionEvent: data.action === 'open' ? 'not applicable' : `${twoUp} popup`,
      locationEvent: data.eventName || this.gtaEventName,
      eventDetails: data.action === 'open' ? `${twoUp} icon`: 'ok',
      urlClicked: 'not applicable',
    }
    this.gtaEventName = data.eventName;
    this.gtm.push('trackEvent', trackEvents);
  }
}
