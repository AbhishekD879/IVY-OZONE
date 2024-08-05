import {StructureComponent} from './structure.component';
import { of } from 'rxjs';

describe('StructureComponent', () => {
  let component: StructureComponent;
  let globalLoaderService, configStructureAPIService, brandService;

  beforeEach(() => {
    globalLoaderService = {
      showLoader: jasmine.createSpy('showLoader'),
      hideLoader: jasmine.createSpy('hideLoader')
    };
    configStructureAPIService = {
      getStructureData: jasmine.createSpy('getStructureData').and.returnValue(of([{body: {config: 'test1'}}, {body: {config: 'test2'}}]))
    };
    brandService = {};
    component = new StructureComponent(
      globalLoaderService, configStructureAPIService, brandService
    );

    component.ngOnInit();
  });

  it('should call getStructureData', () => {
    expect(configStructureAPIService.getStructureData).toHaveBeenCalled();
  });
});
