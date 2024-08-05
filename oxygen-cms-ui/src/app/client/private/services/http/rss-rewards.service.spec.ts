import { RssRewardsService } from "./rss-rewards.service";

describe('RssRewardsService', () => {
    let service: RssRewardsService, http, rssRewards;
    beforeEach(() => {
        service = new RssRewardsService(http, 'test', 'bma');
        rssRewards = {
            id: 'test-id'
        };
        service['sendRequest'] = jasmine.createSpy('sendRequest');
    });
    it('get', () => {
        service.get();
        expect(service['sendRequest']).toHaveBeenCalledWith('get', 'rss-rewards/brand/bma', null);
    });
    it('update', () => {
        service.update(rssRewards);
        expect(service['sendRequest']).toHaveBeenCalledWith('put', 'rss-rewards/test-id', rssRewards);
    });
    it('create', () => {
        service.create(rssRewards);
        expect(service['sendRequest']).toHaveBeenCalledWith('post', 'rss-rewards', rssRewards);
    });
});