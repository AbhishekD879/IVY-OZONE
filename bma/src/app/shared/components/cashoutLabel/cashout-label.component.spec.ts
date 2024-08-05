import { CashoutLabelComponent } from './cashout-label.component';

describe('CashoutLabelComponent', () => {
  let component: CashoutLabelComponent;

  beforeEach(() => {
    component = new CashoutLabelComponent();
  });

  it('should create component', () => {
    expect(component).toBeTruthy();
  });

  describe('isBigMode', () => {
    it('should return true if no mode received', () => {
      component['mode'] = undefined;
      expect(component.isBigMode).toEqual(true);
    });
    it('should return true if big mode received', () => {
      component['mode'] = 'big';
      expect(component.isBigMode).toEqual(true);
    });
    it('should return true if no big mode received', () => {
      component['mode'] = 'md';
      expect(component.isBigMode).toEqual(false);
    });
  });

});
