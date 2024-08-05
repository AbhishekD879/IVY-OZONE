import { ImageManagerListComponent } from '@app/image-manager/image-manager-list/image-manager-list.component';
import { of } from 'rxjs';

describe('ImageManagerListComponent', () => {
  let dialogService;
  let imageManagerService;
  let component;
  let globalLoaderService;
  let sanitizer;

  beforeEach(() => {
    dialogService = {
      showDeleteDialog: jasmine.createSpy('dialogService')
    };
    imageManagerService = {
      deleteAndUpdateList: jasmine.createSpy('imageManagerService'),
      getData: jasmine.createSpy('getData').and.returnValues(of('data'))
    };
    globalLoaderService = {
      showLoader: jasmine.createSpy('showLoader'),
      hideLoader: jasmine.createSpy('hideLoader')
    };
    sanitizer = {
      bypassSecurityTrustHtml: jasmine.createSpy('bypassSecurityTrustHtml'),
    };

    component = new ImageManagerListComponent(dialogService, imageManagerService, globalLoaderService, sanitizer);

  });

  it('ngOnInit', () => {
    component.ngOnInit();
    expect(component.tableDataList).toBe('data');
  });

  it('should call showDeleteDialog', () => {
    const image = {
      svgId: '1',
      id: '2'
    } as any;
    component.removeHandler(image);

    expect(component.dialogService.showDeleteDialog).toHaveBeenCalled();
  });

  it('should call deleteAndUpdateList', () => {
    component.tableDataList = 'data';
    const image = {
      svgId: '1',
      id: '2'
    } as any;

    component.dialogService.showDeleteDialog = (params) => {
      params.deleteCallback();
    };
    component.removeHandler(image);

    expect(component.imageManagerService.deleteAndUpdateList).toHaveBeenCalledWith('data', '2');
  });
});
