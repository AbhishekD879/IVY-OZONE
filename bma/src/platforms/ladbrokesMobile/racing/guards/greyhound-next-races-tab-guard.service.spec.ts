import { of } from 'rxjs';
import { TestBed, fakeAsync, flush, tick } from '@angular/core/testing';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { Router } from '@angular/router';
import { GreyhoundNextRacesTabGuard } from './greyhound-next-races-tab-guard.service';

describe('GreyhoundNextRacesTabGuard', () => {
    beforeEach(() => {
        TestBed.configureTestingModule({
            providers: [
                {
                    provide: CmsService,
                    useValue: { getSystemConfig: () => of({ GreyhoundNextRacesToggle: { nextRacesTabEnabled: true } }) },
                },
                {
                    provide: Router,
                    useValue: { navigate: () => true },
                }
            ],
        });
    })

    it('should call with true', fakeAsync(() => {
        const guard = TestBed.runInInjectionContext(() => GreyhoundNextRacesTabGuard({} as any, {} as any) as any) as any;
        tick();
        let retVal;
        guard.subscribe(el => retVal = el)
        flush();
        expect(retVal).toBeTruthy();
    }))
    it('should call with false', fakeAsync(() => {
        TestBed.overrideProvider(CmsService, { useValue: { getSystemConfig: () => of({ GreyhoundNextRacesToggle: { nextRacesTabEnabled: false } }) } });
        const guard = TestBed.runInInjectionContext(() => GreyhoundNextRacesTabGuard({} as any, {} as any) as any) as any;
        tick();
        let retVal;
        guard.subscribe(el => retVal = el)
        flush();
        expect(retVal).toBeFalsy();
    }))
});
