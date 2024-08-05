import { inject } from '@angular/core';
import { Router, CanActivateFn } from '@angular/router';

/**
 * Guard for Lazy Loading Modules which defined in routing.module
 * Just keeps redirect to home page
 */
export const LazyRouteGuard: CanActivateFn = () => {
  const router = inject(Router);
  router.navigate(['/']);
  return false;
}