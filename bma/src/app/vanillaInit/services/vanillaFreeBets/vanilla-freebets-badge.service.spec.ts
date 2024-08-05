import {
  FreeBetsBadgeService
} from '@vanillaInitModule/services/vanillaFreeBets/vanilla-freebets-badge.service';

describe('VanillaFreebetsBadgeService', () => {
  let vanillaFBService;
  beforeEach(() => {
    vanillaFBService = new FreeBetsBadgeService();
  });

  it('get order', () => {
    const spy = spyOnProperty(vanillaFBService, 'order').and.callThrough();
    expect(vanillaFBService.order).toBe(50);
    expect(spy).toHaveBeenCalled();
  });

  it('setCounters', () => {
    const funcArg = {
      section: 'w',
      item: 'z',
      count: 'y',
      cssClass: 'z',
      set: jasmine.createSpy()
    } as any;

    vanillaFBService.freeBetCounters = [
      { section: 'a', item: 'b', count: 'c', cssClass: 'd' }
    ];
    vanillaFBService.setCounters(funcArg);
    expect(vanillaFBService.freeBetCounters[0]).toEqual({ section: 'a', item: 'b', count: 'c', cssClass: 'd' });
  });
});
