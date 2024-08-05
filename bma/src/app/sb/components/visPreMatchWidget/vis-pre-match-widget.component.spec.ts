import { VisPreMatchWidgetComponent } from './vis-pre-match-widget.component';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';

describe('VisPreMatchWidgetComponent', () => {
  let component: VisPreMatchWidgetComponent;

  let domSanitizer;
  let pubSubService;

  beforeEach(() => {
    domSanitizer = {
      bypassSecurityTrustResourceUrl: jasmine.createSpy('bypassSecurityTrustResourceUrl')
    };
    pubSubService = {
      API: pubSubApi,
      publish: jasmine.createSpy('publish')
    };

    component = new VisPreMatchWidgetComponent(domSanitizer, pubSubService);
  });

  it('should create component', () => {
    expect(component).toBeTruthy();
  });

  it('should create component', () => {
    component. ngOnInit();
    expect(domSanitizer.bypassSecurityTrustResourceUrl).toHaveBeenCalled();
  });

  describe('loadHandler', () => {
    it(`should publish SCOREBOARD_VISUALIZATION_LOADED event`, () => {
      component.loadHandler();

      expect(pubSubService.publish).toHaveBeenCalledWith(pubSubService.API.SCOREBOARD_VISUALIZATION_LOADED);
    });
  });
});
