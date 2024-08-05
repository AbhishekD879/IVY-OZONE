import { CorrectScoreComponent } from '@app/edp/components/markets/correctScore/correct-score.component';
import { SbCorrectScoreMarketItemComponent } from './sb-correct-score-market-item.component';

describe('SbCorrectScoreMarketItemComponent', () => {
  let component: SbCorrectScoreMarketItemComponent;
  let filterService;
  let correctScoreService;

  beforeEach(() => {
    component = new SbCorrectScoreMarketItemComponent(correctScoreService, filterService);
  });
  it('should create', () => {
    expect(component).toBeTruthy();
  });
  describe('ngOnInit', () => {
    it('should push teamHpoints,teamAPoints and sort', () => {
      spyOn(CorrectScoreComponent.prototype, 'ngOnInit');
      component.groupedOutcomes = [[{ outcomeMeaningScores: '1,2' }, { outcomeMeaningScores: '3,4' }]] as any
      component.ngOnInit();
      expect(component.teamHPoints).toEqual([1, 3]);
      expect(component.teamAPoints).toEqual([2, 4]);
    });
  });

  describe('handleCounterValueChange', () => {
    it('should assign value to teamHCounterValue', () => {
      spyOn(component, 'onScoreChange')
      component['handleCounterValueChange'](1, 'H');
      expect(component.teamHCounterValue).toEqual(1);
      expect(component.onScoreChange).toHaveBeenCalled();
    });
    it('should assign value to teamACounterValue', () => {
      spyOn(component, 'onScoreChange')
      component['handleCounterValueChange'](1, 'A');
      expect(component.teamACounterValue).toEqual(1);
      expect(component.onScoreChange).toHaveBeenCalled();
    });
  });

  describe('handleSelectionClick', () => {
    it('should emit the market', () => {
      component.selectionClickEmit.emit = jasmine.createSpy('selectionClickEmit.emit');
      component.handleSelectionClick({ name: 'Team A and Over 2.5' } as any);
      expect(component.selectionClickEmit.emit).toHaveBeenCalledOnceWith({ name: 'Team A and Over 2.5' } as any);
    });
  });
});
