import { async } from '@angular/core/testing';
import { FiveASidePreHeaderService } from '@app/fiveASideShowDown/services/fiveaside-pre-header.service';

describe('FiveASidePreHeaderService', () => {
  let service: FiveASidePreHeaderService;

  beforeEach(async(() => {
    service = new FiveASidePreHeaderService();
  }));

  it('should create', () => {
    expect(service).toBeTruthy();
  });

  describe('#getTimeDifference', () => {
    it('should return correct time difference', () => {
      const eventStartTime = new Date();
      expect(service.getTimeDifference(eventStartTime, eventStartTime)).toEqual(0);
    });
  });

  describe('#checkForMatchDay scenario', () => {
    it('should return false if its not current year', () => {
      const eventStartTime = new Date(new Date().setFullYear(new Date().getFullYear() + 1));
      expect(service.checkForMatchDay(eventStartTime)).toEqual(false);
    });
    it('should return false if its not current month', () => {
      const eventStartTime = new Date(new Date().setMonth(new Date().getMonth() + 1));
      expect(service.checkForMatchDay(eventStartTime)).toEqual(false);
    });
    it('should return false if its not current Day', () => {
      const eventStartTime = new Date(new Date().setDate(new Date().getDate() + 1));
      expect(service.checkForMatchDay(eventStartTime)).toEqual(false);
    });
    it('should return true if present day', () => {
      const eventStartTime = new Date();
      expect(service.checkForMatchDay(eventStartTime)).toEqual(true);
    });
  });
  describe('formParamArray', () => {
    it('should be used to generate array of element', () => {
      service['formParamArray']('element', 2);
    });
});
});
