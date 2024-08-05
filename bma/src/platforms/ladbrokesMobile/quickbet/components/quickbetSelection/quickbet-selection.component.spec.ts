import { LadbrokesQuickbetSelectionComponent } from '@ladbrokesMobile/quickbet/components/quickbetSelection/quickbet-selection.component';
import { of } from 'rxjs';
import { IAvailableContests } from '@app/fiveASideShowDown/models/available-contests.model';
import { CONTESTS } from '@app/lazy-modules/fiveASideShowDown/components/fiveASideContestSelection/fiveaside-contest-selection.mock';
import { BYBBet } from '@app/yourCall/models/bet/byb-bet';

describe('LadbrokesQuickbetSelectionComponent', () => {
  let pubSubService;
  let userService;
  let localeService;
  let filtersService;
  let quickbetDepositService;
  let quickbetService;
  let quickbetUpdateService;
  let freeBetsService;
  let quickbetNotificationService;
  let commandService;
  let cmsService;
  let component: LadbrokesQuickbetSelectionComponent;
  let gtmService;
  let windowRef;
  let cdr;
  let timeService;
  let bppProviderService;
  let fiveASideContestSelectionService;
  let contests: IAvailableContests[];
  let serviceClosureService;
  let sessionStorageService;
  let bonusSuppressionService;
  let storageService;

  beforeEach(() => {
    pubSubService = {};
    userService = {};
    localeService = {
      getString: jasmine.createSpy().and.returnValue('test_str')
    };
    filtersService = {};
    quickbetDepositService = {};
    quickbetService = {};
    quickbetUpdateService = {};
    freeBetsService = {};
    quickbetNotificationService = {};
    commandService = {};
    cmsService = {};
    gtmService = {};
    cdr = {};
    windowRef = {
      nativeWindow: {
        addEventListener: jasmine.createSpy('addEventListener'),
        removeEventListener: jasmine.createSpy('removeEventListener'),
        setTimeout: jasmine.createSpy('setTimeout')
      }
    };
    windowRef = {
      nativeWindow: {
        addEventListener: jasmine.createSpy('addEventListener'),
        removeEventListener: jasmine.createSpy('removeEventListener'),
        setTimeout: jasmine.createSpy('setTimeout')
      }
    };
    timeService = jasmine.createSpyObj(['qbCountDownTimer']);
    bppProviderService = {
      quickBet: jasmine.createSpy('quickBet')
    };
    serviceClosureService = {
      checkUserServiceClosureStatus : jasmine.createSpy('checkUserServiceClosureStatus')
    };

    fiveASideContestSelectionService = {
      getAllActiveFiveASideContests: jasmine.createSpy('getAllActiveFiveASideContests'),
      validateRoleBasedContests: jasmine.createSpy('validateRoleBasedContests'),
      defaultSelectedContest: '61b2f0372cb30f010f8fa61b'
    };

    bonusSuppressionService = {
      checkIfYellowFlagDisabled: jasmine.createSpy('checkIfYellowFlagDisabled').and.returnValue(true)
    };

    contests = CONTESTS;

    component = new LadbrokesQuickbetSelectionComponent(pubSubService, userService, localeService, filtersService,
      quickbetDepositService, quickbetService, quickbetUpdateService, freeBetsService, quickbetNotificationService, commandService,
      cmsService, gtmService, cdr, windowRef, timeService, bppProviderService, fiveASideContestSelectionService, serviceClosureService, sessionStorageService, storageService, bonusSuppressionService);
  });

  describe('@showMessage', () => {
    it('should show deposit message', () => {
      component.infoPanel = {
        msg: 'err',
        location: 'quick-deposit',
        type: 'error'
      };
      expect(component.showMessage()).toBe(true);
    });

    it('should show boosted price change message', () => {
      component.isBoostEnabled = true;
      component.selection = {
        oddsBoost: {},
        price: { isPriceChanged: true },
        isBoostActive: true
      } as any;
      expect(component.showMessage()).toBe(true);
    });

    it('should not show message', () => {
      expect(component.showMessage()).toBe(false);
    });
  });

  describe('executeFiveASideResponse', () => {
    it('if response is empty', () => {
      component.fiveASideContests = contests;
      fiveASideContestSelectionService.defaultSelectedContest = '';
      component.defaultSelectedContest = fiveASideContestSelectionService.defaultSelectedContest;
      fiveASideContestSelectionService.validateRoleBasedContests.and.returnValue([]);
      component.executeFiveASideResponse([]);
      expect(component.defaultSelectedContest).toBe('');
      expect(component.fiveASideContests.length).toEqual(0);
    });
    it('if response is not empty', () => {
      component.fiveASideContests = contests;
      fiveASideContestSelectionService.defaultSelectedContest = '61b2f0372cb30f010f8fa61b';
      component.defaultSelectedContest = fiveASideContestSelectionService.defaultSelectedContest;
      fiveASideContestSelectionService.validateRoleBasedContests.and.returnValue(contests);
      component.executeFiveASideResponse(contests);
      expect(component.defaultSelectedContest).toBe('61b2f0372cb30f010f8fa61b');
      expect(component.fiveASideContests).toBe(contests);
    });
  });

  describe('getFiveASideContests', () => {
    it('should get all contests for given user name and event ID', () => {
      component.selection = {
        eventId: 'abcd'
      } as any;
      component['user'] = {
        username: 'abcd',
        bppToken: 'token'
      } as any;
      spyOn(component as any, 'executeFiveASideResponse');
      fiveASideContestSelectionService.getAllActiveFiveASideContests.and.returnValue(of(contests));
      component.getFiveASideContests();
      expect(component.executeFiveASideResponse).toHaveBeenCalled();
    });
  });

  describe('getFiveASideContestsForLegs', () => {
    it('should get all contests if 5 legs are present', () => {
      component.selection = new BYBBet({
        dashboardData: {
          channel: 'f',
          selections: [1, 2, 3, 4, 5],
          game: { title: '|A| |vs| |B|' }
        },
        odds: '10.00',
        oddsFract: {},
        currencySymbol: '$',
        currency: 'USD',
        token: 'token',
        oddsFormat: 'frac',
        channel: 'f'
      }) as any;
      component['user'] = {
        username: 'abcd'
      } as any;
      spyOn(component as any, 'getFiveASideContests');
      component['getFiveASideContestsForLegs']();
      expect(component.getFiveASideContests).toHaveBeenCalled();
    });
    it('should not get the contests if 5 legs are not present', () => {
      component.selection = new BYBBet({
        dashboardData: {
          selections: [1, 2, 3],
          game: { title: '|A| |vs| |B|' }
        },
        odds: '10.00',
        oddsFract: {},
        currencySymbol: '$',
        currency: 'USD',
        token: 'token',
        oddsFormat: 'frac',
        channel: 'f'
      }) as any;
      component['user'] = {
        username: 'abcd'
      } as any;
      spyOn(component as any, 'getFiveASideContests');
      component['getFiveASideContestsForLegs']();
      expect(component.getFiveASideContests).not.toHaveBeenCalled();
    });
    it('should not get the contests if selection is null', () => {
      component.selection = null;
      component['user'] = {
        username: 'abcd'
      } as any;
      spyOn(component as any, 'getFiveASideContests');
      component['getFiveASideContestsForLegs']();
      expect(component.getFiveASideContests).not.toHaveBeenCalled();
    });
    it('should not get the contests if channel is not f', () => {
      component.selection = new BYBBet({
        dashboardData: {
          selections: [1, 2, 3, 4, 5],
          game: { title: '|A| |vs| |B|' }
        },
        odds: '10.00',
        oddsFract: {},
        currencySymbol: '$',
        currency: 'USD',
        token: 'token',
        oddsFormat: 'frac',
        channel: 'g'
      }) as any;
      component['user'] = {
        username: 'abcd'
      } as any;
      spyOn(component as any, 'getFiveASideContests');
      component['getFiveASideContestsForLegs']();
      expect(component.getFiveASideContests).not.toHaveBeenCalled();
    });
  });

  describe('checkYellowFlag', () => {
    it('should not set default selected contest to null', () => {
      bonusSuppressionService.checkIfYellowFlagDisabled = jasmine.createSpy('checkIfYellowFlagDisabled').and.returnValue(true);
      const status = component.checkYellowFlag();
      expect(bonusSuppressionService.checkIfYellowFlagDisabled).toHaveBeenCalled();
      expect(status).toBe(true)
    });
    it('should set default selected contest to null', () => {
      bonusSuppressionService.checkIfYellowFlagDisabled = jasmine.createSpy('checkIfYellowFlagDisabled').and.returnValue(false);
      fiveASideContestSelectionService.defaultSelectedContest = null;
      component.defaultSelectedContest = fiveASideContestSelectionService.defaultSelectedContest;
      const status = component.checkYellowFlag();
      expect(component.defaultSelectedContest).toBe(null);
      expect(bonusSuppressionService.checkIfYellowFlagDisabled).toHaveBeenCalled();
      expect(status).toBe(false)
    });
  });
});
