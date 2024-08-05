import { of } from 'rxjs';
import { CashOutTabGuard } from '@core/guards/cashout-tab-guard.service';
import { TestBed, fakeAsync, tick } from '@angular/core/testing';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { Router } from '@angular/router';

describe('CashOutTabGuard', () => {

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        {
          provide: CmsService,
          useValue: { getSystemConfig: () => of({ CashOut: { isCashOutTabEnabled: true } }) },
        },
        {
          provide: Router,
          useValue: { navigateByUrl: () => true },
        },
      ],
    });
  })

  it('should call truthy', fakeAsync(() => {
    const guard = TestBed.runInInjectionContext(CashOutTabGuard as any) as any;
    let retVal;
    guard.subscribe(d => retVal = d)
    tick();
    expect(retVal).toBeTruthy();
  }));

  it('should call falsy', fakeAsync(() => {
    TestBed.overrideProvider(CmsService, { useValue: { getSystemConfig: () => of({ CashOut: { isCashOutTabEnabled: false } }) } });
    const guard = TestBed.runInInjectionContext(CashOutTabGuard as any) as any;
    let retVal;
    guard.subscribe(d => retVal = d)
    tick();
    expect(retVal).toBeFalsy();
  }));
});
