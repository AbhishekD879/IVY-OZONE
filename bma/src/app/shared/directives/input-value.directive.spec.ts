import { InputValueDirective } from '@shared/directives/input-value.directive';

describe('InputValueDirective', () => {
  let directive: InputValueDirective,
    elementRef;

  beforeEach(() => {
    elementRef = { nativeElement: {  } };
    directive = new InputValueDirective(elementRef);
  });

  it('should create event emitters', () => {
    expect(directive.errorBlockChange.constructor.name).toEqual('EventEmitter_');
    expect(directive.fieldValueChange.constructor.name).toEqual('EventEmitter_');
  });
  it('should set element property', () => {
    expect((directive as any).element).toEqual(elementRef.nativeElement);
  });

  describe('onChange', () => {
    let event;

    beforeEach(() => {
      (directive as any).errorBlockChange = jasmine.createSpyObj('errorBlockChange', ['emit']);
      (directive as any).fieldValueChange = jasmine.createSpyObj('fieldValueChange', ['emit']);
      event = { target: { value: 10 } };
    });
    it('should emit values when event.target.value is available', () => {
      directive.onChange(event);
      expect((directive as any).errorBlockChange.emit).toHaveBeenCalledWith(false);
      expect((directive as any).fieldValueChange.emit).toHaveBeenCalledWith(10);
      expect((directive as any).element.value).toEqual(undefined);
    });
    describe('should emit values and set element value when event.target.value is available', () => {
      it('', () => {
        directive.onChange(undefined);
        expect((directive as any).errorBlockChange.emit).toHaveBeenCalledWith(false);
        expect((directive as any).fieldValueChange.emit).toHaveBeenCalledWith(undefined);
        expect((directive as any).element.value).toEqual(null);
      });
    });
  });
});

