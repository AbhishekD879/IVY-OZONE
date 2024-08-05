import { ScrollToDirective } from '@app/fiveASideShowDown/directives/scroll.position.directive';

describe('ScrollToDirective', () => {
    let elementRef;
    let window;
    let directive: ScrollToDirective;

    beforeEach(() => {
        elementRef = {
            nativeElement: {
                offsetTop: '100'
            }
        };
        window = {
            nativeWindow: {
                scrollTo: jasmine.createSpy('scrollTo')
            }
        };
        directive = new ScrollToDirective(elementRef, window);
    });

    it('ScrollToDirective, should be', () => {
        expect(new ScrollToDirective(elementRef, window)).toBeTruthy();
    });
    it('ScrollToDirective, should be ngOnChanges', () => {
        directive.uptoscroll = true;
        directive.ngOnChanges();
        expect(window.nativeWindow.scrollTo).toHaveBeenCalled();
    });
    it('ScrollToDirective, should be ngOnChanges', () => {
        directive.uptoscroll = false;
        directive.ngOnChanges();
        expect(window.nativeWindow.scrollTo).not.toHaveBeenCalled();
    });
});
