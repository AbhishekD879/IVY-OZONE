import { SbMultipleOddsMarketItemComponent } from './sb-multiple-odds-market-item.component';
import { EventEmitter } from '@angular/core';

describe('SbMultipleOddsMarketItemComponent', () => {
  let component: SbMultipleOddsMarketItemComponent;
  let templateService;
  let streamBetService; 

  beforeEach(() => {
    templateService = {
      sortOutcomesByPriceAndDisplayOrder: jasmine.createSpy('sortOutcomesByPriceAndDisplayOrder').and.returnValue([]),
      sortOutcomesByPrice: jasmine.createSpy('sortOutcomesByPrice').and.returnValue([]),
    } as any;
  
    streamBetService = {
      multiOddMarketCounter: 0,
      totalMultiOddMarketElemsCount: 0,
      lastTemplateLoadedSubj: new EventEmitter(),
    } as any;

    component = new SbMultipleOddsMarketItemComponent(templateService, streamBetService);    
  });

  it('should create the component', () => {
    expect(component).toBeTruthy();
  });

  it('should handle ngOnInit', () => {
    component.market = { outcomes: [] as any } as any;
    component.event = {} as any;
    component.ngOnInit();
    expect(component['templateService'].sortOutcomesByPriceAndDisplayOrder).toHaveBeenCalled();
    expect(component['templateService'].sortOutcomesByPrice).toHaveBeenCalled();
    expect(component.newOutcomes.length).toBe(0);
    expect(component['streamBetService'].multiOddMarketCounter).toBe(1);
  });

  it('should handle ngOnInit#1', () => {
    component.market = { outcomes: [{id: 1, displayOrder: 1}, {id: 2, displayOrder: 2}, {id: 3, displayOrder: 3}] as any } as any;
    component.event = {} as any;
    component.ngOnInit();
    expect(component['templateService'].sortOutcomesByPriceAndDisplayOrder).toHaveBeenCalled();
    expect(component['streamBetService'].multiOddMarketCounter).toBe(1);
  });

  it('should handle ngOnInit with different displayOrder', () => {
    component.market = { outcomes: [{id: 1, displayOrder: -90}, {id: 2, displayOrder: -80}] as any } as any;
    component.ngOnInit();
    expect(component.sortOutcomesDisplayOrder(component.market.outcomes)).toEqual(1);
  });

  it('should handle ngOnInit with different displayOrder#1', () => {
    component.market = { outcomes: [{id: 1, displayOrder: 90}, {id: 2, displayOrder: 80}] as any } as any;
    component.ngOnInit();
    expect(component.sortOutcomesDisplayOrder(component.market.outcomes)).toEqual(-1)
  });

  it('should handle ngOnInit with same displayOrder', () => {
    component.market = { outcomes: [{id: 1, displayOrder: 90}, {id: 2, displayOrder: 90}] as any } as any;
    component.ngOnInit();
    expect(component.sortOutcomesDisplayOrder(component.market.outcomes)).toEqual(0);
  });

  it('should handle handleSelectionClick correctly', () => {
    const mockMarket = {} as any;
    spyOn(component.selectionClickEmit, 'emit');
    component.handleSelectionClick(mockMarket);
    expect(component.selectionClickEmit.emit).toHaveBeenCalledWith(mockMarket);
  });

  it('should handle ngAfterViewInit correctly', () => {
    component.currTemplateNumber = 1;
    component['streamBetService'].totalMultiOddMarketElemsCount = 1;
    spyOn(component['streamBetService'].lastTemplateLoadedSubj, 'next');
    component.ngAfterViewInit();
    expect(component['streamBetService'].lastTemplateLoadedSubj.next).toHaveBeenCalled();
  });
});
