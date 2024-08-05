import { inject } from '@angular/core';
import { ActivatedRouteSnapshot, CanActivateFn, Router, RouterStateSnapshot } from '@angular/router';
import { forkJoin} from 'rxjs';
import { map } from 'rxjs/operators';

import { CmsService } from '@app/core/services/cms/cms.service';
import { UserService } from '@app/core/services/user/user.service';
import { FanzoneStorageService } from '@app/core/services/fanzone/fanzone-storage.service';

import { ISystemConfig } from '@app/core/services/cms/models/system-config';
import { FanzoneDetails } from '@app/fanzone/models/fanzone.model';
import { fanzoneRoutePath, fanzone, FANZONE_CATEGORY_ID, fanzoneVacationPath } from '@app/fanzone/constants/fanzoneconstants';

export const FanzoneAuthGuard: CanActivateFn = async(route: ActivatedRouteSnapshot, state: RouterStateSnapshot) => {

    const router = inject(Router);
    const userService = inject(UserService);
    const cmsService = inject(CmsService);
    const { isConfigDisabled, isEnabled } = fanzoneConfigEnabled();

    let selectedTeamName :string = '';

    const url = state.url.split('/');
    const urlTeamName = url[url.length-2].replace(/%20/g,'');
    const fanzoneTeam = inject(FanzoneStorageService).get(fanzone);
    if(fanzoneTeam && fanzoneTeam.teamName) {
        selectedTeamName = fanzoneTeam.teamName.replace(/ /g,'');
    }
    if (isConfigDisabled && isUserLoggedIn(userService) && (state.url && state.url.indexOf(`${fanzoneVacationPath}`) !== -1)) {
        return true;
    } else if (isEnabled  && ((state.url && state.url.indexOf(`${fanzoneRoutePath}`) !== -1) || (isUserLoggedIn(userService)  && await getFanzoneTeam(fanzoneTeam, cmsService).then() && urlTeamName === selectedTeamName))) {
        return true;
    } else {
        router.navigate(['/']);
        return false;
    }

}

    /**
     * Method to check if fanzone configuration is enabled or not
     * @returns Object
     */
    function fanzoneConfigEnabled(): any {
        let isEnableFanzone:boolean = false;
        let isFanzoneConfigDisabled:boolean = false;

        const cmsService = inject(CmsService);
        forkJoin({ menuItems: cmsService.getMenuItems(), sysConfig: cmsService.getSystemConfig() }).subscribe((data) => {
            const fzMenuIndex = data.menuItems.findIndex(menu => menu.categoryId === FANZONE_CATEGORY_ID);
            isEnableFanzone = fzMenuIndex !== -1 && (!data.menuItems[fzMenuIndex].disabled || (data.menuItems[fzMenuIndex].disabled && data.menuItems[fzMenuIndex].fzDisabled))  && data.sysConfig.Fanzone && data.sysConfig.Fanzone.enabled;
            isFanzoneConfigDisabled = !data.sysConfig.Fanzone.enabled;
        });
        return { isEnabled : isEnableFanzone, isConfigDisabled : isFanzoneConfigDisabled }
    }

    /**
     * Returns username if user logged in
     * @returns - boolean
     */
    function isUserLoggedIn(userService: UserService): boolean {
        return userService.username;
    }


    /**
     * Method to get fanzone config is enablem and team is selected 
     * @returns - Observable<boolean>
     */
    async function getFanzoneTeam(fanzoneTeam, cmsService): Promise<boolean> {
        let selectedTeam: FanzoneDetails;

        return forkJoin(cmsService.getFanzone(), cmsService.getSystemConfig())
            .pipe(
                map(([fanzoneData, sysConfig]: [any, ISystemConfig]) => {
                    if(fanzoneTeam && fanzoneTeam.teamId) {
                        [selectedTeam] = fanzoneData.filter((selectedFanzone) => selectedFanzone.teamId === fanzoneTeam.teamId)
                        return selectedTeam.active;
                    } else {
                        return false;
                    }
                })).toPromise()
    }
