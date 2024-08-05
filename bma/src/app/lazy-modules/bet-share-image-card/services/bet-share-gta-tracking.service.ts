import { Injectable } from "@angular/core";
import { GtmService } from "@app/core/services/gtm/gtm.service";
import { BET_SHARE_GA_CONSTANTS } from "../constants/bet-share-ga-constants";

@Injectable()
export class BetShareGTAService {
  constructor(
    private gtm: GtmService
  ) {}

  public setGtmData(positionEvent: string, locationEvent: string, eventDetails: string): void {
    const gtmData = {
        event: BET_SHARE_GA_CONSTANTS.EVENT,
        'component.CategoryEvent': BET_SHARE_GA_CONSTANTS.BET_SLIP,
        'component.LabelEvent': BET_SHARE_GA_CONSTANTS.BET_SHARING,
        'component.ActionEvent': BET_SHARE_GA_CONSTANTS.CLICK,
        'component.PositionEvent': positionEvent,
        'component.LocationEvent': locationEvent,
        'component.EventDetails':  eventDetails,
        'component.URLClicked': BET_SHARE_GA_CONSTANTS.NOT_APPLICABLE
    }

    this.gtm.push(gtmData.event, gtmData);
  }
}