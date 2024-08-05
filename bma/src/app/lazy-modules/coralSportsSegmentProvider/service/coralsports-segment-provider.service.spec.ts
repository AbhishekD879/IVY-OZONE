import { pubSubApi } from '@app/core/services/communication/pubsub/pubsub-api.constant';
import { of, throwError } from 'rxjs';
import environment from '@environment/oxygenEnvConfig';
import { CoralSportsSegmentProviderService } from './coralsports-segment-provider.service';

describe('CoralSportsSegmentProviderService', () => {
    let service: CoralSportsSegmentProviderService,
        vanillaApiService,
        userService,
        pubsubService,
        storageService,
        deviceService,
        userInterfaceConfig;

    beforeEach(() => {
        storageService = {
            set: jasmine.createSpy('set'),
        };
        vanillaApiService = {
            get: jasmine.createSpy('get')
        };
        userService = {
            username: 'username'
        };
        pubsubService = {
            publish: jasmine.createSpy('publish'),
            API: pubSubApi
        },
        deviceService = {
            requestPlatform : 'mobile'
        };
        userInterfaceConfig = {
            cspSegmentExpiry: 1
        };
        service = new CoralSportsSegmentProviderService(
            vanillaApiService,
            pubsubService,
            storageService,
            userService,
            deviceService,
            userInterfaceConfig
        );
    });

    describe('getSegmentDetails', () => {
        it('when API return data', () => {
            const segmentGroup = [{ group: 'CSP_Hyd_Test_Madhu_LD_369' }];
            service['getCoralSportsSegment'] = jasmine.createSpy('getCoralSportsSegment').and.returnValue(of(segmentGroup));
            service.getSegmentDetails();
            expect(storageService.set).toHaveBeenCalledTimes(1);
        });
        it('when the request hits with desktop mode', () => {
            service['getCoralSportsSegment'] = jasmine.createSpy('getCoralSportsSegment');
            deviceService.requestPlatform = 'desktop';
            service.getSegmentDetails();
            expect(service.getCoralSportsSegment).not.toHaveBeenCalled();
        });
        it('when API return empty response data', () => {
            const segmentGroup = [];
            service['getCoralSportsSegment'] = jasmine.createSpy('getCoralSportsSegment').and.returnValue(of(segmentGroup));
            service.getSegmentDetails();
            expect(storageService.set).toHaveBeenCalledTimes(1);
        });
        it('when API return data', () => {
            const segmentGroup = [{ group: 'Hyd_Test_Madhu_LD_369' },{ group: 'CSP_Hyd_Test_Madhu_LD_369' }];
            service['getCoralSportsSegment'] = jasmine.createSpy('getCoralSportsSegment').and.returnValue(of(segmentGroup));
            service.getSegmentDetails();
            expect(storageService.set).toHaveBeenCalledTimes(1);
        });
        it('when API return data', () => {
            const segmentGroup = [{ group: 'Hyd_Test_Madhu_LD_369' },{ group: 'Hyd_Test_Madhu_LD_36' }];
            service['getCoralSportsSegment'] = jasmine.createSpy('getCoralSportsSegment').and.returnValue(of(segmentGroup));
            service.getSegmentDetails();
            expect(storageService.set).toHaveBeenCalledTimes(1);
        });
        it('when API throw error', () => {
            service['getCoralSportsSegment'] = jasmine.createSpy().and.returnValue(throwError({ error: 'Error message!' }));
            service.getSegmentDetails();
            expect(storageService.set).toHaveBeenCalledTimes(1);
        });
        it('when API return data with firsttime login true', () => {
            const segmentGroup = [{ group: 'CSP_Hyd_Test_Madhu_LD_369' }];
            userInterfaceConfig.cspSegmentExpiry = 0;
            service['getCoralSportsSegment'] = jasmine.createSpy('getCoralSportsSegment').and.returnValue(of(segmentGroup));
            service.getSegmentDetails(true);
            expect(storageService.set).toHaveBeenCalled();           
        });
        it('when API return data with firsttime login true with more expiry time', () => {
            const segmentGroup = [{ group: 'CSP_Hyd_Test_Madhu_LD_369' }];
            userInterfaceConfig.cspSegmentExpiry = 24;
            service['getCoralSportsSegment'] = jasmine.createSpy('getCoralSportsSegment').and.returnValue(of(segmentGroup));
            service.getSegmentDetails(true);
            expect(storageService.set).toHaveBeenCalled();           
        });
    });

    describe('getCoralSportsSegment', () => {
        it('calls CampaignData API', () => {
            const segmentGroup = [{ group: 'CSP_Hyd_Test_Madhu_LD_369' }];
            vanillaApiService.get.and.returnValue(segmentGroup);
            const response = service['getCoralSportsSegment']();
            expect(response[0].group).toEqual(segmentGroup[0].group);
        });
    });

    describe('getOtfUserStatusApi', () => {
        beforeEach(() => {
            service['userService'].username='';
            environment.ONE_TWO_FREE_API_ENDPOINT='https://otf-api.beta.ladbrokes.com/';       
        })
        it('should fetch data from api', () => {
            vanillaApiService.get.and.returnValue(of({ status: false }));
            service['userService'].bppToken = 'abjdjddkjddhjkjklkllk';
            service['getOtfUserStatusApi']().subscribe(); 
            expect(vanillaApiService.get).toHaveBeenCalled()
        })
    })
    describe('getOtfSegmentUserStatus', () => {
        it('getOtfSegmentUserStatus cspSegmentExpiry 24 ', () => {
            storageService.get= jasmine.createSpy('get').and.returnValue({ user: 'user1', segment: false });
            service['getOtfUserStatusApi']=jasmine.createSpy().and.returnValue(of({ status: false }));
            service.getOtfSegmentUserStatus();
            expect(service['getOtfUserStatusApi']).toHaveBeenCalled()
        })

        it('should test the error scenario ', () => {
            storageService.get= jasmine.createSpy('get').and.returnValue({ user: 'user1', segment: false });
            service['getOtfUserStatusApi']=jasmine.createSpy().and.returnValue(of({ status: null }));
            
            service.getOtfSegmentUserStatus();
            
            expect(storageService.get).not.toHaveBeenCalled();
        })
    })
});
