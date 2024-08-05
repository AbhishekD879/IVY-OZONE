import { EqualColumnDirective } from '@shared/directives/equal-column.directive';

describe('EqualColumnDirective', () => {
  let windowRef;
  let element;
  let rendererService;
  let directive;

  beforeEach(() => {
    element = {
      nativeElement: {
        children: [
          {
            children: [
              {
                clientHeight: 1
              },
              {
                clientHeight: 2
              },
              {
                clientHeight: 3
              }
            ]
          }
        ]
      }
    };

    rendererService = {
      renderer: {
        _listenCb: () => {},
        listen: jasmine.createSpy('listen').and.callFake((el, event, cb) =>
          rendererService.renderer._listenCb = cb),
        setStyle: jasmine.createSpy('setStyle')
      }
    };

    windowRef = {
      nativeWindow : {
        _timeoutCb: () => {},
        setTimeout: jasmine.createSpy('setTimeout').and.callFake(cb => windowRef.nativeWindow._timeoutCb = cb)
      }
    };
    directive = new EqualColumnDirective(
      windowRef,
      element,
      rendererService
    );
  });

  it('directive should set maxHeight setting, related to children max ClientHeight', () => {
    directive['equal-column'] = true;

    directive.ngOnInit();

    windowRef.nativeWindow._timeoutCb();

    expect(rendererService.renderer.setStyle).toHaveBeenCalledTimes(3);
    expect(rendererService.renderer.setStyle).toHaveBeenCalledWith(jasmine.any(Object), 'height', '3px');
  });


  it('directive should not set maxHeight when no maxHeight', () => {
    directive['equal-column'] = true;
    directive.element.nativeElement.children = [
      {
        children: [
          {
            clientHeight: 0
          },
          {
            clientHeight: 0
          },
          {
            clientHeight: 0
          }
        ]
      }
    ];

    directive.ngOnInit();
    rendererService.renderer._listenCb();

    expect(rendererService.renderer.setStyle).not.toHaveBeenCalled();
  });

  it('directive should not set maxHeight when less that 2 elems', () => {
    directive['equal-column'] = true;
    directive.element.nativeElement.children = [
      {
        children: [
          {
            clientHeight: 10
          },
          {
            clientHeight: 10
          }
        ]
      }
    ];

    directive.ngOnInit();

    windowRef.nativeWindow._timeoutCb();

    expect(rendererService.renderer.setStyle).not.toHaveBeenCalled();
  });

  it('directive should not set maxHeight when equal-column input is false', () => {
    directive['equal-column'] = false;
    directive.element.nativeElement.children = [
      {
        children: [
          {
            clientHeight: 10
          },
          {
            clientHeight: 10
          },
          {
            clientHeight: 10
          }
        ]
      }
    ];

    directive.ngOnInit();

    rendererService.renderer._listenCb();

    expect(rendererService.renderer.setStyle).not.toHaveBeenCalled();
  });

  it('directive should not set maxHeight when maxHeight already set', () => {
    directive['equal-column'] = false;
    directive.maxHeight = 10;
    directive.element.nativeElement.children = [
      {
        children: [
          {
            clientHeight: 10
          },
          {
            clientHeight: 10
          },
          {
            clientHeight: 10
          }
        ]
      }
    ];

    directive.ngOnInit();
    windowRef.nativeWindow._timeoutCb();
    expect(rendererService.renderer.setStyle).not.toHaveBeenCalled();
  });

  afterEach(() => {
    expect(windowRef.nativeWindow.setTimeout)
      .toHaveBeenCalledWith(jasmine.any(Function));
    expect(rendererService.renderer.listen)
      .toHaveBeenCalledWith(windowRef.nativeWindow, 'resize', jasmine.any(Function));
  });
});
