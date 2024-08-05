import { PromotionsLeaderboardService } from './promotions-leaderboard.service';
import { of } from 'rxjs';

describe('PromotionsLeaderboardService', () => {
    let service: PromotionsLeaderboardService;
    let http, brand, domain;
    beforeEach(() => {
        service = new PromotionsLeaderboardService(http, domain, brand);
    });

    describe('getActiveLeaderboard', () => {
        it('should call get Method', () => {
            let sendRequestSpy = spyOn(service as any, 'sendRequest').and.returnValue(of({}));
            service.getActiveLeaderboard();
            expect(sendRequestSpy).toHaveBeenCalled();
        });
    });
});