import { VirtualSilkComponent } from '@shared/components/virtualSilk/virtual-silk.component';

describe('VirtualSilkComponent', () => {
  let component, virtualSharedService;

  beforeEach(() => {
    virtualSharedService = {
      getVirtualSilkSrc: jasmine.createSpy('getVirtualSilkSrc')
    };
    component = new VirtualSilkComponent(
      virtualSharedService
    );
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  describe('ngOnInit', () => {
    it('should set Silk Name if silkName exist', () => {
      component.event = {} as any;
      component.outcome = {
        silkName: '1'
      } as any;
      component.ngOnInit();
      expect(virtualSharedService.getVirtualSilkSrc).toHaveBeenCalledWith({}, '1');
    });

    it('should set Silk Name if racingForm exist', () => {
      component.event = {} as any;
      component.outcome = {
        racingFormOutcome: {
          silkName: '2'
        }
      } as any;
      component.ngOnInit();
      expect(virtualSharedService.getVirtualSilkSrc).toHaveBeenCalledWith({}, '2');
    });

    it('should not set Silk name if neither silkName nor racingForm exists', () => {
      component.event = {} as any;
      component.outcome = {} as any;

      component.ngOnInit();
      expect(virtualSharedService.getVirtualSilkSrc).not.toHaveBeenCalled();
    });
  });
});
