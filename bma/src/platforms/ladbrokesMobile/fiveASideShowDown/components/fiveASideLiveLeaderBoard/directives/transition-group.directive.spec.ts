import {
  TransitionGroupDirective
} from '@ladbrokesMobile/fiveASideShowDown/components/fiveASideLiveLeaderBoard/directives/transition-group.directive';

xdescribe('TransitionGroupComponent', () => {
  let directive: TransitionGroupDirective, windowRef;
  const window = {
    bottom: 338.03126525878906,
    height: 73.66667175292969,
    left: 0,
    right: 375.3333435058594,
    top: 264.3645935058594,
    width: 375.3333435058594,
    x: 0,
    y: 264.3645935058594,
  };
  const mock = [{
    changes: {
      'dirty': false,
      el: {
        parentElement: 'div.content.ng-star-inserted',
        parentNode: 'div.content.ng-star-inserted'
      },
      first: {
        moved: true,
        newPos: {
          bottom: 190.6979217529297,
          height: 73.66667175292969,
          left: 0,
          right: 375.3333435058594,
          top: 117.03125,
          width: 375.3333435058594,
          x: 0,
          y: 117.03125
        },
        prevPos: {
          bottom: 338.03126525878906,
          height: 73.66667175292969,
          left: 0,
          right: 375.3333435058594,
          top: 264.3645935058594,
          width: 375.3333435058594,
          x: 0,
          y: 264.3645935058594,
        }
      },

    },
    newPos: {
      bottom: 190.6979217529297,
      height: 73.66667175292969,
      left: 0,
      right: 375.3333435058594,
      top: 117.03125,
      width: 375.3333435058594,
      x: 0,
      y: 117.03125
    },
    prevPos: {
      bottom: 338.03126525878906,
      height: 73.66667175292969,
      left: 0,
      right: 375.3333435058594,
      top: 264.3645935058594,
      width: 375.3333435058594,
      x: 0,
      y: 264.3645935058594,
    },
    el: {
      getBoundingClientRect: jasmine.createSpy().and.returnValue(window),
      addEventListener: jasmine.createSpy().and.callFake((a, b) => {
        b(property);
      }),
      removeEventListener: jasmine.createSpy(),
      classList: {
        remove: jasmine.createSpy(),
        add: jasmine.createSpy()
      },
      style: {
        WebkitTransform: jasmine.createSpy()
      }
    },
    moved: true,
    moveCallback: undefined
  }];

  const property = { propertyName: 'transform' };
  beforeEach(() => {
    windowRef = {
      nativeWindow: {
        setTimeout: jasmine.createSpy('setTimeout').and.callFake(fn => fn()),
        clearInterval: jasmine.createSpy('clearInterval')
      }
    };
    directive = new TransitionGroupDirective(windowRef);
  });

  it('should be instantiated', () => {
    expect(directive).toBeTruthy();
  });
  describe('applyTranslation', () => {
    it('check for transition', () => {
      directive.applyTranslation(mock[0] as any);
    });
  });
  describe('refreshPosition', () => {
    it('check for refresh position', () => {
      directive.items = mock as any;
      directive.refreshPosition('newPos');
    });
  });
  describe('ngAfterViewInit', () => {
    it('check for content after animation triggers', () => {
      spyOn(directive as any, 'refreshPosition');
      spyOn(directive as any, 'runCallback');
      spyOn(directive as any, 'applyTranslation');
      spyOn(directive as any, 'runTransition');
      directive.items = mock[0] as any;
      directive.items = {
        changes: {
          subscribe: jasmine.createSpy('subscribe').and.callFake(fn => fn(mock))
        }
      } as any;
      directive.ngAfterViewInit();
    });
  });

  describe('runCallback', () => {
    it('check for refresh position', () => {
      directive.runCallback(mock[0] as any);
    });
    it('check for refresh position', () => {
      directive.runCallback({ moveCallback: jasmine.createSpy() } as any);
    });
  });
  describe('runTransition', () => {
    it('check for item moved true', () => {
      directive.runTransition(mock[0] as any);
    });
    it('check for item moved false', () => {
      mock[0].moved = false;
      directive.runTransition(mock[0] as any);
    });
  });
});
