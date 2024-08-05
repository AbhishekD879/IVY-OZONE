import { VanillaFreebetsBadgeDynamicLoaderService } from './vanilla-fb-badges-loader.service';
import { of as observableOf } from 'rxjs';

describe('Ladbrokes VanillaFreebetsBadgeDynamicLoaderService', () => {
  let fbBadgeLoaderService;
  let menuCountersService;
  let freebetsBadgeService;
  let cmsService;

  beforeEach(() => {
    menuCountersService = {
      update: jasmine.createSpy()
    };

    freebetsBadgeService = {
      freeBetCounters: []
    };

    cmsService = {
      getSystemConfig: jasmine.createSpy('getSystemConfig').and.returnValue(observableOf({'isAvatarBalance':false})),
  };

    fbBadgeLoaderService = new VanillaFreebetsBadgeDynamicLoaderService(menuCountersService, freebetsBadgeService,cmsService);
  });

  describe('sportsFreebetsCount', () => {

    it('user has FreeBets" ', () => {
      const freeBetArr = [{ freebetTokenType: 'SPORTS' } as any];
      expect(fbBadgeLoaderService.sportsFreebetsCount(freeBetArr)).toEqual(1);
    });

    it('user has no FreeBets', () => {
      const freeBetArr = [];
      expect(fbBadgeLoaderService.sportsFreebetsCount(freeBetArr)).toEqual(0);
    });

  });

});
