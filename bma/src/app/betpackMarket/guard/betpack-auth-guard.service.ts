import { inject } from '@angular/core';
import {  CanActivateFn, Router } from '@angular/router';
import { CmsService } from '@app/core/services/cms/cms.service';

export const BetPackAuthGuard:CanActivateFn = () =>{
    if (!(inject(CmsService).systemConfiguration['BetPack']?.enableBetPack)) {
        inject(Router).navigate(['/']);
        return false;
    }
    return true;
}