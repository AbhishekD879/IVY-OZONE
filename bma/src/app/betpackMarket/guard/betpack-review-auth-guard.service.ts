import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';
import { CmsService } from '@app/core/services/cms/cms.service';
import { UserService } from '@app/core/services/user/user.service';


export const BetPackReviewAuthGuard:CanActivateFn = () =>{
    const router = inject(Router);
    if (inject(CmsService).systemConfiguration['BetPack']?.enableBetPack) {
        if (inject(UserService).status) {
            return true;
        } else {
            router.navigate(['/promotions']);
            return false;
        }
    } else {
        router.navigate(['/']);
        return false;
    }
}
