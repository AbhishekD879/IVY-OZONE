import { PrizePoolComponent } from '@app/five-a-side-showdown/components/prize-pool/prize-pool.component';

describe('PrizePoolComponent', () => {
  let component: PrizePoolComponent;

  beforeEach(() => {
    component = new PrizePoolComponent();
    component.prizePool = {} as any;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('ngOnInit should initialize data', () => {
    spyOn(component as any, 'emitPrizePool');
    component.prizePool = { cash: 1} as any;
    component.poolData = {cash: 2} as any;
    component.ngOnInit();
    expect(component.form).not.toBeNull();
  });
  
  it('ngOnInit should emit prizepool data', () => {
    component.form = {
      valueChanges: {
        subscribe: jasmine.createSpy().and.callFake(cb => cb({cash: 1}))
      }
    } as any;
    component.prizePoolChanged = {
      emit: jasmine.createSpy()
    } as any;
    component['emitPrizePool']();
    expect(component.prizePoolChanged.emit).toHaveBeenCalled();
  });

  it('#test for block special chars ', () => {
    const event = {
      target: {
        value: '@@@@test123%%%&****((())_'
      }
    } as any;
    component.blockSpecialChars(event);
    expect(event.target.value).toEqual('test123');
  });
});
