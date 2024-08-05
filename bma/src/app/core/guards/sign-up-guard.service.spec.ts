import { SignUpRouteGuard } from '@core/guards/sign-up-guard.service';
import { LoginNavigationService } from '@frontend/vanilla/core';
import { TestBed } from '@angular/core/testing';

describe('SignUpRouteGuard', () => {
  it('should call' , ()=> {
    TestBed.configureTestingModule({
      providers: [
        {
          provide: LoginNavigationService,
          useValue: { goToRegistration: () => false, },
        },
      ],
    });

    const guard = TestBed.runInInjectionContext(SignUpRouteGuard as any);
    expect(guard).toBeFalsy();
  })
});

