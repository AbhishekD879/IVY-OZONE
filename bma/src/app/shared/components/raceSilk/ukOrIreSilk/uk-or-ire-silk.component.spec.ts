import { UkOrIreSilkComponent } from './uk-or-ire-silk.component';

describe('UkOrIreSilkComponent', () => {
  let component: UkOrIreSilkComponent;
  let raceOutcomeDetailsService;

  beforeEach(() => {
    raceOutcomeDetailsService = {
      getSilkStyle: jasmine.createSpy('getSilkStyle')
    };
    component = new UkOrIreSilkComponent(
      raceOutcomeDetailsService
    );
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  describe('ngOnInit', () => {
    it('should call getSilkStyle', () => {
      component.eventEntity = {
        markets: [
          'market'
        ]
      } as any;
      component.outcomeEntity = 'outcome' as any;
      component.ngOnInit();
      expect(raceOutcomeDetailsService.getSilkStyle).toHaveBeenCalledWith('market', 'outcome', '', false, undefined);
    });
  });
});
