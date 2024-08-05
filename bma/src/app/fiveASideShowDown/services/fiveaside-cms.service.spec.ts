import { FiveASideCmsService } from './fiveaside-cms.service';
import { pubSubApi } from '@app/core/services/communication/pubsub/pubsub-api.constant';
import { of } from 'rxjs';
import environment from '@environment/oxygenEnvConfig';


describe('FiveASideCmsService', () => {
    let service: FiveASideCmsService,
        pubSubService,
        cmsToolsService,
        deviceService,
        httpClient,
        coreToolsService,
        fanzoneStorageService,
        casinoLinkService,
        nativeBridgeService,
        userService,
        segmentEventManagerService,
        segmentedCMSService,
        cmsInitConfigPromise;

    beforeEach(() => {
        pubSubService = {
            publish: jasmine.createSpy('publish'),
            subscribe: jasmine.createSpy('subscribe'),
            API: pubSubApi
        };

        cmsToolsService = {
            processResult: jasmine.createSpy('processResult').and.returnValue([])
        };

        deviceService = {
            strictViewType: 'mobile',
            requestPlatform: 'mobile'
        };

        httpClient = {
            get: jasmine.createSpy('get').and.returnValue(of(
                {
                    body: []
                }))
        };

        coreToolsService = {
            deepClone: jasmine.createSpy('deepClone')
        };

        fanzoneStorageService = {
            get: jasmine.createSpy('get')
        };

        casinoLinkService = {
            filterGamingLinkForIOSWrapper: jasmine.createSpy('filterGamingLinkForIOSWrapper')
        };

        nativeBridgeService = {
            isRemovingGamingEnabled: false
        };

        userService = {
            currencySymbol: '$'
        };
        segmentEventManagerService = {
            getSegmentDetails: jasmine.createSpy('getSegmentDetails')
        };
        segmentedCMSService = {
            getCmsInitData: jasmine.createSpy('getCmsInitData')
        };
        cmsInitConfigPromise = undefined;

        service = new FiveASideCmsService(
            pubSubService,
            cmsToolsService,
            deviceService,
            httpClient,
            coreToolsService,
            fanzoneStorageService,
            casinoLinkService,
            nativeBridgeService,
            userService,
            segmentEventManagerService,
            segmentedCMSService,
            cmsInitConfigPromise
        );
    });
    describe('#getWelcomeOverlay', () => {
        it('should handle success', () => {
            service.getWelcomeOverlay().subscribe();
            expect(httpClient.get).toHaveBeenCalled();
            expect(httpClient.get).toHaveBeenCalledWith(
                `${environment.CMS_ENDPOINT}/${environment.brand}/overlay`,
                { observe: 'response', params: {} }
            );
        });
    });

    describe('#getFAQs', () => {
        it('should handle success', () => {
            service.getFAQs().subscribe();
            expect(httpClient.get).toHaveBeenCalled();
            expect(httpClient.get).toHaveBeenCalledWith(
                `${environment.CMS_ENDPOINT}/${environment.brand}/faq`,
                { observe: 'response', params: {} }
            );
        });
    });

    describe('#getTermsAndConditions', () => {
        it('should handle success', () => {
            service.getTermsAndConditions().subscribe();
            expect(httpClient.get).toHaveBeenCalled();
            expect(httpClient.get).toHaveBeenCalledWith(
                `${environment.CMS_ENDPOINT}/${environment.brand}/termsandcondition`,
                { observe: 'response', params: {} }
            );
        });
    });
});
