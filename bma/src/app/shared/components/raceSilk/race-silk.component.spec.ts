import { RaceSilkComponent } from './race-silk.component';
import { ISportEvent } from '@core/models/sport-event.model';
import { IOutcome } from '@core/models/outcome.model';

describe('RaceSilkComponent', () => {
  let component: RaceSilkComponent;
  let virtualSharedService;
  let raceOutcomeDetailsService;

  beforeEach(() => {
    virtualSharedService = {
      isVirtual() {
        return false;
      }
    };
    raceOutcomeDetailsService = {
      isGreyhoundSilk() {
        return false;
      },
      isGenericSilk() {
        return false;
      }
    };
    component = new RaceSilkComponent(
      virtualSharedService,
      raceOutcomeDetailsService
    );
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  describe('ngOnInit', () => {
    beforeEach(() => {
      component.eventEntity = {} as ISportEvent;
      component.outcomeEntity = {} as IOutcome;
    });

    it('should be virtual silk or other', () => {
      spyOn(virtualSharedService, 'isVirtual').and.returnValue(true);
      spyOn(raceOutcomeDetailsService, 'isGreyhoundSilk').and.returnValue(true);
      spyOn(raceOutcomeDetailsService, 'isGenericSilk').and.returnValue(true);
      component.outcomeEntity = { racingFormOutcome: { silkName : 'Any' } } as IOutcome;

      component.ngOnInit();
      expect(component.isVirtual).toBeTruthy();
      expect(component.isGreyhound).toBeFalsy();
      expect(component.isGeneric).toBeFalsy();
      expect(component.isUKorIRE).toBeFalsy();
    });

    it('should detect virtualSilk', () => {
      spyOn(virtualSharedService, 'isVirtual').and.returnValue(true);

      component.ngOnInit();
      expect(component.isVirtual).toBeTruthy();
    });

    it('should detect Greyhound silk', () => {
      spyOn(virtualSharedService, 'isVirtual').and.returnValue(false);
      spyOn(raceOutcomeDetailsService, 'isGreyhoundSilk').and.returnValue(true);
      component.eventEntity = { categoryId: '21'} as ISportEvent;

      component.ngOnInit();
      expect(component.isGreyhound).toBeTruthy();
    });

    it('should detect Generic silk', () => {
      spyOn(virtualSharedService, 'isVirtual').and.returnValue(false);
      spyOn(raceOutcomeDetailsService, 'isGenericSilk').and.returnValue(true);

      component.ngOnInit();
      expect(component.isGeneric).toBeTruthy();
    });

    it('should detect Generic silk with default silk', () => {
      spyOn(virtualSharedService, 'isVirtual').and.returnValue(false);
      spyOn(raceOutcomeDetailsService, 'isGenericSilk').and.returnValue(false);
      component.outcomeEntity = { racingFormOutcome: undefined } as IOutcome;
      component.eventEntity = { categoryId: '21'} as ISportEvent;
      component.isStreamBet = true;

      component.ngOnInit();
      expect(component.isGeneric).toBeTruthy();
    });

    it('should detect UK or IRE silk', () => {
      spyOn(virtualSharedService, 'isVirtual').and.returnValue(false);
      component.outcomeEntity = { racingFormOutcome: { silkName : 'Any' } } as IOutcome;

      component.ngOnInit();
      expect(component.isUKorIRE).toBeTruthy();
    });
  });
});
