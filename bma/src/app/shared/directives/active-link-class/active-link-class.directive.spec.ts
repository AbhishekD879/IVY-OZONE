import { ActiveLinkClassDirective } from './active-link-class.directive';
import { of } from 'rxjs';
import { NavigationEnd } from '@angular/router';

describe('LinkHrefDirective', () => {
  let element, servingService, router;
  let directive: ActiveLinkClassDirective;

  beforeEach(() => {
    element = {
      nativeElement: {
        classList: {
          add: jasmine.createSpy('add'),
          remove: jasmine.createSpy('remove')
        }
      }
    };

    servingService = {
      pathStartsWith: jasmine.createSpy('pathStartsWith')
    };

    router = {
      events: of({})
    };

    directive = new ActiveLinkClassDirective(element, servingService, router);
    directive.link = 'anchor-link';
  });

  it('should create an instance', () => {
    expect(directive).toBeTruthy();
  });

  it('@ngOnInit should not update state if event is not NavigationEnd', () => {
    router.events = of({});

    directive.ngOnInit();
    expect(servingService.pathStartsWith).not.toHaveBeenCalled();
  });

  it('@ngOnInit should remove class on init and route event', () => {
    servingService.pathStartsWith.and.returnValue(true);
    const routeEvent = new NavigationEnd(1, 'url', 'urlAfterRedirect');
    router.events = of(routeEvent);

    directive.ngOnInit();
    expect(servingService.pathStartsWith).toHaveBeenCalledWith('anchor-link');
    expect(element.nativeElement.classList.add).toHaveBeenCalledWith('active');
  });

  it('@ngOnChanges should remove active class', () => {
    servingService.pathStartsWith.and.returnValue(false);
    directive.ngOnChanges();
    expect(servingService.pathStartsWith).toHaveBeenCalledWith('anchor-link');
    expect(element.nativeElement.classList.remove).toHaveBeenCalledWith('active');
  });

  it('@ngOnDestroy should unsubscribe from route events', () => {
    directive['routerSubscription'] = {
      unsubscribe: jasmine.createSpy('unsubscribe')
    } as any;

    directive.ngOnDestroy();
    expect(directive['routerSubscription'].unsubscribe).toHaveBeenCalled();
  });
});
