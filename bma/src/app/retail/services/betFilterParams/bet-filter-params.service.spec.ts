import { Observable } from 'rxjs';
import { BetFilterParamsService } from '@app/retail/services/betFilterParams/bet-filter-params.service';

describe('BetFilterParamsService', () => {
  let service: BetFilterParamsService;

  beforeEach(() => {
    service = new BetFilterParamsService();
  });

  it('constructor', () => {
    expect(service).toBeTruthy();
  });

  it('get params', () => {
    expect(service.params).toEqual(service.betFilterParams);
  });

  describe('@chooseMode', () => {
    it('should return inshop mode in chooseMode', () => {
      const result = service.chooseMode();
      expect(service['betFilterParams']).toEqual({ mode: 'inshop' });
      result.subscribe((value) => {
        expect(value).toEqual({ mode: 'inshop' });
      });
      expect(result).toEqual(jasmine.any(Observable));
    });
  });

  describe('betFilterDialog actions', () => {
    let subject;

    beforeEach(() => {
      subject = jasmine.createSpyObj('Subject', ['next', 'complete']);
    });

    it('should select mode with some value', () => {
      const mode = 'inshop';
      service['selectModeAction']('inshop', subject);

      expect(service['betFilterParams'].mode).toEqual(mode);
      expect(subject.next).toHaveBeenCalledWith(service['betFilterParams']);
      expect(subject.complete).toHaveBeenCalled();
    });

    it('should select mode without value', () => {
      service['selectModeAction'](undefined, subject);

      expect(subject.next).toHaveBeenCalledWith(service['betFilterParams']);
      expect(subject.complete).toHaveBeenCalled();
    });

    it('should cancel action', () => {
      service['cancelAction'](true, subject);

      expect(service['betFilterParams'].cancelled).toBeTruthy();
      expect(subject.next).toHaveBeenCalledWith(service['betFilterParams']);
      expect(subject.complete).toHaveBeenCalled();
    });
  });
});
