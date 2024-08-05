import { ScrollOnceDirective } from './scroll-once-directive';
import { of } from 'rxjs';
describe('#scrollOnceDirective', () => {
    let directive: ScrollOnceDirective,
        elr,
        gtmService,
        sessionStorage;

        const gaTrackingData =  {
            isHomePage: true,
            event: 'trackEvent',
            GATracking: {
              eventAction: 'scroll',
              eventCategory: 'module ribbon',
              eventLabel: "",
            }
          };

    beforeEach(() => {
        elr = {
            nativeElement: {
                addEventListener: jasmine.createSpy('addEventListener'),
                removeEventListener: jasmine.createSpy('removeEventListener')
            }
        };
        gtmService = {
            push: jasmine.createSpy('push')
        };
        sessionStorage = {
            get: jasmine.createSpy('get'),
            set: jasmine.createSpy('set')
        };

        directive = new ScrollOnceDirective(elr, gtmService, sessionStorage);
        directive.targetElementFrom = 'moduleribbon';
    });

    describe('ngAfterViewInit', () => {
        it('should call fromEventPattern', () => {
            directive['callEventPattern'] = jasmine.createSpy('callEventPattern').and.callFake(() => of(null));
            directive['gtmUpdate'] = jasmine.createSpy('gtmUpdate');
            directive.ngAfterViewInit();
            expect(directive.gtmUpdate).toHaveBeenCalled();
        })
    });

    it('should return observable', () => {
        const returnValue = directive.callEventPattern();
        expect(returnValue).not.toBeNull();
    })

    it('should call addclickHandler', () => {
        directive.addClickHandler('');
        expect(elr.nativeElement.addEventListener).toHaveBeenCalled();
    });

    it('should call removeclickHandler', () => {
        directive.removeClickHandler('');
        expect(elr.nativeElement.removeEventListener).toHaveBeenCalled();
    });

    it('should call gtmUpdate method with if condition', () => {
        directive.GAtrackingObject = gaTrackingData;
        directive['gtmDataHandler'] = jasmine.createSpy('gtmDataHandler');
        directive.gtmUpdate();
        expect(sessionStorage.set).toHaveBeenCalled();
        expect(directive.gtmDataHandler).toHaveBeenCalled();
    });
    
    it('should call gtmUpdate method with else condition', () => {
        directive.GAtrackingObject = gaTrackingData;
        directive.targetElementFrom = 'surfaceBet';
        directive['gtmDataHandler'] = jasmine.createSpy('gtmDataHandler');
        directive.gtmUpdate();
        expect(sessionStorage.set).not.toHaveBeenCalled();
        expect(directive.gtmDataHandler).toHaveBeenCalled();
    });

    it('should call gtmDataHandler method', () => {
        directive.gtmDataHandler(gaTrackingData);
        expect(gtmService.push).toHaveBeenCalled();
    })
})