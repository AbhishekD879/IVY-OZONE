import { FiveAsideLauncherComponent } from './five-a-side-launcher.component';

describe('FiveAsideLauncherComponent', () => {
    let component;
    let router;
    let gtmService;

    beforeEach(() => {
        router = {
            navigateByUrl: jasmine.createSpy('navigateByUrl')
        };
        gtmService = {
            push: jasmine.createSpy('push')
        };
        component = new FiveAsideLauncherComponent(router, gtmService);
    });

    it('should create', () => {
        expect(component).toBeTruthy();
    });

    describe('#navigation', () => {
        it('should navigate to 5 a side', () => {
            component.eventTabs = [
                {
                    id: 'tab-all-markets'
                },{
                    id: 'tab-5-a-side'
                }
            ] as any;
            component.onNavigate();
            expect(gtmService.push).toHaveBeenCalled();
            expect(router.navigateByUrl).toHaveBeenCalled();
        });

    });

});
