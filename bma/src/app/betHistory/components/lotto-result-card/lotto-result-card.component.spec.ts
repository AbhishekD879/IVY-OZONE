import {fakeAsync,} from '@angular/core/testing';
import { LottoResultCardComponent } from './lotto-result-card.component';
import environment from '@environment/oxygenEnvConfig';

describe('LottoResultCardComponent', () => {
  let component: LottoResultCardComponent,
   locale,
   userService,
   timeService;
  
  beforeEach(fakeAsync(() => { 
    locale = {
      getString: jasmine.createSpy('getString').and.returnValue('test'),
      toLowerCase: jasmine.createSpy('toLowerCase')
     }; 
    userService = {
      currency: 'USD',
      oddsFormat : 'frac'
    };

    timeService = {
      convertDateStr: jasmine.createSpy('convertDateStr')
    };
    createComp();
  }));

  function createComp() {
    component = new LottoResultCardComponent(
      locale,
      userService,
      timeService
    )
  }

  it('should create', () => {
    expect(component).toBeDefined();
  });

  it('trackByBall should return joined string', () => {
    const index: number = 11;
    const item: any = {
      ballNo: '22'
    };
    const result = component.trackByBall(index, item);
    expect(result).toEqual('1122');
  });

  it('should call nginit() method',  () => {
    environment.brand = 'ladbrokes';
    component.lottoResult = { drawAt : '12/04/2023'} as any;
    const bma = {returned: "returned",drawresults: "drawresults",brands :'ladbrokes'};
    component.settled = 'N';
    component.ngOnInit();

    expect(component.lottoResult.drawAt).toEqual('12/04/2023');
    expect(bma.returned).toEqual('returned');
    expect(bma.drawresults).toEqual('drawresults');
    expect(component['locale'].getString).toHaveBeenCalled();
    expect(environment.brand).toEqual(bma.brands)

  }); 
  it('should call nginit() method',  () => {
    component.lottoResult = { drawAt : '12/04/2023'} as any;
    component.settled = 'Y';
    const bma = { returned: "returned", drawresults: "drawresults"};
    
    component.ngOnInit();
    expect(component.lottoResult.drawAt).toEqual('12/04/2023');
    expect(bma.returned).toEqual('returned');
    expect(bma.drawresults).toEqual('drawresults');
  
  }); 
});
