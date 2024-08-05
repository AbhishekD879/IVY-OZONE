import { of as observableOf, Subject } from 'rxjs';

import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { SeoDataService } from './seo-data.service';

describe('SeoDataService', () => {
  let service: SeoDataService;
  let windowRef;
  let cms;
  let pubsub;
  let router;
  let routeSubject;
  let domElement;

  beforeEach(() => {
    routeSubject = new Subject();
    domElement = {
      setAttribute: jasmine.createSpy('setAttribute')
    };
    windowRef = {
      nativeWindow: {
        location: {
          pathname: '/'
        },
        document: {
          querySelector: jasmine.createSpy('querySelector').and.returnValue(domElement)
        }
      }
    };
    cms = {
      getSeoPagesPaths: jasmine.createSpy('getSeoPagesPaths').and.returnValue(observableOf({
        '/': 'askjdhsakjd',
        'test': 'bcd'
      })),
      getSeoPage: jasmine.createSpy('getSeoPage').and.returnValue(observableOf({
        '/': 'askjdhsakjd',
        'test': 'bcd'
      }))
    };
    pubsub = {
      publish: jasmine.createSpy('publish'),
      API: pubSubApi
    };
    router = {
      events: routeSubject
    };
  });

  function createService() {
    service = new SeoDataService(windowRef, cms, pubsub, router);
  }

  it('should have default title and description', () => {
    createService();

    expect(service.defaultPage).toEqual(jasmine.objectContaining({
      title: 'Ladbrokes Sports Betting - Football, Horse Racing and more!',
      description: 'Sports betting odds at Ladbrokes Sports. View for tips, available match odds, ' +
        'live-results and more. Football, Horse Racing and more! Bet now with Ladbrokes!'
    }));
  });
});
