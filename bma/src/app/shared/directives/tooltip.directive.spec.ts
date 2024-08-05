import { TooltipDirective } from './tooltip.directive';
import environment from '@environment/oxygenEnvConfig';

describe('TooltipDirective', () => {
  let directive: TooltipDirective,
   element,
   rendererService,
   resolver,
   vcr,
   locale,gtmService;

  beforeEach(() => {
    element = {
      nativeElement : { contains : jasmine.createSpy('element.contains').and.returnValue(false)},
    };

    rendererService = {
      renderer: {
        createText: jasmine.createSpy('renderer.createText'),
        listen: jasmine.createSpy('listen'),
        appendChild: jasmine.createSpy('appendChild'),
        addClass: jasmine.createSpy('addClass'),
        createElement: jasmine.createSpy('renderer.createElement').and.returnValue({
          setAttribute: jasmine.createSpy('setAttribute'),
          classList : {
            add : () => 'test'
          }
        }),
      }
    };

    resolver = {
      resolveComponentFactory: jasmine.createSpy('resolver.resolveComponentFactory')
    };

    vcr = {
      createComponent: jasmine.createSpy('vcr.createComponent')
    };

    locale = {
      getString: jasmine.createSpy('locale.getString').and.returnValue('welcome')
    };

    gtmService = {
      push: jasmine.createSpy('push')
    };

    directive = new TooltipDirective(
      element,
      rendererService,
      resolver,
      vcr,
      locale,
      gtmService
    );
  });

  it('ngOnInit should call display tooltip', () => {
    directive.showTooltip = true;
    spyOn(directive, 'displayTooltip');

    directive.ngOnInit();
    expect(directive.displayTooltip).toHaveBeenCalled();
  });
  it('ngOnInit should not call display tooltip', () => {
    directive.showTooltip = false;
    spyOn(directive, 'displayTooltip');

    directive.ngOnInit();
    expect(directive.displayTooltip).not.toHaveBeenCalled();
  });

  it('click should hide tooltip as tooltip exists', () => {
    directive['componentRef'] = {location : 'test'} as any;
    spyOn(directive, 'destroy');

    directive.click();
    expect(directive.destroy).toHaveBeenCalled();
  });

  it('click should hide tooltip as tooltip showOnce is true', () => {
    directive['showOnce'] = true;
    spyOn(directive, 'destroy');

    directive.click();
    expect(directive.destroy).toHaveBeenCalled();
  });

  it('click should show tooltip', () => {
    spyOn(directive, 'displayTooltip');

    directive.click();
    expect(directive.displayTooltip).toHaveBeenCalled();
  });

  it('onMouseHover should show tooltip', () => {
    spyOn(directive, 'displayTooltip');
    directive.mouseOver = true;
    directive.onMouseHover();
    expect(directive.displayTooltip).toHaveBeenCalled();
  });

  it('should call onMouseOut', () => {
    spyOn(directive, 'destroy');
    const event = {
      target: null
    } as any;
    directive.mouseOver = true;
    directive.onMouseOut(event);
    expect((directive as any).element.nativeElement.contains).toHaveBeenCalledWith(null);
    expect(directive.destroy).toHaveBeenCalled();
  });
  it('clickOutside', () => {
    spyOn(directive, 'destroy');
    const event = {
      target: null
    } as any;

    directive.clickOutside(event);
    expect((directive as any).element.nativeElement.contains).toHaveBeenCalledWith(null);
    expect(directive.destroy).toHaveBeenCalled();
  });

  it('clickOutside', () => {
    element.nativeElement.contains.and.returnValue(true);
    spyOn(directive, 'destroy');
    const event = { target: { tagName: 'target '} } as any;
    directive.clickOutside(event);
    expect((directive as any).element.nativeElement.contains).toHaveBeenCalledWith({ tagName: 'target '});
    expect(directive.destroy).not.toHaveBeenCalled();
  });

  it('displayTooltip --- false', () => {
    directive.createElementTag = false;
    directive.displayTooltip();
    expect(resolver.resolveComponentFactory).toHaveBeenCalled();
    expect(vcr.createComponent).toHaveBeenCalled();
  });

  it('displayTooltip -- true', () => {
    directive.createElementTag = true;
    spyOn(directive, 'generateElement');
    directive.displayTooltip();
    expect(resolver.resolveComponentFactory).toHaveBeenCalled();
    expect(vcr.createComponent).toHaveBeenCalled();
  });

  it('generateNgContent', () => {
    directive.tooltip = 'test tooltip';
    directive.createElementTag = false;
    directive.generateNgContent();

    expect(locale.getString).toHaveBeenCalledWith('app.tooltip.test tooltip', undefined);
    expect(rendererService.renderer.createText).toHaveBeenCalled();
  });

  it('generateElement', () => {
    const spy = spyOn(directive.arrowToggle as any, 'emit');
    spyOn<any>(directive, 'sendGTMData');
    directive.createElementTag = true;
    environment.brand = 'ladbrokes';
    directive.toolTipArgs = {
      maxpayout: 'You have maxed payout.',
      click:'here',
      link:'www.coral.co.uk'
    }
    rendererService.renderer.listen.and.callFake((dom, message, eventFn) => {
      eventFn && eventFn('click');
    });
    directive.generateElement();
    expect(rendererService.renderer.createText).toHaveBeenCalled();
  });

  it('generateElement brand = coral', () => {
    const spy = spyOn(directive.arrowToggle as any, 'emit');
    spyOn<any>(directive, 'sendGTMData');
    directive.createElementTag = true;
    environment.brand = 'bma';
    directive.toolTipArgs = {
      maxpayout: 'You have maxed payout.',
      click:'here',
      link:'www.coral.co.uk'
    }
    rendererService.renderer.listen.and.callFake((dom, message, eventFn) => {
      eventFn && eventFn('click');
    });
    directive.generateElement();
    expect(rendererService.renderer.addClass).toHaveBeenCalled();
  });

  it('destroy', () => {
    const spy = spyOn(directive.arrowToggle as any, 'emit');
    directive['componentRef'] = {location : 'test', destroy : jasmine.createSpy()} as any;
    directive.destroy();

    expect(directive['componentRef']).toBeNull();
  });

  it('ngOnDestroy', () => {
    spyOn(directive, 'destroy');
    directive.ngOnDestroy();

    expect(directive.destroy).toHaveBeenCalled();
  });

  it('sendGTMData', () => {
    directive['sendGTMData']();
    expect(gtmService.push).toHaveBeenCalled();
  });

  it('ngOnChanges', () =>{
    const changes = {
    showTooltip:{ 
    currentValue: false,
    firstChange: false,
    previousValue: undefined
      }
    }
    spyOn(directive, 'destroy');
    directive.ngOnChanges(changes as any)
    expect(directive.destroy).toHaveBeenCalled();
  });

});
