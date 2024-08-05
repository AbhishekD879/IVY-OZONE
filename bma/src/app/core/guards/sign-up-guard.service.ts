import { inject } from '@angular/core';
import { CanActivateFn } from '@angular/router';
import { LoginNavigationService } from '@frontend/vanilla/core';

/**
 * Guard for /signup to open Vanilla registration
 */
export const SignUpRouteGuard: CanActivateFn = () => {
  inject(LoginNavigationService).goToRegistration();
  return false;
}