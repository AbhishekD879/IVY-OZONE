import { SbOverUnderMarketItemComponent } from './sb-over-under-market-item.component';

describe('SbOverUnderMarketItemComponent', () => {
  let component: SbOverUnderMarketItemComponent;

  beforeEach(() => {
    component = new SbOverUnderMarketItemComponent();
  });
  it('should create', () => {
    expect(component).toBeTruthy();
  });
  describe('ngOnInit', () => {
    it('should push teamHpoints and sort', () => {
      component.markets = [{
        rawHandicapValue: 1, outcomes: [
          { name: 'Team A and Over 3.5' },
          { name: 'Team B and Under 1.5' },
          { name: 'Team A and Under 3.5' }
        ]
      }, {
        rawHandicapValue: 2, outcomes: [
          { name: 'Team A and Over 3.5' },
          { name: 'Team B and Under 1.5' },
          { name: 'Team A and Under 3.5' }
        ]
      }] as any;
      component.ngOnInit();
      expect(component.teamHPoints).toEqual([1, 2]);
      expect(component.pointsToOutcome).toEqual({
        1: [
          { name: 'Team A and Over 3.5' },
          { name: 'Team B and Under 1.5' },
          { name: 'Team A and Under 3.5' }
        ], 2: [{ name: 'Team A and Over 3.5' },
        { name: 'Team B and Under 1.5' },
        { name: 'Team A and Under 3.5' }]
      });
    });
  });

  describe('handleCounterValueChange', () => {
    it('should assign currOutcomes and currPoints', () => {
      component.pointsToOutcome = { 1: { name: 'teamA' } };
      component['handleCounterValueChange'](1);
      expect(component.currOutcomes).toEqual({ name: 'teamA' } as any);
      expect(component.currPoints).toEqual(1);
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
