import { Injectable } from "@angular/core";
import { GtmService } from "@app/core/services/gtm/gtm.service";
import { GA_FIRST_BET_CONSTANTS } from "../constants/first-bet-ga-constants";

@Injectable({providedIn: 'root'})
export class FirstBetGAService {
  constructor(
    private gtm: GtmService
  ) {}

  public setGtmData(event: string, actionEvent: string, positionEvent: string, eventDetails: string, locationEvent?: string): void {
    const gtmData = {
        event: event,
        'component.CategoryEvent': GA_FIRST_BET_CONSTANTS.BETTING,
        'component.LabelEvent': GA_FIRST_BET_CONSTANTS.FIRST_BET_PLACEMENT,
        'component.ActionEvent': actionEvent,
        'component.PositionEvent': positionEvent,
        'component.LocationEvent': locationEvent || GA_FIRST_BET_CONSTANTS.NOT_APPLICABLE,
        'component.EventDetails':  eventDetails,
        'component.URLClicked': GA_FIRST_BET_CONSTANTS.NOT_APPLICABLE
    }

    this.gtm.push(gtmData.event, gtmData);
  }
}