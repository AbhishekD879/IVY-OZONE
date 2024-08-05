import { InformationDialogComponent } from '@sharedModule/components/informationDialog/information-dialog.component';
import { InfoDialogComponent } from '@app/questionEngine/components/shared/infoDialog/info-dialog.component';

describe('InfoDialogComponent', () => {
  let component: InfoDialogComponent;

  let deviceService,
      rendererService,
      windowRef,
      pubSubService,
      navigationService,
      gtmService;

  beforeEach(() => {
    deviceService = jasmine.createSpy('deviceService');
    rendererService = jasmine.createSpy('rendererService');
    windowRef = jasmine.createSpy('windowRef');
    pubSubService = jasmine.createSpy('pubSubService');
    navigationService = jasmine.createSpy('navigationService');
    gtmService = jasmine.createSpy('gtm');

    component = new InfoDialogComponent(
      deviceService as any,
      rendererService as any,
      windowRef as any,
      pubSubService as any,
      navigationService as any,
      gtmService as any
    );
  });

  it('should create', () => {
    expect(component).toBeDefined();
  });

  it('should extend InformationDialogComponent', () => {
    expect(component instanceof InformationDialogComponent).toBeTruthy();
  });
});
