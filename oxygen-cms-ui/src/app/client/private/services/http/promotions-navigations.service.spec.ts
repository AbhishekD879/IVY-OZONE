import { PromotionsNavigationsService } from './promotions-navigations.service';
import { of } from 'rxjs';

describe('PromotionsNavigationsService', () => {
    let service: PromotionsNavigationsService;
    let http, brand, domain;
    beforeEach(() => {
        service = new PromotionsNavigationsService(http, domain, brand);
    });

    describe('getNavListById', () => {
        it('should call get Method', () => {
            const id="1";
            let sendRequestSpy = spyOn(service as any, 'sendRequest').and.returnValue(of({}));
            service.getNavListById(id);
            expect(sendRequestSpy).toHaveBeenCalled();
        });
    });
});