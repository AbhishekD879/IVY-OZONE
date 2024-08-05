import { VirtualTopSportsComponent } from './virtual-top-sports.component';

describe('VirtualSportsPageComponent', () => {
  let component: VirtualTopSportsComponent;
  let router;
  let windowRef;
  let deviceService;
  let virtualHubService;


  beforeEach(() => {

    router = {
      navigate: jasmine.createSpy(),
      navigateByUrl: jasmine.createSpy('navigateByUrl'),
    };
    windowRef = {
      nativeWindow: {
        setInterval: window.setInterval,
        open: jasmine.createSpy('open')
      }
    }

    virtualHubService = {
      onClickNavigationDetails: {
        id:'',
        sportInfo: null
      }
    }
    deviceService = {}

    component = new VirtualTopSportsComponent(router, windowRef, virtualHubService, deviceService);
  });


  it('should call ngOnInit', () => {
    component.ngOnInit();
  });

  it('should call onSportClickGTMEvent and navigate to the redirection URL', () => {
    const imageInfo = {
      redirectionURL: 'http://abc.com',
    };
    component.goToVirtualSports(imageInfo as any);
    expect(windowRef.nativeWindow.open).toHaveBeenCalledWith(imageInfo.redirectionURL, '_self');
    expect(router.navigateByUrl).not.toHaveBeenCalled();
  });
  it('should call onSportClickGTMEvent and navigate to the redirection URL', () => {
    const imageInfo = {
      redirectionURL: 'https://www.example.com/#!?parameter=value',
    };
    component.goToVirtualSports(imageInfo as any);
    expect(windowRef.nativeWindow.open).toHaveBeenCalledWith(
      'https://www.example.com/#!?parameter=value',
      '_self'
    );
    expect(router.navigateByUrl).not.toHaveBeenCalled();
  });

  it('should open external URL do not containing http || #!? ', () => {
    const imageInfo = {
      redirectionURL: 'www.abc.com',
    };
    component.goToVirtualSports(imageInfo as any);
    expect(router.navigateByUrl).toHaveBeenCalledWith('www.abc.com');
  });

  it('should update backgroundPosition correctly based on scroll position', () => {
    const eventData: Partial<Event> = {
      target: {
        scrollLeft: 100,
      } as any,
    };
    const element: Partial<HTMLElement> = {
      style: {} as any,
    };
    spyOn(document, 'querySelector').and.returnValue(element as any);
    component.onScroll(eventData as Event);
    expect(element.style.backgroundPosition).toBe('-150px 0px');
  });


});