import { GhSilkComponent } from './gh-silk.component';

describe('GreyhoundSilkComponent', () => {
  let component: GhSilkComponent;

  beforeEach(() => {
    component = new GhSilkComponent();
    component.event = {
      typeFlagCodes: 'UK,NONE,'
    } as any;
    component.outcome = {
      runnerNumber: '1'
    } as any;
  });

  describe('@ngOnInit', () => {
    it('event-outcome', () => {
      component.ngOnInit();
      expect(component.greyhoundClass).toBe('runner-deflt-gh1');
    });

    it('for racing-post-pick', () => {
      component.postPickSilk = 3;
      component.ngOnInit();
      expect(component.greyhoundClass).toBe('runner-deflt-gh3');
    });
  });


  describe('@getCountryFlag', () => {
    it('default', () => {
      expect(component['getCountryFlag']()).toBe('-deflt');
    });

    it('US', () => {
      component.event.typeFlagCodes = 'NONE,US,OTHER,';
      expect(component['getCountryFlag']()).toBe('-us');
    });

    it('AU', () => {
      component.event.typeFlagCodes = 'NONE,AU,';
      expect(component['getCountryFlag']()).toBe('-au');
    });
  });
});
