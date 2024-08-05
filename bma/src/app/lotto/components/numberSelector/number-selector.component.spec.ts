import { NumberSelectorComponent } from './number-selector.component';

describe('NumberSelectorComponent', () => {
  let component: NumberSelectorComponent;
  let locale;

  beforeEach(() => {
    locale = {
      getString: jasmine.createSpy('getString').and.returnValue('bma')
    };
    component = new NumberSelectorComponent(
      locale,
    );
  });
   

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('numbersTrackBy should return joined string', () => {
    const index: number = 11;
    const item: any = {
      id: '22',
      value: '33'
    };
    const result = component.numbersTrackBy(index, item);
    expect(result).toEqual('1133');
  });

  it('#numbers', () => {
    component.numbers;
    expect(component.numbers).toEqual([]);
  });
  it('set numbers', () => {
    component.numbers = [];
     expect(component.numbers).toEqual([]);
  });

})








