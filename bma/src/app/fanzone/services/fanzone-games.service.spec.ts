import { FanzoneGamesService } from "@app/fanzone/services/fanzone-games.service";

describe('FanzoneGamesService', () => {
    let service;
    let userService;
    let fanzoneStorageService;

    beforeEach(() => {
        fanzoneStorageService = {
            set: jasmine.createSpy('set'),
            get: jasmine.createSpy('get')
        };
        userService = {
            username: 'test'
        };
        service = new FanzoneGamesService(
            userService,
            fanzoneStorageService
        );
    });

    it('should create service instance', () => {
        expect(service).toBeTruthy();
    });

    describe('setNewFanzoneGamesPopupSeen', () => {
        it('should set storage to true when new popup is seen', () => {
            service.setNewFanzoneGamesPopupSeen();
            expect(fanzoneStorageService.set).toHaveBeenCalledWith('newFanzoneGamesPopupSeen-test', true);
        });
    });

    describe('getNewFanzoneGamesPopupSeen', () => {
        it('should get new games popup seen value from storage', () => {
            service.getNewFanzoneGamesPopupSeen();
            expect(fanzoneStorageService.get).toHaveBeenCalled();
        });
    });

    describe('setFanzoneGamesTooltipSeen', () => {
        it('should set storage to true when games tooltip is seen', () => {
            service.setFanzoneGamesTooltipSeen();
            expect(fanzoneStorageService.set).toHaveBeenCalledWith('newFanzoneGamesTooltipSeen-test', true);
        });
    });

    describe('getFanzoneGamesTooltipSeen', () => {
        it('should get new games tooltip seen value from storage', () => {
            service.getFanzoneGamesTooltipSeen();
            expect(fanzoneStorageService.get).toHaveBeenCalled();
        });
    });

    describe('getNewSignPostingSeenDate', () => {
        it('if new signposting seen date exists in storage', () => {
            fanzoneStorageService.get.and.returnValue(new Date().toDateString());
            expect(service.getNewSignPostingSeenDate()).toBeDefined();
        });

        it('if new signposting seen date not exists in storage', () => {
            fanzoneStorageService.get.and.returnValue(undefined);
            expect(service.getNewSignPostingSeenDate()).toBeUndefined();
        });
    });

    describe('setNewSignPostingSeenDate', () => {
        it('should set signposting date in storage if not exists in storage and seen date is less than cms end date', () => {
            const endDate = new Date();
            endDate.setDate(new Date().getDate() + 3);
            service.setNewSignPostingSeenDate({endDate});
            expect(fanzoneStorageService.set).toHaveBeenCalled();
        });

        it('should not set signposting date in storage if not exists in storage and seen date is greater than cms end date', () => {
            const endDate = new Date();
            endDate.setDate(new Date().getDate() - 3);
            service.setNewSignPostingSeenDate({endDate});
            expect(fanzoneStorageService.set).not.toHaveBeenCalled();
        });

        it('should not set signposting date in storage if exists in storage and new game not yet launched', () => {
            const date = new Date();
            jasmine.clock().mockDate(date);
            fanzoneStorageService.get.and.returnValue(date);
            spyOn(service, 'checkForNewGameLaunched').and.returnValue(false);
            service.setNewSignPostingSeenDate({});
            expect(fanzoneStorageService.set).not.toHaveBeenCalled();
        });

        it('should set signposting date with latest seen date in storage if new game is launched', () => {
            const date = new Date();
            jasmine.clock().mockDate(date);
            fanzoneStorageService.get.and.returnValue(date);
            spyOn(service, 'checkForNewGameLaunched').and.returnValue(true);
            service.setNewSignPostingSeenDate({});
            expect(fanzoneStorageService.set).toHaveBeenCalledWith('newSignPostingSeenDate-test', date);
        });
    });

    describe('checkForNewGameLaunched', () => {
        it('if storage seen date is in between signposting start date and end date', () => {
            const startDate = new Date();
            const endDate = new Date();
            startDate.setDate(new Date().getDate() - 3);
            endDate.setDate(new Date().getDate() + 3);
            const signPostingData = {
                startDate,
                endDate
            };
            const isNewGameLaunched = service.checkForNewGameLaunched(signPostingData, new Date());
            expect(isNewGameLaunched).toBeFalsy();
        });

        it('if storage seen date is not in between signposting start date and end date', () => {
            const startDate = new Date();
            const endDate = new Date();
            startDate.setDate(new Date().getDate() + 3);
            endDate.setDate(new Date().getDate() + 6);
            const signPostingData = {
                startDate,
                endDate
            };
            const isNewGameLaunched = service.checkForNewGameLaunched(signPostingData, new Date());
            expect(isNewGameLaunched).toBeTruthy();
        });
    });

    describe('showNewSignPostingIcon', () => {
        it('should not show new signposting icon if it is not active', () => {
            const showNewSignPostingIcon = service.showNewSignPostingIcon({ active: false });
            expect(showNewSignPostingIcon).toBeFalsy();
        });

        it('should show new signposting icon if signposting date is not available in storage and seen date is less than cms end date', () => {
            spyOn(service, 'getNewSignPostingSeenDate').and.returnValue(undefined);
            const endDate = new Date();
            endDate.setDate(new Date().getDate() + 3);
            const showNewSignPostingIcon = service.showNewSignPostingIcon({ active: true, endDate });
            expect(showNewSignPostingIcon).toBeTruthy();
        });

        it('should not show new signposting icon if signposting date is not available in storage and seen date is greater than cms end date', () => {
            spyOn(service, 'getNewSignPostingSeenDate').and.returnValue(undefined);
            const endDate = new Date();
            endDate.setDate(new Date().getDate() - 3);
            const showNewSignPostingIcon = service.showNewSignPostingIcon({ active: true, endDate });
            expect(showNewSignPostingIcon).toBeFalsy();
        });

        it('should not show new signposting icon if signposting date is available in storage and new game is not yet launched', () => {
            spyOn(service, 'getNewSignPostingSeenDate').and.returnValue(new Date());
            spyOn(service, 'checkForNewGameLaunched').and.returnValue(false);
            const showNewSignPostingIcon = service.showNewSignPostingIcon({ active: true });
            expect(showNewSignPostingIcon).toBeFalsy();
        });

        it('should not show new signposting icon if signposting date is available in storage and new game is launched', () => {
            spyOn(service, 'getNewSignPostingSeenDate').and.returnValue(new Date());
            spyOn(service, 'checkForNewGameLaunched').and.returnValue(true);
            const showNewSignPostingIcon = service.showNewSignPostingIcon({ active: true });
            expect(showNewSignPostingIcon).toBeTruthy();
        });
    });

    describe('showFanzoneGamesTooltip', () => {
        it('should not show tooltip if it is not enabled', () => {
            const showFanzoneGamesTooltip = service.showFanzoneGamesTooltip({ Enable: false });
            expect(showFanzoneGamesTooltip).toBeFalsy();
        });

        it('should show tooltip if toolstip seen value is not available in storage', () => {
            spyOn(service, 'getFanzoneGamesTooltipSeen').and.returnValue(undefined);
            const showFanzoneGamesTooltip = service.showFanzoneGamesTooltip({ Enable: true });
            expect(showFanzoneGamesTooltip).toBeTruthy();
        });

        it('should not show tooltip if tooltip seen value is available in storage', () => {
            spyOn(service, 'getFanzoneGamesTooltipSeen').and.returnValue(true);
            const showFanzoneGamesTooltip = service.showFanzoneGamesTooltip({ Enable: true });
            expect(showFanzoneGamesTooltip).toBeFalsy();
        });
    });
});