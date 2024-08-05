import { SbSingleDropDownSingleOddComponent } from './sb-single-drop-down-single-odd.component';

describe('SbSingleDropDownSingleOddComponent', () => {
  let component: SbSingleDropDownSingleOddComponent;
  let templateService;
  beforeEach(() => {
    templateService = {
      sortOutcomesByPriceAndDisplayOrder: jasmine.createSpy('sortOutcomesByPriceAndDisplayOrder').and.returnValue([
        { name: 'Team A and Over 2.5' },
        { name: 'Team B and Under 1.5' },
        { name: 'Team A and Under 3.5' },
      ])
    };
    component = new SbSingleDropDownSingleOddComponent(templateService);
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  describe('ngOnInit', () => {
    it('should call getOutcomeNames', () => {
      spyOn(component as any, 'getOutcomeNames');
      const market = {
        outcomes: [
          { name: 'Team A and Over 2.5' },
          { name: 'Team B and Under 1.5' },
          { name: 'Team A and Under 3.5' },
        ]
      };
      component.market = market as any;

      component.ngOnInit();
      expect(component.getOutcomeNames).toHaveBeenCalledWith(component.market.outcomes as any);
    });
    it('should call getOutcomeNames and assign undefined to alteredOutcomes', () => {
      spyOn(component as any, 'getOutcomeNames');
      component.market = null;
      component.ngOnInit();
      expect(component.alteredOutComes).toBeUndefined();
    });
  });
  describe('getOutcomeNames', () => {
    it('should call templateService.sortOutcomesByPriceAndDisplayOrder and return formated outcomes', () => {
      const market = {
        outcomes: [
          { name: 'Team A and Over 2.5' },
          { name: 'Team B and Under 1.5' },
          { name: 'Team A and Under 3.5' },
        ]
      };
      component.market = market as any;

      component['getOutcomeNames'](component.market.outcomes as any);
      expect(templateService.sortOutcomesByPriceAndDisplayOrder).toHaveBeenCalled();
    });
  });

  describe('OnValuechange', () => {
    it('should assign to outcomeEntity', () => {
      const market = { outcomes: [{ name: '1' }] };
      component.market = market as any;
      component.onValueChange('1');
      expect(component.outcomeEntity as any).toEqual({ name: '1' })
    });
    it('should assign to outcomeEntity', () => {
      const market = null;
      component.market = market as any;
      component.onValueChange('1');
      expect(component.outcomeEntity as any).toBeUndefined();
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
