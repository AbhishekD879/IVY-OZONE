import { BetslipFctcListComponent } from '@betslip/components/betslipFctcList/betslip-fctc-list.component';

describe('#BetslipFctcListComponent', () => {
  let component;

  beforeEach(() => {
    component = new BetslipFctcListComponent();
  });

  it('constructor', () => {
    expect(component).toBeTruthy();
  });

  describe('#trackByOutcome', () => {
    it('trackByOutcome for betslip', () => {
      component.modifire = 'betslip';
      expect(component.trackByOutcome({ id: '1' } as any)).toBe('1');
    });

    it('trackByOutcome for receipt', () => {
      component.modifire = 'receipt';
      expect(component.trackByOutcome({ description: '1' } as any)).toBe('1');
    });
  });

  describe('ngOnInit', () => {
    it('should set default value if undefined', () => {
      component.modifire = undefined;
      component.ngOnInit();

      expect(component.modifire).toEqual('betslip');
    });

    it('should left set value', () => {
      component.modifire = 'quickbet';
      component.ngOnInit();

      expect(component.modifire).toEqual('quickbet');
    });
  });
});
