import { async } from '@angular/core/testing';
import { CmsUploadComponent } from './cms-upload.component';

describe('CmsUploadComponent', () => {
  let component,
    dialogService;

  beforeEach(async(() => {
    dialogService = {};

    component = new CmsUploadComponent(
      dialogService
    );

    component.ngOnInit();
  }));

  it('should create', () => {
    expect(component.label).toEqual('Filename');
  });
});
