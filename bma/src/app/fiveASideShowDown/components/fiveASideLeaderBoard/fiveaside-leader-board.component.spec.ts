import { FiveASideLeaderBoardComponent
} from '@app/fiveASideShowDown/components/fiveASideLeaderBoard/fiveaside-leader-board.component';
import { of, throwError } from 'rxjs';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { USER_SHOWDOWN_DATA
} from '@app/fiveASideShowDown/components/fiveASideLiveLeaderBoard/fiveaside-live-leader-board.mock';
import { EVENTSTATUS } from '../../constants/constants';

describe('FiveasideLeaderBoardComponent', () => {
  let component: FiveASideLeaderBoardComponent;
  let activatedRoute,
  leaderBoardService,
  userService,
  pubSub,
  changeDetectorRef,
  navigationService,
  coreToolsService,
  bonusSuppression;
  beforeEach(() => {
    activatedRoute = {
      snapshot: {
        params: {
          id: '602f52152c05212d1b9336bc'
        }
      }
    };
    changeDetectorRef = {
      markForCheck: jasmine.createSpy('markForCheck')
    };
    leaderBoardService = {
      getContestInformationById: jasmine.createSpy('getContestInformationById').and.returnValue(of({contest:USER_SHOWDOWN_DATA})),
      setLeaderBoardData: jasmine.createSpy('setLeaderBoardData'),
      optInUserIntoTheContest: jasmine.createSpy('optInUserIntoTheContest')
    };
    pubSub = {
      subscribe: jasmine.createSpy(),
      publish: jasmine.createSpy(),
      unsubscribe: jasmine.createSpy(),
      API: pubSubApi
    };
    coreToolsService = {
      uuid: jasmine.createSpy('uuid')
    },
    userService = {
      username: 'username'
    };
    navigationService = {
      openRouterUrl: jasmine.createSpy()
    };

    bonusSuppression = {
      navigateAwayForRGYellowCustomer: jasmine.createSpy('navigateAwayForRGYellowCustomer'),
      checkIfYellowFlagDisabled: jasmine.createSpy('checkIfYellowFlagDisabled').and.returnValue(true)
    };

    component = new FiveASideLeaderBoardComponent(activatedRoute, leaderBoardService,
      userService, pubSub, changeDetectorRef, navigationService,coreToolsService, bonusSuppression);
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should initialize and subscribe in ngOnInit', () => {
    spyOn(component as any, 'subscribeToEventChange');
    spyOn(component as any, 'loginTrigger');
    component.ngOnInit();
    expect(component.leaderBoard).not.toBeNull();
    expect(component['subscribeToEventChange']).toHaveBeenCalled();
    expect(leaderBoardService.setLeaderBoardData).toHaveBeenCalled();
  });

  it('should unsubscribe in ngOnDestroy', () => {
    component.ngOnDestroy();
    expect(pubSub.unsubscribe).toHaveBeenCalledWith('FiveASideLeaderBoardComponent');
  });

  it('should set type to post when event is resulted', () => {
    component.leaderBoard = {} as any;
    component['handleResultedEvent']();
    expect(component.leaderBoard.type).toEqual('post');
  });

  it('should set type to Live when event is started', () => {
    component.leaderBoard = {} as any;
    component['handleLiveEvent']();
    expect(component.leaderBoard.type).toEqual('live');
  });

  it('should not initialize leaderboard, if service throws error', () => {
    leaderBoardService.getContestInformationById.and.returnValue(throwError({error: '404'}));
    component['getInitialLeaderboardData']();
    expect(component.leaderBoard).toBeUndefined();
    expect(navigationService.openRouterUrl).toHaveBeenCalled();
  });

  it('should make a transition after passing changeState value', () => {
    component['getInitialLeaderboardData'](EVENTSTATUS.POST);
    expect(component.leaderBoard.type).toEqual(EVENTSTATUS.POST);
  });

  describe('#optInUserIntoTheContest', () => {
    it('should call optInUserToTheContest API', () => {
      const leaderBoard = { isInvitationalContest: true, isPrivateContest : true  } as any;
      leaderBoardService.optInUserIntoTheContest.and.returnValue(of({}));
      component['optInUserIntoTheContest'](leaderBoard);
      expect(leaderBoardService.optInUserIntoTheContest).toHaveBeenCalled();
    });

    it('should not call optInUserToTheContest API if contestDto is null', () => {
      const leaderBoard = null as any;
      leaderBoardService.optInUserIntoTheContest.and.returnValue(of({}));
      component['optInUserIntoTheContest'](leaderBoard);
      expect(leaderBoardService.optInUserIntoTheContest).not.toHaveBeenCalled();
    });

    it('should not call optInUserToTheContest API if leaderBoard is null', () => {
      const leaderBoard = null as any;
      leaderBoardService.optInUserIntoTheContest.and.returnValue(of({}));
      component['optInUserIntoTheContest'](leaderBoard);
      expect(leaderBoardService.optInUserIntoTheContest).not.toHaveBeenCalled();
    });
  });

  describe('#loginTrigger', () => {
    it('if yellow flag enabled', () => {
      pubSub.subscribe.and.callFake((a, method, cb) => {
        cb();
      });
      bonusSuppression.checkIfYellowFlagDisabled = jasmine.createSpy('checkIfYellowFlagDisabled').and.returnValue(false);
      component['componentId'] = 'FiveASideLeaderBoardComponent';
      component['loginTrigger']();
      expect(pubSub.subscribe).toHaveBeenCalledWith('FiveASideLeaderBoardComponent',  [pubSub.API.SUCCESSFUL_LOGIN, pubSub.API.SESSION_LOGIN], jasmine.any(Function));
      expect(bonusSuppression.checkIfYellowFlagDisabled).toHaveBeenCalled();
      expect(bonusSuppression.navigateAwayForRGYellowCustomer).toHaveBeenCalled();
    });

    it('if yellow flag disabled', () => {
      pubSub.subscribe.and.callFake((a, method, cb) => {
        cb();
      });
      component['moduleName'] = 'abc';
      component['componentId'] = 'FiveASideLeaderBoardComponent';
      component['loginTrigger']();
      expect(pubSub.subscribe).toHaveBeenCalledWith('FiveASideLeaderBoardComponent',  [pubSub.API.SUCCESSFUL_LOGIN, pubSub.API.SESSION_LOGIN], jasmine.any(Function));
      expect(bonusSuppression.checkIfYellowFlagDisabled).toHaveBeenCalled();
      expect(bonusSuppression.navigateAwayForRGYellowCustomer).not.toHaveBeenCalled();
    });
  })
});
