import { OutcomeTemplateHelperService } from '@sb/services/outcomeTemplateHelper/outcome-template-helper.service';

describe('OutcomeTemplateHelperService', () => {
  let service: OutcomeTemplateHelperService;

  let templateService;
  let filtersService;

  beforeEach(() => {
    templateService = {
      getCorrectedOutcomeMeaningMinorCode: jasmine.createSpy('getCorrectedOutcomeMeaningMinorCode').and.returnValue(3)
    };
    filtersService = {
      getTeamName: jasmine.createSpy().and.returnValue('England')
    };

    service = new OutcomeTemplateHelperService(filtersService, templateService);
  });

  describe('@setOutcomeMeaningMinorCode', () => {
    it('it should set correct MeaningMinorCode to outcome', () => {
      const event = {
        name: 'England vs Germany',
        markets: [{
          outcomes: [{ displayOrder: 1, name: 'England' }, { name: 'Germany', displayOrder: 2 }]
        }]
      } as any;
      service.setOutcomeMeaningMinorCode(event.markets, event);
      expect(event.markets[0].outcomes).toEqual([{
        name: 'England',
        displayOrder: 1,
        correctedOutcomeMeaningMinorCode: 1
      }, {
        name: 'Germany',
        displayOrder: 2,
        correctedOutcomeMeaningMinorCode: 3
      }]);
    });

    it('it should set correct MeaningMinorCode to outcome if outcomeMeaningMinorCode is exist', () => {
      const event = {
        name: 'England vs Germany',
        isUS: false,
        markets: [{
          outcomes: [{ outcomeMeaningMinorCode: 'A', name: 'Germany', displayOrder: 1 }]
        }]
      } as any;
      service.setOutcomeMeaningMinorCode(event.markets, event);
      expect(templateService.getCorrectedOutcomeMeaningMinorCode).toHaveBeenCalled();
      expect(filtersService.getTeamName).not.toHaveBeenCalled();
      expect(event.markets[0].outcomes).toEqual([{
        isUS: false,
        name: 'Germany',
        displayOrder: 1,
        outcomeMeaningMinorCode: 'A',
        correctedOutcomeMeaningMinorCode: 3
      }]);
    });

    it('it should set correct MeaningMinorCode to outcome ' +
      'if outcomeMeaningMinorCode is not exist and team A is exist', () => {
      const event = {
        name: 'England vs Germany',
        isUS: false,
        markets: [{
          outcomes: [{ name: 'England', displayOrder: 1 }]
        }]
      } as any;
      filtersService.getTeamName = jasmine.createSpy().and.returnValue('England');
      service.setOutcomeMeaningMinorCode(event.markets, event);
      expect(event.markets[0].outcomes).toEqual([{
        name: 'England',
        displayOrder: 1,
        correctedOutcomeMeaningMinorCode: 1
      }]);
    });

    it('it should set correct MeaningMinorCode to outcome ' +
      'if outcomeMeaningMinorCode is not exist and team B is exist', () => {
      const event = {
        name: 'England vs Germany',
        isUS: false,
        markets: [{
          outcomes: [{ name: 'Germany', displayOrder: 1 }]
        }]
      } as any;
      filtersService.getTeamName = jasmine.createSpy().and.returnValue('England');
      service.setOutcomeMeaningMinorCode(event.markets, event);
      expect(event.markets[0].outcomes).toEqual([{
        name: 'Germany',
        displayOrder: 1,
        correctedOutcomeMeaningMinorCode: 3
      }]);
    });

    it('it should set correct MeaningMinorCode to outcome ' +
      'if outcomeMeaningMinorCode is not exist and has name "yes"', () => {
      const event = {
        name: 'England vs Germany',
        markets: [{
          outcomes: [{ name: 'yes', displayOrder: 1 }]
        }]
      } as any;
      filtersService.getTeamName = jasmine.createSpy().and.returnValue('England');
      service.setOutcomeMeaningMinorCode(event.markets, event);
      expect(event.markets[0].outcomes).toEqual([{
        name: 'yes',
        displayOrder: 1,
        correctedOutcomeMeaningMinorCode: 1
      }]);
    });

    it('it should set correct MeaningMinorCode to outcome ' +
      'if outcomeMeaningMinorCode is not exist and has name "no"', () => {
      const event = {
        name: 'England vs Germany',
        markets: [{
          outcomes: [{ name: 'no', displayOrder: 1 }]
        }]
      } as any;
      filtersService.getTeamName = jasmine.createSpy().and.returnValue('England');
      service.setOutcomeMeaningMinorCode(event.markets, event);
      expect(event.markets[0].outcomes).toEqual([{
        name: 'no',
        displayOrder: 1,
        correctedOutcomeMeaningMinorCode: 3
      }]);
    });

    it('it should set correct MeaningMinorCode to outcomes length > 1', () => {
      const event = {
        name: 'England vs Germany',
        markets: [{
          outcomes: [{ name: 'Draw', displayOrder: 2 }, { name: 'Germany', displayOrder: 3 } , { name: 'England', displayOrder: 1 }]
        }]
      } as any;
      service.setOutcomeMeaningMinorCode(event.markets, event);
      expect(event.markets[0].outcomes).toEqual([
        { name: 'England', displayOrder: 1, correctedOutcomeMeaningMinorCode: 1 },
        { name: 'Draw', displayOrder: 2, correctedOutcomeMeaningMinorCode: 2  } ,
        { name: 'Germany', displayOrder: 3, correctedOutcomeMeaningMinorCode: 3  }]);
    });

    it('it should set correct MeaningMinorCode to outcomes length > 1', () => {
      const event = {
        name: 'England vs Germany',
        markets: [{
          outcomes: []
        }]
      } as any;
      service.setOutcomeMeaningMinorCode(event.markets, event);
      expect(event.markets[0].outcomes).toEqual([]);
    });

    it('it should set correct MeaningMinorCode to outcomes without name', () => {
      const event = {
        name: 'England vs Germany',
        markets: [{
          outcomes: [{ displayOrder: 1 }]
        }]
      } as any;
      service.setOutcomeMeaningMinorCode(event.markets, event);
      expect(event.markets[0].outcomes).toEqual([{ displayOrder: 1, correctedOutcomeMeaningMinorCode: 1 }]);
    });

    it('it should set correct MeaningMinorCode to outcome if markets is empty', () => {
      const event = {
        name: 'England vs Germany',
        markets: []
      } as any;
      service.setOutcomeMeaningMinorCode(event.markets, event);
      expect(event).toEqual({
        name: 'England vs Germany',
        markets: []
      } as any);
    });
  });
});
