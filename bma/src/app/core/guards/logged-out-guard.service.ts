import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';
import { UserService } from '@core/services/user/user.service';

export const LoggedOutGuard: CanActivateFn = () => {
  const router = inject(Router);
  const userService = inject(UserService)
  if (!((!userService.status || userService.isSignUpPending) && !userService.loginPending)) {
    router.navigateByUrl('/');
    return false;
  }
  return true;
}

