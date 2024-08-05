import { TestBed } from '@angular/core/testing';
import { NotFoundPageGuard } from '@core/guards/not-found-page-guard.service';
import { NavigationService } from '@core/services/navigation/navigation.service';

describe('NotFoundPageGuard', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        {
          provide: NavigationService,
          useValue: { handleHomeRedirect: () => true },
        },
      ],
    });
  })
  it('should call', () => {
    const guard = TestBed.runInInjectionContext(() => NotFoundPageGuard({} as any, { url: '/url' } as any) as any) as any;
    expect(guard).toBeFalsy();
  })
});
