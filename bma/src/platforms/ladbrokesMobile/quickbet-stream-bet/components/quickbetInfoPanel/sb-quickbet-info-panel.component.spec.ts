import { SbQuickbetInfoPanelComponent } from './sb-quickbet-info-panel.component';
import { Subject } from 'rxjs';
import { LadbrokesQuickbetInfoPanelComponent as QuickbetInfoPanelComponent } from '@ladbrokesMobile/quickbet/components/quickbetInfoPanel/quickbet-info-panel.component';

describe('SbQuickbetInfoPanelComponent', () => {
  let component: SbQuickbetInfoPanelComponent;
  let quickbetNotificationService;
  let pubsub;
  let router;
  let changeDetectorRef;

  beforeEach(() => {

    quickbetNotificationService = {
      snbMaxPayoutMsgSub: new Subject<string>()
    };

    component = new SbQuickbetInfoPanelComponent(
      quickbetNotificationService,
      pubsub,
      router,
      changeDetectorRef
    );

  });

  describe('#SbQuickbetInfoPanelComponent', () => {
    it('ngOnInit is called', () => {
      QuickbetInfoPanelComponent.prototype.ngOnInit = jasmine.createSpy('super.ngOnInit');
      component.ngOnInit();
      quickbetNotificationService.snbMaxPayoutMsgSub.next('Max. Payout limit exceeded');
      expect(component.maxPayoutMsg).toBe('Max. Payout limit exceeded');
    });
  });

})
