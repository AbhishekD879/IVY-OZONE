import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ProfitIndicatorComponent } from './profit-indicator.component';
import { CurrencyPipe } from '@angular/common';
import { CashoutSectionService } from '@app/betHistory/services/cashOutSection/cash-out-section.service';


describe('ProfitIndicatorComponent', () => {
  let currencyPipe: CurrencyPipe;
  let component: ProfitIndicatorComponent;
  let fixture: ComponentFixture<ProfitIndicatorComponent>;
  let cashoutSectionService: jasmine.SpyObj<CashoutSectionService>

  beforeEach(async () => {
    const cashOutServiceSpy = jasmine.createSpyObj('CashoutSectionService', ['getInitialStake'])
    await TestBed.configureTestingModule({
      declarations: [ProfitIndicatorComponent],
      providers: [CurrencyPipe, { provide: CashoutSectionService, useValue: cashOutServiceSpy }]
    })
      .compileComponents();

    fixture = TestBed.createComponent(ProfitIndicatorComponent);
    component = fixture.componentInstance;
    currencyPipe = TestBed.inject(CurrencyPipe)
    cashoutSectionService = TestBed.inject(CashoutSectionService) as jasmine.SpyObj<CashoutSectionService>;
    fixture.detectChanges();
  });

  it('should create component', () => {
    expect(component).toBeTruthy();
  });

  it('should not show profit indicator if returns are less than stake ', () => {
    cashoutSectionService.getInitialStake.and.returnValue('100')
    component.returns = '80';
    component.currencySymbol = '$';
    component.ngOnInit();
    expect(component.isProfit).toBeFalsy();
    expect(component.profitValueWithCurency).toBeUndefined();

  })

  it('should show profit indicator if returns are greater than stake', () => {
    cashoutSectionService.getInitialStake.and.returnValue('100')
    component.returns = '150';
    component.currencySymbol = '$';
    spyOn(currencyPipe, 'transform').and.returnValue('$50')
    component.ngOnInit();
    expect(component.isProfit).toBeTruthy();
    expect(component.profitValueWithCurency).toBe('$50');

  })

});
