import { CreateRacingEdpMarketComponent } from './create-racing-edp-market.component';

describe('CreateRacingEdpMarketComponent', () => {
  let component: CreateRacingEdpMarketComponent;
  let dialogRef;
  let brandService;

  beforeEach(() => {
    dialogRef = {
      close: jasmine.createSpy('close')
    };
    brandService = {
      brand: 'coral'
    };
    component = new CreateRacingEdpMarketComponent(dialogRef, brandService);
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should initialize racing edp market', () => {
    component.ngOnInit();
    expect(component.racingEdpMarket.brand).toBe('coral');
    expect(component.racingEdpMarket).not.toBeNull();
  });

  it('should return edp market', () => {
     component.racingEdpMarket = {
       name: 'Win way'
     } as any;
     const response = component.getNewEdpMarket();
     expect(response).not.toBeNull();
  });

  it('should return true if user enters market name', () => {
    component.racingEdpMarket = {
      name: 'Win way'
    } as any;
    const response = component.isValidEdpMarket();
    expect(response).toBeTrue();
  });

  it('should return false if user submits without entering name', () => {
    component.racingEdpMarket = {
      name: undefined
    } as any;
    const response = component.isValidEdpMarket();
    expect(response).toBeFalse();
  });

  it('should close dialog', () => {
    component.closeDialog();
    expect(dialogRef.close).toHaveBeenCalled();
  });
});
