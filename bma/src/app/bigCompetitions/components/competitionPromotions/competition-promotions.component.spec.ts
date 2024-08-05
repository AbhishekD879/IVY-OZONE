import { CompetitionPromotionsComponent } from '@app/bigCompetitions/components/competitionPromotions/competition-promotions.component';

describe('CompetitionPromotionsComponent', () => {
  let component;
  let user;
  let bonusSuppressionService;
  beforeEach(() => {
    bonusSuppressionService = {
      navigateAwayForRGYellowCustomer: jasmine.createSpy('navigateAwayForRGYellowCustomer'),
      checkIfYellowFlagDisabled: jasmine.createSpy('checkIfYellowFlagDisabled').and.returnValue(false)
    }
    component = new CompetitionPromotionsComponent(bonusSuppressionService);
  });

  describe('ngOnInit', () => {
    it('should select promotions as empty array if no promotionsData in moduleConfig', () => {
      component.moduleConfig = {};
      component.ngOnInit();

      expect(component.promotions).toEqual([]);
    });

    it('should select promotions as empty array if no promotions in promotionsData', () => {
      component.moduleConfig = {
        promotionsData: {}
      };
      component.ngOnInit();

      expect(component.promotions).toEqual([]);
    });

    it('should select promotions from promotionsData in moduleConfig', () => {
      const promotions = [{ id: 1 }];

      component.moduleConfig = {
        promotionsData: {
          promotions
        }
      };
      component.ngOnInit();

      expect(component.promotions).toEqual(promotions);
    });
  });
});
