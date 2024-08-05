import { SegmentEventManagerService } from './segment-event-manager.service';
import { pubSubApi } from '@app/core/services/communication/pubsub/pubsub-api.constant';

describe('SegmentEventManagerService', () => {
    let service: SegmentEventManagerService,
        pubSubService,
        routingState,
        coralSportsSegmentProviderService,
        segmentCacheManagerService,
        userService,
        storageService,
        deviceService;

    beforeEach(() => {
        pubSubService = {
            publish: jasmine.createSpy('publish'),
            subscribe: jasmine.createSpy('subscribe').and.callFake((fileName: string, method: string, callback: Function) => {
                callback();
            }),
            API: pubSubApi
        };
        userService = {
            username: 'username'
        };
        coralSportsSegmentProviderService = {
            getSegmentDetails: jasmine.createSpy('getSegmentDetails')
        };
        segmentCacheManagerService = {
            isCacheAvailable: jasmine.createSpy('isCacheAvailable').and.returnValue(true)
        };
        storageService = {
            get: jasmine.createSpy('get').and.returnValue({ 'segment': '' }),
            remove:jasmine.createSpy('remove')
        };
        routingState = {
            getCurrentUrl: jasmine.createSpy()
        };
        deviceService = {
            requestPlatform : 'mobile'
        };
        service = new SegmentEventManagerService(
            pubSubService,
            routingState,
            coralSportsSegmentProviderService,
            segmentCacheManagerService,
            storageService,
            userService,
            deviceService
        );
    });

    describe('SegmentEventManagerService', () => {
        it('should create instance', () => {
            spyOn(service, 'getSegmentDetails').and.callThrough();
            expect(service instanceof SegmentEventManagerService).toBeTruthy();
            expect(service).toBeDefined();
            expect(pubSubService.subscribe).toHaveBeenCalledTimes(3);
            pubSubService.subscribe = jasmine.createSpy('subscribe').and.callFake(
                (fileName: string, method: string, callback: Function) => {
                    if (method === pubSubService.API.SESSION_LOGIN) {
                        callback();
                        expect(service.getSegmentDetails).toHaveBeenCalled();
                    }
                });
        });
    });

    describe('subscriptionForMobile',()=>{
        it('should subscribe to only for mobile',()=>{
            service.subscriptionForMobile();
            expect(pubSubService.subscribe).toHaveBeenCalled();
        });
        it('publish should not call for Desktop',()=>{
            pubSubService = {
                publish: jasmine.createSpy('publish'),
                subscribe: jasmine.createSpy('subscribe').and.callFake((fileName: string, method: string, callback: Function) => {
                    callback();
                }),
                API: pubSubApi
            };
            deviceService.requestPlatform = jasmine.createSpy('requestPlatform').and.returnValue('desktop');
            service = new SegmentEventManagerService(
                pubSubService,
                routingState,
                coralSportsSegmentProviderService,
                segmentCacheManagerService,
                storageService,
                userService,
                deviceService
            );
            service.subscriptionForMobile();
            expect(pubSubService.publish).not.toHaveBeenCalled();
        });
    });

    describe('getSegmentDetails', () => {
        it('when segment data is expired', () => {
            segmentCacheManagerService.isCacheAvailable = jasmine.createSpy('isCacheAvailable').and.returnValue(false);
            service['chkIsLoggedInUserDiff'] = jasmine.createSpy('chkIsLoggedInUserDiff').and.returnValue(false);
            const result = service.getSegmentDetails();
            expect(coralSportsSegmentProviderService.getSegmentDetails).toHaveBeenCalled();
            expect(result).toEqual('');
        });
        it('when same user and segment data is expired', () => {
            segmentCacheManagerService.isCacheAvailable = jasmine.createSpy('isCacheAvailable').and.returnValue(false);
            storageService.get.and.returnValue({ 'user': 'username', 'segment': '', 'timestamp': Date.now() });
            const result = service.getSegmentDetails();
            expect(coralSportsSegmentProviderService.getSegmentDetails).toHaveBeenCalled();
            expect(result).toEqual('');
        });
        it('when there is no segment data and firstTimeLogin is true', () => {
            segmentCacheManagerService.isCacheAvailable = jasmine.createSpy('isCacheAvailable').and.returnValue(false);
            service['chkIsLoggedInUserDiff'] = jasmine.createSpy('chkIsLoggedInUserDiff').and.returnValue(true);
            const result = service.getSegmentDetails(true);
            expect(coralSportsSegmentProviderService.getSegmentDetails).toHaveBeenCalled();
            expect(result).toEqual('');
        });
        it('when there is segment data and firstTimeLogin is true', () => {
            storageService.get.and.returnValue({ 'segment': 'segment1' });
            service['chkIsLoggedInUserDiff'] = jasmine.createSpy('chkIsLoggedInUserDiff').and.returnValue(true);
            const result = service.getSegmentDetails(true);
            expect(coralSportsSegmentProviderService.getSegmentDetails).toHaveBeenCalled();
            expect(result).toEqual('');
        });
          it('when there is segment data and firstTimeLogin true and segment value is empty string', () => {
            storageService.get.and.returnValue({ 'segment': '' });
            pubSubService.publish = jasmine.createSpy('publish');
            service['chkIsLoggedInUserDiff'] = jasmine.createSpy('chkIsLoggedInUserDiff').and.returnValue(false);
            segmentCacheManagerService.isCacheAvailable = jasmine.createSpy('isCacheAvailable').and.returnValue(true);
            const result = service.getSegmentDetails(true);
            expect(pubSubService.publish).not.toHaveBeenCalled();
            expect(result).toEqual('');
        });
        it('when there is segment data and firstTimeLogin true and segment value is undefined', () => {
            storageService.get.and.returnValue({ 'segment': undefined });
            pubSubService.publish = jasmine.createSpy('publish');
            service['chkIsLoggedInUserDiff'] = jasmine.createSpy('chkIsLoggedInUserDiff').and.returnValue(false);
            segmentCacheManagerService.isCacheAvailable = jasmine.createSpy('isCacheAvailable').and.returnValue(true);
            const result = service.getSegmentDetails(true);
            expect(pubSubService.publish).not.toHaveBeenCalled();
            expect(result).toEqual('');
        });
        it('when there is segment data and firstTimeLogin true and segment value is null', () => {
            storageService.get.and.returnValue({ 'segment': null });
            pubSubService.publish = jasmine.createSpy('publish');
            service['chkIsLoggedInUserDiff'] = jasmine.createSpy('chkIsLoggedInUserDiff').and.returnValue(false);
            segmentCacheManagerService.isCacheAvailable = jasmine.createSpy('isCacheAvailable').and.returnValue(true);
            const result = service.getSegmentDetails(true);
            expect(pubSubService.publish).not.toHaveBeenCalled();
            expect(result).toEqual('');
        });
        it('when there is segment data and firstTimeLogin true and segment value is segmented value string', () => {
            storageService.get.and.returnValue({ 'segment': 'segment1' });
            pubSubService.publish = jasmine.createSpy('publish');
            service['chkIsLoggedInUserDiff'] = jasmine.createSpy('chkIsLoggedInUserDiff').and.returnValue(false);
            segmentCacheManagerService.isCacheAvailable = jasmine.createSpy('isCacheAvailable').and.returnValue(true);
            const result = service.getSegmentDetails(true);
            expect(pubSubService.publish).toHaveBeenCalled();
        });
        it('when there is segment data and firstTimeLogin is true', () => {
            segmentCacheManagerService.isCacheAvailable.and.returnValue(true);
            service['chkIsLoggedInUserDiff'] = jasmine.createSpy('chkIsLoggedInUserDiff').and.returnValue(false);
            const result = service.getSegmentDetails(true);
            expect(pubSubService.publish).toHaveBeenCalled();
            expect(result).toEqual('');
        });
        it('when there is segment data and firstTimeLogin is true', () => {
            segmentCacheManagerService.isCacheAvailable = jasmine.createSpy('isCacheAvailable').and.returnValue(false);
            spyOn(service as any, 'chkIsLoggedInUserDiff').and.returnValue(false);
            const result = service.getSegmentDetails(true);
            expect(coralSportsSegmentProviderService.getSegmentDetails).toHaveBeenCalled();
            expect(result).toEqual('');
        });
        it('when there is segment data and firstTimeLogin is false', () => {
            storageService.get.and.returnValue({ 'segment': 'segment1' });
            segmentCacheManagerService.isCacheAvailable = jasmine.createSpy('isCacheAvailable').and.returnValue(false);
            spyOn(service as any, 'chkIsLoggedInUserDiff').and.returnValue(false);
            const result = service.getSegmentDetails();
            expect(storageService.get).toHaveBeenCalled();
            expect(result).toEqual('');
        });
        it('when there is segment data and firstTimeLogin is false case 2', () => {
            storageService.get.and.returnValue({});
            segmentCacheManagerService.isCacheAvailable = jasmine.createSpy('isCacheAvailable').and.returnValue(false);
            service['chkIsLoggedInUserDiff'] = jasmine.createSpy('chkIsLoggedInUserDiff').and.returnValue(false);
            const result = service.getSegmentDetails();
            expect(storageService.get).toHaveBeenCalled();
            expect(result).toEqual('');
        });
        it('when there is segment data and firstTimeLogin is false', () => {
            storageService.get.and.returnValue({ 'segment': 'segment1' });
            segmentCacheManagerService.isCacheAvailable = jasmine.createSpy('isCacheAvailable').and.returnValue(true);
            spyOn(service as any, 'chkIsLoggedInUserDiff').and.returnValue(false);
            const result = service.getSegmentDetails();
            expect(storageService.get).toHaveBeenCalled();
            expect(result).toEqual('segment1');
        });
        it('when there is segment data and firstTimeLogin is false case 2', () => {
            storageService.get.and.returnValue({});
            segmentCacheManagerService.isCacheAvailable = jasmine.createSpy('isCacheAvailable').and.returnValue(true);
            service['chkIsLoggedInUserDiff'] = jasmine.createSpy('chkIsLoggedInUserDiff').and.returnValue(false);
            const result = service.getSegmentDetails();
            expect(storageService.get).toHaveBeenCalled();
            expect(result).toEqual(undefined);
        });
        it('when there is no segment data and firstTimeLogin is false', () => {
            const result = service.getSegmentDetails();
            expect(coralSportsSegmentProviderService.getSegmentDetails).toHaveBeenCalled();
            expect(result).toEqual('');
        });
        it('when there is segment data and firstTimeLogin is false not called', () => {
            storageService.get.and.returnValue({ 'segment': 'segment1' });
            segmentCacheManagerService.isCacheAvailable = jasmine.createSpy('isCacheAvailable').and.returnValue(true);
            spyOn(service as any, 'chkIsLoggedInUserDiff').and.returnValue(false);
            const result = service.getSegmentDetails();
            expect(result).toEqual('segment1');
        });
        it('when there is segment data and firstTimeLogin is false', () => {
            storageService.get.and.returnValue({ 'segment': 'segment1' });
            service['chkIsLoggedInUserDiff'] = jasmine.createSpy('chkIsLoggedInUserDiff').and.returnValue(false);
            const result = service.getSegmentDetails();
            expect(coralSportsSegmentProviderService.getSegmentDetails).toHaveBeenCalled();
        });
        it('when there is username diff', () => {
            storageService.get.and.returnValue({ 'user': 'username', 'segment': 'segment1' });
            const result = service.getSegmentDetails();
            expect(result).toEqual('segment1');
        });
        it('when there is username diff and no storage data', () => {
            storageService.get.and.returnValue({});
            const result = service.getSegmentDetails();
            expect(result).toEqual('');
        });
        it('when there is username diff and storage data undefined', () => {
            storageService.get.and.returnValue(null);
            const result = service.getSegmentDetails();
            expect(result).toEqual('');
        });
    });

    describe('chkIsLoggedInUserDiff', () => {
        it('return true if different username', () => {
            storageService.get.and.returnValue({ 'user': 'username1', 'segment': 'segment1', 'timestamp': Date.now() });
            expect(service.chkIsLoggedInUserDiff()).toBeTruthy();
        });
        it('return false if same username', () => {
            storageService.get.and.returnValue({ 'user': 'username', 'segment': 'segment1', 'timestamp': Date.now() });
            expect(service.chkIsLoggedInUserDiff()).toBeFalsy();
        });
        it('return false if no storage data', () => {
            storageService.get.and.returnValue({});
            expect(service.chkIsLoggedInUserDiff()).toBeTruthy();
        });
        it('return false if  undefined storage data', () => {
            storageService.get.and.returnValue(null);
            expect(service.chkIsLoggedInUserDiff()).toBeTruthy();
        });
    });

    describe('chkModuleForSegmentation', () => {
        it('return true', () => {
            expect(service.chkModuleForSegmentation(true)).toBeTruthy();
        });
        it('return true if route URL is home', () => {
            routingState.getCurrentUrl = jasmine.createSpy('getCurrentUrl').and.returnValue('/');
            expect(service.chkModuleForSegmentation(false)).toBeTruthy();
        });
        it('return true if route URL is home', () => {
            routingState.getCurrentUrl = jasmine.createSpy('getCurrentUrl').and.returnValue('/home/featured');
            expect(service.chkModuleForSegmentation(false)).toBeTruthy();
        });
        it('return true if route URL is a one of home tabs', () => {
            routingState.getCurrentUrl = jasmine.createSpy('getCurrentUrl').and.returnValue('/home/nextraces');
            expect(service.chkModuleForSegmentation(true)).toBeTruthy();
        });
        it('return true if route URL is a big-competition', () => {
            routingState.getCurrentUrl = jasmine.createSpy('getCurrentUrl').and.returnValue('/big-competition/euro2020/test');
            expect(service.chkModuleForSegmentation(true)).toBeTruthy();
        });
    });

    describe('getOtfSegmentUserStatus', () => {
        it('should  call  getOtfSegmentUserStatus if different User', () => {
            storageService.get.and.returnValue({ 'user': 'username', 'segment': true });
            service.chkIsLoggedInUserDiff = jasmine.createSpy('chkIsLoggedInUserDiff').and.returnValue(true);
            coralSportsSegmentProviderService.getOtfSegmentUserStatus = jasmine.createSpy('getOtfSegmentUserStatus').and.returnValue(false);
           service.getOtfSegmentUserStatus();

            
            expect(coralSportsSegmentProviderService.getOtfSegmentUserStatus).toHaveBeenCalled();
        })
        it('should not call coralSportsSegmentProviderService.getOtfSegmentUserStatus ', () => {
            service.chkIsLoggedInUserDiff = jasmine.createSpy('chkIsLoggedInUserDiff').and.returnValue(false);
            storageService.get.and.returnValue({ 'user': 'username', 'segment': true,timestamp : new Date().toUTCString() });
            coralSportsSegmentProviderService.getOtfSegmentUserStatus = jasmine.createSpy('getOtfSegmentUserStatus').and.returnValue(false);
            
            service.getOtfSegmentUserStatus();

            
            expect(coralSportsSegmentProviderService.getOtfSegmentUserStatus).not.toHaveBeenCalled();
        })
        it('should be False', () => {
            coralSportsSegmentProviderService.getOtfSegmentUserStatus = jasmine.createSpy('getOtfSegmentUserStatus').and.returnValue(false);
            service.chkIsLoggedInUserDiff = jasmine.createSpy('chkIsLoggedInUserDiff').and.returnValue(false);
            storageService.get.and.returnValue({ 'user': 'username', 'segment': false });
            expect(service.getOtfSegmentUserStatus()).toBeFalsy();
        })
    })
    
});
