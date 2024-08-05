import { BehaviorSubject, of } from 'rxjs';
import environment from '@environment/oxygenEnvConfig';
import { PromotionsNavigationService } from '@app/promotions/services/promotions/promotions-navigation.service';

describe('@PromotionsNavigationService', () => {

    let service: PromotionsNavigationService,
        httpClient;

    beforeEach(() => {
        httpClient = {
            get: jasmine.createSpy('get').and.returnValue(of(
                {
                    body: []
                }))
        };

        service = new PromotionsNavigationService(httpClient);
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

    describe('setNavGroupData', () => {
        it('should call next method of behaviour sub', () => {
            const mockNavData = [{
                id: 'abc',
                brand: 'abc',
                title: 'abc',
                status: true,
                navItems: []
            }];
            service.isNavGroup = new BehaviorSubject<any>(1);
            service.setNavGroupData(mockNavData);
            service.isNavGroup.next(mockNavData);
            service.isNavGroup.subscribe((data) => {
                expect(data).toEqual(mockNavData);
            });

        });
    });

    describe('getNavigationGroups', () => {
        it('should get navigation-groups', () => {
            service.getNavigationGroups().subscribe();
            expect(httpClient.get).toHaveBeenCalled();
            expect(httpClient.get).toHaveBeenCalledWith(
                `${environment.CMS_ENDPOINT}/${environment.brand}/navigation-group`,
                { observe: 'response', params: {} }
            );
        });
    });

    describe('getLeaderBoards', () => {
        it('should get promo-leaderboard', () => {
            service.getLeaderBoards().subscribe();
            expect(httpClient.get).toHaveBeenCalled();
            expect(httpClient.get).toHaveBeenCalledWith(
                `${environment.CMS_ENDPOINT}/${environment.brand}/promo-leaderboard`,
                { observe: 'response', params: {} }
            );
        });
    });
});
