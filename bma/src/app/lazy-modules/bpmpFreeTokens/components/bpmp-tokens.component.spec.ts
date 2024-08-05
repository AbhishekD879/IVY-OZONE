import { BpmpTokensProviderComponent } from '@lazy-modules/bpmpFreeTokens/components/bpmp-tokens.component';
import { of, throwError } from 'rxjs';
import {
    cmsServiceBetPackData,
    betpackCmsServiceBetPackDetailsData,
    freeBetsServiceFreeBetsData,
    cmsTokenDataEqualsUserTokenData,
    availabletokenData,
    cmsTokenDataNotEqualsTouserTokenData,
    cmsBetPackIdNotEqualsUserOfferId,
    NofreebetOfferCategories,
    NobetPackOffer
} from '@lazy-modules/bpmpFreeTokens/mock-data/bpmp-tokens.mock-data';

describe('BpmpTokensProviderComponent', () => {
    let component: BpmpTokensProviderComponent;
    let cmsService, betpackCmsService, freeBetsService, datePipe, gtmService, router, userService, timeService, changeDetectorRef;
    beforeEach(() => {
        cmsService = {
            getSystemConfig: jasmine.createSpy('getSystemConfig').and.returnValue(of({
                BetPack: cmsServiceBetPackData
            }))
        };
        betpackCmsService = {
            getBetPackDetails: jasmine.createSpy('getBetPackDetails').and.returnValue(of(betpackCmsServiceBetPackDetailsData))
        };
        freeBetsService = {
            getFreeBetsData: jasmine.createSpy('getFreeBetsData').and.returnValue(freeBetsServiceFreeBetsData)
        };
        datePipe = {
            transform: jasmine.createSpy('transform').and.returnValue('string')
        };
        gtmService = {
            push: jasmine.createSpy('push')
        };
        router = {
            url: '/sports/football/matches',
            navigateByUrl: jasmine.createSpy('navigateByUrl'),
            routeReuseStrategy: {
                shouldReuseRoute: function () { }
            }
        }
        userService = {
            currencySymbol: '$'
        };
        timeService = {
            parseDateTime: (parseDate) => {
               return new Date(parseDate);
            }
        };
        changeDetectorRef = {
            detectChanges: jasmine.createSpy('detectChanges'),
        };
        component = new BpmpTokensProviderComponent(
            cmsService, betpackCmsService, freeBetsService, datePipe, gtmService, router, userService, timeService, changeDetectorRef
        );
        spyOn(component, 'pushGTMdata').and.callThrough();
    });

    it('constructor', () => {
        expect(component).toBeTruthy();
    });

    it('ngOnInit when cms betpack token data equals user account token data', () => {
        component.ngOnInit();
        expect(component.viewAllTokenLink).toEqual('/betbundle-market');
        expect(component.viewAllTokenLabel).toEqual('View All Tokens');
        expect(component.isLoading).toBeFalse();
        expect(component.toShowList).toBeTrue();
        expect(component.pushGTMdata).toHaveBeenCalledWith('render');
        expect(gtmService.push).toHaveBeenCalledWith('trackEvent', {
            event: 'trackEvent',
            eventAction: 'bet receipt',
            eventCategory: 'bet bundles marketplace',
            eventLabel: 'render'
        });
    });

    it('ngOnInit when cms betpack token data equals user account token data with token title starting number', () => {

        betpackCmsService.getBetPackDetails.and.returnValue(of(cmsTokenDataEqualsUserTokenData));
        component.ngOnInit();
        expect(component.isLoading).toBeFalse();
        expect(component.toShowList).toBeTrue();
        expect(component.pushGTMdata).toHaveBeenCalledWith('render');
        expect(gtmService.push).toHaveBeenCalledWith('trackEvent', {
            event: 'trackEvent',
            eventAction: 'bet receipt',
            eventCategory: 'bet bundles marketplace',
            eventLabel: 'render'
        });
        expect(component.availabletokenData).toEqual(availabletokenData)
    });

    it('ngOnInit when cms betpack token id not equals user account token id', () => {
        freeBetsService.getFreeBetsData.and.returnValue(cmsTokenDataNotEqualsTouserTokenData);
        component.ngOnInit();
        expect(component.isLoading).toBeFalse();
        expect(component.toShowList).toBeFalse();
        expect(component.pushGTMdata).not.toHaveBeenCalled();
        expect(gtmService.push).not.toHaveBeenCalled();
    });

    it('ngOnInit when cms betpack id not equals user account offer id', () => {
        freeBetsService.getFreeBetsData.and.returnValue(cmsBetPackIdNotEqualsUserOfferId);
        component.ngOnInit();
        expect(component.isLoading).toBeFalse();
        expect(component.toShowList).toBeFalse();
        expect(component.pushGTMdata).not.toHaveBeenCalled();
        expect(gtmService.push).not.toHaveBeenCalled();
    });

    it('ngOnInit when user account offer do not have freebetOfferCategories', () => {
        freeBetsService.getFreeBetsData.and.returnValue(NofreebetOfferCategories);
        component.ngOnInit();
        expect(component.isLoading).toBeFalse();
        expect(component.toShowList).toBeFalse();
        expect(component.pushGTMdata).not.toHaveBeenCalled();
        expect(gtmService.push).not.toHaveBeenCalled();
    });

    it('ngOnInit when user account offer is not bet pack', () => {
        freeBetsService.getFreeBetsData.and.returnValue(NobetPackOffer);
        component.ngOnInit();
        expect(component.isLoading).toBeFalse();
        expect(component.toShowList).toBeFalse();
        expect(component.pushGTMdata).not.toHaveBeenCalled();
        expect(gtmService.push).not.toHaveBeenCalled();
    });

    it('ngOnInit error in cms service', () => {
        cmsService.getSystemConfig.and.returnValue(throwError({}));
        component.ngOnInit();
        expect(component.isLoading).toBeFalse();
        expect(component.toShowList).toBeFalse();
        expect(component.pushGTMdata).not.toHaveBeenCalled();
        expect(gtmService.push).not.toHaveBeenCalled();
    });

    it('ngOnInit error in bet pack cms service', () => {
        betpackCmsService.getBetPackDetails.and.returnValue(throwError({}));
        component.ngOnInit();
        expect(component.isLoading).toBeFalse();
        expect(component.toShowList).toBeFalse();
        expect(component.pushGTMdata).not.toHaveBeenCalled();
        expect(gtmService.push).not.toHaveBeenCalled();
    });

    it('when user clicks on View all bet token button', () => {
        component.pushGTMdata('view all bet tokens');
        expect(component.pushGTMdata).toHaveBeenCalledWith('view all bet tokens');
        expect(gtmService.push).toHaveBeenCalledWith('trackEvent', {
            event: 'trackEvent',
            eventAction: 'bet receipt',
            eventCategory: 'bet bundles marketplace',
            eventLabel: 'view all bet tokens'
        });
    });

    it('when user clicks on use now button', () => {
        component.pushGTMdata('use now');
        expect(component.pushGTMdata).toHaveBeenCalledWith('use now');
        expect(gtmService.push).toHaveBeenCalledWith('trackEvent', {
            event: 'trackEvent',
            eventAction: 'bet receipt',
            eventCategory: 'bet bundles marketplace',
            eventLabel: 'use now'
        });
    });

    it('when user clicks on use now button with path /sports/football/matches', () => {
        component.pushGTMdata('use now', '/sports/football/matches');
        component[router.routeReuseStrategy.shouldReuseRoute()];
        expect(component.pushGTMdata).toHaveBeenCalledWith('use now', '/sports/football/matches');
    });

    it('when user clicks on use now button with path sports/football/matches', () => {
        component.pushGTMdata('use now', 'sports/football/matches');
        component[router.routeReuseStrategy.shouldReuseRoute()];
        expect(component.pushGTMdata).toHaveBeenCalledWith('use now', 'sports/football/matches');
    });

    it('when user clicks on use now button with path sports/tennis/matches', () => {
        component.pushGTMdata('use now', 'sports/tennis/matches');
        expect(component.pushGTMdata).toHaveBeenCalledWith('use now', 'sports/tennis/matches');
    });
});