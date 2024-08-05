
import { of } from 'rxjs';
import { HttpClient } from '@angular/common/http';
import { firstBetPlacementService } from './firstBetPlacement.service';

describe('firstBetPlacementService', () => {
    let service, http: HttpClient, domain, brand;

    beforeEach(() => {
        service = new firstBetPlacementService(http, domain, brand);
    });

    it('should call getDetailsByBrand Method', () => {
        const sendRequestSpy = spyOn(service as any, 'sendRequest').and.returnValue(of({}));
        service.getDetailsByBrand();
        expect(sendRequestSpy).toHaveBeenCalled();
    });

    it('should call saveFirstBet Method', () => {
        const sendRequestSpy = spyOn(service as any, 'sendRequest').and.returnValue(of({}));
        service.saveFirstBet({});
        expect(sendRequestSpy).toHaveBeenCalled();
    });

    it('should call updateFirstBet Method', () => {
        const sendRequestSpy = spyOn(service as any, 'sendRequest').and.returnValue(of({}));
        service.updateFirstBet({});
        expect(sendRequestSpy).toHaveBeenCalled();
    });
    it('should call postFirstBetBulbIcon Method', () => {
        const sendRequestSpy = spyOn(service as any, 'sendRequest').and.returnValue(of({}));
        service.postFirstBetBulbIcon('',{});
        expect(sendRequestSpy).toHaveBeenCalled();
    });
    it('should call removeFirstBetBulbIcon Method', () => {
        const sendRequestSpy = spyOn(service as any, 'sendRequest').and.returnValue(of({}));
        service.removeFirstBetBulbIcon('');
        expect(sendRequestSpy).toHaveBeenCalled();
    });
});
