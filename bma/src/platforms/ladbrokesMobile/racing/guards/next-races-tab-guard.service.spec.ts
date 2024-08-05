import { of } from 'rxjs';
import { NextRacesTabGuard } from '@ladbrokesMobile/racing/guards/next-races-tab-guard.service';
import { TestBed, fakeAsync, flush, tick } from '@angular/core/testing';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { Router } from '@angular/router';

describe('NextRacesTabGuard', () => {
    beforeEach(() => {
        TestBed.configureTestingModule({
            providers: [
                {
                    provide: CmsService,
                    useValue: { getSystemConfig: () => of({ NextRacesToggle: { nextRacesTabEnabled: true } }) },
                },
                {
                    provide: Router,
                    useValue: { navigate: () => true },
                }
            ],
        });
    })

    it('should call', fakeAsync(() => {
        const guard = TestBed.runInInjectionContext(() => NextRacesTabGuard({} as any, {} as any) as any) as any;
        tick();
        let retVal;
        guard.subscribe(el => retVal = el)
        flush();
        expect(retVal).toBeTruthy();
    }))
    it('should call', fakeAsync(() => {
        TestBed.overrideProvider(CmsService, { useValue: { getSystemConfig: () => of({ NextRacesToggle: { nextRacesTabEnabled: false } }) } });
        const guard = TestBed.runInInjectionContext(() => NextRacesTabGuard({} as any, {} as any) as any) as any;
        tick();
        let retVal;
        guard.subscribe(el => retVal = el)
        flush();
        expect(retVal).toBeFalsy();
    }))
});
