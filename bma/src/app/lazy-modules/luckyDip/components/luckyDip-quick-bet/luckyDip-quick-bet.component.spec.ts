import { LuckyDipBetSelectionComponent } from './luckyDip-quick-bet.component';
import { LUCKY_DIP_CONSTANTS } from '@lazy-modules/luckyDip/constants/lucky-dip-constants';

describe('LuckyDipBetSelectionComponent', () => {

    let component: LuckyDipBetSelectionComponent,
        pubsub, 
        dialogService;

    beforeEach(() => {
        pubsub = {
            publish: jasmine.createSpy('publish'),
            publishSync: jasmine.createSpy('publishSync'),
            subscribe: jasmine.createSpy('subscribe'),
            API: {
                QUICKBET_PANEL_CLOSE: 'QUICKBET_PANEL_CLOSE',
                MY_BET_PLACED: 'MY_BET_PLACED'
            }
        }

        component = new LuckyDipBetSelectionComponent(
             pubsub, dialogService);
    });


    describe('handleLuckyDipEvents', () => {

        it('call', () => {
            const mockEvent = {
                output: 'placeBetFn',
                value: ''
            };
            component.handleLuckyDipEvents(mockEvent);
            expect(pubsub.publish).toHaveBeenCalled()
        })

    })

    describe('setTagforLd', () => {
        it('should set tag upon calling setTagforLd', () => {
            component.setTagforLd();
            expect(component.tag).toBe(LUCKY_DIP_CONSTANTS.LUCKY_DIP);
        });
    });
});