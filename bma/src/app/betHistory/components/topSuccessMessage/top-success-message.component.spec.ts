import { TopSuccessMessageComponent } from './top-success-message.component';

describe('TopSuccessMessageComponent', () => {
  let currencyPipe,
    component: TopSuccessMessageComponent;
  beforeEach(() => {
    currencyPipe = {
      transform: jasmine.createSpy('transform').and.callFake((a, b) => `${a}${b}`)
    } as any;
    component = new TopSuccessMessageComponent(currencyPipe);
    component.value = '12.50';
    component.currencySymbol = '$';
  });

  it('ngOnInit should set valueWithCurrency property', () => {
    component.ngOnInit();
    expect(component.valueWithCurrency).toEqual('12.50$');
    expect(currencyPipe.transform).toHaveBeenCalledWith('12.50', '$', 'code');
  });
});
