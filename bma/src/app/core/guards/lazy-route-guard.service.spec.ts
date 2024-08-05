import { TestBed } from '@angular/core/testing';
import { Router } from '@angular/router';
import { LazyRouteGuard } from '@core/guards/lazy-route-guard.service';

describe('LazyRouteGuard', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        {
          provide: Router,
          useValue: { navigate: () => true },
        }
      ],
    });
  })
  it('should call', () => {
    const guard = TestBed.runInInjectionContext(() => LazyRouteGuard({} as any, {} as any) as any) as any;
    expect(guard).toBeFalsy();
  })
});
