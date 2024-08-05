import { DisableDraggingDirective } from '@shared/directives/disable-dragging.directive';

describe('DisableDraggingDirective', () => {
  let directive: DisableDraggingDirective;

  beforeEach(() => {
    directive = new DisableDraggingDirective();
  });

  it('should set draggable property', () => {
    expect((directive as any).draggable).toEqual('false');
  });

  describe('onMouseDown', () => {
    it('should call event.preventDefault if available', () => {
      const event = jasmine.createSpyObj('event', ['preventDefault']);
      directive.onMouseDown(event as any);
      expect(event.preventDefault).toHaveBeenCalled();
    });
    it('should not call event.preventDefault if not available', () => {
      const event = {},
        preventDefaultGetter = jasmine.createSpy('preventDefault').and.returnValue(null);
      Object.defineProperty(event, 'preventDefault', { get: preventDefaultGetter });
      directive.onMouseDown(event as any);
      expect(preventDefaultGetter).toHaveBeenCalled();
    });
  });
});

