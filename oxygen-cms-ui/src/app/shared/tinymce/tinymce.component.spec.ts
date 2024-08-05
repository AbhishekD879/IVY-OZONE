import { TestBed } from '@angular/core/testing';
import { ApiClientService } from '@app/client/private/services/http';
import { of, throwError } from 'rxjs';
import { TinymceComponent } from './tinymce.component';

describe('TinymceComponent', () => {
  let component,
    dialogService,
    snackBar,
    apiClientService,
    tinymceService;

  (global as any).tinymce = {
    PluginManager: {
      add: jasmine.createSpy('tinymce.PluginManager.add')
    },
    init: jasmine.createSpy('tinymce.init')
  };

  beforeEach(() => {
    dialogService = {
      showNotificationDialog: jasmine.createSpy('showNotificationDialog').and.callThrough()
    };
    snackBar = {
      open: jasmine.createSpy('open').and.callThrough()
    };
    apiClientService = {
      tinymceService: () => tinymceService
    };
    tinymceService = {
      uploadImage: jasmine.createSpy('uploadImage').and.returnValue(of({ body: {} }))
    };
    component = new TinymceComponent(
      dialogService,
      snackBar,
      apiClientService
    );

    component.ngAfterViewInit();
    TestBed.configureTestingModule({
      providers: [ApiClientService]
    });
  });

  it('should init tinymce Lib plugin and view', () => {
    expect(global['tinymce'].init).toHaveBeenCalled();
    expect(global['tinymce'].PluginManager.add).toHaveBeenCalled();
  });

  it('should construct a html table template on csv upload', () => {
    const data = {
      body: [{ name: 'PK', role: 'SA', rank: '1' }]
    };
    const tableHTML = component.createTableFromFile(data);
    expect(tableHTML).toBeDefined();
  });

  it('should call upload table service', async () => {
    const pagename = 'promotion';
    const formData = new FormData();
    component.handleTableUpload(pagename, 'pageId', formData, 'table');
    expect(tinymceService.uploadImage).toHaveBeenCalled();
  });

  it('should call upload image service', async () => {
    const pagename = 'promotion';
    const formData = new FormData();
    component.handleImageUpload(pagename, 'pageId', formData, 'table');
    expect(tinymceService.uploadImage).toHaveBeenCalled();
  });

  it('should call handleTableUpload for file input method', async () => {
    spyOn(component, 'handleTableUpload');
    component.handleFileInputChange({ target: { files: 'file', value: 'value' } }, 'table');
    expect(component.handleTableUpload).toHaveBeenCalled();
  });

  it('should not call handleTableUpload for file input method', async () => {
    spyOn(component, 'handleTableUpload');
    spyOn(component, 'handleImageUpload');
    component.handleFileInputChange({ target: { files: 'file', value: 'value' } }, 'tabless');
    expect(component.handleTableUpload).not.toHaveBeenCalled();
    expect(component.handleImageUpload).toHaveBeenCalled();
  });

  it('error case', async () => {
    tinymceService = {
      uploadImage: jasmine.createSpy('uploadImage').and.returnValue(throwError({ status: 404 }))
    };
    const pagename = 'promotion';
    const formData = new FormData();
    component.handleImageUpload(pagename, 'pageId', formData, 'table');
    expect(dialogService.showNotificationDialog).toHaveBeenCalled();
  });
});
