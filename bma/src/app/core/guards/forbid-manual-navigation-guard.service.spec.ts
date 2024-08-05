import { TestBed } from '@angular/core/testing';
import { Router } from '@angular/router';
import { ForbidManualNavigationGuard } from '@core/guards/forbid-manual-navigation-guard.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';

describe('ForbidManualNavigationGuard', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        {
          provide: WindowRefService,
          useValue: { document: {referrer : ''}}
        },
        {
          provide: Router,
          useValue: { navigate: () => true },
        }
      ],
    });
  })
  it('should call', () => {
    const guard = TestBed.runInInjectionContext(() => ForbidManualNavigationGuard({} as any, {} as any) as any) as any;
    expect(guard).toBeFalsy();
  })

  it('should call', () => {
    TestBed.overrideProvider(WindowRefService, {useValue: { document: {referrer : 'text'}}});
    const guard = TestBed.runInInjectionContext(() => ForbidManualNavigationGuard({} as any, {} as any) as any) as any;
    expect(guard).toBeTruthy();
  })
});
