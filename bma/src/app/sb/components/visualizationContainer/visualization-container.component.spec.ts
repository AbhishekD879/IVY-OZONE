import { VisualizationContainerComponent } from './visualization-container.component';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';

const visParams = [
  { id: '1', sportName: 'tennis', canDisplayCastro: true },
  { id: '2', sportName: 'basketball', canDisplayCastro: true },
  { id: '3', sportName: 'baseball', canDisplayCastro: true },
];

describe('#VisualizationContainerComponent', () => {
  let component: VisualizationContainerComponent,
      domSanitizer,
      pubSubService;

  beforeEach(() => {
    domSanitizer = {
      bypassSecurityTrustResourceUrl: jasmine.createSpy('domSanitizer.bypassSecurityTrustResourceUrl')
    };

    pubSubService = {
      API: pubSubApi,
      publish: jasmine.createSpy()
    };

    component = new VisualizationContainerComponent(domSanitizer, pubSubService);
  });

  describe('#ngOnInit', () => {
    it('Display visualization', () => {
      component.eventId = '1';
      component.visType = 'not-castro';
      component.expandable = false;
      component.visParams = visParams;
      component['VISUALIZATION_IFRAME_URL'] = '/vis-url';

      domSanitizer.bypassSecurityTrustResourceUrl.and.returnValue('/test-url');
      component.ngOnInit();

      expect(component['eventParams']).toEqual(component.visParams[0]);
      expect(component['canDisplayCastro']).toBeTruthy();
      expect(component.isVisualizationAvailable).toBeTruthy();
      expect(component['sportName']).toBe('tennis');
      expect(component.delta).toBe(33);
      expect(component['visUrl']).toBe('tennis-iframe.html');
      expect(domSanitizer.bypassSecurityTrustResourceUrl).toHaveBeenCalledWith('/vis-url/tennis-iframe.html#1:not-castro');
      expect(component.iframeURL).toBe('/test-url');
    });

    it('Do not display visualization', () => {
      component.eventId = '5';
      component.visType = 'castro';
      component.expandable = true;
      component.visParams = visParams;

      component.ngOnInit();

      expect(component['eventParams']).toBeUndefined();
      expect(component['canDisplayCastro']).toBeFalsy();
      expect(component['sportName']).toBe('football');
      expect(component.delta).toBe(0);
      expect(component['visUrl']).toBe('football/iframe.html');
    });
  });

  describe('loadHandler', () => {
    it(`should publish SCOREBOARD_VISUALIZATION_LOADED event`, () => {
      component.loadHandler();

      expect(pubSubService.publish).toHaveBeenCalledWith(pubSubService.API.SCOREBOARD_VISUALIZATION_LOADED);
    });
  });
});
