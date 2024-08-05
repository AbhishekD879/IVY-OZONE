import { SymbolBackgroundDirective } from '@shared/directives/symbol-background.directive';

describe('SymbolBackgroundDirective', () => {
  let directive: SymbolBackgroundDirective,
    rendererService,
    elementMock,
    el;
  beforeEach(() => {
    rendererService = {
      _listenMap: {},
      _unlistenMap: {},
      // renderer: {
        listen: jasmine.createSpy('listen').and.callFake((elm, event, cb) => {
          rendererService._listenMap[event] = cb;
          rendererService._unlistenMap[event] = jasmine.createSpy(`unlisten${event}`);
          return rendererService._unlistenMap[event];
        }),
        createElement: () => {
          return document.createElementNS("http://www.w3.org/2000/svg", "svg");
        },
        setStyle: jasmine.createSpy('setStyle'),
        addClass: jasmine.createSpy('addClass'),
        removeClass: jasmine.createSpy('removeClass'),
      // }
    };
    elementMock = {
      offsetWidth: 0,
      scrollLeft: 0,
      querySelector: jasmine.createSpy('querySelector').and.returnValue({
        offsetLeft: 0,
        offsetWidth: 0
      })
    };

    el = { nativeElement: elementMock };

    directive = new SymbolBackgroundDirective(el, rendererService);
  });

  it('should call createDataUrl', () => {
    const symbolElement = {
      innerHTML: '',
      getAttribute: (viewBox) => {
        return '190 190 20 20';
      },
      setAttribute: (key, value) => {
        return value;
      }
    } as any;
    
    expect(directive['createDataUrl'](symbolElement)).toContain('data:image/svg+xml;base64');
  });

  it('should call applyBackground', () => {
    directive['applyBackground']('');
    expect(rendererService.setStyle).toHaveBeenCalled();
  });
  it('should call clearBackground', () => {
    directive['clearBackground']();
    expect(rendererService.setStyle).toHaveBeenCalled();
  });
  describe("#imgObj", () => {
    it("should call imgObj", () => {
      spyOn<any>(directive, "applyBackground");
      spyOn<any>(directive, "createDataUrl").and.returnValue("/images");
      directive.imgObj = {
        svgBgId: "elemId",
        svgBgImgPath: "/images",
      };
      const elem = document.createElement("div");
      elem.setAttribute("id", "elemId");
      document.body.appendChild(elem);
      directive.imgObj = {
        svgBgId: "elemId",
        svgBgImgPath: "/images",
      };
      expect(directive["applyBackground"]).toHaveBeenCalled();
    });
    it("should call imgObj", () => {
      spyOn<any>(directive, "applyBackground");
      directive.imgObj = {
        svgBgId: "1",
        svgBgImgPath: "/images",
      };
      expect(directive["applyBackground"]).toHaveBeenCalled();
    });
    it("should call imgObj no svgBgId", () => {
      spyOn<any>(directive, "clearBackground");
      directive.imgObj = {};
      expect(directive["clearBackground"]).toHaveBeenCalled();
    });
  });

});
 