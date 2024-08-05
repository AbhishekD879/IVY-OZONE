
import { map } from 'rxjs/operators';
import { inject } from "@angular/core";
import { IOddsBoostConfig } from '@core/services/cms/models/odds-boost-config.model';
import { CanActivateFn, Router } from '@angular/router';
import { CmsService } from '@coreModule/services/cms/cms.service';

export const OddsBoostGuard:CanActivateFn = () => {
  const router = inject(Router);
  return inject(CmsService).getOddsBoost().pipe(map((config:IOddsBoostConfig)=>{
    if(!config.enabled){
      router.navigateByUrl('/');
      return false;

    }
    return true;
  }))
}

