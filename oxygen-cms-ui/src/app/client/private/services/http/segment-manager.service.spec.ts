import { SegmentManagerService } from './segment-manager.service';
import { of } from 'rxjs';

describe('SegmentManagerService', () => {
    let service: SegmentManagerService;
    let http, brand, domain;
    beforeEach(() => {
        service = new SegmentManagerService(http, domain, brand);
    });

    describe('getSegments', () => {
        it('should call get Method', () => {
            let sendRequestSpy = spyOn(service as any, 'sendRequest').and.returnValue(of({}));
            service.getSegments();
            expect(sendRequestSpy).toHaveBeenCalled();
        });
    });
});