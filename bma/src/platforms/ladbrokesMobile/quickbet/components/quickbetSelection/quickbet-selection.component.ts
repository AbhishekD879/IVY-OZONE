import { Component, OnInit } from '@angular/core';

import { QuickbetSelectionComponent } from '@app/quickbet/components/quickbetSelection/quickbet-selection.component';
import { IQuickbetNotificationModel } from '@app/quickbet/models/quickbet-notification.model';
import { IAvailableContests } from '@app/fiveASideShowDown/models/available-contests.model';
import environment from '@environment/oxygenEnvConfig';
import { BYBBet } from '@app/yourCall/models/bet/byb-bet';
import { CHANNEL } from '@app/shared/constants/channel.constant';
import { rgyellow } from '@app/bma/constants/rg-yellow.constant';

@Component({
  selector: 'quickbet-selection',
  templateUrl: './quickbet-selection.component.html',
  styleUrls: ['quickbet-selection.component.scss']
})

export class LadbrokesQuickbetSelectionComponent extends QuickbetSelectionComponent implements OnInit {
  public infoMessages: Array<string> = [];
  public infoPanel: IQuickbetNotificationModel;
  public fiveASideContests: IAvailableContests[];
  public defaultSelectedContest: string;

  ngOnInit(): void {
    super.ngOnInit();
    this.updatePanelMessage = this.updatePanelMessage.bind(this);
    this.updatePanelMessage(this.quickbetNotificationService.config);
    this.pubsub.subscribe(this.QB_SELECTION_NAME, this.pubsub.API.QUICKBET_INFO_PANEL, this.updatePanelMessage);
    this.getFiveASideContestsForLegs();
  }

  /**

   * checks price boost message length and returns boolean

   * @return { boolean } uses it as input for lazy component

   */
  public showMessage(): boolean {
    const isDepositMessage = this.infoPanel && this.infoPanel.msg && this.infoPanel.location === 'quick-deposit';
    const isPriceBoostMessage = this.canBoostSelection && this.selection.price.isPriceChanged && this.selection.isBoostActive;
    const messages = [];

    if (isDepositMessage) {
      messages.push(this.infoPanel.msg);
    }

    if (isPriceBoostMessage) {
      messages.push(this.locale.getString('quickbet.reboostPriceChanged'));
    }

    this.infoMessages = messages;

    return !!messages.length;
  }

  /**

   * Makes an API call to get all the five contests and

   * @return { void } uses it as input for lazy component

   */

  public getFiveASideContests(): void {
    const contestObj = {
      brand: environment.brand,
      eventId: this.selection.eventId,
      contestId: this.fiveASideContestSelectionService.defaultSelectedContest,
      userId: this.user.username,
      token: this.user.bppToken
    };
    this.fiveASideContestSelectionService.getAllActiveFiveASideContests(contestObj).subscribe(resp => {
      this.executeFiveASideResponse(resp);
    });
  }

  /**
   * Common method to filter the available contests and
   * sets the default contest ID
   * @return { void }
   */
  public executeFiveASideResponse(resp: IAvailableContests[]): void {
    resp = this.fiveASideContestSelectionService.validateRoleBasedContests(resp);
    if (!resp || resp.length <= 0) {
      this.fiveASideContestSelectionService.defaultSelectedContest = '';
    }
    this.defaultSelectedContest = this.fiveASideContestSelectionService.defaultSelectedContest;
    this.fiveASideContests = resp;
  }

   /**
   * Common method to check the yellow flag
   * sets the default contest ID to null if user is rg enabled 
   * @return { Boolean }
   */
  public checkYellowFlag(): boolean {
    if(!this.bonusSuppressionService.checkIfYellowFlagDisabled(rgyellow.FIVE_A_SIDE)) {
      this.fiveASideContestSelectionService.defaultSelectedContest = null;
    }
    return this.bonusSuppressionService.checkIfYellowFlagDisabled(rgyellow.FIVE_A_SIDE)
  }

  /**
   * @param infoPanelObj contains information related to bet deposit
   * @return { void }
   */
  private updatePanelMessage(infoPanelObj: IQuickbetNotificationModel): void {
    const isDepositMessage = !infoPanelObj.location || infoPanelObj.location === 'quick-deposit';

    if (isDepositMessage) {
      this.infoPanel = Object.assign({}, infoPanelObj);
    }
  }

  /**
   * Validate fiveASide Legs and get contests
   * @returns void
   */
  private getFiveASideContestsForLegs(): void {
    if (this.selection instanceof BYBBet) {
      const sel = this.selection as BYBBet;
      if (sel.selections.length === 5 && sel.channel === CHANNEL.fiveASide) {
        this.getFiveASideContests();
      }
    }
  }
}
