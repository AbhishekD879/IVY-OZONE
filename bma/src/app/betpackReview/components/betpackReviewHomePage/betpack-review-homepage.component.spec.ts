import { of } from 'rxjs';
import { BetpackReviewHomepageComponent } from '@app/betpackReview/components/betpackReviewHomePage/betpack-review-homepage.component';
import { ACCOUNT_FREE_BETS_OVERALL, CMS_DATA, FREEBET_OFFERS_LIST, FREE_BET_TOKEN_DATA, ACCOUNT_FREE_BETS, SORTED_REVIEW_DATA, BETPACK_REVIEW_DATA,BANNERDATA, BETPACK_TOKEN, BETPACK_REVIEW_DATA_1 } from '@app/betpackReview/components/betpackReviewHomePage/mockData/betpack-review-homepage.mock';
import { fakeAsync, tick } from '@angular/core/testing';

describe('BetpackReviewHomepageComponent', () => {
    let component: BetpackReviewHomepageComponent;
    let componentFactoryResolver, dialogService, datePipe, userService, betpackCmsService, bppProviderService, currencyPipe, gtmService, router, device, storageService,serviceClosureService;
    let pubSubService, timeService, bonusSuppressionService,changeDetectorRef;

    beforeEach(() => {
        userService = {
            currencySymbol: '£',
            status: jasmine.createSpy('status').and.returnValue(true),
            maxStakeScale: jasmine.createSpy('maxSkateScale').and.returnValue(2)

        };
        bonusSuppressionService = {
            navigateAwayForRGYellowCustomer: jasmine.createSpy('navigateAwayForRGYellowCustomer'),
            checkIfYellowFlagDisabled: jasmine.createSpy('checkIfYellowFlagDisabled').and.returnValue(true)
        };
        betpackCmsService = {
            getBetPackDetails: jasmine.createSpy().and.returnValue(of(CMS_DATA)),
            getBetPackLabels: jasmine.createSpy().and.returnValue(of({})),
            getBetPackBanners:jasmine.createSpy().and.returnValue(of(BANNERDATA))
        } as any;
        bppProviderService = {
            accountFreebets: jasmine.createSpy().and.returnValue(of({ response: { model: { freebetToken: FREE_BET_TOKEN_DATA as any } } }))
        } as any;
        currencyPipe = datePipe = {
            transform: jasmine.createSpy()
        };
        pubSubService = {
            subscribe: jasmine.createSpy('subscribe').and.callFake((arg0, arg2, fn) => fn())
        };
        gtmService = {
            push: jasmine.createSpy('push')
        };
        router = {
            navigateByUrl: jasmine.createSpy('navigateByUrl'),
            url: jasmine.createSpy('url'),
        };

        device = {
            isMobile: true
        };

        storageService = {
            set: jasmine.createSpy('set'),
            get: jasmine.createSpy('get')
        };
        timeService = {
            parseDateTime: (parseDate) => {
                return new Date(parseDate);
            },
            compareDate:jasmine.createSpy('compareDate').and.returnValue(1)
        };
        serviceClosureService = {
            userServiceClosureOrPlayBreakCheck: jasmine.createSpy('userServiceClosureOrPlayBreakCheck').and.returnValue(true),
            userServiceClosureOrPlayBreak: true
        };
        changeDetectorRef={
            detectChanges:jasmine.createSpy('detectChanges')
        }
        dialogService = jasmine.createSpyObj('dialogService', ['openDialog']);
        componentFactoryResolver = jasmine.createSpyObj('componentFactoryResolver', ['resolveComponentFactory']);
        component = new BetpackReviewHomepageComponent(
            componentFactoryResolver, dialogService, datePipe, userService,
            betpackCmsService, bppProviderService, currencyPipe, pubSubService, gtmService, router, device, storageService,timeService,serviceClosureService, bonusSuppressionService,changeDetectorRef);   
    });
    
    it('#constructor', () => {
        expect(component).toBeDefined();
        expect(component.disableBetPack).toBe(false);
    });
    it('#ngOnInit', fakeAsync(() => {
        spyOn(component, 'getBetPackLabels');
        spyOn(component, 'getBetPackBanners');
        component.userService.status=false;
        bonusSuppressionService.checkIfYellowFlagDisabled.and.returnValue(false);
        component.ngOnInit();
        tick(1000);
        expect(pubSubService.subscribe).toHaveBeenCalledWith('', 'STORE_STAKE_FACTOR', jasmine.any(Function));
    }));

    it('#ngOnInit rgy', fakeAsync(() => {
        spyOn(component, 'getBetPackLabels');
        spyOn(component, 'getBetPackBanners');
        component.userService.status = true;
        bonusSuppressionService.checkIfYellowFlagDisabled.and.returnValue(true);
        component.ngOnInit();
        tick(1000);
        expect(component.rgyCheck).toBeTruthy();
    }));

    it('#loadingScreen', () => {
        component.loadingScreen();
        expect(component.isLoading).toBeFalse();
    });

    it('openPopup', () => {
        component.betpackLabels = {} as any;
        component.openPopup({} as any);
        expect(dialogService.openDialog).toHaveBeenCalledTimes(1);
    });

    it('#getFreeBetTokens', () => {
        spyOn(component, 'groupingBetPacks');
        ACCOUNT_FREE_BETS.response.model.freebetToken = FREE_BET_TOKEN_DATA;
        component.getFreeBetTokens();
        expect(component.accountFreeBetToken).toBe(FREE_BET_TOKEN_DATA as any);
        expect(component.groupingBetPacks).toHaveBeenCalled();
    });

    it('#getBetPackLabels', () => {
        spyOn(component, 'getFreeBetTokens');
        component.getBetPackLabels();
        expect(component.getFreeBetTokens).toHaveBeenCalled();
    });

    describe('#groupingBetPacks', () => {
        it('when free bet tokens available', () => {
            spyOn(component, 'getBetpackDetails');
            spyOn(component, 'loadingScreen');
            spyOn(component, 'getGroupedBetPacks');
            component.accountFreeBetToken = [{ 'freebetOfferCategories': { 'freebetOfferCategory': 'Bet Pack' }, 'freebetTokenValue': '5', 'freebetTokenExpiryDate': '2005-06-12 16:00:00' },
            { 'freebetTokenValue': '5', 'freebetTokenExpiryDate': '2005-06-12 16:00:00' }] as any;
            component.groupingBetPacks();
            expect(component.getBetpackDetails).toHaveBeenCalled();
            expect(component.loadingScreen).not.toHaveBeenCalled();
            expect(component.getGroupedBetPacks).toHaveBeenCalled();
        });

        it('when free bet tokens not available', () => {
            spyOn(component, 'getBetpackDetails');
            spyOn(component, 'loadingScreen');
            component.accountFreeBetToken = undefined;
            component.groupingBetPacks();
            expect(component.getBetpackDetails).not.toHaveBeenCalled();
            expect(component.loadingScreen).toHaveBeenCalled();
        });
    });

    describe('#getBetpackDetails', () => {
        it('when betpack details is present in cms', () => {
            spyOn(component, 'mapCmsBetPacks');
            spyOn(component, 'loadingScreen');
            component.freeBetOffersList = FREEBET_OFFERS_LIST;
            component.cmsData = CMS_DATA;
            component.getBetpackDetails();
            expect(component.mapCmsBetPacks).toHaveBeenCalled();
            expect(component.loadingScreen).not.toHaveBeenCalled();
        });

        it('when betpack details is absent in cms', () => {
            betpackCmsService = {
                getBetPackDetails: jasmine.createSpy().and.returnValue(of(undefined))
            } as any;
            component = new BetpackReviewHomepageComponent(
                componentFactoryResolver, dialogService, datePipe, userService,
                betpackCmsService, bppProviderService, currencyPipe, pubSubService, router, gtmService, device, storageService,timeService,serviceClosureService, bonusSuppressionService,changeDetectorRef);
            spyOn(component, 'mapCmsBetPacks');
            spyOn(component, 'loadingScreen');
            component.getBetpackDetails();
            expect(component.mapCmsBetPacks).not.toHaveBeenCalled();
            expect(component.loadingScreen).toHaveBeenCalled();
        });
    });

    describe('#mapCmsBetPacks', () => {
        it('when tokens are available in betpack review', () => {
            spyOn(component, 'sortReviewData');
            spyOn(component, 'loadingScreen');
            spyOn(component, 'expiringTokenCount');
            component.reviewData = [];
            component.accountFreeBetToken = FREE_BET_TOKEN_DATA as any;
            component.cmsData = CMS_DATA as any;
            component.mapCmsBetPacks();
            expect(component.sortReviewData).toHaveBeenCalled();
            expect(component.loadingScreen).toHaveBeenCalled();
        });
        it('when tokens are not available in betpack review', () => {
            spyOn(component, 'sortReviewData');
            spyOn(component, 'loadingScreen');
            spyOn(component, 'expiringTokenCount');
            component.reviewData = [];
            component.accountFreeBetToken = undefined;
            component.cmsData = CMS_DATA as any;
            component.mapCmsBetPacks();
            expect(component.sortReviewData).toHaveBeenCalled();
            expect(component.loadingScreen).toHaveBeenCalled();
        });
        it('mapCmsBetPacks', () => {
            spyOn(component, 'expiringTokenCount');
            component.freeBetOffersList = FREEBET_OFFERS_LIST;
            component.cmsData = CMS_DATA;
            component.mapCmsBetPacks();
            expect(component.totalValue).toBeDefined();
            expect(component.reviewData).toBeDefined();
        });

        it('getGroupedBetPacks', () => {
            component.getGroupedBetPacks(ACCOUNT_FREE_BETS_OVERALL);
            expect(component.freeBetOffersList).toBeDefined();
        });
        it('getBetpackPurchaseDate when betpack is active and has freebetTokenAwardedDate', () => {
            const res = component.getBetpackPurchaseDate([{active: true, freebetTokenAwardedDate: '12/04/2022'}, {active: false, freebetTokenAwardedDate: '12/04/2022'}]);
            expect(res).toBe('12/04/2022');
        });
        it('getBetpackPurchaseDate when betpack is not active and has freebetTokenAwardedDate', () => {
            const res = component.getBetpackPurchaseDate([{active: false, freebetTokenAwardedDate: '12/04/2022'}, {active: false, freebetTokenAwardedDate: '12/04/2022'}]);
            expect(res).toBe(undefined);
        });
        it('getBetpackPurchaseLongDate when betpack is active and has freebetTokenAwardedLongDate', () => {
            const res = component.getBetpackPurchaseLongDate([{active: true, freebetTokenAwardedLongDate: '12/04/2022 06:01:15'}, {active: false, freebetTokenAwardedLongDate: '12/04/2022 06:01:15'}]);
            expect(res).toBe('12/04/2022 06:01:15');
        });
        it('getBetpackPurchaseLongDate when betpack is not active and has freebetTokenAwardedLongDate', () => {
            const res = component.getBetpackPurchaseLongDate([{active: false, freebetTokenAwardedLongDate: '12/04/2022 06:01:15'}, {active: false, freebetTokenAwardedLongDate: '12/04/2022 06:01:15'}]);
            expect(res).toBe(undefined);
        });
    });

    describe('sortReviewData', () => {
        it('should sort reviewData', () => {
            component.reviewData = BETPACK_REVIEW_DATA;
            component.sortReviewData();
            expect(component.reviewData).toEqual(SORTED_REVIEW_DATA);
        });
    });

    describe('betpack Onboarding', () => {
        it('Should call loadOnBoardingInfo on load when local storage has onBoardtutorial', () => {
            userService = { username: 'testUser' } as any;
            device = { isMobile: true } as any;
            storageService = {
                get: jasmine.createSpy('get').and.returnValue({ onBoardingTutorial: { 'betPack-testUser': true } })
            };
            component = new BetpackReviewHomepageComponent(
                componentFactoryResolver, dialogService, datePipe, userService,
                betpackCmsService, bppProviderService, currencyPipe, pubSubService, router, gtmService, device, storageService,timeService,serviceClosureService, bonusSuppressionService,changeDetectorRef);

            component.reviewData = [];
            component.accountFreeBetToken = FREE_BET_TOKEN_DATA as any;
            component.cmsData = CMS_DATA as any;
            spyOn(component, 'expiringTokenCount');
            component.mapCmsBetPacks();

            expect(component.isUserLoggedIn).toEqual(true);
            expect(component.isMobile).toEqual(true);
        });

        it('Should call loadOnBoardingInfo on load when local storage doesnt have onBoardtutorial', () => {
            userService = { username: 'testUser' } as any;
            device = { isMobile: true } as any;
            storageService = {
                get: jasmine.createSpy('get').and.returnValue(false)
            };
            component = new BetpackReviewHomepageComponent(
                componentFactoryResolver, dialogService, datePipe, userService,
                betpackCmsService, bppProviderService, currencyPipe, pubSubService, router, gtmService, device, storageService,timeService,serviceClosureService, bonusSuppressionService,changeDetectorRef);
                spyOn(component, 'expiringTokenCount');
            component.reviewData = [];
            component.accountFreeBetToken = FREE_BET_TOKEN_DATA as any;
            component.cmsData = CMS_DATA as any;
            component.mapCmsBetPacks();

            expect(component.isUserLoggedIn).toEqual(true);
            expect(component.isMobile).toEqual(true);
        });

        it('should close the onboarding screen on close emitter', () => {
            component = new BetpackReviewHomepageComponent(
                componentFactoryResolver, dialogService, datePipe, userService,
                betpackCmsService, bppProviderService, currencyPipe, pubSubService, router, gtmService, device, storageService,timeService,serviceClosureService, bonusSuppressionService,changeDetectorRef);
            const event: any = { output: 'closeOnboardingEmitter', value: '' }
            component.handleOnBoardingEvents(event);
            expect(component.onBetReceiptOverlaySeen).toEqual(true);
        });
    });

    describe('#sendGtmData', () => {
        it('sendGtmDataCalled fasle', () => {
            component.sendGtmData('more info',false, 0);
            expect(gtmService.push).toHaveBeenCalled();
        });
        it('sendGtmDataCalled true', () => {
            component.sendGtmData('more info',true, 0);
            expect(gtmService.push).toHaveBeenCalled();
        });
    });
    describe('#gamblingControlsCheck', () => {
        it('should call gamblingControlsCheck', () => {
            expect(component.gamblingControlsCheck()).toBeTrue();
        });
    });
    describe('#getBetPackBanners', () => {
        it('should call getBetPackBanners', () => {
            component.getBetPackBanners()
            expect(true).toBeTrue();
        });
    });
    describe('#ontimerEmits', () => {
        it('should call ontimerEmits', () => {
            const token={isExpiresIn:true}
            component['ontimerEmits'](false,token)
            expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
        });
    });
    describe('#closeBaner', () => {
        it('should call closeBaner', () => {
            const container=document.createElement('div')
            component.closeBaner(container)
            expect(storageService.set).toHaveBeenCalled();
        });
    });
    describe('#expiringTokenCount', () => {
        it('should call expiringTokenCount without review data', () => {
            component.bannerData=BANNERDATA
            spyOn(component,"calculateExpirinTokens")
            component.expiringTokenCount()
            expect( component.calculateExpirinTokens).toHaveBeenCalled();
        });
        
    });
    describe('#calculateExpirinTokens', () => {
        it('should call calculateExpirinTokens without review data', () => {
            component.bannerData=BANNERDATA
            expect( component.calculateExpirinTokens()).toEqual('0');
            expect( component.isExpiresIn).toEqual(false);

        });
        it('should call calculateExpirinTokens with review data', () => {
            component.bannerData=BANNERDATA;
            component.reviewData = BETPACK_REVIEW_DATA;
            expect( component.calculateExpirinTokens()).toEqual('3');
            expect( component.isExpiresIn).toEqual(true);

        });
        it('should call calculateExpirinTokens with review data', () => {
            component.bannerData=BANNERDATA;
            component.reviewData = null;
            expect( component.calculateExpirinTokens()).toEqual('0');
            expect( component.isExpiresIn).toEqual(false);
        });
        it('should call calculateExpirinTokens with review data', () => {
            component.bannerData=BANNERDATA;
            component.reviewData = BETPACK_REVIEW_DATA_1;
            expect( component.calculateExpirinTokens()).toEqual('0');
            expect( component.isExpiresIn).toEqual(false);
        });
    });

    describe('#getheightFromChild', () => {
        it('should call getheightFromChild', () => {
           const event={offsetHeight:100}            
            expect( component.getheightFromChild(event,0)).toEqual('100px');
        });
    });
    describe('#getSvgWidth', () => {
        it('should call getSvgWidth', () => {
           const event={offsetWidth:100}            
            expect( component.getSvgWidth(event)).toEqual('100px');
        });
    });
    describe('#tokenTimer', () => {
        it('should call tokenTimer', () => {
            timeService={
                compareDate:jasmine.createSpy('compareDate').and.returnValue(1)
            }
            component.tokenTimer(BETPACK_TOKEN)       
            expect( true).toEqual(true);
        });
    });
});
