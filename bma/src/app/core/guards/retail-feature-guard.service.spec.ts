
import { RetailFeatureGuard } from './retail-feature-guard.service';
import { of } from 'rxjs/internal/observable/of';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { TestBed } from '@angular/core/testing';
import { Router } from '@angular/router';

describe('SignUpRouteGuard', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        {
          provide: CmsService,
          useValue: { getSystemConfig: () => of({Connect: {retailFeatureKey: 'retailFeatureKey'}}), },
        },
        {
          provide: Router,
          useValue: { navigate: () => true },
        }
      ],
    });
  })
  it('should call' , ()=> {
    const guard = TestBed.runInInjectionContext(() => RetailFeatureGuard({routeConfig: {data: {feature: 'retailFeatureKey'}}} as any ,{} as any) as any) as any;
    let retVal;
    guard.subscribe(el => retVal = el)
    expect(retVal).toBeTruthy();
  })

  it('should call' , ()=> {
    TestBed.overrideProvider(CmsService, {useValue:  { getSystemConfig: () => of({Connect: {retailFeatureKey: 'retailFeatureKey'}})}});
    const guard = TestBed.runInInjectionContext(() => RetailFeatureGuard({routeConfig: {data: {feature: 'otherretailFeatureKey'}}} as any ,{} as any) as any) as any;
    let retVal;
    guard.subscribe(el => retVal = el)
    expect(retVal).not.toBeTruthy();
  })
});