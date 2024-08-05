import {
  SportsHighlightCarouselsService
} from '@app/sports-modules/highlight-carousels-module/highlight-carousels/highlight-carousels.service';
import { Observable } from 'rxjs/Observable';
import { SportsHighlightCarousel } from '@app/client/private/models/sportsHighlightCarousel.model';
import {HttpResponse} from '@angular/common/http';

describe('SportsHighlightCarouselsService', () => {
  let service: SportsHighlightCarouselsService;
  let carousel: SportsHighlightCarousel;
  let error: any;
  let apiClientService;

  beforeEach(() => {
    carousel = {
      'id': '5c08e4dac9e77c00013099c2',
      'createdBy': '54905d04a49acf605d645271',
      'createdByUserName': 'test.admin@coral.co.uk',
      'updatedBy': '54905d04a49acf605d645271',
      'updatedByUserName': 'test.admin@coral.co.uk',
      'createdAt': '2018-12-06T08:59:06.770Z',
      'updatedAt': '2018-12-06T16:09:35.808Z',
      'sortOrder': -4.0,
      'disabled': false,
      'sportId': 0,
      'pageType': 'sport',
      'pageId': '0',
      'title': 't1',
      'brand': 'bma',
      'displayFrom': '2018-12-01T23:00:00Z',
      'displayTo': '2018-12-31T00:00:00Z',
      'svg': '',
      'displayMarketType': 'string',
      'svgFilename': {
        'filename': '',
        'path': '',
        'size': 0,
        'filetype': '',
      },
      'limit': null,
      'inPlay': false,
      'typeId': null,
      'events': ['2'],
      'displayOnDesktop':false
    };

    error = {
      'timestamp': '2018-12-14T10:45:22Z',
      'status': 400,
      'error': 'Bad Request',
      'exception': 'org.springframework.web.bind.MethodArgumentNotValidException',
      'errors': [{
        'codes': ['Pattern.highlightCarousel.title', 'Pattern.title', 'Pattern.java.lang.String', 'Pattern'],
        'arguments': [{
          'codes': ['highlightCarousel.title', 'title'],
          'arguments': null,
          'defaultMessage': 'title',
          'code': 'title'
        }, [], { 'arguments': null, 'defaultMessage': '^[a-zA-Z0-9_ ]*$', 'codes': ['^[a-zA-Z0-9_ ]*$'] }],
        'defaultMessage': 'should contain only letters, digits and spaces',
        'objectName': 'highlightCarousel',
        'field': 'title',
        'rejectedValue': 't12345678(&^*&%^',
        'bindingFailure': false,
        'code': 'Pattern'
      }],
      'message': 'Bad Request',
      'path': '/v1/api/highlight-carousel/5c125aaec9e77c00016051f2'
    };

    apiClientService = {
      sportsHighlightCarousel: jasmine.createSpy('sportsHighlightCarousel').and.returnValue({
        save: jasmine.createSpy('save').and.returnValue(Observable.of({ body: carousel })),
        uploadIcon: jasmine.createSpy('save').and.returnValue(Observable.of({ body: carousel }))
      })
    };
    service = new SportsHighlightCarouselsService(apiClientService as any);
  });

  it('#saveWithIcon should call only #save', () => {
    spyOn(service, 'uploadIcon');
    service['generateErrorMsg'] = jasmine.createSpy('generateErrorMsg');
    service.saveWithIcon(carousel, null).subscribe(() => {
      expect(apiClientService.sportsHighlightCarousel().save).toHaveBeenCalledWith(carousel);
      expect(service.uploadIcon).not.toHaveBeenCalled();
      expect(service['generateErrorMsg']).not.toHaveBeenCalled();
    });
  });

  it('#saveWithIcon should call only #save and #uploadIcon', () => {
    const file = {
      name: 'filename'
    } as any;
    spyOn(service, 'uploadIcon').and.returnValue(Observable.of({ body: {} } as HttpResponse<SportsHighlightCarousel>));
    service['generateErrorMsg'] = jasmine.createSpy('generateErrorMsg');
    service.saveWithIcon(carousel, file).subscribe(() => {
      expect(apiClientService.sportsHighlightCarousel().save).toHaveBeenCalledWith(carousel);
      expect(service.uploadIcon).toHaveBeenCalledWith(carousel.id, file);
      expect(service['generateErrorMsg']).not.toHaveBeenCalled();
    });
  });

  it('#saveWithIcon should call only #save and #generateErrorMsg', () => {
    const file = {
      name: 'filename'
    } as any;
    apiClientService.sportsHighlightCarousel().save.and.returnValue(Observable.throw({ error: error }));
    spyOn(service, 'uploadIcon').and.returnValue(Observable.of({ body: {} } as HttpResponse<SportsHighlightCarousel>));
    service['generateErrorMsg'] = jasmine.createSpy('generateErrorMsg').and.returnValue('generated error');
    service.saveWithIcon(carousel, file).subscribe(() => {
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
    service.saveWithIcon(carousel, file).subscribe(() => {
    }, err => {
      expect(err).toEqual(
        'Sport Highlight Carousel was created, but Image not uploaded. Error: generated error'
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
    service.saveWithIcon(carousel, file).subscribe(() => {
    }, err => {
      expect(err).toEqual(
        'Sport Highlight Carousel was created, but Image not uploaded. Error: generated error'
      );
      expect(service.uploadIcon).toHaveBeenCalledWith('5c08e4dac9e77c00013099c2', file);
      expect(service['generateErrorMsg']).toHaveBeenCalledWith({ error: error });
    });
  });

  it('#uploadIcon', () => {
    const file = {
      name: 'filename'
    } as any;

    service.uploadIcon(carousel.id, file).subscribe(() => {
      expect(apiClientService.sportsHighlightCarousel().uploadIcon).toHaveBeenCalledWith(
        '5c08e4dac9e77c00013099c2', jasmine.any(FormData)
      );
    });
  });

  it('#generateErrorMsg should return error string', () => {
    expect(service['generateErrorMsg']({ error: error })).toEqual('title should contain only letters, digits and spaces. \n');
    expect(service['generateErrorMsg']({})).toEqual('Unknown error');
  });
});

