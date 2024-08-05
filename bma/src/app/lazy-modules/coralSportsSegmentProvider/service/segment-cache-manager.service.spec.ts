import { SegmentCacheManagerService } from './segment-cache-manager.service';

describe('SegmentCacheManagerService', () => {
    let service: SegmentCacheManagerService,
        storageService, userService;

    beforeEach(() => {
        storageService = {
            get: jasmine.createSpy('get'),
            set: jasmine.createSpy('set'),
        };
        userService = {
            username: 'username'
        };
        service = new SegmentCacheManagerService(
            storageService,
            userService
        );
    }); 
    const SEGMENT_STORE_KEYTEXT: string = 'Segment';

    describe('isCacheAvailable', () => {
        it('when storage has no segment value', () => {
            expect(service.isCacheAvailable()).toBeFalsy();
        });
        it('when storage has segment value and currenttime is before expiry time', () => {
            const currentTime = new Date();
            currentTime.setHours(currentTime.getHours() + 2);
            storageService.get.and.returnValue({ 'user': userService.username, 'segment': 'segment1', 'timestamp': currentTime.toUTCString() });
            const result = service.isCacheAvailable();
            expect(result).toBeTruthy();
        });
        it('when storage has segment value and currenttime is before expiry time by a day', () => {
            const currentTime = new Date();
            currentTime.setDate(currentTime.getDate() + 1);
            storageService.get.and.returnValue({ 'user': userService.username, 'segment': 'segment1', 'timestamp': currentTime.toUTCString() });
            const result = service.isCacheAvailable();
            expect(result).toBeTruthy();
        });
        it('when storage has segment value and currenttime is after expiry time by a day', () => {
            const currentTime = new Date();
            currentTime.setDate(currentTime.getDate() - 1);
            storageService.get.and.returnValue({ 'user': userService.username, 'segment': 'segment1', 'timestamp': currentTime.toUTCString() });
            const result = service.isCacheAvailable();
            expect(result).toBeDefined();
        });
        it('when storage has segment value and currenttime is after expiry time by a month', () => {
            const currentTime = new Date();
            currentTime.setMonth(currentTime.getMonth() - 1);
            storageService.get.and.returnValue({ 'user': userService.username, 'segment': 'segment1', 'timestamp': currentTime.toUTCString() });
            const result = service.isCacheAvailable();
            expect(result).toBeFalsy();
        });
        it('when storage has segment value and currenttime is falling to current month, expiry is falling to next month', () => {
            const currentTime = new Date();
            currentTime.setMonth(currentTime.getMonth() + 1);
            storageService.get.and.returnValue({ 'user': userService.username, 'segment': 'segment1', 'timestamp': currentTime.toUTCString() });
            const result = service.isCacheAvailable();
            expect(result).toBeTruthy();
        });
        it('when storage has segment value and currenttime is after expiry time by a year', () => {
            const currentTime = new Date();
            currentTime.setFullYear(currentTime.getFullYear() - 1);
            storageService.get.and.returnValue({ 'user': userService.username, 'segment': 'segment1', 'timestamp': currentTime.toUTCString() });
            const result = service.isCacheAvailable();
            expect(result).toBeFalsy();
        });
        it('when storage has segment value and currenttime is falling to current year, expiry is falling to next year', () => {
            const currentTime = new Date();
            currentTime.setFullYear(currentTime.getFullYear() + 1);
            storageService.get.and.returnValue({ 'user': userService.username, 'segment': 'segment1', 'timestamp': currentTime.toUTCString() });
            const result = service.isCacheAvailable();
            expect(result).toBeTruthy();
        });
        it('when storage has segment value and curent time afer expiry time', () => {
            const currentTime = new Date();
            currentTime.setHours(currentTime.getHours() - 7);
            storageService.get.and.returnValue({ 'user': userService.username, 'segment': 'segment1', 'timestamp': currentTime.toUTCString() });
            const result = service.isCacheAvailable();
            expect(result).toBeDefined();
        });
        it('when storage has segment value and curent time is equals to expiry time', () => {
            const currentTime = new Date();
            currentTime.setHours(currentTime.getHours() - 7);
            storageService.get.and.returnValue({ 'user': userService.username, 'segment': 'segment1', 'timestamp': currentTime.toUTCString() });
            const result = service.isCacheAvailable();
            expect(result).toBeDefined();
        });
    });

    describe('isSegmentChanged', () => {
        it('when segment changed', () => {
            service.isChanged = true;
            expect(service.isSegmentChanged(true)).toBeTruthy();
        });
        it('when segment unchanged', () => {
            service.isChanged = true;
            expect(service.isSegmentChanged(false)).toBeFalsy();
        });
    });
});
