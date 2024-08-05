
import { of as observableOf } from 'rxjs';
import { OddsBoostGuard } from './oddsboost-guard.service';
import { TestBed } from '@angular/core/testing';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { Router } from '@angular/router';

describe('OddsBoostGuard', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        {
          provide: CmsService,
          useValue: { getOddsBoost: () => observableOf({ enabled:true })},
        },
        {
          provide: Router,
          useValue: { navigateByUrl: () => true },
        }
      ],
    });
  })

  it('should call truthy', () => {
    const guard = TestBed.runInInjectionContext(() => OddsBoostGuard({ routeConfig: { data: { feature: 'retailFeatureKey' } } } as any, {} as any) as any) as any;
    let retVal;
    guard.subscribe(el => retVal = el)
    expect(retVal).toBeTruthy();
  })

  it('should call falsy', () => {
    TestBed.overrideProvider(CmsService, {useValue: { getOddsBoost: () => observableOf({ enabled:false })}});
    const guard = TestBed.runInInjectionContext(() => OddsBoostGuard({ routeConfig: { data: { feature: 'retailFeatureKey' } } } as any, {} as any) as any) as any;
    let retVal;
    guard.subscribe(el => retVal = el)
    expect(retVal).toBeFalsy();
  })
});
