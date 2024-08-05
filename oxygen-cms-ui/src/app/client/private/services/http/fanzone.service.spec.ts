import { FanzoneService } from './fanzone.service';
import { of } from 'rxjs';
import { Fanzone } from '../../models/fanzone.model';
import { HttpClient } from '@angular/common/http';

describe('FanzoneService', () => {
    let service: FanzoneService;
    let http: HttpClient;
    const brand = 'ladbrokes';
    const domain = 'https://cms-tst0.com/';

    const fanzone: Fanzone = {
        name: 'abc',
        brand: 'ladbrokes',
        id: '1232342',
        createdAt: 'abc',
        createdBy: 'abc',
        updatedAt: 'abc',
        updatedBy: 'abc',
        createdByUserName: 'abc',
        updatedByUserName: 'abc'
    };
    beforeEach(() => {
        service = new FanzoneService(http, domain, brand);
    });

    it('should call create Fanzone Method', () => {
        const sendRequestSpy = spyOn(service as any, 'sendRequest').and.returnValue(of({}));
        service.createFanzone(fanzone);
        expect(sendRequestSpy).toHaveBeenCalled();
    });
});
