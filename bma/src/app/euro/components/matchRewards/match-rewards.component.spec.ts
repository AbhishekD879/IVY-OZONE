
import { MatchRewardsComponent } from './match-rewards.component';
import { dialogIdentifierDictionary } from '@core/constants/dialog-identifier-dictionary.constant';
import { MATCHDAY_REWARDS_MOCK } from '@app/euro/constants/matchday-rewards-data';
import { EURO_DISPLAY_MESSAGES } from '@app/euro/constants/euro-constants';

describe('MatchRewardsComponent', () => {
    let component, userService, scroller, componentFactoryResolver, dialogService, resolvedDialogComponent,
    deviceService;

    beforeEach(() => {

        scroller = {
            scrollToAnchor: jasmine.createSpy('scrollToAnchor').and.callThrough()
        };
        userService = {
            status: true,
            currencySymbol: '£'
        };
        dialogService = {
            API: dialogIdentifierDictionary,
            openDialog: jasmine.createSpy('openDialog')
        };
        resolvedDialogComponent = {
            name: dialogService.API.howItWorksDialog
        };
        componentFactoryResolver = {
            resolveComponentFactory: jasmine.createSpy('resolveComponentFactory').and.returnValue(resolvedDialogComponent)
        };
        deviceService = {
            isMobile: true,
            isDesktop: false
        };
        component = new MatchRewardsComponent
        (scroller, deviceService, userService);
        component.TokenAmount = '12';
        component.currentBadge = 12;
        component.totalNoOfBadges = 30;
        component.freeBetPositionSequence = [3,6,20];
        component.statusrenderIndex = 15;
    });

    describe('onInit', () => {
        it(`should call euroBadgesArr`, () => {
            spyOn(component, 'calculateNextFreeToken');
            component.ngOnInit();

            expect(component.calculateNextFreeToken).toHaveBeenCalledTimes(1);
        });

        it(`should call euroBadgesArr with no tokenamount`, () => {
            spyOn(component, 'calculateNextFreeToken');
            spyOn(component, 'populateMatchRewardBadges');
            component.TokenAmount = undefined;
            component.init();

            expect(component.populateMatchRewardBadges).toHaveBeenCalledTimes(1);
        });

        it(`should call with no tokenamount for anonymous users`, () => {
            spyOn(component, 'calculateNextFreeToken');
            spyOn(component, 'populateMatchRewardBadges');
            userService.status = false;
            component.TokenAmount = undefined;
            component.currentBadge = 0;
            component.init();

            expect(component.populateMatchRewardBadges).toHaveBeenCalledTimes(1);
        });

        it(`should call scrollDown`, () => {
            spyOn(component, 'scrollDown');
            component.ngAfterViewInit();

            expect(component.scrollDown).toHaveBeenCalledTimes(1);
        });

        it(`should not call scrollDown`, () => {
            spyOn(component, 'scrollDown');
            deviceService.isDesktop = true;
            component.ngAfterViewInit();

            expect(component.scrollDown).not.toHaveBeenCalled();
        });

        it(`should not call scrollToAnchor for badge less than 5`, () => {
            component.currentBadge = 2;
            component.scrollDown();
            expect(scroller.scrollToAnchor).not.toHaveBeenCalled();
        });

        it(`should call scrollToAnchor`, () => {
            component.currentBadge = 25;
            component.scrollDown();
            expect(scroller.scrollToAnchor).toHaveBeenCalled();
        });


        it(`should call calculateNextFreeToken with multiple bets`, () => {
            component.freeBetPositionSequence = MATCHDAY_REWARDS_MOCK.freeBetPositionSequence;
            component.placedBetToday = false;
            component.currentBadge = 8;
            component.calculateNextFreeToken();
            expect(component.freeTokenMessage[0]). toBe(EURO_DISPLAY_MESSAGES.FREEBET.REWARD);
            expect(component.freeTokenMessage[1]). toBe(EURO_DISPLAY_MESSAGES.FREEBET.QUALIFYING_SINGLE_BET);
            expect(component.freeTokenMessage[3]). toBe(undefined);
        });

        it(`should call calculateNextFreeToken with single bet`, () => {
            component.freeBetPositionSequence = MATCHDAY_REWARDS_MOCK.freeBetPositionSequence;
            component.placedBetToday = false;
            component.currentBadge = 9;
            component.calculateNextFreeToken();
            expect(component.freeTokenMessage[0]). toBe(EURO_DISPLAY_MESSAGES.FREEBET.REWARD);
            expect(component.freeTokenMessage[1]). toBe(EURO_DISPLAY_MESSAGES.FREEBET.QUALIFYING_SINGLE_BET);
            expect(component.freeTokenMessage[3]). toBe(undefined);
        });

        it(`should call congrats message`, () => {
            component.freeBetPositionSequence = MATCHDAY_REWARDS_MOCK.freeBetPositionSequence;
            component.currentBadge = 8;
            component.placedBetToday = true;
            component.calculateNextFreeToken();
            expect(component.freeTokenMessage[0]). toBe(EURO_DISPLAY_MESSAGES.CONGRATULATIONS_MSG.CONGRATS);
            expect(component.freeTokenMessage[1]). toBe(EURO_DISPLAY_MESSAGES.CONGRATULATIONS_MSG.STAMP);
            expect(component.freeTokenMessage[2]). toBe('');
            expect(component.freeTokenMessage[3]). toBe(EURO_DISPLAY_MESSAGES.CONGRATULATIONS_MSG.NEXT_DAY);
        });

        it(`should call congrats message and token amount`, () => {
            component.freeBetPositionSequence = MATCHDAY_REWARDS_MOCK.freeBetPositionSequence;
            component.currentBadge = 9;
            component.placedBetToday = true;
            component.calculateNextFreeToken();
            expect(component.freeTokenMessage[0]). toBe(EURO_DISPLAY_MESSAGES.CONGRATULATIONS_MSG.CONGRATS);
            expect(component.freeTokenMessage[1]). toBe(EURO_DISPLAY_MESSAGES.CONGRATULATIONS_MSG.EARNED);
            expect(component.freeTokenMessage[2]). toBe('£12 FREE BET');
            expect(component.freeTokenMessage[3]). toBe(EURO_DISPLAY_MESSAGES.CONGRATULATIONS_MSG.MORE_STAMPS);
        });

        it(`should call onchanges`, () => {
            const changes: any = {
                freeBetPositionSequence: {
                  isFirstChange: () => false
                }
            };
            spyOn(component, 'calculateNextFreeToken');
            spyOn(component, 'init');
            component.ngOnChanges(changes);
            expect(component.init).toHaveBeenCalledTimes(1);
        });

        it(`should not call onchanges`, () => {
            const changes: any = {
                freeBetPositionSequence: {
                  isFirstChange: () => true
                }
            };
            spyOn(component, 'calculateNextFreeToken');
            spyOn(component, 'init');
            component.ngOnChanges(changes);
            expect(component.init).not.toHaveBeenCalled();
        });
    });
});

