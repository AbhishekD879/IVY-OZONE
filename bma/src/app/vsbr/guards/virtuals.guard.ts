import { inject } from '@angular/core';
import { ActivatedRouteSnapshot, CanActivateFn, RouterStateSnapshot } from '@angular/router';
import { CmsService } from '@app/core/services/cms/cms.service';
import { ISystemConfig } from '@app/core/services/cms/models';
import { Router } from '@angular/router';
import { VirtualHubService } from '@app/vsbr/services/virtual-hub.service';

export const VirtualsGuard: CanActivateFn = (route: ActivatedRouteSnapshot, state: RouterStateSnapshot) => {
  const router = inject(Router);
  const cmsService = inject(CmsService);
  const virtualService = inject(VirtualHubService);

  let cmsVirtualSportsData: any;

  cmsService.getSystemConfig()
    .subscribe((config: ISystemConfig) => {
      if (config && config.VirtualHubHomePage && config.VirtualHubHomePage.enabled) {
        if(config.VirtualHubHomePage.headerBanner){
          virtualService.bannerInit();
        }
        if (config.VirtualHubHomePage.topSports || config.VirtualHubHomePage.otherSports) {
          cmsService.getVirtualSports().subscribe((cmsVirtdata) => {
            cmsVirtualSportsData = cmsVirtdata;
            virtualService.setOrUpdateCmsConfig({ cmsConfig: config, cmsVirtualSportsData: cmsVirtualSportsData });
          });
        } else if (!config.VirtualHubHomePage.topSports && !config.VirtualHubHomePage.otherSports && !config.VirtualHubHomePage.nextEvents
          && !config.VirtualHubHomePage.featureZone && !config.VirtualHubHomePage.headerBanner) {
          router.navigate(['virtual-sports/sports']);
        } else {
          virtualService.setOrUpdateCmsConfig({ cmsConfig: config, cmsVirtualSportsData: [] });
        }
      }
      else {
        router.navigate(['virtual-sports/sports']);
      }
    });
  return true;
}
