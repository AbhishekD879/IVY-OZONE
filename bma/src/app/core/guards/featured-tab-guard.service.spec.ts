import { FeaturedTabGuard } from './featured-tab-guard.service';
import { UserService } from '@core/services/user/user.service';
import { ModuleRibbonService } from '@core/services/moduleRibbon/module-ribbon.service';
import { Router } from '@angular/router';
import { TestBed } from '@angular/core/testing';

describe('FeaturedTabGuard', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        {
          provide: UserService,
          useValue: { status: true },
        },
        {
          provide: ModuleRibbonService,
          useValue: { isPrivateMarketsTab: () => true, privateMarketsUrl: '/privateMarketsUrl' },
        },
        {
          provide: Router,
          useValue: { navigateByUrl: () => true },
        }
      ],
    });
  })
  it('should call', () => {
    const guard = TestBed.runInInjectionContext(() => FeaturedTabGuard({} as any, {} as any) as any) as any;
    expect(guard).toBeFalsy();
  })

  it('should call', () => {
    TestBed.overrideProvider(ModuleRibbonService, { useValue: { isPrivateMarketsTab: () => false, privateMarketsUrl: '/privateMarketsUrl' } });
    TestBed.overrideProvider(UserService, { useValue: { status: false } });
    const guard = TestBed.runInInjectionContext(() => FeaturedTabGuard({} as any, {} as any) as any) as any;
    expect(guard).toBeTruthy();
  })
});
