import { ToteInfoComponent } from './tote-info.component';
import { of as observableOf } from 'rxjs';

describe('ToteInfoComponent', () => {
  let component: ToteInfoComponent, cmsService;

  beforeEach(() => {
    cmsService = {
      getItemSvg: jasmine.createSpy('cmsService.getItemSvg')
    };

    component = new ToteInfoComponent(cmsService);
  });

  it('ngOnInit with svg', () => {
    cmsService.getItemSvg.and.returnValue(observableOf({svg: 'test', svgId: '1'}));
    component.ngOnInit();

    expect(cmsService.getItemSvg).toHaveBeenCalled();
    expect(component.svg).toBe('test');
    expect(component.svgId).toBe('1');
  });

  it('ngOnInit without svg', () => {
    cmsService.getItemSvg.and.returnValue(observableOf(null));
    component.ngOnInit();

    expect(component.svg).toBeNull();
    expect(component.svgId).toBeNull();
  });
});
