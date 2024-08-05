import { TestBed, fakeAsync, flush, tick } from '@angular/core/testing';

import { VirtualsGuard } from './virtuals.guard';
import { Router } from '@angular/router';
import { CmsService } from '@core/services/cms/cms.service';
import { of } from 'rxjs/internal/observable/of';
import { VirtualHubService } from '@app/vsbr/services/virtual-hub.service';

describe('VirtualsGuard', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        {
          provide: Router,
          useValue: { navigate: () => true },
        },
        {
          provide: CmsService,
          useValue: { getSystemConfig: () => of({VirtualHubHomePage: {enabled: true, headerBanner: true, otherSports: true}}),
          getVirtualSports: () =>  of('data')},
        },
        {
          provide: VirtualHubService,
          useValue: { bannerInit: () => true, setOrUpdateCmsConfig: ({}) => true },
        },
      ],
    });
  })

  it('should call virtual guard' , fakeAsync(()=> {
    const guard = TestBed.runInInjectionContext(() => VirtualsGuard({data: {moduleName: 'virtual'}} as any, {url:'/sports'} as any));
    tick();
    flush();
    expect(guard).toBeTruthy();
  }))

  it('should call virtual guard witho out config flags' , fakeAsync(()=> {
    TestBed.overrideProvider(CmsService, { useValue: { getSystemConfig: () => of({VirtualHubHomePage: {enabled: true}})}});
    const guard = TestBed.runInInjectionContext(() => VirtualsGuard({data: {moduleName: 'virtual'}} as any, {url:'/sports'} as any));
    tick();
    flush();
    expect(guard).toBeTruthy();
  }))

  it('should call virtual guard witho out config flags' , fakeAsync(()=> {
    TestBed.overrideProvider(CmsService, { useValue: { getSystemConfig: () => of({VirtualHubHomePage: {enabled: true, featureZone: true}})}});
    const guard = TestBed.runInInjectionContext(() => VirtualsGuard({data: {moduleName: 'virtual'}} as any, {url:'/sports'} as any));
    tick();
    flush();
    expect(guard).toBeTruthy();
  }))

  it('should call virtual guard witho out config flags' , fakeAsync(()=> {
    TestBed.overrideProvider(CmsService, { useValue: {getSystemConfig: () => of(null)}});
    const guard = TestBed.runInInjectionContext(() => VirtualsGuard({data: {moduleName: 'virtual'}} as any, {url:'/sports'} as any));
    tick();
    flush();
    expect(guard).toBeTruthy();
  }))
});