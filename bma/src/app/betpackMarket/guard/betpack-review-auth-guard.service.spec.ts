import { TestBed } from '@angular/core/testing';
import { Router } from '@angular/router';
import { BetPackReviewAuthGuard } from '@app/betpackMarket/guard/betpack-review-auth-guard.service';
import { CmsService } from '@app/core/services/cms/cms.service';
import { UserService } from '@app/core/services/user/user.service';

describe('BetPackReviewAuthGuard', () => {
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
                },
                {
                    provide: UserService,
                    useValue: { status: true }
                }
            ],
        });
    })
    it('should call betpack review 1', () => {
        const guard = TestBed.runInInjectionContext(() => BetPackReviewAuthGuard({} as any, {} as any) as any) as any;
        expect(guard).toBeTruthy();
    })

    it('should call betpack review 2', () => {
        TestBed.overrideProvider(UserService, { useValue: { status: false } });
        const guard = TestBed.runInInjectionContext(() => BetPackReviewAuthGuard({} as any, {} as any) as any) as any;
        expect(guard).toBeFalsy();
    })

    it('should call betpack review 3', () => {
        TestBed.overrideProvider(CmsService, { useValue: { systemConfiguration: { BetPack: { enableBetPack: false}}}});
        const guard = TestBed.runInInjectionContext(() => BetPackReviewAuthGuard({} as any, {} as any) as any) as any;
        expect(guard).toBeFalsy();
    })

    it('should call betpack review 3', () => {
        TestBed.overrideProvider(CmsService, { useValue: { systemConfiguration: { BetPack: undefined}}});
        const guard = TestBed.runInInjectionContext(() => BetPackReviewAuthGuard({} as any, {} as any) as any) as any;
        expect(guard).toBeFalsy();
    })
});