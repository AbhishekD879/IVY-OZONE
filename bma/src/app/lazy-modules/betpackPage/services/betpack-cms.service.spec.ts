import { fakeAsync, tick, flush } from '@angular/core/testing';
import { of as observableOf, of } from 'rxjs';
import { BetpackCmsService } from "./betpack-cms.service";

describe('BetpackCmsService', () => {
    let service: BetpackCmsService;
    let bppService, http, pubSubService, freeBetsService, cmsService, kycStatusService;

    beforeEach(() => {
        bppService = {
            send: jasmine.createSpy('send').and.returnValue(of({}))
        };
        http = {
            get: jasmine.createSpy().and.returnValue(observableOf({body: {}})),
        };
        pubSubService = {
            subscribe: jasmine.createSpy('subscribe').and.callFake((arg0, arg2, fn) => fn()),
            publish: jasmine.createSpy('publish').and.returnValue(of({})),
            API: { SESSION_LOGIN: 'SESSION_LOGIN' }
        } as any;
        freeBetsService = {
            getFreeBets: jasmine.createSpy('getFreeBets').and.returnValue(of({})),
        } as any;
        cmsService = {
            getSystemConfig: jasmine.createSpy('getSystemConfig').and.returnValue(of({ BetPack: { enableBetPack: true } })),
        } as any;
        kycStatusService = {
            kycStatus :{
                subscribe: jasmine.createSpy('subscribe').and.returnValue(of({kycVerified: true, verificationStatus: true}))
            }
        };

        service = new BetpackCmsService(
            bppService,
            http,
            pubSubService,
            kycStatusService
        );
    });

    describe('constructor', () => {
        it('should invoke in case of invalid kyc status', fakeAsync(() => {
            kycStatusService.kycStatus.subscribe = jasmine.createSpy('subscribe').and.callFake((fn) => fn(null));
            service = new BetpackCmsService(
                bppService,
                http,
                pubSubService,
                kycStatusService
            );
            expect(service.kycVerified).toBeTruthy();
            flush();
        }));

        it('should invoke in case of valid kyc status', fakeAsync(() => {
            kycStatusService.kycStatus.subscribe = jasmine.createSpy('subscribe').and.callFake((fn) => fn({kycVerified: true, verificationStatus: true}));
            service = new BetpackCmsService(
                bppService,
                http,
                pubSubService,
                kycStatusService
            );
            expect(service.kycVerified).toBeTruthy();
            flush();
        }));
    });

    describe('getCmsBetPackLabels', () => {
        it('getCmsBetPackLabels should be called in case of background image exists', fakeAsync(() => {
            const data = {
                backgroundImage: {
                    path: 'test',
                    filename: 'betpack.png'
                }
            };
            service['getBetPackLabels'] = jasmine.createSpy('getBetPackLabels').and.returnValue(of(data));
            service['getCmsBetPackLabels']();
            tick(1000);
            expect(service.betpackLabels).toBeTruthy();
        }));

        it('getCmsBetPackLabels should be called in case of no background image exists', fakeAsync(() => {
            service['getBetPackLabels'] = jasmine.createSpy('getBetPackLabels').and.returnValue(of({}));
            service['getCmsBetPackLabels']();
            tick(1000);
            expect(service.betpackLabels).toBeTruthy();
        }))
    });

    describe('@getData()', () => {
        it('should call getData() with params', () => {
            const url = 'test-link',
                options = { option: 'option' };

            service['getData'](url, options);
            expect(http.get).toHaveBeenCalled();
        });

        it('should call getData() without params', () => {
            const url = 'test-link';

            service['getData'](url);

            expect(http.get).toHaveBeenCalled();
        });
    });

    describe('Betpack Cms Calls', () => {
        it('should call getBetPackDetails()', () => {
            service.getBetPackDetails().subscribe();

            expect(http.get).toHaveBeenCalled();
        });

        it('should call getBetPackLabels()', () => {
            service.getBetPackLabels().subscribe();

            expect(http.get).toHaveBeenCalled();
        });

        it('should call getBetPackFilters()', () => {
            service.getBetPackFilters().subscribe();

            expect(http.get).toHaveBeenCalled();
        });

        it('should call getBetPackBanners()', () => {
            service.getBetPackBanners().subscribe();

            expect(http.get).toHaveBeenCalled();
        });

        it('should call getBetPackOnboarding()', () => {
            service.getBetPackOnboarding().subscribe();

            expect(http.get).toHaveBeenCalled();
        });
    })

    describe('getAccountLevelLimits', () => {
        it('getAccountLevelLimits should be called', () => {
            service.getAccountLevelLimits().subscribe();
            expect(bppService.send).toHaveBeenCalled();
        })
    })
});