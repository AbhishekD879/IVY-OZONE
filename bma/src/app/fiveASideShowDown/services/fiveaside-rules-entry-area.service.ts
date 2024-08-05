import { Injectable } from '@angular/core';
import { UserService } from '@core/services/user/user.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { RoutingHelperService } from '@core/services/routingHelper/routing-helper.service';
import { IContest } from '@core/services/cms/models/contest';
import { GtmService } from '@core/services/gtm/gtm.service';
import { FiveASideShowDownApiModule } from '@app/fiveASideShowDown/fiveASideShowDown-api.module';
import {
  ENTRY_BUTTON, ENTRY_ENABLE_STATUSES
} from '@fiveASideShowDownModule/components/fiveASideRulesEntryArea/fiveaside-rules-entry-area.constant';
import { PubSubService } from '@app/core/services/communication/pubsub/pubsub.service';
import { IEventDetails } from '../models/show-down';

@Injectable({
  providedIn: FiveASideShowDownApiModule
})
export class FiveasideRulesEntryAreaService {

  constructor(private userService: UserService,
    private localeService: LocaleService,
    private routingHelper: RoutingHelperService,
    private gtm: GtmService,
    private pubsubService: PubSubService) { }

  /**
   * To Fetch Button status, based on rules
   * @param {number} contestSize
   * @param {number} userContestSize
   * @param {IContest} contest
   * @returns {buttonType: string, isBuildBetEnabled: boolean }}
   */
  getButtonStatus(contestSize: number, userContestSize: number,
    contest: IContest): { buttonType: string, isBuildBetEnabled: boolean } {
    let buttonType: string;
    const isContestFull: boolean = contest.maxEntries ?
    contestSize >= contest.maxEntries: false;
    const hasMaxUserEntries: boolean = contest.maxEntriesPerUser ?
     userContestSize >= contest.maxEntriesPerUser: false;
    const hasAlreadyPlacedBet: boolean = userContestSize >= 1;
    if (this.userService.username) {
      buttonType = ENTRY_BUTTON.buildTeam;
    } else {
      buttonType = ENTRY_BUTTON.loginOrJoin;
    }
    if (this.userService.status && !isContestFull) {
      if (hasAlreadyPlacedBet) {
        buttonType = !hasMaxUserEntries ? ENTRY_BUTTON.buildAnotherTeam :
          this.localeService.applySubstitutions(ENTRY_BUTTON.maxEntriesReached,
            { maxUserEntries: contest.maxEntriesPerUser, betsPlaced: userContestSize });
      }
    } else if (isContestFull) {
      buttonType = ENTRY_BUTTON.contestFull;
    }
    const isBuildBetEnabled: boolean = ENTRY_ENABLE_STATUSES.includes(buttonType);
    return { buttonType, isBuildBetEnabled};
  }

  /**
   * To Form Five A side Url
   * @param {ISportEvent} event
   * @returns {string}
   */
  formFiveASideUrl(event: IEventDetails): string {
    const parts: Array<string|number> = ['event', event.categoryName, event.className || 'class',
    event.typeName || 'type', event.name, event.id];
    const url: string = parts.map((part: string | number) => `/${this.routingHelper.encodeUrlPart(part)}`).join('');
    return url;
  }

  /**
   * To Track Gtm event for all actions
   * @param {string} eventCategory
   * @param {string} eventAction
   * @param {string} eventLabel
   * @returns {void}
   */
  trackGTMEvent(eventCategory: string, eventAction: string, eventLabel: string): void {
    this.gtm.push('trackEvent', {eventCategory, eventAction, eventLabel});
  }

  /**
   * Forming team flag name from team name
   * @param { string } name
   * @returns { string }
   */
  formFlagName(name: string): string {
    if (name) {
      const teamName: string = name.toLowerCase().split(' ').join('_');
      const flagName: string = this.localeService.getString('fs.flagIcon', {teamName});
      return flagName;
    }
  }

}
