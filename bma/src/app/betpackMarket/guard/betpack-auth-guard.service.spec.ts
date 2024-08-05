import { TestBed } from '@angular/core/testing';
import { Router } from '@angular/router';
import { BetPackAuthGuard } from '@app/betpackMarket/guard/betpack-auth-guard.service';
import { CmsService } from '@app/core/services/cms/cms.service';

describe('BetPackAuthGuard', () => {
    beforeEach(() => {
        TestBed.configureTestingModule({
            providers: [
                {
                    provide: CmsService,
                    useValue: { systemConfiguration: { BetPack: { enableBetPack: true } } },
                },
                {
                    provide: Router,
                    useValue: { navigate: () => true },
                }
            ],
        });
    })
    it('should call betpack auth', () => {
        const guard = TestBed.runInInjectionContext(() => BetPackAuthGuard({} as any, {} as any) as any) as any;
        expect(guard).toBeTruthy();
    })

    it('should call betpack auth', () => {
        TestBed.overrideProvider(CmsService, { useValue: { systemConfiguration: { BetPack: { enableBetPack: false } } } });
        const guard = TestBed.runInInjectionContext(() => BetPackAuthGuard({} as any, {} as any) as any) as any;
        expect(guard).toBeFalsy();
    })

    it('should call betpack auth', () => {
        TestBed.overrideProvider(CmsService, { useValue: { systemConfiguration: { BetPack: undefined } } });
        const guard = TestBed.runInInjectionContext(() => BetPackAuthGuard({} as any, {} as any) as any) as any;
        expect(guard).toBeFalsy();
    })
});