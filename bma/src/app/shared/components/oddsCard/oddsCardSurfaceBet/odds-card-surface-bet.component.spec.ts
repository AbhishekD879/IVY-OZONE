import { OddsCardSurfaceBetComponent } from './odds-card-surface-bet.component';
import { FracToDecService } from '@core/services/fracToDec/frac-to-dec.service';

describe('OddsCardSurfaceBetComponent', () => {
  let component: OddsCardSurfaceBetComponent,
    fracToDecService: Partial<FracToDecService>;
    const changeDetectorRef = {
      detectChanges: jasmine.createSpy('detectChanges'),
      detach: jasmine.createSpy('detach'),
    } as any;
  beforeEach(() => {
    fracToDecService = {
      getFormattedValue: jasmine.createSpy('getFormattedValue').and.returnValue('3/7')
    };
    component = new OddsCardSurfaceBetComponent(fracToDecService as FracToDecService);
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('#ngOnInit should not set old price', () => {
    component.surfaceBet = { markets: [{outcomes: [{name: null}]}] } as any;
    component.ngOnInit();
    expect(component.oldPrice).toEqual(undefined);
    expect(fracToDecService.getFormattedValue).not.toHaveBeenCalled();
  });

  it('#ngOnInit should set old price', () => {
    component.surfaceBet = {
      markets: [{
        outcomes: [{
          name: 'price (Was 3/7 )'
        }]
      }]
    } as any;

    component.ngOnInit();
    expect(fracToDecService.getFormattedValue).toHaveBeenCalledWith(3 as any, 7 as any);
    expect(component.oldPrice).toEqual('3/7');
  });

  it('#ngOnInit should set old price on Changes', () => {
    fracToDecService.getFormattedValue = jasmine.createSpy('getFormattedValue').and.callFake((a, b) => (`${a}/${b}`));

    component.surfaceBet = {
      markets: [{
        outcomes: [{
          name: 'price (Was 3/7 )'
        }]
      }]
    } as any;

    component.ngOnInit();
    expect(component.oldPrice).toEqual('3/7');

    component.surfaceBet = {
      markets: [{
        outcomes: [{
          name: 'price (Was 10/10 )'
        }]
      }]
    } as any;

    component.ngOnChanges();

    expect(component.oldPrice).toEqual('10/10');
  });


  it('#ngOnInit should not set surface bet background image url', () => {
    component.surfaceBet = {
      markets: [{
        outcomes: [{
          name: 'price (Was 3/7 )'
        }]
      }],
      svgBgImgPath: null
    } as any;
    component.ngOnInit();
    expect(component.oldPrice).toEqual('3/7');
  });




  describe('#ngOnChanges', () => {
    it('component isButton should be true', () => {
      component.surfaceBet = { markets: [{ outcomes: [{}] }] } as any;
      component.ngOnChanges();
      expect(component.isButton).toBeTruthy();
    });

    it('component isButton should be true', () => {
      component.surfaceBet = { markets: [] } as any;
      component.ngOnChanges();
      expect(component.isButton).toBeFalsy();
    });

    it('#ngOnChanges should set surface bet background image url', () => {
      component.surfaceBet = { markets: [], svgBgImgPath: '/images/svg/uploads/imageName.svg' } as any;
      component.ngOnChanges();
      expect(component.oldPrice).toBeUndefined();
    });

    it('#ngOnChanges should not set surface bet background image url', () => {
      component.surfaceBet = { markets: [], svgBgImgPath: null } as any;
      component.ngOnChanges();
      expect(component.oldPrice).toBeUndefined();
    });
  });

  describe('#setOldPrice', () => {
    it('component setOldPrice markets check', () => {
      component.surfaceBet = { markets: [] } as any;
      component['setOldPrice']();
      expect(component.oldPrice).toBeUndefined();
      expect(fracToDecService.getFormattedValue).not.toHaveBeenCalled();
    });

    it('component setOldPrice outcomes check', () => {
      component.surfaceBet = { markets: [{ outcomes: [{}] }] } as any;
      component['setOldPrice']();
      expect(component.oldPrice).toBeUndefined();
      expect(fracToDecService.getFormattedValue).not.toHaveBeenCalled();
    });
    
    it('component setOldPrice name check', () => {
      component.surfaceBet = { markets: [{ outcomes: [{name: null}] }] } as any;
      component['setOldPrice']();
      expect(component.oldPrice).toBeUndefined();
      expect(fracToDecService.getFormattedValue).not.toHaveBeenCalled();
    });

    it('component setOldPrice to set 3/7', () => {
      component.surfaceBet = { markets: [{ outcomes: [{name: 'price (Was 3/7 )'}] }] } as any;
      component['setOldPrice']();
      expect(component.oldPrice).toEqual('3/7');
      expect(fracToDecService.getFormattedValue).toHaveBeenCalled();
    });
  });

});
