import { Breadcrumb } from '@app/client/private/models/breadcrumb.model';
import { SportsHighlightCarousel } from '@app/client/private/models/sportsHighlightCarousel.model';

export const sportCarouselBreadcrumbs: Breadcrumb[] = [
  {
    label: 'Sport Categories',
    url: '/sports-pages/sport-categories'
  }, {
    label: 'Football',
    url: '/sports-pages/sport-categories/57fcfcd9b6aff9ba6c252a2c'
  }, {
    label: 'Highlights Carousel Module',
    url: '/sports-pages/sport-categories/57fcfcd9b6aff9ba6c252a2c/sports-module/sports-highlight-carousels/5bf53af4c9e77c0001a533d1'
  }, {
    label: 'title',
    url: `/sports-pages/sport-categories/57fcfcd9b6aff9ba6c252a2c/sports-module/sports-highlight-carousels/5bf53af4c9e77c0001a533d1/
  /carousel/edit/5c055537c9e77c000168a3b7`
  }];

export const carouselMock: SportsHighlightCarousel = {
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
  'inclusionList': [],
  'exclusionList': [],
  'universalSegment': true,
  'displayMarketType': '',
  'displayOnDesktop': false
};
