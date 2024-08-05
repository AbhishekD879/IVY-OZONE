import { USER_SHOWDOWN_DATA } from '@app/fiveASideShowDown/components/fiveASideRulesEntryArea/fiveaside-rules-entry-area.mock';
import { FiveasideRulesEntryAreaService } from '@app/fiveASideShowDown/services/fiveaside-rules-entry-area.service';

describe('FiveasideRulesEntryAreaService', () => {
  let service: FiveasideRulesEntryAreaService;
  let userService,
  localeService,
  routingHelper,
  gtm,
  pubSubService;

  beforeEach(() => {
    userService = {
      status: true,
      username: 'Nick'
    };
    localeService = {
      applySubstitutions: jasmine.createSpy('applySubstitutions').and
        .returnValue('MAX ENTRIES REACHED ({betsPlaced}/{maxUserEntries})'),
      getString: jasmine.createSpy('getString').and.returnValue('#flag_round_england')
    };
    routingHelper = {
      encodeUrlPart: jasmine.createSpy('encodeUrlPart').and.callFake((part) => {
        return `${part}`.replace(/([^a-zA-Z0-9])+/g, '-')
          .replace(/^-+|-+$/g, '')
          .toLowerCase();
      })
    };
    gtm = {
      push: jasmine.createSpy('push')
    };
    pubSubService = {
      subscribe: jasmine.createSpy('subscribe'),
    } as any;
    service = new FiveasideRulesEntryAreaService(userService, localeService, routingHelper,
      gtm,pubSubService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  describe('#getButtonStatus', () => {
    it('should get button status when contest size is not mentioned', () => {
      const contest = {} as any;
      const response = service.getButtonStatus(400, 0, contest);
      const userName = userService.username;
      if (userName) {
        expect(response).toEqual({
          buttonType: 'BUILD TEAM',
          isBuildBetEnabled: true
        });
      }
    });
    it('should get button status when contest size is mentioned (Case: 0 User Entries)', () => {
      const contest = {
        size: 1000,
        teams: 5
      } as any;
      const response = service.getButtonStatus(400, 0, contest);
      expect(response).toEqual({
        buttonType: 'BUILD TEAM',
        isBuildBetEnabled: true
      });
    });
    it('should get button status when contest size is mentioned (Case: 1 User Entries)', () => {
      const contest = {
        size: 1000,
        teams: 5
      } as any;
      const response = service.getButtonStatus(400, 1, contest);
      expect(response).toEqual({
        buttonType: 'BUILD ANOTHER TEAM',
        isBuildBetEnabled: true
      });
    });
    it('should get button status when contest size is mentioned when username is null', () => {
      userService.status = false;
      const userName = userService.username = null;
      const contest = {
        size: 1000,
        teams: 5
      } as any;
      const response = service.getButtonStatus(0, 0, contest);
      if (userName) {
        expect(response).toEqual({
          buttonType: 'Log in/Join To Enter',
          isBuildBetEnabled: true
        });
      }
    });
    it('should get button status when contest size is mentioned (Case: Max User Entries)', () => {
      const contest = {
        maxEntries: 1000,
        maxEntriesPerUser: 5
      } as any;
      const response = service.getButtonStatus(400, 5, contest);
      expect(response).toEqual({
        buttonType: 'MAX ENTRIES REACHED ({betsPlaced}/{maxUserEntries})',
        isBuildBetEnabled: false
      });
    });
    it('should get button status when contest size is mentioned (Case: contest full)', () => {
      const contest =  {
        maxEntries: 1000,
        maxEntriesPerUser: 5
      } as any;
      const response = service.getButtonStatus(1000, 5, contest);
      expect(response).toEqual({
        buttonType: 'CONTEST FULL',
        isBuildBetEnabled: false
      });
    });
    it('should get button status when contest size is mentioned (Case: Not Logged In)', () => {
      userService.status = false;
      const userName =  userService.userName = null;
      const contest = {
        maxEntries: 1000,
        maxEntriesPerUser: 5
      } as any;
      const response = service.getButtonStatus(0, 0, contest);
      if (userName) {
        expect(response).toEqual({
          buttonType: 'Log in/Join To Enter',
          isBuildBetEnabled: true
        });
      }
    });
  });

  describe('#formFiveASideUrl', () => {
    it('should form five a side Url( Case-1)', () => {
      const event = USER_SHOWDOWN_DATA.eventDetails as any;
      const response = service.formFiveASideUrl(event);
      expect(response).toEqual('/event/football/football-auto-test/2-autotest-league/england-v-scotland/1722516');
    });
    it('should form five a side Url( Case-2)', () => {
      const event = USER_SHOWDOWN_DATA.eventDetails as any;
      event.className = null;
      event.typeName = null;
      const response = service.formFiveASideUrl(event);
      expect(response).toEqual('/event/football/class/type/england-v-scotland/1722516');
    });
  });

  it('should track gtm event', () => {
    service.trackGTMEvent('category', 'action', 'label');
    expect(gtm.push).toHaveBeenCalledWith('trackEvent', {eventCategory: 'category',
     eventAction: 'action', eventLabel: 'label'});
  });

  it('should form flag name', () => {
    const response = service.formFlagName('England');
    expect(response).toEqual('#flag_round_england');
  });
  it('should not return form flag name', () => {
    const response = service.formFlagName(null);
    expect(response).toBeUndefined();
  });
});
