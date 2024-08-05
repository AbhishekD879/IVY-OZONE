import { RssRewardsApiService } from "./rss-rewards.api.service";

describe('RssRewardsApiService', () => {
    let service: RssRewardsApiService, apiClientService;
    const rssRewardsMock =  {
        brand: 'bma',
        id: '12345',
        createdAt: 'test',
        createdBy: 'test',
        createdByUserName: 'test',
        updatedAt: 'test',
        updatedBy: 'test',
        updatedByUserName: 'test',
        enabled: false,
        coins: 20,
        communicationType: 'Inbox',
        sitecoreTemplateId: 'testId',
        source: 'Sports',
        subSource: 'RSS',
        product: 'Sportsbook'
    };
    beforeEach(() => {
        apiClientService = {
            rssRewards: jasmine.createSpy('rssRewards').and.returnValue({
                get: jasmine.createSpy('get').and.returnValue({body: rssRewardsMock}),
                create: jasmine.createSpy('create').and.returnValue({body: rssRewardsMock}),
                update: jasmine.createSpy('update').and.returnValue({body: rssRewardsMock})
            })
        };
        service = new RssRewardsApiService(apiClientService);
    });
    it('get', () => {
        expect(service.get()).toEqual({body: rssRewardsMock} as any);
    });
    it('create', () => {
        expect(service.create(rssRewardsMock)).toEqual({body: rssRewardsMock} as any);
    });
    it('update', () => {
        expect(service.update(rssRewardsMock)).toEqual({body: rssRewardsMock} as any);
    });
});