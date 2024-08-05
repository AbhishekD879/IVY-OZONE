import { fakeAsync } from '@angular/core/testing';
import { BetpackBannerComponent } from '@app/betpackMarket/components/betpackBanner/betpack-banner.component';

describe('BetpackBannerComponent', () => {
    let component, domSanitizer, betpackCmsService, router, cmsService, gtmService,changeDetectorRef;
    beforeEach(() => {
        cmsService = {
            getSystemConfig: jasmine.createSpy('subscribe').and.returnValue({
                subscribe: jasmine.createSpy('subscribe').and.callFake((cb) => {
                    cb({
                        BetPack: {
                            enableBetPack: true
                        }
                    });
                })
            })
        };
        domSanitizer = {
            bypassSecurityTrustHtml: jasmine.createSpy('bypassSecurityTrustHtml').and.returnValue('<p>welcome msg</p>')
        };
        betpackCmsService = {
            getBetPackBanners: jasmine.createSpy('getBetPackBanners').and.returnValue({
                subscribe: jasmine.createSpy('subscribe').and.callFake((cb) => {
                    cb({
                        bannerImage: {
                            path: 'abc',
                            filename: '123'
                        },
                        welcomeMsg: 'welcome',
                        enabled: 'true',
                    });
                })
            })
        } as any;
        router = {
            navigateByUrl: jasmine.createSpy('navigateByUrl')
        } as any;
        gtmService = {
            push: jasmine.createSpy('push')
        };
        changeDetectorRef = {
            detectChanges: jasmine.createSpy('detectChanges'),
            detach: jasmine.createSpy('detach'),
          };
        component = new BetpackBannerComponent(router, domSanitizer, betpackCmsService, cmsService, gtmService,changeDetectorRef);
    });

    describe('ngOnInit', () => {
        it('ngOnInit be called without data', () => {
            betpackCmsService.getBetPackBanners = jasmine.createSpy('getBetPackBanners').and.returnValue({
                subscribe: jasmine.createSpy('subscribe').and.callFake((cb) => {
                    cb();
                })
            });
            component.ngOnInit();
            expect(component.welcomeMsg).toBeUndefined();
        });

        it('ngOnInit be called with data', () => {
            component.ngOnInit();
            expect(gtmService.push).toHaveBeenCalled();
            expect(component.welcomeMsg).not.toBeUndefined();
        });
    });

    describe('migrateToBPMP', () => {
        it('migrateToBPMP be called', fakeAsync(() => {
            component.migrateToBPMP();
            expect(router.navigateByUrl).toHaveBeenCalled();
        }));
    });

    describe('closeBanner', () => {
        it('closeBanner', () => {
            const event = '123';
            component.closeBanner();
            expect(component.enableBanner).toBeFalsy();
        });
    });
});
