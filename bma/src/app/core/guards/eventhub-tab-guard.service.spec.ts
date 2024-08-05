import { of as observableOf } from 'rxjs';
import { EventhubTabGuard } from '@core/guards/eventhub-tab-guard.service';
import { TestBed, fakeAsync, tick } from '@angular/core/testing';
import { Router } from '@angular/router';
import { CmsService } from '@coreModule/services/cms/cms.service';

describe('EventhubTabGuard', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        {
          provide: CmsService,
          useValue: { getRibbonModule: () => observableOf({ getRibbonModule: [{hubIndex: 10},{hubIndex: 20}] })},
        },
        {
          provide: Router,
          useValue: { navigate: () => true },
        }
      ],
    });
  })
  it('should call 1', fakeAsync(() => {
    // TestBed.overrideProvider(ModuleRibbonService, { useValue: { isPrivateMarketsTab: () => false }});
    const guard = TestBed.runInInjectionContext(() => EventhubTabGuard({ params: { hubIndex: 10 } } as any, {} as any) as any) as any;
    let retVal;
    guard.subscribe(el => retVal = el)
    tick();
    // expect(retVal).toBeFalsy();
  }))

  it('should call 2', fakeAsync(() => {
    TestBed.overrideProvider(CmsService, { useValue: { getRibbonModule: () => observableOf({ getRibbonModule: [{hubIndex: 11, url: 'url'},{hubIndex: 20, url: 'url'}] })}});
    const guard = TestBed.runInInjectionContext(() => EventhubTabGuard({ params: { hubIndex: 10 } } as any, {} as any) as any) as any;
    tick();
    expect(guard).toBeTruthy();
  }))

  it('should call 3', fakeAsync(() => {
    TestBed.overrideProvider(CmsService, { useValue: { getRibbonModule: () => observableOf({ getRibbonModule: [{hubIndex: 11, url: 'url'},{hubIndex: 20, url: 'url'}] })}});
    const guard = TestBed.runInInjectionContext(() => EventhubTabGuard({ params: { hubIndex: 10 } } as any, {} as any) as any) as any;
    let retVal;
    guard.subscribe(el => retVal = el)
    tick();
  }))

  it('should call 4', fakeAsync(() => {
    TestBed.overrideProvider(CmsService, { useValue: { getRibbonModule: () => observableOf({ getRibbonModule: [{hubIndex: 11, url: 'url'},{hubIndex: 20, url: 'url'}] })}});
    const guard = TestBed.runInInjectionContext(() => EventhubTabGuard({ params: {} } as any, {} as any) as any) as any;
    let retVal;
    guard.subscribe(el => retVal = el)
    tick();
  }))
});
