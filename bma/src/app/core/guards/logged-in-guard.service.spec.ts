import { TestBed } from '@angular/core/testing';
import { LoggedInGuard } from './logged-in-guard.service';
import { UserService } from '@core/services/user/user.service';
import { Router } from '@angular/router';

describe('LoggedInGuard', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        {
          provide: UserService,
          useValue: { loginPending: true, status: true },
        },
        {
          provide: Router,
          useValue: { navigate: () => true },
        }
      ],
    });
  })
  it('should call', () => {
    const guard = TestBed.runInInjectionContext(() => LoggedInGuard({ routeConfig: { data: { feature: 'retailFeatureKey' } } } as any, {} as any) as any) as any;
    expect(guard).toBeTruthy();
  })

  it('should call', () => {
    TestBed.overrideProvider(UserService, { useValue: { loginPending: false, status: false } });
    const guard = TestBed.runInInjectionContext(() => LoggedInGuard({ routeConfig: { data: { feature: 'retailFeatureKey' } } } as any, {} as any) as any) as any;
    expect(guard).toBeFalsy();
  })
});
