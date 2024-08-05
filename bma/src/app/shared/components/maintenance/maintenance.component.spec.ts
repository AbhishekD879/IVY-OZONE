import { MaintenanceComponent } from '@shared/components/maintenance/maintenance.component';

describe('MaintenanceComponent', () => {
  let component: MaintenanceComponent;

  let activatedRoute;
  let rendererService;
  let pubSubService;
  let routingUtilsService;
  let reloadDataCb;

  const pageData = {
    uriOriginal: '/img',
    targetUri: '/target'
  };

  beforeEach(() => {
    activatedRoute = {
      snapshot: {
        data: {
          data: pageData
        }
      }
    };

    pubSubService = {
      subscribe: jasmine.createSpy('subscribe').and.callFake((file, method, callback) => {
        if (method === 'MAINTENANCE_PAGE_DATA_CHANGED') {
          reloadDataCb = callback;
        }
      }),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      API: {
        MAINTENANCE_PAGE_DATA_CHANGED: 'MAINTENANCE_PAGE_DATA_CHANGED'
      }
    };

    rendererService = {
      renderer: jasmine.createSpyObj(['addClass', 'removeClass'])
    };

    routingUtilsService = jasmine.createSpyObj(['openUrl']);

    component = new MaintenanceComponent(activatedRoute, rendererService, routingUtilsService, pubSubService);
  });

  it('constructor', () => {
    expect(component).toBeDefined();
    expect(component.CMS_ROOT_URI).toContain('cms');
  });

  describe('ngOnInit', () => {

    it('should initialize properties using route data', () => {
      component.reloadData = jasmine.createSpy('reloadData');
      component.ngOnInit();
      reloadDataCb();

      expect(component.imagePath).toContain(pageData.uriOriginal);
      expect(component.buttonTarget).toBe(pageData.targetUri);
      expect(pubSubService.subscribe).toHaveBeenCalledWith('maintenance', 'MAINTENANCE_PAGE_DATA_CHANGED', jasmine.any(Function));
      expect(component.reloadData).toHaveBeenCalled();
    });

    it('should initialize properties using route data (url fallback)', () => {
      activatedRoute.snapshot.data.data.targetUri = '';
      component.ngOnInit();

      expect(component.buttonTarget).toBe('/');
    });

    it('should skip ini (no data fallback)', () => {
      activatedRoute.snapshot.data = {};
      component.ngOnInit();

      expect(component.imagePath).not.toBeDefined();
      expect(component.buttonTarget).not.toBeDefined();
      expect(rendererService.renderer.addClass).not.toHaveBeenCalled();
    });

    it('should modify content adding class on body', () => {
      component.ngOnInit();

      expect(rendererService.renderer.addClass).toHaveBeenCalledWith(jasmine.anything(), 'maintenance');
    });

    it('should replace data with new data from cms', () => {
      component.data = <any>{
        targetUri: 'test'
      };
      component.ngOnInit();

      expect(component.buttonTarget).toBe('test');
    });
  });

  describe('ngOnDestroy', () => {

    it('should modify content removing class on body', () => {
      component.ngOnDestroy();

      expect(rendererService.renderer.removeClass).toHaveBeenCalledWith(jasmine.anything(), 'maintenance');
    });
  });

  describe('reloadData', () => {
    it('should reinit component with new data', () => {
      const data = <any>{
        targetUri: 'test'
      };
      component.ngOnInit = jasmine.createSpy('ngOnInit');
      component.ngOnDestroy = jasmine.createSpy('ngOnDestroy');
      component.reloadData(data);
      expect(component.ngOnInit).toHaveBeenCalled();
      expect(component.ngOnDestroy).toHaveBeenCalled();
      expect(component.data).toEqual(data);
    });
  });

  describe('reloadOrNavigate', () => {

    it('should delegate click handling to service', () => {
      component.buttonTarget = '/foo';
      component.reloadOrNavigate();

      expect(routingUtilsService.openUrl).toHaveBeenCalledWith('/foo', true);
    });
  });
});
