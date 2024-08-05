import { of } from 'rxjs';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { FreeRideCMSService } from '@lazy-modules/freeRide/services/freeRide-cms.service';
import environment from '@environment/oxygenEnvConfig';

describe('@FreeRideCmsService', () => {

    let service: FreeRideCMSService,
        pubSubService,
        httpClient;

    beforeEach(() => {
        pubSubService = {
            publish: jasmine.createSpy('publish'),
            API: pubSubApi
        };
        httpClient = {
            get: jasmine.createSpy('get').and.returnValue(of(
                {
                    body: []
                }))
        };

        service = new FreeRideCMSService(
            pubSubService,
            httpClient
        );
    });

    afterEach(() => {
        service = null;
    });

    it('should create instance', () => {
        expect(service).toBeDefined();

    });

    it('should be created', () => {
        expect(service).toBeTruthy();
    });

    describe('getFreeRideSplashPage', () => {
        it('should get getFreeRideSplashPage', () => {
            let res;
            service.getFreeRideSplashPage().subscribe();
            expect(httpClient.get).toHaveBeenCalled();
            expect(httpClient.get).toHaveBeenCalledWith(
                `${environment.CMS_ENDPOINT}/${environment.brand}/freeride-splashpage`,
                { observe: 'response', params: {} }
            );
            expect(pubSubService.publish).toHaveBeenCalledWith(pubSubApi.FREE_RIDE_BET, true);
        });
    });
});