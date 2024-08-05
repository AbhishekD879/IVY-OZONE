import { GlobalLoaderService } from "./loader.service";

describe('GlobalLoaderService', () => {
  let service: GlobalLoaderService;

  beforeEach(() => {
    service = new GlobalLoaderService();
    service.isVisible = false;
  });

  it('#showLoader should set isVisible value to true', () => {
    service.showLoader();
    expect(service.isVisible).toEqual(true);
  });

  it('#hideLoader should set isVisible value to false', () => {
    service.isVisible = true;
    service.hideLoader();
    expect(service.isVisible).toEqual(false);
  });
});
