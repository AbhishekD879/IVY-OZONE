import {
    VanillaFreebetsBadgeDynamicLoaderService
} from '@vanillaInitModule/services/vanillaFreeBets/vanilla-fb-badges-loader.service';
import { of as observableOf } from 'rxjs';

describe('VanillaFreebetsBadgeDynamicLoaderService', () => {
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
            getSystemConfig: jasmine.createSpy('getSystemConfig').and.returnValue(observableOf({ 'isAvatarBalance': { 'enabled': true } })),
        };

        fbBadgeLoaderService = new VanillaFreebetsBadgeDynamicLoaderService(
            menuCountersService,
            freebetsBadgeService,
            cmsService
        );
    });

    it('addCounter', () => {
        fbBadgeLoaderService.addCounter({} as any);
        expect(freebetsBadgeService.freeBetCounters.length).toBe(1);
    });

    it('setAvatar, when isAvatarBalance is true', () => {
        cmsService = {
            getSystemConfig: jasmine.createSpy('getSystemConfig').and.returnValue(observableOf({'isAvatarBalance':{ 'enabled': true }})),
        };
        fbBadgeLoaderService = new VanillaFreebetsBadgeDynamicLoaderService(
            menuCountersService,
            freebetsBadgeService,
            cmsService
        );
        fbBadgeLoaderService.setAvatar();
        expect(fbBadgeLoaderService['headerBadge'].item).toBe('avatarbalance');
    });
    
    it('setAvatar, when isAvatarBalance is false', () => {
        cmsService = {
            getSystemConfig: jasmine.createSpy('getSystemConfig').and.returnValue(observableOf({'isAvatarBalance':{ 'enabled': false }})),
        };
        fbBadgeLoaderService = new VanillaFreebetsBadgeDynamicLoaderService(
            menuCountersService,
            freebetsBadgeService,
            cmsService
        );
        fbBadgeLoaderService.setAvatar();
        expect(fbBadgeLoaderService['headerBadge'].item).toBe('avatar');
    });
    it('setAvatar, when config is empty Object', () => {
        cmsService = {
            getSystemConfig: jasmine.createSpy('getSystemConfig').and.returnValue(observableOf({})),
        };
        fbBadgeLoaderService = new VanillaFreebetsBadgeDynamicLoaderService(
            menuCountersService,
            freebetsBadgeService,
            cmsService
        );
        fbBadgeLoaderService.setAvatar();
        expect(fbBadgeLoaderService['headerBadge'].item).toBe('avatar');
    });
    it('setAvatar, when isAvatarBalance is empty Object', () => {
        cmsService = {
            getSystemConfig: jasmine.createSpy('getSystemConfig').and.returnValue(observableOf({ 'isAvatarBalance': {} })),
        };
        fbBadgeLoaderService = new VanillaFreebetsBadgeDynamicLoaderService(
            menuCountersService,
            freebetsBadgeService,
            cmsService
        );
        fbBadgeLoaderService.setAvatar();
        expect(fbBadgeLoaderService['headerBadge'].item).toBe('avatar');
    });
    describe('sportsFreebetsCount', () => {
        it('#when freebetTokenType === "SPORTS" ', () => {
            const freeBetArr = [{ freebetTokenType: 'SPORTS' } as any];
            expect(fbBadgeLoaderService.sportsFreebetsCount(freeBetArr)).toBe(1);
        });
        it('#when we have no FreeBets', () => {
            const freeBetArr = [];
            expect(fbBadgeLoaderService.sportsFreebetsCount(freeBetArr)).toBe(0);
        });
        it('#when freebetTokenType !== "SPORTS"', () => {
            const freeBetArr = [{ freebetTokenType: 'FreeBets' } as any];
            expect(fbBadgeLoaderService.sportsFreebetsCount(freeBetArr)).toBe(0);
        });
    });
    it('add when Bet Tokens are available', () => {
        const freeBetsState = { bettokens:[{}], data: [{}]};
        fbBadgeLoaderService.addCounter = jasmine.createSpy();
        fbBadgeLoaderService.updateBadge = jasmine.createSpy();
        fbBadgeLoaderService.sportsFreebetsCount = jasmine.createSpy();
        fbBadgeLoaderService.addBadgesToVanillaElements(freeBetsState);
        expect(fbBadgeLoaderService.addCounter).toHaveBeenCalledTimes(1);
        expect(fbBadgeLoaderService.updateBadge).toHaveBeenCalled();
        })
    it('update', () => {
        fbBadgeLoaderService.update();
        expect(menuCountersService.update).toHaveBeenCalled();
    });

    describe('addBadgesToVanillaElements', () => {
        it('add when free-bets are available', () => {
            const freeBetsState = { data: [{}], available: true };
            const oddsboostCounter = [{}];
            fbBadgeLoaderService.addCounter = jasmine.createSpy();
            fbBadgeLoaderService.update = jasmine.createSpy();
            fbBadgeLoaderService.sportsFreebetsCount = jasmine.createSpy();
            fbBadgeLoaderService.addBadgesToVanillaElements(freeBetsState, oddsboostCounter);
            expect(fbBadgeLoaderService.addCounter).toHaveBeenCalledTimes(3);
            expect(fbBadgeLoaderService.update).toHaveBeenCalled();
        });

        it('add sports freebets and oddsboosts counters', () => {
            const freeBetsState = { data: [], available: false };
            const oddsboostCounter = [{}];
            fbBadgeLoaderService.addCounter = jasmine.createSpy('addCounter');
            fbBadgeLoaderService.update = jasmine.createSpy('update');
            fbBadgeLoaderService.sportsFreebetsCount = jasmine.createSpy();
            fbBadgeLoaderService.addBadgesToVanillaElements(freeBetsState, oddsboostCounter);
            expect(fbBadgeLoaderService.addCounter).toHaveBeenCalledTimes(3);
            expect(fbBadgeLoaderService.update).toHaveBeenCalledTimes(2);
        });

        it('not add sports freebets and oddsboosts counters', () => {
            const oddsboostCounter = [{}];
            fbBadgeLoaderService.addCounter = jasmine.createSpy('addCounter');
            fbBadgeLoaderService.update = jasmine.createSpy('update');
            fbBadgeLoaderService.sportsFreebetsCount = jasmine.createSpy().and.returnValue(0);
            fbBadgeLoaderService.addBadgesToVanillaElements(1, oddsboostCounter);
            expect(fbBadgeLoaderService.addCounter).toHaveBeenCalledTimes(3);
            expect(fbBadgeLoaderService.update).toHaveBeenCalledTimes(2);
        });

        it('remove oddsboosts counters', () => {
            const oddsboostCounter = [];
            fbBadgeLoaderService.addCounter = jasmine.createSpy('addCounter');
            fbBadgeLoaderService.update = jasmine.createSpy('update');
            fbBadgeLoaderService.sportsFreebetsCount = jasmine.createSpy().and.returnValue(0);
            fbBadgeLoaderService.addBadgesToVanillaElements(1, oddsboostCounter);
            expect(fbBadgeLoaderService.addCounter).toHaveBeenCalledTimes(3);
            expect(fbBadgeLoaderService.update).toHaveBeenCalledTimes(2);
        });

    });


    it('addOddsBoostCounter', () => {
        const oddsboostCounter = [{}];
        fbBadgeLoaderService.addCounter = jasmine.createSpy('addCounter');
        fbBadgeLoaderService.update = jasmine.createSpy('update');
        fbBadgeLoaderService.addOddsBoostCounter(oddsboostCounter);
        expect(fbBadgeLoaderService.addCounter).toHaveBeenCalled();
        expect(fbBadgeLoaderService.update).toHaveBeenCalled();
    });

    describe('addBetpackCounter', () => {
        it('addBetpackCounter', () => {
            const betpackCounter = [{}];
            fbBadgeLoaderService.addCounter = jasmine.createSpy('addCounter');
            fbBadgeLoaderService.update = jasmine.createSpy('update');
            fbBadgeLoaderService.addBetpackCounter(betpackCounter);
            expect(fbBadgeLoaderService.addCounter).toHaveBeenCalled();
            expect(fbBadgeLoaderService.update).toHaveBeenCalled();
        });

        it('addBetpackCounter with length', () => {
            const betpackCounter = {betTokens: {}};
            fbBadgeLoaderService.addCounter = jasmine.createSpy('addCounter');
            fbBadgeLoaderService.update = jasmine.createSpy('update');
            fbBadgeLoaderService.addBetpackCounter(betpackCounter);
            expect(fbBadgeLoaderService.addCounter).toHaveBeenCalled();
            expect(fbBadgeLoaderService.update).toHaveBeenCalled();
        });
    });

});
