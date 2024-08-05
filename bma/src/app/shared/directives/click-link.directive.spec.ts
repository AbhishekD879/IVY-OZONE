import { ClickLinkDirective } from '@shared/directives/click-link.directive';

describe('ClickLinkDirective', () => {
  let directive: ClickLinkDirective;

  beforeEach(() => {
    directive = new ClickLinkDirective();
  });

  it('should have properties initialized', () => {
    expect(directive.draggable).toEqual('false');
    expect((directive as any).CLICK_THRESHOLD_PX).toEqual(3);
    expect((directive as any).moved).toEqual(false);
    expect((directive as any).position).toEqual({ x: 0, y: 0 });
  });

  describe('onMouseDown', () => {
    it('should set parameters', () => {
      (directive as any).moved = undefined;
      directive.onMouseDown({ pageX: 10, pageY: 20 } as any);
      expect((directive as any).position.x).toEqual(10);
      expect((directive as any).position.y).toEqual(20);
    });
  });

  describe('onMouseUp', () => {
    beforeEach(() => {
      (directive as any).position.x = 10;
      (directive as any).position.y = 20;
      (directive as any).moved = undefined;
    });
    describe('should set is moved to false when moved not more than by 3 px', () => {
      it('(positive delta)', () => {
        directive.onMouseUp({ pageX: 7, pageY: 17 } as any);
      });
      it('(negative delta)', () => {
        directive.onMouseUp({ pageX: 13, pageY: 23 } as any);
      });
      afterEach(() => {
        expect((directive as any).moved).toEqual(false);
      });
    });
    describe('should set is moved to true when moved more than by 3 px', () => {
      it('horizontally (positive delta)', () => {
        directive.onMouseUp({ pageX: 6, pageY: 20 } as any);
      });
      it('horizontally (negative delta)', () => {
        directive.onMouseUp({ pageX: 14, pageY: 20 } as any);
      });
      it('vertically (positive delta)', () => {
        directive.onMouseUp({ pageX: 10, pageY: 16 } as any);
      });
      it('vertically (negative delta)', () => {
        directive.onMouseUp({ pageX: 10, pageY: 24 } as any);
      });
      afterEach(() => {
        expect((directive as any).moved).toEqual(true);
      });
    });
  });

  describe('onClick', () => {
    let event;

    beforeEach(() => {
      event = jasmine.createSpyObj('event', ['preventDefault']);
    });
    it('should call event.preventDefault if moved', () => {
      (directive as any).moved = true;
      directive.onClick(event as any);
      expect(event.preventDefault).toHaveBeenCalled();
    });
    it('should not call event.preventDefault if not moved', () => {
      (directive as any).moved = false;
      directive.onClick(event as any);
      expect(event.preventDefault).not.toHaveBeenCalled();
    });
  });
});
