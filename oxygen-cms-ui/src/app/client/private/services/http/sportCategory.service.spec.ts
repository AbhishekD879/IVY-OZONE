import { of } from 'rxjs';
import { SportCategoriesService } from './sportCategory.service';

describe('SportCategoriesService', () => {
    let service: SportCategoriesService;
    let http, brand, domain;
    beforeEach(() => {
        service = new SportCategoriesService(http, domain, brand);
    });

    describe('getSportCategories', () => {
        it('should call get Method', () => {
            let sendRequestSpy = spyOn(service as any, 'sendRequest').and.returnValue(of([]));
            service.getSportCategories();
            expect(sendRequestSpy).toHaveBeenCalled();
        });
    });

    describe('getSportCategory', () => {
        it('should call get Method', () => {
            let sendRequestSpy = spyOn(service as any, 'sendRequest').and.returnValue(of([]));
            service.getSportCategory("");
            expect(sendRequestSpy).toHaveBeenCalled();
        });
    });
});