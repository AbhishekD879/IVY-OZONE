import { LinkHrefDirective } from './link-href.directive';

describe('LinkHrefDirective', () => {
  let element;
  let directive: LinkHrefDirective;
  beforeEach(() => {
    element = {
      nativeElement: {
        setAttribute: jasmine.createSpy()
      }
    };
    directive = new LinkHrefDirective(element);
  });

  it('should create an instance', () => {
    expect(directive).toBeTruthy();
  });

  it('setAttribute', () => {
    directive.link = '/somelink';
    directive.ngOnInit();
    expect(element.nativeElement.setAttribute).toHaveBeenCalledTimes(1);
    expect(element.nativeElement.setAttribute).toHaveBeenCalledWith('href', '/somelink');
  });

  it('check if prevent default executed', () => {
    const event = {
      preventDefault: jasmine.createSpy()
    };
    directive.onclick(<any>event);
    expect(event.preventDefault).toHaveBeenCalledTimes(1);
  });
});
