import { of as observableOf } from 'rxjs';
import { FiveASideContestSelectionService } from '@app/fiveASideShowDown/services/fiveASide-ContestSelection.service';
import environment from '@environment/oxygenEnvConfig';

describe('FiveASideContestSelectionService', () => {
  let service: FiveASideContestSelectionService;
  let http, userService;

  beforeEach(() => {
    http = {
      post: jasmine.createSpy().and.returnValue(observableOf({}))
    };

    userService = {
      email: 'test@gmail.com'
    };

    service = new FiveASideContestSelectionService(http, userService);
  });

  it('constructor', () => {
    expect(service).toBeTruthy();
  });

  describe('#defaultSelection', () => {
    it('should set the default selection value when event id is passed', () => {
      const id = '1234565';
      service.defaultSelectedContest = id;
      expect(service.defaultSelectedContest).toBe(id);
    });
  });

  it('get all active contests for the user and event', () => {
    const userName = 'M8sha';
    const contestObj = {
      brand: environment.brand,
      eventId: '12313',
      contestId: service.defaultSelectedContest,
      userId: userName
    };
    service.getAllActiveFiveASideContests(contestObj);
    expect(http.post).toHaveBeenCalledWith(
      `${environment.SHOWDOWN_MS}/${environment.brand}/betslip-contests`, contestObj);
  });

  it('should set default selection for the event id value', () => {
    const contestId = '12312313';
    service.defaultSelectedContest = contestId;
    expect(service.defaultSelectedContest).toBe(contestId);
  });

  it('should set default selection as null', () => {
    service.defaultSelectedContest = null;
    expect(service.defaultSelectedContest).toBeNull();
  });

  describe('#validateRoleBasedContests', () => {
    it('should not return test contests for real user', () => {
      const contests = [{ id: '1', testAccount: true, realAccount: false }, { id: '2', testAccount: true, realAccount: false }] as any;
      userService.email = 'test@gmail.com';
      const resultArray = service.validateRoleBasedContests(contests);
      expect(resultArray.length).toEqual(0);
    });
    it('should return real contests for real user', () => {
      const contests = [{ id: '1', testAccount: false, realAccount: true }, { id: '2', testAccount: true, realAccount: false }] as any;
      userService.email = 'test@gmail.com';
      const resultArray = service.validateRoleBasedContests(contests);
      expect(resultArray.length).toEqual(1);
    });
    it('should return test contests for test user', () => {
      const contests = [{ id: '1', testAccount: true, realAccount: false }, { id: '2', testAccount: false, realAccount: true }] as any;
      userService.email = 'testgvccl@internalgvc.com';
      const resultArray = service.validateRoleBasedContests(contests);
      expect(resultArray.length).toEqual(1);
    });
    it('should return contests when real account is true', () => {
      const contests = [{ id: '1', testAccount: true, realAccount: true }] as any;
      userService.email = 'test@gmail.com';
      const resultArray = service.validateRoleBasedContests(contests);
      expect(resultArray.length).toEqual(1);
    });
    it('should return all contests when real account is true', () => {
      const contests = [{ id: '1', testAccount: true, realAccount: true }] as any;
      userService.email = 'testgvccl@internalgvc.com';
      const resultArray = service.validateRoleBasedContests(contests);
      expect(resultArray.length).toEqual(1);
    });
    it('should return contests when real account is true and test account is false', () => {
      const contests = [{ id: '1', testAccount: false, realAccount: true }] as any;
      userService.email = 'test@gmail.com';
      const resultArray = service.validateRoleBasedContests(contests);
      expect(resultArray.length).toEqual(1);
    });
    it('should not return test contests', () => {
      const contests = [{ id: '1', testAccount: true, realAccount: false }] as any;
      userService.email = 'test@gmail.com';
      const resultArray = service.validateRoleBasedContests(contests);
      expect(resultArray.length).toEqual(0);
    });
    it('should not return any contests', () => {
      const contests = [{ id: '1', testAccount: false, realAccount: false }] as any;
      userService.email = 'test@gmail.com';
      const resultArray = service.validateRoleBasedContests(contests);
      expect(resultArray.length).toEqual(0);
    });
    it('should return empty array if null passed', () => {
      userService.email = 'test@gmail.com';
      const resultArray = service.validateRoleBasedContests(null);
      expect(resultArray.length).toEqual(0);
    });
  });

  describe('#isTestOrRealUser', () => {
    it('should return test user for testgvccl@coral domain', () => {
      const useremail = 'testgvccl@coral.co.uk';
      const testUser = 'testUser';
      expect(service['isTestOrRealUser'](useremail)).toBe(testUser);
    });
    it('should return realUser for not GVC/Entain domains', () => {
      const useremail = 'coral@gmail.com';
      const realUser = 'realUser';
      expect(service['isTestOrRealUser'](useremail)).toBe(realUser);
    });
    it('should return test user for internalgvc.com domain', () => {
      const useremail = 'test@internalgvc.com';
      const testUser = 'testUser';
      expect(service['isTestOrRealUser'](useremail)).toBe(testUser);
    });
    it('should return realUser for not gmail.com domain', () => {
      const useremail = 'user@gmail.com';
      const realUser = 'realUser';
      expect(service['isTestOrRealUser'](useremail)).toBe(realUser);
    });
    it('should return test user for coral.co.uk domain', () => {
      const useremail = 'testgvcld@coral.co.uk';
      const testUser = 'testUser';
      expect(service['isTestOrRealUser'](useremail)).toBe(testUser);
    });
  });
});
