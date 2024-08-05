import { FanzoneSelectYourTeamComponent } from './fanzone-select-your-team.component';

describe('FanzoneSelectYourTeamComponent', () => {
  let component: FanzoneSelectYourTeamComponent;

  beforeEach(() => {
    let cmsService, componentFactoryResolver, deviceService, dialogService, fanzoneSharedService, gtmService, localeService, pubSubService, route, routingState, storageService, userService, timeService, changeDetectorRef, fanzoneStorageService;
    component = new FanzoneSelectYourTeamComponent(
      cmsService as any,
      componentFactoryResolver as any,
      deviceService as any,
      dialogService as any,
      fanzoneSharedService as any,
      gtmService as any,
      localeService as any,
      pubSubService as any,
      route as any,
      routingState as any,
      storageService as any,
      userService as any,
      timeService as any,
      changeDetectorRef as any,
      fanzoneStorageService as any
    );
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});