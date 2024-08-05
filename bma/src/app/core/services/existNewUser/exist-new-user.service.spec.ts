import { ExistNewUserService } from './exist-new-user.service';

describe('ExistNewUserService', () => {
  let service: ExistNewUserService;
  let storage;

  beforeEach(() => {
    storage = {
      get: jasmine.createSpy().and.callFake((value: string) => {
        if (value === 'vipLevel') {
          return '1';
        } else if (value === 'existingUser') {
          return true;
        }
      })
    };
    service = new ExistNewUserService(
      storage
    );
  });

  it('constructor', () => {
    expect(service).toBeDefined();
  });

  it('should filter exist new items', () => {
    const items = [{
        displayFrom: '12/12/12',
        displayTo: '12/12/32',
        vipLevels: [1, 2, 3],
        showToCustomer: ['existing']
    }];
    expect(service.filterExistNewUserItems(items)).toEqual([items[0]]);
  });
});
