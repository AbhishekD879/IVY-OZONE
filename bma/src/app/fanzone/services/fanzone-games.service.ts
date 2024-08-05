import { Injectable } from "@angular/core";
import { UserService } from "@app/core/services/user/user.service";
import { FanzoneStorageService } from "@app/core/services/fanzone/fanzone-storage.service";
import { IFanzoneGamesSignPostingData } from "@app/fanzone/models/fanzone-games.model";
import { IFanzoneGameTooltipConfig } from "@app/fanzone/models/fanzone.model";
@Injectable()
export class FanzoneGamesService {
    isGameClosedForcibly: boolean;
    constructor(
        protected userService: UserService,
        protected fanzoneStorageService: FanzoneStorageService
        ) {
    }

  /**
   * sets the new fanzone game popup seen value in storage
   * @param {}
   * @returns { Void }
   */
  setNewFanzoneGamesPopupSeen(): void {
    this.fanzoneStorageService.set(`newFanzoneGamesPopupSeen-${this.userService.username}`,true);
  }

  /**
   * gets the new fanzone game popup value in storage
   * @param {}
   * @returns { booelan }
   */
  getNewFanzoneGamesPopupSeen(): boolean {
    return this.fanzoneStorageService.get(`newFanzoneGamesPopupSeen-${this.userService.username}`);
  }

  /**
   * gets the new fanzone game tooltip seen value in storage
   * @param {}
   * @returns { booelan }
   */
  getFanzoneGamesTooltipSeen(): boolean {
    return this.fanzoneStorageService.get(`newFanzoneGamesTooltipSeen-${this.userService.username}`);
  }

  /**
   * sets the new fanzone game tooltip value in storage
   * @param {}
   * @returns { Void }
   */
  setFanzoneGamesTooltipSeen(): void {
    this.fanzoneStorageService.set(`newFanzoneGamesTooltipSeen-${this.userService.username}`,true);
  }

  /**
   * Gets the new sign posting seen date value from storage
   * @param {}
   * @returns { Date }
   */
  getNewSignPostingSeenDate(): Date {
    let newSignPostingSeenDate = this.fanzoneStorageService.get(`newSignPostingSeenDate-${this.userService.username}`);
    if (newSignPostingSeenDate) {
      newSignPostingSeenDate = new Date(newSignPostingSeenDate);
    }
    return newSignPostingSeenDate;
  }

  /**
   * sets the new sign posting seen date value in storage if user visits game tab first time in between cms start date and end date or when new game is launched
   * @param {newSignPostingData: IFanzoneGamesSignPostingData}
   * @returns { Void }
   */
  setNewSignPostingSeenDate(newSignPostingData: IFanzoneGamesSignPostingData): void {
    const newSignPostingSeenDate = this.getNewSignPostingSeenDate();
    if((!newSignPostingSeenDate && new Date().getTime() <= new Date(newSignPostingData.endDate).getTime()) || (newSignPostingSeenDate && this.checkForNewGameLaunched(newSignPostingData, newSignPostingSeenDate))){
      this.fanzoneStorageService.set(`newSignPostingSeenDate-${this.userService.username}`,new Date());
    }
  }

  /**
   * checks if new fanzone game is launched if signposting is available in storage
   * @param {newSignPostingData: IFanzoneGamesSignPostingData}
   * @returns { boolean }
   */
  checkForNewGameLaunched(newSignPostingData: IFanzoneGamesSignPostingData, newSignPostingSeenDate: Date): boolean {
    let isNewGameLaunched = true;
    if (newSignPostingSeenDate.getTime() >= new Date(newSignPostingData.startDate).getTime() && newSignPostingSeenDate.getTime() <= new Date(newSignPostingData.endDate).getTime()){
      isNewGameLaunched = false;
    }
    return isNewGameLaunched;
  }

  /**
   * check to show new signposting icon before fanzone games tab name
   * @param {newSignPostingData: IFanzoneGamesSignPostingData}
   * @returns { boolean }
   */
  showNewSignPostingIcon(newSignPostingData: IFanzoneGamesSignPostingData): boolean {
    let showNewSignPostingIcon = false;
    if (newSignPostingData.active) {
        const newSignPostingStorageSeenDate = this.getNewSignPostingSeenDate();
        if (newSignPostingStorageSeenDate) {
            if (this.checkForNewGameLaunched(newSignPostingData, newSignPostingStorageSeenDate)) {
                showNewSignPostingIcon = true;
            }
        } else {
            const newSignPostingSeenDate = new Date();
            if (newSignPostingSeenDate.getTime() <= new Date(newSignPostingData.endDate).getTime()){
              showNewSignPostingIcon = true;
            }
        }
    }
    return showNewSignPostingIcon;
  }

  /**
   * check to show fanzone games tooltip on top of games tab name
   * @param {fanzoneGamesTooltipConfig: IFanzoneGameTooltipConfig}
   * @returns { boolean }
   */
  showFanzoneGamesTooltip(fanzoneGamesTooltipConfig: IFanzoneGameTooltipConfig): boolean {
    let showFanzoneGamesTooltip = fanzoneGamesTooltipConfig.Enable;
    if (fanzoneGamesTooltipConfig.Enable) {
        const fanzoneTooltipSeenValueFromStorage =  this.getFanzoneGamesTooltipSeen();
        if (fanzoneTooltipSeenValueFromStorage) {
          showFanzoneGamesTooltip = false;
        } else {
          showFanzoneGamesTooltip = true;
        }
    }
    return showFanzoneGamesTooltip;
  }
}