import { Component, Input, OnInit } from '@angular/core';
import PROMOTIONS_TABS, {
  ID_TAB_PROMOTION_ALL,
  ID_TAB_PROMOTION_CONNECT
} from '../../constants/promotion-tabs.constant';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { ISystemConfig } from '@core/services/cms/models';

@Component({
  selector: 'promotions',
  templateUrl: './promotions.component.html',
  styleUrls: ['../../assets/styles/main.scss']
})
export class PromotionsComponent implements OnInit {
  title: string = 'Promotions';
  promotionTabs: { id: string, label: string, name: string, url: string }[];
  promotionActiveTab: { [id: string]: string };

  @Input() isRetail?: boolean;

  constructor(private cmsService: CmsService) {

  }

  ngOnInit(): void {
    this.cmsService.getSystemConfig()
      .subscribe((config: ISystemConfig) => {
        // TODO: rename to retail after changes in cms.
        this.promotionTabs = config.Connect && config.Connect.promotions ? PROMOTIONS_TABS : [PROMOTIONS_TABS[0]];
        this.promotionActiveTab = !this.isRetail ? { id: ID_TAB_PROMOTION_ALL } : { id: ID_TAB_PROMOTION_CONNECT };
      });

  }
}
