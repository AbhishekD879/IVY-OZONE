import { MarketsOptaLinksService } from '@edp/services/marketsOptaLinks/markets-opta-links.service';
import { of as observableOf } from 'rxjs';


describe('MarketsOptaLinksService', () => {
  let service: MarketsOptaLinksService;
  let cmsService;
  beforeEach(() => {
    cmsService = {
      getMarketLinks: jasmine.createSpy('getMarketLinks').and.returnValue(observableOf([])),
      getSystemConfig: jasmine.createSpy('getSystemConfig').and.returnValue(observableOf({StatisticsLinks: {markets: true}} as any))
    };
    service = new MarketsOptaLinksService(
      cmsService
    );
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('should get config', () => {
    service.getMarketLinks().subscribe(() => {
      expect(cmsService.getSystemConfig).toHaveBeenCalled();
      expect(cmsService.getMarketLinks).toHaveBeenCalled();
    }) ;

  });

  it('should get error', () => {
    cmsService.getSystemConfig.and.returnValue(observableOf({StatisticsLinks: {markets: false}} as any));

    service.getMarketLinks().subscribe(() => {},
      (result) => {
        expect(result).toEqual('market links are disabled on cms');
      });
  });
});
