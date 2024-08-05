import { DigitListComponent } from '@app/betHistory/components/digitList/digit-list.component';

describe('DigitListComponent', () => {
  let component: DigitListComponent;
  let device: any;

  beforeEach(() => {
    device = {};

    component = new DigitListComponent(device);
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('ngOnInit', () => {

    component['device'] = {
      isAndroid: true,
      isWrapper: true
    } as any;
    component.number = '12';

    component.ngOnInit();
  });

  describe('generateOptions', () => {

    it('should create array with this.number+1 length', () => {
      component['isDecimalPart'] = true;
      component['generateOptions'](14);

      expect(component.digits.length).toEqual(100);
      expect(component.digits[0]).toEqual('00');
    });

    it('should create array with one element', () => {
      component['generateOptions'](0);

      expect(component.digits.length).toEqual(1);
    });

    it('should generate for not decimal part', () => {
      component['isDecimalPart'] = false;
      component['generateOptions'](50);
      expect(component.digits.length).toEqual(51);
      expect(component.digits[0]).toEqual('0');
    });

    it(`should generate 1-figure array for 'whole' part`, () => {
      component.isDecimalPart = false;
      component['generateOptions'](10);
      expect(component.digits[1]).toEqual('1');
      expect(component.digits[9]).toEqual('9');
    });

    it('should generate 2-figure array for decimal part', () => {
      component.isDecimalPart = true;
      component['generateOptions'](20);
      expect(component.digits[1]).toEqual('01');
      expect(component.digits[9]).toEqual('09');
      expect(component.digits[19]).toEqual('19');
    });
  });

  it('changePosition', () => {
    component.changePosition(2);

    expect(component.offset).toEqual(-26);
  });

  it('trackByIndex', () => {
    expect(component.trackByIndex(2)).toEqual(2);
  });

  describe('ngOnChanges', () => {
    beforeEach(() => {
      spyOn(component, 'changePosition');
    });

    it('should not call changePosition method', () => {
      component.isAndroidWrapper = true;

      component.ngOnChanges({number: {currentValue: 12}} as any);

      expect(component.changePosition).not.toHaveBeenCalled();
    });

    it('should call changePosition', () => {
      component.isAndroidWrapper = false;

      component.ngOnChanges({number: {currentValue: 12}} as any);

      expect(component.changePosition).toHaveBeenCalledWith(12);
    });

    it('should call not call changePosition if number doesn\'t exist', () => {
      component.isAndroidWrapper = false;

      component.ngOnChanges({number: null} as any);

      expect(component.changePosition).not.toHaveBeenCalled();
    });
  });
});
