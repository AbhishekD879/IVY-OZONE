import { TestBed } from '@angular/core/testing';
import { LoggedOutGuard } from './logged-out-guard.service';
import { UserService } from '@core/services/user/user.service';
import { Router } from '@angular/router';

describe('LoggedOutGuard', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        {
          provide: UserService,
          useValue: { isSignUpPending: true, loginPending: true, status: true },
        },
        {
          provide: Router,
          useValue: { navigateByUrl: () => true },
        }
      ],
    });
  })
  it('should call', () => {
    // TestBed.overrideProvider(ModuleRibbonService, { useValue: { isPrivateMarketsTab: () => false }});
    const guard = TestBed.runInInjectionContext(() => LoggedOutGuard({} as any, {} as any) as any) as any;
    expect(guard).toBeFalsy();
  })

  it('should call', () => {
    TestBed.overrideProvider(UserService, { useValue: { isSignUpPending: true, loginPending: false, status: true } });
    const guard = TestBed.runInInjectionContext(() => LoggedOutGuard({} as any, {} as any) as any) as any;
    expect(guard).toBeTruthy();
  })
});
