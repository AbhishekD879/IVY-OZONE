import { SportEventComponent } from './sport-event.component';

describe('SportEventComponent -', () => {
  let component: SportEventComponent;

  let
    siteServerService,
    routingHelperService,
    router,
    activatedRoute,
    navigationService;

  const event = {foo: ''};

  beforeEach(() => {
    siteServerService = {
      getEventByEventId: jasmine.createSpy('getEventByEventId').and.returnValue(Promise.resolve(event))
    };
    routingHelperService = {
      getSportConfigName: jasmine.createSpy('getSportConfigName').and.returnValue('123'), // TODO remove this after refactoring
      formResultedEdpUrl: jasmine.createSpy('formResultedEdpUrl').and.returnValue('/foo')
    };
    router = jasmine.createSpyObj(['navigateByUrl']);
    activatedRoute = {snapshot: {paramMap: {
      get: jasmine.createSpy('get').and.returnValue(123)
    }}};
    navigationService = jasmine.createSpyObj('navigationService', ['handleHomeRedirect']);

    component = new SportEventComponent(
      siteServerService,
      routingHelperService,
      router,
      activatedRoute,
      navigationService
    );
  });

  it('constructor', () => {
    expect(component).toBeTruthy();
  });

  describe('@ngOnInit', () => {

    beforeEach(() => {
      component.ngOnInit();
    });

    it('should get sport id from route', () => {
      expect(activatedRoute.snapshot.paramMap.get).toHaveBeenCalledWith('sport');
      expect(component.sportId).toBe(123);
    });

    it('should get event by id', () => {
      expect(siteServerService.getEventByEventId).toHaveBeenCalledWith(123);
    });

    it('using event details should form and process full link', () => {
      siteServerService.getEventByEventId(111).then( (sportEvent) => {
        expect(sportEvent).toEqual(event);
        expect(routingHelperService.formResultedEdpUrl).toHaveBeenCalledWith(sportEvent);
        expect(router.navigateByUrl).toHaveBeenCalledWith('/foo');
      });
    });
  });

  it('should process to home page if no event given', () => {
    activatedRoute.snapshot.paramMap.get.and.returnValue('*');
    siteServerService.getEventByEventId.and.returnValue(Promise.resolve(null));
    component.ngOnInit();

    siteServerService.getEventByEventId(111).then( (sportEvent) => {
      expect(sportEvent).toEqual(null);
      expect(routingHelperService.formResultedEdpUrl).not.toHaveBeenCalled();
      expect(navigationService.handleHomeRedirect).toHaveBeenCalledWith('edp');
    });
  });

  it('should redirect to home page when invalid eventId', () => {
    activatedRoute.snapshot.paramMap.get.and.returnValue('i_love_coral');
    component.ngOnInit();

    expect(routingHelperService.formResultedEdpUrl).not.toHaveBeenCalled();
    expect(navigationService.handleHomeRedirect).toHaveBeenCalledWith('edp');
  });
});
