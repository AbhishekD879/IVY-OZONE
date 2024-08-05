import { TestBed } from '@angular/core/testing';
import { DepositRedirectGuard } from './deposit-redirect.guard';
import { CashierService } from '@frontend/vanilla/core';

describe('DepositRedirectGuard', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        {
          provide: CashierService,
          useValue: { goToCashierDeposit: () => true },
        }
      ],
    });
  })

  it('should call', () => {
    const guard = TestBed.runInInjectionContext(() => DepositRedirectGuard({} as any, {} as any) as any) as any;
    expect(guard).toBeFalsy();
  })
});
