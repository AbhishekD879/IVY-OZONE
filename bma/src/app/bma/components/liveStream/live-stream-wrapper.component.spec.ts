import { LiveStreamWrapperComponent } from './live-stream-wrapper.component';

describe('#LiveStreamWrapperComponent', () => {
  let location;

  let component: LiveStreamWrapperComponent;

  beforeEach(() => {
    location = {
      path: jasmine.createSpy('path')
    } as any;

    component = new LiveStreamWrapperComponent(location);
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });

  it('should show top bar if it is separate live stream page', () => {
    location.path.and.returnValue('live-stream');

    component.ngOnInit();

    expect(component.isTopBarShown).toBeTruthy();
  });

  it('should now show top bar if it is live stream tab on home page', () => {
    location.path.and.returnValue('home');

    component.ngOnInit();

    expect(component.isTopBarShown).toBeFalsy();
  });

  it('childComponentLoaded should set initialized to true', () => {
    component.childComponentLoaded();
    expect(component.initialized).toBeTruthy();
  });
});

