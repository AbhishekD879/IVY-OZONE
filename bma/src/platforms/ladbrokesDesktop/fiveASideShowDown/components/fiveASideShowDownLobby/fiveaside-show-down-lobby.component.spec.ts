import {
  FiveASideShowDownLobbyComponent
} from '@ladbrokesDesktop/fiveASideShowDown/components/fiveASideShowDownLobby/fiveaside-show-down-lobby.component';
import { T_AND_C } from '@app/fiveASideShowDown/components/fiveASideTermsRules/fiveaside-terms-rules.mock';
import { of } from 'rxjs';

describe('ShowDownLobbyComponent', () => {
  let component: FiveASideShowDownLobbyComponent;
  const fiveASideShowDownLobbyService = null;
  const fiveAsideLiveServeUpdatesSubscribeService = null;
  const userService = null;
  let gtmService, changeDetectorRef = null, cmsService = null, liveServeService,navigationService;
  const timeService = null;
  const windowRef = null;
  const pubSubService = null;
  const device = null;

  beforeEach(() => {
    gtmService = {
      push: jasmine.createSpy('push')
    };
    changeDetectorRef = {
      detectChanges: jasmine.createSpy('detectChanges')
    };
    cmsService = {
      getTermsAndConditions: jasmine.createSpy('getTermsAndConditions').and.returnValue(of(T_AND_C))
    };
    liveServeService = {
      connect: jasmine.createSpy('connect').and.returnValue(of({}))
    };
    navigationService = {}
    component = new FiveASideShowDownLobbyComponent(fiveASideShowDownLobbyService,
      fiveAsideLiveServeUpdatesSubscribeService,
      userService, gtmService, windowRef, changeDetectorRef, timeService, cmsService, pubSubService, device,
      liveServeService,navigationService);
  });

  it('should create component', () => {
    expect(component).toBeTruthy();
  });
});
