import { of } from 'rxjs';
import { LuckyDipCMSService } from '@lazy-modules/luckyDip/services/luckyDip-cms.service';
import environment from '@environment/oxygenEnvConfig';

describe('@FreeRideCmsService', () => {

    let service: LuckyDipCMSService,
        httpClient;

    beforeEach(() => {
        httpClient = {
            get: jasmine.createSpy('get').and.returnValue(of(
                {
                    body: []
                }))
        };

        service = new LuckyDipCMSService(
            
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
            service.getLuckyDipCMSData().subscribe();
            expect(httpClient.get).toHaveBeenCalled();
            expect(httpClient.get).toHaveBeenCalledWith(
                `${environment.CMS_ENDPOINT}/${environment.brand}/luckydip`,
                { observe: 'response', params: {} }
            );
        });
    });

    describe('getLuckyDipCMSAnimationData', () => {
        it('getLuckyDipCMSAnimationData', () => {
            service.getLuckyDipCMSAnimationData({cmsConfig: {playerPageBoxImgPath: '{123-456-abc}'}}).subscribe();
            expect(httpClient.get).toHaveBeenCalled();
        });
    }); 
});