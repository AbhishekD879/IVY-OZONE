import { Injectable } from '@angular/core';

import { GtmService } from '@core/services/gtm/gtm.service';
import { IPlayerGTM } from './player-scores.model';

@Injectable()
export class YourCallPlayerStatsGTMService {
  route: string;
  constructor(private GTM: GtmService) {
    this.route = '';
  }

  /**
   * send GTM tracking, when user chooses to change statistic number
   * @params {object} statisticInfo
   */
  sendChangeStatisticGTM(statisticInfo: IPlayerGTM): void {
    this.GTM.push('trackEvent', {
      eventCategory: 'your call',
      eventAction: 'ds in play player stat',
      eventLabel: 'update statistic',
      playerName: statisticInfo.playerName,
      playerStat: statisticInfo.playerStat,
      playerStatNum: statisticInfo.playerStatNum
    });
  }

  /**
   * send GTM tracking, when user uses team switcher
   * @params {string} teamName
   */
  sendTeamSwitcherGTM(teamName: string): void {
    const action = `switch team - ${teamName}`;
    this.sendGTM(action);
  }

  /**
   * Tracking GA data
   * @params {string} eventLabel
   * @params {string} action
   */
  sendGTMData(eventLabel: string, action: string): void {
    const eventAction = this.cutEventAction(`${action} ${this.route}`);
    const gtmAction = `${eventLabel} ${eventAction}`;

    this.sendGTM(gtmAction);
  }

  /**
   * deleting extra text from eventLabel
   * @params {string} eventAction
   */
  private cutEventAction(eventAction: string): string {
    const extraSubstring = 'Player_Stats_';
    return eventAction.indexOf(extraSubstring) === 0 ? eventAction.substr(extraSubstring.length) : eventAction;
  }

  /**
   * Send GTM object
   * @params {string} eventAction
   */
  private sendGTM(eventAction: string): void {
    this.GTM.push('trackEvent', {
      eventCategory: 'your call',
      eventAction: 'ds in play player stat',
      eventLabel: eventAction
    });
  }
}
