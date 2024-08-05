import { Injectable } from '@angular/core';

import { GtmService } from '@core/services/gtm/gtm.service';
import { GOLF_CONSTANTS, GOLF_CURRENT_TAB} from '@app/shared/constants/channel.constant';

@Injectable()
export class MarketSelectorTrackingService {

  constructor(
    private gtmService: GtmService
  ) {}

  /**
   * Send market selector data to GA
   * @param {string} marketName
   * @param {string} eventCategory
   * @param {number} sportId
   */
  pushToGTM(marketName, sportId) {
    const data = {
      eventCategory: 'market selector',
      eventAction: 'change market',
      eventLabel: marketName,
      categoryID: sportId
    };

    this.gtmService.push('trackEvent', data);
  }
  sendGTMDataOnMarketSelctorChange(filter, selectedTab){
    const gtmData = {
      event: 'Event.Tracking',
      'component.CategoryEvent': 'navigation',
      'component.LabelEvent': 'golf',
      'component.ActionEvent': 'click',
      'component.PositionEvent': filter,
      'component.LocationEvent': GOLF_CONSTANTS[GOLF_CURRENT_TAB.activeTab],
      'component.EventDetails': 'change',
      'component.URLClicked': 'not applicable'
    }
    this.gtmService.push(gtmData.event, gtmData);
  }
}
