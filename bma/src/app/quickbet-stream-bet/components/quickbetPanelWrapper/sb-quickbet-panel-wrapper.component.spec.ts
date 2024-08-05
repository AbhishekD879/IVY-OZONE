import { SbQuickbetPanelWrapperComponent } from '@app/quickbet-stream-bet/components/quickbetPanelWrapper/sb-quickbet-panel-wrapper.component';

describe('SbQuickbetPanelWrapperComponent', () => {
  let component: SbQuickbetPanelWrapperComponent;
  let pubsubService;
  let changeDetectorRef;
  let cmsService;
  let remoteBsService;

  beforeEach(() => {

    pubsubService = {
      subscribe: jasmine.createSpy('subscribe'),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      API: {
        RENDER_QUICKBET_COMPONENT: 'RENDER_QUICKBET_COMPONENT'
      }
    };

    component = new SbQuickbetPanelWrapperComponent(
      pubsubService,
      changeDetectorRef,
      cmsService,
      remoteBsService
    );
  });

  it('should subscribe to pubsub event on init', () => {

    component.addListeners();
    expect(pubsubService.subscribe).toHaveBeenCalledWith('SbQuickbetPanelWrapperComponent',
      pubsubService.API.RENDER_QUICKBET_COMPONENT, component['renderQuickbet']);
  });

  it('should unsubscribe from pubsub event on destroy', () => {
    component.ngOnDestroy();
    expect(pubsubService.unsubscribe).toHaveBeenCalledWith('SbQuickbetPanelWrapperComponent');
  });

});
