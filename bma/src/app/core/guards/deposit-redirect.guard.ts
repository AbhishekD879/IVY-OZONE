import { inject } from '@angular/core';
import { CanActivateFn } from '@angular/router';
import { CashierService } from '@frontend/vanilla/core';

export const DepositRedirectGuard: CanActivateFn = () => {
  inject(CashierService).goToCashierDeposit({});
  return false;
}
