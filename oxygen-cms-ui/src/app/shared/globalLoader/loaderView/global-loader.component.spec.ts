import {GlobalLoaderComponent} from './global-loader.component';

describe('GlobalLoaderComponent', () => {
  let component,
    globalLoaderService;

  beforeEach(() => {
    globalLoaderService = {
      isVisible: true
    };

    component = new GlobalLoaderComponent(
      globalLoaderService
    );
  });

  it('should set property', () => {
    expect(component.isVisible).toEqual(globalLoaderService.isVisible);
  });
});
