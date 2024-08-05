import { FiveASideEntryConfirmationComponent
} from '@lazy-modules/fiveASideShowDown/components/fiveASideEntryConfirmation/fiveaside-entry-confirmation.component';
import { ENTRY_CONFIRMATION } from '@app/fiveASideShowDown/constants/constants';

describe('FiveASideEntryConfirmationComponent', () => {
    let component;
    let windowRefService;
    let gtmService;
    let routerStub;


    beforeEach(() => {
        windowRefService = {
            nativeWindow: {
                location: {
                    pathname: jasmine.createSpy()
                },
                setTimeout: jasmine.createSpy().and.callFake((callback: Function) => {
                    callback();
                })
            }
        };
        routerStub = {
            navigate: jasmine.createSpy('navigate')
        };
        gtmService = {
            push: jasmine.createSpy('push')
        };
        component = new FiveASideEntryConfirmationComponent(windowRefService, gtmService, routerStub);
    });

    it('should create', () => {
        expect(component).toBeTruthy();
    });

    describe('#navigation', () => {
        it('should navigate lobby', () => {
            component.onNavigate();
            expect(gtmService.push).toHaveBeenCalled();
            expect(routerStub.navigate).toHaveBeenCalled();
        });
    });

    describe('#ngOnInit', () => {
        it('should call getContestInformation on ngoninit', () => {
            spyOn(component as any,'triggerSlideUp');
            component.ngOnInit();
            expect(component['triggerSlideUp']).toHaveBeenCalled();
        });

        it('should assign entryTerms value on init', () =>{
          component.termsConditionTag = 'Conditions Apply';
          component.ngOnInit();
          expect(component.entryConfirmTerms).toEqual('Conditions Apply');
        });

        it('should assign default value to terms on init if system config doesnt exist', () =>{
            component.ngOnInit();
            expect(component.entryConfirmTerms).toEqual(ENTRY_CONFIRMATION.entryConfirmationTerms);
        });
    });

    describe('#triggerSlideUp', () => {
        it('should set slideout class name after 500 ms', () => {
            component['triggerSlideUp']();
            expect(component.slideUpClass).toEqual(ENTRY_CONFIRMATION.slideUpClassName);
        });
    });
});
