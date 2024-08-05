import { FallbackScoreboardComponent } from '@edp/components/fallbackScoreboard/fallback-scoreboard.component';

describe('FallbackScoreboardComponent', () => {
  let component: FallbackScoreboardComponent;

  beforeEach(() => {
    component = new FallbackScoreboardComponent();

  });

  describe('@onInit', () => {
    it('should set isBoxScore to true when scoreType is BoxScore', () => {
      component['scoreType'] = 'BoxScore';
      component.ngOnInit();

      expect(component.isBoxScore).toBeTruthy();
    });

    it('should set isBoxScore to true when scoreType is SetsPoints', () => {
      component['scoreType'] = 'SetsPoints';
      component.ngOnInit();

      expect(component.isBoxScore).toBeTruthy();
    });

    it('should set isBoxScore to true when scoreType is GamesPoints', () => {
      component['scoreType'] = 'GamesPoints';
      component.ngOnInit();

      expect(component.isBoxScore).toBeTruthy();
    });

    it('should set isBoxScore to true when scoreType is SetsGamesPoints', () => {
      component['scoreType'] = 'SetsGamesPoints';
      component.ngOnInit();

      expect(component.isBoxScore).toBeTruthy();
    });

    it('should set isBoxScore to true when scoreType is Simple', () => {
      component['scoreType'] = 'Simple';
      component.ngOnInit();

      expect(component.isBoxScore).toBeFalsy();
    });
  });
});

