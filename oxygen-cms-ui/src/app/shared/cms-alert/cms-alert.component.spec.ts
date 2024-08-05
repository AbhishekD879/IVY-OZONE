import { async } from '@angular/core/testing';
import { CmsAlertComponent } from './cms-alert.component';

describe('CmsAlertComponent', () => {
  let component, globalLoaderService;

  beforeEach(async(() => {
    globalLoaderService = {};

    component = new CmsAlertComponent(
      globalLoaderService
    );

    component.ngOnInit();
  }));

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
