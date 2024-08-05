import { of } from 'rxjs';
import { SportsConfigHelperService } from './sport-config-helper.service';

describe('SportsConfigHelperService', () => {
  let service: SportsConfigHelperService;

  let cmsService;

  beforeEach(() => {
    cmsService = {
      getSportCategoryById: jasmine.createSpy('getSportCategoryById').and.returnValue(of({ sportName: 'sport/SportName'})),
      getSportCategoryByName: jasmine.createSpy('getSportCategoryByName').and.returnValue(of({ sportName: 'sports/name/SportName'}))
    };

    service = new SportsConfigHelperService(cmsService);
  });

  it('constructor', () => {
    expect(service).toBeTruthy();
  });

  describe('#getSportConfigName', () => {
    it('should return sport name', () => {
      const result = service.getSportConfigName('/Sport Name|-');

      expect(result).toEqual('sportname');
    });
  });

  describe('#getSportPathByCategoryId', () => {
    it('should return sport category name', () => {
      service.getSportPathByCategoryId(123).subscribe(data => {
        expect(data).toEqual('SportName');
      });

      expect(cmsService.getSportCategoryById).toHaveBeenCalledWith(123);
    });
  });

  describe('#getSportPathByName', () => {
    it('should return sport category name', () => {
      service.getSportPathByName('SportName').subscribe(data => {
        expect(data).toEqual('SportName');
      });

      expect(cmsService.getSportCategoryByName).toHaveBeenCalledWith('SportName');
    });
  });
});
