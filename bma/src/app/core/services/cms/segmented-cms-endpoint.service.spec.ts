import { SegmentedCMSEndPointService } from './segmented-cms-endpoint.service';

describe('SegmentedCMSEndPointService', () => {
    let service: SegmentedCMSEndPointService,
        segmentEventManagerService;

    beforeEach(() => {
        segmentEventManagerService = {
            getSegmentDetails: jasmine.createSpy('getSegmentDetails')
        };
        service = new SegmentedCMSEndPointService(
            segmentEventManagerService
        );
    });

    describe('getInitialDataEndPoint', () => {
        it('returns segment init CMS endpoint', () => {
            segmentEventManagerService.getSegmentDetails = jasmine.createSpy('getSegmentDetails').and.returnValue('segmentValue');
            const endpoint = service.getInitialDataEndPoint();
            expect(endpoint).toBe('initial-data/segment/segmentValue/mobile');

        });
        it('returns universal init CMS endpoint', () => {
            segmentEventManagerService.getSegmentDetails = jasmine.createSpy('getSegmentDetails').and.returnValue('');
            const endpoint = service.getInitialDataEndPoint();
            expect(endpoint).toBe('initial-data/mobile');
        });
    });
});
