import { inject } from "@angular/core";
import { CanActivateFn, Router } from '@angular/router';
import { UserService } from '@core/services/user/user.service';

export const LoggedInGuard :CanActivateFn = () => {

  const router = inject(Router);
  const user = inject(UserService);
  if (user.status || user.loginPending) {
    return true;
  }
  router.navigate(['/']);
  return false;
}
