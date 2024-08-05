import { inject } from '@angular/core';
import { ActivatedRouteSnapshot, CanActivateFn, CanMatchFn, Route, Router } from '@angular/router';
import { DialogService } from '@core/services/dialogService/dialog.service';
import { BonusSuppressionErrorDialogComponent } from '@sharedModule/components/bonusSuppressionErrorDialog/bonus-suppression-error-dialog.component';
import { CmsService } from '@core/services/cms/cms.service';
import { ISystemConfig } from '../services/cms/models';
import { rgyellow } from '@app/bma/constants/rg-yellow.constant';
import { BonusSuppressionService } from '@app/core/services/BonusSuppression/bonus-suppression.service';

export const RgyMatchGuard:CanMatchFn = (route:Route) =>{
  return bonusSuppressionCheck(route);
}

export const RgyCheckGuard:CanActivateFn = (route:ActivatedRouteSnapshot) =>{
  return bonusSuppressionCheck(route);
}

  /**
   * A common method to check the flag details
   * @param route will have the route data
   * @returns {Boolean | UrlTree}
   */
  function bonusSuppressionCheck(route: Route | ActivatedRouteSnapshot) {
    const dialogService = inject(DialogService);
    const bonusSuppRedirUrl = getRedirectionURL();
    const router = inject(Router);
    const isRGDisabled = inject(BonusSuppressionService).checkIfYellowFlagDisabled(route.data.moduleName);
    if (!isRGDisabled) {
      setTimeout(() => {
        dialogService.openDialog(dialogService.ids.bonusSuppresionError, BonusSuppressionErrorDialogComponent, true);
      }, 3000);
      router.navigate([bonusSuppRedirUrl]);
    }
    return isRGDisabled;
  }

  /**
   * Subscribes to CMS config and fetches the URL
   */
  function getRedirectionURL() {
    let homeUrl:string;
    inject(CmsService).getSystemConfig()
      .subscribe((config: ISystemConfig) => {
         homeUrl = config.BonusSupErrorMsg ? config.BonusSupErrorMsg.url : rgyellow.HOME_URL;
      });
      return homeUrl;
  }
