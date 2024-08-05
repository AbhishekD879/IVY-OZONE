import { of } from 'rxjs';
import {
  BigCompetitionsProvider
} from '@app/bigCompetitions/services/bigCompetitionsProvider/big-competitions-provider.service';

describe('BigCompetitionsProvider', () => {
  let service;
  let httpService;
  const httpResponse = {};

  beforeEach(() => {
    httpService = {
      get: jasmine.createSpy().and.returnValue(of(httpResponse))
    };
    service = new BigCompetitionsProvider(httpService);
  });

  describe('get tab, module, etc', () => {
    const responseBody = {};

    beforeEach(() => {
      service['getData'] = jasmine.createSpy().and.returnValue(of({ body: responseBody }));
    });

    it('#tabs', () => {
      const name = 'name';
      service.tabs(name).subscribe((data) => {
        expect(service['getData']).toHaveBeenCalledWith('', name);
        expect(data).toBe(responseBody);
      });
    });

    it('#tab', () => {
      const id = 'id';
      service.tab(id).subscribe((data) => {
        expect(service['getData']).toHaveBeenCalledWith('/tab', id);
        expect(data).toBe(responseBody);
      });
    });

    it('#subtab', () => {
      const id = 'id';
      service.subtab(id).subscribe((data) => {
        expect(service['getData']).toHaveBeenCalledWith('/subtab', id);
        expect(data).toBe(responseBody);
      });
    });

    it('#module', () => {
      const id = 'id';
      service.module(id).subscribe((data) => {
        expect(service['getData']).toHaveBeenCalledWith('/module', id);
        expect(data).toBe(responseBody);
      });
    });

    it('#participant', () => {
      const id = 'id';
      service.participants(id).subscribe((data) => {
        expect(service['getData']).toHaveBeenCalledWith(id, 'participant');
        expect(data).toBe(responseBody);
      });
    });
  });

  it('#getData', () => {
    const url = 'url';
    const params = 'params';
    service['getData'](url, params).subscribe((data) => {
      expect(httpService.get).toHaveBeenCalledWith(
        `${service.BIG_COMPETITION_MS}${url}/${params}`,
        jasmine.objectContaining({ observe: 'response' })
      );
      expect(data).toBe(httpResponse);
    });
  });
});
