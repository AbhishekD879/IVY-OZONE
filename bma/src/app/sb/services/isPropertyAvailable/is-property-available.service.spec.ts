import { IsPropertyAvailableService } from '@sb/services/isPropertyAvailable/is-property-available.service';

describe('IsPropertyAvailableService', () => {
  let service: IsPropertyAvailableService,
    checkFn;

  beforeEach(() => {
    checkFn = jasmine.createSpy('callbackSpy');
    service = new IsPropertyAvailableService();
  });

  describe('isPropertyAvailable', () => {
    let resultFn;

    beforeEach(() => {
      resultFn = service.isPropertyAvailable(checkFn);
    });

    it('call should return a function', () => {
      expect(resultFn).toEqual(jasmine.any(Function));
    });

    describe('result function', () => {
      const mockArray = [{ id: 1 }, { id: 2 }, { id: 3 }],
        mockConfig = [{ cashoutAvail: 'Y' }];

      it('should return false if the check function is falsy for all elements in the provided array, based on the config', () => {
        checkFn.and.returnValue(false);
        expect(resultFn(mockArray, mockConfig)).toEqual(false);
        expect(checkFn.calls.allArgs()).toEqual([
          [{ id: 1 }, [{ cashoutAvail: 'Y' }]],
          [{ id: 2 }, [{ cashoutAvail: 'Y' }]],
          [{ id: 3 }, [{ cashoutAvail: 'Y' }]]
        ]);
      });

      it('should return true if the check function is truthy for any element in the provided array, based on the config', () => {
        checkFn.and.callFake(item => item.id === 2);
        expect(resultFn(mockArray, mockConfig)).toEqual(true);
        expect(checkFn.calls.allArgs()).toEqual([
          [{ id: 1 }, [{ cashoutAvail: 'Y' }]],
          [{ id: 2 }, [{ cashoutAvail: 'Y' }]]
        ]);
      });
    });
  });
});


