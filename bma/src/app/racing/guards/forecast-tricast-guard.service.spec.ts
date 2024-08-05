import { of } from 'rxjs';
import { TestBed, fakeAsync, tick } from '@angular/core/testing';

import { ForecastTricastGuard } from '@racing/guards/forecast-tricast-guard.service';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { Router } from '@angular/router';

describe('#ForecastTricastGuardService', () => {
    beforeEach(() => {
        TestBed.configureTestingModule({
            providers: [
                {
                    provide: CmsService,
                    useValue: { getSystemConfig: () => of({ forecastTricastRacing: { enabled: true } }), },
                },
                {
                    provide: Router,
                    useValue: { navigate: () => true },
                }
            ],
        });
    })
    it('should call 1', fakeAsync(() => {
        // TestBed.overrideProvider(ModuleRibbonService, { useValue: { isPrivateMarketsTab: () => false } });
        const guard = TestBed.runInInjectionContext(() => ForecastTricastGuard({} as any, {} as any) as any) as any;
        let retVal;
        guard.subscribe(el => retVal = el)
        tick();
        expect(retVal).toBeTruthy();
    }))

    it('should call 2', fakeAsync(() => {
        TestBed.overrideProvider(CmsService, { useValue: {getSystemConfig: () => of({ forecastTricastRacing: { enabled: true}})}});
        const guard = TestBed.runInInjectionContext(() => ForecastTricastGuard({ paramMap: { get: () => { return 'forecast' } } } as any, {} as any) as any) as any;
        let retVal;
        guard.subscribe(el => retVal = el)
        tick();
        expect(retVal).toBeTruthy();
    }))

    it('should call 3', fakeAsync(() => {
        TestBed.overrideProvider(CmsService, { useValue: { getSystemConfig: () => of({ forecastTricastRacing: { enabled: false } }) } });
        const guard = TestBed.runInInjectionContext(() => ForecastTricastGuard({ paramMap: { get: () => { return 'forecast' } } } as any, {} as any) as any) as any;
        let retVal;
        guard.subscribe(el => retVal = el)
        tick();
        expect(retVal).toBeFalsy();
    }))
});
