import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { CmsService } from '@core/services/cms/cms.service';
import { rgyellow } from '@app/bma/constants/rg-yellow.constant';
import { BonusSuppressionErrorDialogComponent } from '@shared/components/bonusSuppressionErrorDialog/bonus-suppression-error-dialog.component';
import { ISystemConfig } from '../cms/models';
import { DialogService } from '../dialogService/dialog.service';
import { UserService } from '@core/services/user/user.service';
import environment from '@environment/oxygenEnvConfig';
import { YellowFlagInfo } from '../user/yellow-flag.model';
@Injectable()
export class BonusSuppressionService {

  bonusSuppresionUrl: string;
  homeURL = rgyellow.HOME_URL;

  constructor(private dialogService: DialogService, private router: Router, private cmsService: CmsService, private userService: UserService) {
    this.getRedirectionURL();
  }

 /**
   * navigates to home page and displays an error message for RG Yellow customer
   * @returns {void}
   */
  navigateAwayForRGYellowCustomer(): void{
    this.dialogService.openDialog(this.dialogService.ids.bonusSuppresionError, BonusSuppressionErrorDialogComponent, true);
    this.router.navigate([this.bonusSuppresionUrl]);
  }

  /**
   * Takes brand as input and checks user yellow flag restrictions.
   * @return {boolean}
   */
  checkIfYellowFlagDisabled(moduleName: string, subModule?: string): boolean {
    const rgyData = this.cmsService.getCMSYellowFlagInfo();
    if (this.userService.status && rgyData && rgyData.length) {
      const data = rgyData.find((infoObj: YellowFlagInfo) => (infoObj.brand === environment.brand
        && this.clubAndCheck(infoObj, moduleName) && this.checkRGYSubmodules(infoObj, subModule)
      ));
      return !data;
    }
    return true;
  }

  /**
   * Checks and returns existence of RGY subModules
   * @param  {YellowFlagInfo} module
   * @param  {string} subModule
   * @returns boolean
   */
  checkRGYSubmodules(module: YellowFlagInfo, subModule: string): boolean {
    if (subModule && module.subModuleEnabled && module.subModules.length) {
      return !!module.subModules.find(infoObj => (this.clubAndCheck(infoObj, subModule)));
    }
    return !module.subModuleEnabled;
  }

  /**
   * Subscribes to CMS config and fetches the URL
   */
   private getRedirectionURL() {
    this.cmsService.getSystemConfig()
      .subscribe((config: ISystemConfig) => {
        this.bonusSuppresionUrl = config.BonusSupErrorMsg ? config.BonusSupErrorMsg.url : this.homeURL
      });
  }

  /**
  * Clubs module name with all of it's alias and check for existence
  * @param {YellowFlagInfo} infoObj
  * @param {string} moduleName
  * @returns boolean
  */
  private clubAndCheck(infoObj: YellowFlagInfo, moduleName: string) {
    const moduleNameArray: string[] = [infoObj.moduleName.toLowerCase(), ...infoObj.aliasModuleNames.toLowerCase().split(',')];
    return moduleNameArray.findIndex((name) => name.trim() === moduleName.trim().toLowerCase()) > -1;
  }
}
