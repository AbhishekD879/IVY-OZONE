import { ILazyComponentOutput } from "@app/shared/components/lazy-component/lazy-component.model";
import { SbBetSummaryComponent } from "./sb-bet-summary.component";
import { IFreebetToken } from "@app/bpp/services/bppProviders/bpp-providers.model";

describe('', () => {
    let component: SbBetSummaryComponent;
    let user, currencyPipe, bppProviderService, germanSupportService, pubSubService;

    beforeEach(() => {
        currencyPipe = {
            transform: jasmine.createSpy('transform')
        };
        user = {};
        component = new SbBetSummaryComponent(
            user,
            currencyPipe,
            bppProviderService,
            germanSupportService,
            pubSubService
        );
    });

    it('onFreebetChange is called', () => {
        const event = {} as ILazyComponentOutput;
        event.output = 'selectedChange';
        const emitSpy = spyOn(component.fbChange, 'emit');
        component.onFreebetChange(event);
        expect(emitSpy).toHaveBeenCalled();
    });

    it('showFreeBet is called with freebets', () => {
        component.freebetsList = [{}, {}] as IFreebetToken[];
        expect(component.showFreeBet()).toBe(true);
    });

    it('showFreeBet is called with betPackList', () => {
        component.betPackList = [{}, {}] as IFreebetToken[];
        expect(component.showFreeBet()).toBe(true);
    });

    it('getStakeEntered is called', () => {
        component.selection = {stake: '1.50'} as any;
        user.currencySymbol = '£';
        currencyPipe.transform.and.returnValue('£1.50');
        expect(component.getStakeEntered()).toBe('£1.50');
    });

    it('stakeElemClick is called', () => {
        const emitSpy = spyOn(component.stakeClick, 'emit');
        component.stakeElemClick();
        expect(emitSpy).toHaveBeenCalled();
    });
});