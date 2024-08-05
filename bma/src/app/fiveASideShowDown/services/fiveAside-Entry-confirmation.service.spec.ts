import { of as observableOf } from 'rxjs';
import { FiveASideEntryConfirmationService } from '@app/fiveASideShowDown/services/fiveAside-Entry-confirmation.service';

describe('FiveASideEntryConfirmationService', () => {
  let service: FiveASideEntryConfirmationService;
  let http;

  beforeEach(() => {
    http = {
      post: jasmine.createSpy().and.returnValue(observableOf({})),
      ENTRYCONFIRMATION_URL: jasmine.createSpy().and.returnValue(observableOf({})),
    };

    service = new FiveASideEntryConfirmationService(http);
  });

  it('showdownObj', () => {
    expect(service).toBeTruthy();
  });

  describe('#isTestOrRealUser', () => {
    it('should test if a user is a test user for coral domain', () => {
        const useremail = 'testgvccl@coral.co.uk';
        const testAccount = 'testAccount';
        expect(service['isTestOrRealUser'](useremail)).toBe(testAccount);
    });
    it('should test if a user is a test user for ladbrokes domain', () => {
        const useremail = 'testgvcld@coral.co.uk';
        const testAccount = 'testAccount';
        expect(service['isTestOrRealUser'](useremail)).toBe(testAccount);
    });
    it('should test if a user is a test user for coral domain', () => {
        const useremail = 'test@internalgvc.com';
        const testAccount = 'testAccount';
        expect(service['isTestOrRealUser'](useremail)).toBe(testAccount);
    });
    it('should test if a user is a real user for coral domain', () => {
        const useremail = 'coral@gmail.com';
        const realAccount = 'realAccount';
        expect(service['isTestOrRealUser'](useremail)).toBe(realAccount);
    });
    it('should test if a user is a real user for ladbrokes domain', () => {
        const useremail = 'ladbrokes@gmail.com';
        const realAccount = 'realAccount';
        expect(service['isTestOrRealUser'](useremail)).toBe(realAccount);
    });
  });

  it('getShowdownConfirmationDisplay', () => {
    service.getShowdownConfirmationDisplay('showdownObj');
  });
});
