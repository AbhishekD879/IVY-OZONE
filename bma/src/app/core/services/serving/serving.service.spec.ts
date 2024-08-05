import { ServingService } from './serving.service';

describe('ServingService', () => {
  let service: ServingService;
  let location;
  let userService;

  beforeEach(() => {
    location = {
      path: jasmine.createSpy()
    };
    userService = {
      setExternalCookies: jasmine.createSpy()
    };

    service = new ServingService(
      location,
      userService
    );
  });

  it('constructor', () => {
    expect(service).toBeTruthy();
  });

  it('trimPath', () => {
    expect(ServingService.trimPath('#/feed/news')).toBe('feed/news');
  });

  it('pathStartsWith', () => {
    expect(service.pathStartsWith(null)).toBeFalsy();

    location.path.and.returnValue('/');
    expect(service.pathStartsWith('#/feed/news')).toBeFalsy();

    location.path.and.returnValue('#/feed/newsf');
    expect(service.pathStartsWith('#/feed/news')).toBeTruthy();
  });

  it('getClass', () => {
    expect(service.getClass('')).toBeFalsy();

    location.path.and.returnValue('feed/news');
    expect(service.getClass('/news')).toBeTruthy();

    location.path.and.returnValue('/feed/news');
    expect(service.getClass('/news/1')).toBeFalsy();
  });

  it('sendExternalCookies', () => {
    service.sendExternalCookies('/');
    expect(userService.setExternalCookies).toHaveBeenCalled();
  });
});
