import { Observable } from 'rxjs/Observable';
import { SurfaceBet } from '@app/client/private/models/surfaceBet.model';
import { SportsSurfaceBetsService } from '@app/sports-modules/surface-bets/surface-bets.service';
import {HttpResponse} from '@angular/common/http';

describe('SportsSurfaceBetsService module', () => {
  let service: SportsSurfaceBetsService,
    error: any,
    apiClientService,
    surfaceBet: SurfaceBet;

  beforeEach(() => {
    error = {
      'errors': [{
        'defaultMessage': 'should contain only letters, digits and spaces',
        'field': 'title',
      }]
    };
    surfaceBet = {
      id: '5c08e4dac9e77c00013099c2'
    } as any;

    apiClientService = {
      sportsSurfaceBets: jasmine.createSpy('sportsSurfaceBet').and.returnValue({
        save: jasmine.createSpy('save').and.returnValue(Observable.of({ body: surfaceBet })),
        uploadIcon: jasmine.createSpy('save').and.returnValue(Observable.of({ body: surfaceBet }))
      }),
      sportCategoriesService: jasmine.createSpy('sportCategoriesService').and.returnValue({
        getSportCategories: jasmine.createSpy('getSportCategories').and.returnValue(Observable.of([]))
      })
    };
    service = new SportsSurfaceBetsService(apiClientService as any);
  });

  it('#getSportCategories should call api', () => {
    service.getSportCategories();
    expect(apiClientService.sportCategoriesService().getSportCategories).toHaveBeenCalledTimes(1);
  });

  it('#saveWithIcon should call only #save', () => {
    spyOn(service, 'uploadIcon');
    service['generateErrorMsg'] = jasmine.createSpy('generateErrorMsg');
    service.saveWithIcon(surfaceBet, null).subscribe(() => {
      expect(apiClientService.sportsSurfaceBets().save).toHaveBeenCalledWith(surfaceBet);
      expect(service.uploadIcon).not.toHaveBeenCalled();
      expect(service['generateErrorMsg']).not.toHaveBeenCalled();
    });
  });

  it('#saveWithIcon should call only #save and #uploadIcon', () => {
    const file = {
      name: 'filename'
    } as any;
    spyOn(service, 'uploadIcon').and.returnValue(Observable.of({ body: {} } as HttpResponse<SurfaceBet>));
    service['generateErrorMsg'] = jasmine.createSpy('generateErrorMsg');
    service.saveWithIcon(surfaceBet, file).subscribe(() => {
      expect(apiClientService.sportsSurfaceBets().save).toHaveBeenCalledWith(surfaceBet);
      expect(service.uploadIcon).toHaveBeenCalledWith(surfaceBet.id, file);
      expect(service['generateErrorMsg']).not.toHaveBeenCalled();
    });
  });

  it('#saveWithIcon should call only #save and #generateErrorMsg', () => {
    const file = {
      name: 'filename'
    } as any;
    apiClientService.sportsSurfaceBets().save.and.returnValue(Observable.throw({ error: error }));
    spyOn(service, 'uploadIcon').and.returnValue(Observable.of({ body: {} } as HttpResponse<SurfaceBet>));
    service['generateErrorMsg'] = jasmine.createSpy('generateErrorMsg').and.returnValue('generated error');
    service.saveWithIcon(surfaceBet, file).subscribe(() => {
    }, err => {
      expect(err).toEqual('generated error');
      expect(service['generateErrorMsg']).toHaveBeenCalledWith({ error: error });
      expect(service['uploadIcon']).not.toHaveBeenCalled();
    });
  });

  it('#saveWithIcon should call only #save -> #uploadIcon -> #generateErrorMsg', () => {
    const file = {
      name: 'filename'
    } as any;
    spyOn(service, 'uploadIcon').and.returnValue(Observable.throw({ error: error }));
    service['generateErrorMsg'] = jasmine.createSpy('generateErrorMsg').and.returnValue('generated error');
    service.saveWithIcon(surfaceBet, file).subscribe(() => {
    }, err => {
      expect(err).toEqual(
        'Sport surface bet was created, but Image not uploaded. Error: generated error'
      );
      expect(service.uploadIcon).toHaveBeenCalledWith('5c08e4dac9e77c00013099c2', file);
      expect(service['generateErrorMsg']).toHaveBeenCalledWith({ error: error });
    });
  });

  it('#saveWithIcon should call only #save -> #uploadIcon -> #generateErrorMsg', () => {
    const file = {
      name: 'filename'
    } as any;
    spyOn(service, 'uploadIcon').and.returnValue(Observable.throw({ error: error }));
    service['generateErrorMsg'] = jasmine.createSpy('generateErrorMsg').and.returnValue('generated error');
    service.saveWithIcon(surfaceBet, file).subscribe(() => {
    }, err => {
      expect(err).toEqual(
        'Sport surface bet was created, but Image not uploaded. Error: generated error'
      );
      expect(service.uploadIcon).toHaveBeenCalledWith('5c08e4dac9e77c00013099c2', file);
      expect(service['generateErrorMsg']).toHaveBeenCalledWith({ error: error });
    });
  });

  it('#uploadIcon', () => {
    const file = {
      name: 'filename'
    } as any;

    service.uploadIcon(surfaceBet.id, file).subscribe(() => {
      expect(apiClientService.sportsSurfaceBets().uploadIcon).toHaveBeenCalledWith(
        '5c08e4dac9e77c00013099c2', jasmine.any(FormData)
      );
    });
  });

  it('#generateErrorMsg should return error string', () => {
    expect(service['generateErrorMsg']({ error: error })).toEqual('title should contain only letters, digits and spaces. \n');
    expect(service['generateErrorMsg']({})).toEqual('Unknown error');
  });
});

