import { BackButtonService } from '@core/services/backButton/back-button.service';
import { RoutingState } from '@shared/services/routingState/routing-state.service';
import { NavigationEnd, Router, RouterEvent } from '@angular/router';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { Location } from '@angular/common';
import { StorageService } from '@core/services/storage/storage.service';
import { Subject } from 'rxjs';

describe('BackButtonservice', () => {
  let router, routingState, storageService, windowRefService, pubSubService,
    backButtonService: BackButtonService;

  beforeEach(() => {
    pubSubService = {
      publish: jasmine.createSpy('publish'),
      subscribe: jasmine.createSpy('subscribe'),
      API: {
        REDIRECT: 'REDIRECT'
      }
    };
    storageService = jasmine.createSpyObj('StorageService', ['getCookie']);
    windowRefService = {
      nativeWindow: {
        location: {
          pathname: jasmine.createSpy()
        },
        document: {
          body: {
            classList: {
              remove: jasmine.createSpy('classList.remove')
            }
          }
        }
      }
    };
    router = jasmine.createSpyObj('RouterService', ['navigate', 'navigateByUrl']);
    router.events = new Subject();
    routingState = {
      getCurrentUrl: jasmine.createSpy('getCurrentUrl').and.returnValue(''),
      getPreviousUrl: jasmine.createSpy('getPreviousUrl'),
      getCurrentSegment: jasmine.createSpy('getCurrentSegment'),
      getRouteSegment: jasmine.createSpy('getRouteSegment'),
      getPreviousRouteSnapshot: jasmine.createSpy('getPreviousRouteSnapshot')
    };
    backButtonService = new BackButtonService(
      storageService as StorageService,
      {} as Location,
      windowRefService as WindowRefService,
      router as Router,
      routingState as RoutingState,
      pubSubService);
  });

  describe('#constructor', () => {
    it('should subscribe to Router events', () => {
      expect(router.events.observers.length).toEqual(1);
    });

    describe('on route change', () => {
      describe('when back-button was not pressed', () => {
        describe('for any router event instance other than NavigationEnd type', () => {
          beforeEach(() => {
            router.events.next(new RouterEvent(1, 'url'));
          });

          it('should not check current segment, current and previous url', () => {
            expect(routingState.getCurrentUrl).not.toHaveBeenCalled();
            expect(routingState.getPreviousUrl).not.toHaveBeenCalled();
            expect(routingState.getCurrentSegment).not.toHaveBeenCalled();
          });
        });

        describe('for NavigationEnd instance of router event', () => {
          beforeEach(() => {
            routingState.getCurrentUrl.and.returnValue('currUrl');
            routingState.getPreviousUrl.and.returnValue('prevUrl');
            routingState.getCurrentSegment.and.returnValue('currSegment');
          });

          it('should check current segment, current and previous url', () => {
            router.events.next(new NavigationEnd(1, 'url', 'urlAfterRedirects'));

            expect(routingState.getCurrentUrl).toHaveBeenCalled();
            expect(routingState.getPreviousUrl).toHaveBeenCalled();
            expect(routingState.getCurrentSegment).toHaveBeenCalled();
          });

          it('should check current url and previous url for GH', () => {
            routingState.getCurrentSegment.and.returnValue('greyhound.display');
            routingState.getRouteSegment.and.returnValue('greyhound');
            backButtonService['segmentsArray'] = [
              {
                segmentName: 'home',
                url: '/'
              } ,
              {
                segmentName: 'greyhound',
                url: 'greyhound-racing'
              } ,
              {
                segmentName: 'greyhound',
                url: 'prevUrl'
              }
            ];
            router.events.next(new NavigationEnd(1, 'url', 'urlAfterRedirects'));
            expect(backButtonService['segmentsArray'].length).toEqual(3);
          });

          describe('when currentUrl is not the same as previousUrl and routingService.getCurrentSegment result is defined', () => {
            beforeEach(() => {
              routingState.getPreviousRouteSnapshot.and.returnValue('prevSnapshot');
              routingState.getRouteSegment.and.returnValue('prevSegment');
              router.events.next(new NavigationEnd(1, 'url', 'urlAfterRedirects'));
            });

            it('should get data from routingService.getRouteSegment for further back-route customization', () => {
              expect(routingState.getPreviousRouteSnapshot).toHaveBeenCalled();
              expect(routingState.getRouteSegment).toHaveBeenCalledWith('segment', 'prevSnapshot');
            });
          });
          describe('when currentUrl is not the same as previousUrl and routingService.getCurrentSegment result is virtual-sports.category', () => {
            beforeEach(() => {
              routingState.getPreviousRouteSnapshot.and.returnValue('prevSnapshot');
              routingState.getRouteSegment.and.returnValue('virtual-sports.category');
              router.events.next(new NavigationEnd(1, 'url', 'urlAfterRedirects'));
            });

            it('should get data from routingService.getRouteSegment for further back-route customization', () => {
              expect(routingState.getPreviousRouteSnapshot).toHaveBeenCalled();
              expect(routingState.getRouteSegment).toHaveBeenCalledWith('segment', 'prevSnapshot');
            });
          });

          describe('should not get data from routingService.getRouteSegment for further back-route customization', () => {
            it('when currentUrl is the same as previousUrl', () => {
              routingState.getPreviousUrl.and.returnValue('currUrl');
            });

            it('when routingService.getCurrentSegment result is falsy', () => {
              routingState.getCurrentSegment.and.returnValue(null);
            });

            afterEach(() => {
              router.events.next(new NavigationEnd(1, 'url', 'urlAfterRedirects'));
              expect(routingState.getPreviousRouteSnapshot).not.toHaveBeenCalled();
              expect(routingState.getRouteSegment).not.toHaveBeenCalled();
            });
          });

          it('should pop segment if previous segment is event.eventId', () => {
            routingState.getCurrentSegment.and.returnValue('eventMain');
            routingState.getRouteSegment.and.returnValue('event.eventId');
            router.events.next(new NavigationEnd(1, 'url', 'urlAfterRedirects'));
            expect(backButtonService['segmentsArray'].length).toEqual(0);
          });

          it('should Not pop segment if previous segment is Not event.eventId', () => {
            routingState.getCurrentSegment.and.returnValue('eventMain');
            routingState.getRouteSegment.and.returnValue('blabla');
            router.events.next(new NavigationEnd(1, 'url', 'urlAfterRedirects'));
            expect(backButtonService['segmentsArray'].length).toEqual(1);
          });

          describe( 'should call segmentsArray.pop or push if current or previous segment is "account-closure.step-two"' , () => {
            beforeEach(() => {
              backButtonService['segmentsArray'] = [];
            });

            it('should pop if current page is account-closure.step-two', () => {
              routingState.getCurrentUrl.and.returnValue('account-closure/step-one');
              routingState.getPreviousUrl.and.returnValue('account-closure/step-two');
              routingState.getCurrentSegment.and.returnValue('account-closure.step-two');
              router.events.next(new NavigationEnd(1, 'url', 'urlAfterRedirects'));
              expect(backButtonService['segmentsArray'].length).toEqual(0);
            });

            it('should pop if previous page is account-closure.step-two', () => {
              routingState.getCurrentUrl.and.returnValue('account-closure/step-two');
              routingState.getPreviousUrl.and.returnValue('account-closure/step-one');
              routingState.getCurrentSegment.and.returnValue('account-closure.step-one');
              routingState.getRouteSegment.and.returnValue('account-closure.step-two');
              router.events.next(new NavigationEnd(1, 'url', 'urlAfterRedirects'));
              expect(backButtonService['segmentsArray'].length).toEqual(0);
            });

            it('should SegmentsArray.push if prev page is closure.step-two and current is not closure.step-one', () => {
              routingState.getCurrentUrl.and.returnValue('some-page');
              routingState.getPreviousUrl.and.returnValue('account-closure/step-two');
              routingState.getCurrentSegment.and.returnValue('some.page');
              routingState.getRouteSegment.and.returnValue('account-closure.step-two');
              router.events.next(new NavigationEnd(1, 'url', 'urlAfterRedirects'));
              expect(backButtonService['segmentsArray'].length).toEqual(1);
            });

            it('should pop segment if current segment is betSlipUnavailable and prev segment is addToBetSlip', () => {
              routingState.getCurrentSegment.and.returnValue('betSlipUnavailable');
              routingState.getRouteSegment.and.returnValue('addToBetSlip');
              router.events.next(new NavigationEnd(1, 'url', 'urlAfterRedirects'));
              expect(backButtonService['segmentsArray'].length).toEqual(0);
            });

            it('should clear segment if current segment is 1-2-free', () => {
              routingState.getPreviousUrl.and.returnValue('/1-2-free');
              routingState.getRouteSegment.and.returnValue('1-2-free');
              router.events.next(new NavigationEnd(1, 'url', 'urlAfterRedirects'));
              expect(backButtonService['segmentsArray'].length).toEqual(0);
            });

            it('should clear segment if current segment is question-engine', () => {
              routingState.getPreviousUrl.and.returnValue('/question-engine');
              routingState.getRouteSegment.and.returnValue('question-engine');
              router.events.next(new NavigationEnd(1, 'url', 'urlAfterRedirects'));
              expect(backButtonService['segmentsArray'].length).toEqual(0);
            });

            it('Should not add object if prev link is "menu"', () => {
              routingState.getPreviousUrl.and.returnValue('menu');
              router.events.next(new NavigationEnd(1, 'url', 'urlAfterRedirects'));
              expect(backButtonService['segmentsArray'].length).toEqual(0);
            });

            it('Should check if previous Url include mobileportal/contact', () => {
              backButtonService['segmentsArray'] = [
                {
                  segmentName: 'home',
                  url: '/'
                } ,
                {
                  segmentName: 'account-closure.step-one',
                  url: 'account-closure/step-one'
                }
              ];
              routingState.getPreviousUrl.and.returnValue('en/mobileportal/contact');

              router.events.next(new NavigationEnd(1, 'url', 'urlAfterRedirects'));
              expect(backButtonService['segmentsArray'].length).toEqual(2);
            });

            it('Should check if previous Url include mobileportal/contact', () => {
              backButtonService['segmentsArray'] = [
                {
                  segmentName: 'home',
                  url: '/'
                } ,
                {
                  segmentName: 'account-closure.step-one',
                  url: 'account-closure/step-one'
                }
              ];
              routingState.getPreviousUrl.and.returnValue('en/mobileportal/contact');

              router.events.next(new NavigationEnd(1, 'url', 'urlAfterRedirects'));
              expect(backButtonService['segmentsArray'].length).toEqual(2);
            });

            it('Should check if previous Url not include mobileportal', () => {
              backButtonService['segmentsArray'] = [
                {
                  segmentName: 'home',
                  url: '/'
                } ,
                {
                  segmentName: 'account-closure.step-one',
                  url: 'account-closure/step-one'
                }
              ];
              routingState.getPreviousUrl.and.returnValue('en/mobileportal/test');

              router.events.next(new NavigationEnd(1, 'url', 'urlAfterRedirects'));
              expect(backButtonService['segmentsArray'].length).toEqual(2);
            });

            it('Should check if currentUrl not the same with previous Url', () => {
              backButtonService['segmentsArray'] = [
                {
                  segmentName: 'home',
                  url: '/'
                } ,
                {
                  segmentName: 'account-closure/step-one',
                  url: 'account-closure.step-one'
                },
                {
                  segmentName: 'some-page',
                  url: 'some-page'
                }
              ];

              routingState.getCurrentUrl.and.returnValue('some-page');
              routingState.getPreviousUrl.and.returnValue('en/menu');
              routingState.getCurrentSegment.and.returnValue('some-page');
              router.events.next(new NavigationEnd(1, 'url', 'urlAfterRedirects'));
              expect(backButtonService['segmentsArray'].length).toEqual(2);
            });

          });
        });
      });

      describe('when back-button was pressed', () => {
        beforeEach(() => {
          backButtonService.redirectToPreviousPage();
        });

        describe('for NavigationEnd instance of router event', () => {
          beforeEach(() => {
            router.events.next(new NavigationEnd(1, 'url', 'urlAfterRedirects'));
          });

          it('should not check current segment', () => {
            expect(routingState.getCurrentSegment).not.toHaveBeenCalled();
          });
        });
      });
    });
  });

  it('lotto.lottery-receipt', () => {
    backButtonService['segmentsArray'] = <any>[{}, {}, {}];
    routingState.getCurrentSegment.and.returnValue('lotto');
    routingState.getRouteSegment.and.returnValue('lotto.lottery-receipt');
    routingState.getCurrentUrl.and.returnValue('lotto');
    routingState.getPreviousUrl.and.returnValue('football');
    router.events.next(new NavigationEnd(1, 'url', 'urlAfterRedirects'));
    expect(backButtonService['segmentsArray'].length).toEqual(2);
  });

  describe('bigCompetition Route', () => {
    beforeEach(() => {
      routingState.getCurrentUrl.and.returnValue('big-competition');
      routingState.getPreviousUrl.and.returnValue('home');
    });

    it('bigCompetition.tab - should pop array', () => {
      backButtonService['segmentsArray'] = <any>[{}, {}];
      routingState.getCurrentSegment.and.returnValue('bigCompetition.tab');
      routingState.getRouteSegment.and.returnValue('bigCompetition.tab');
      router.events.next(new NavigationEnd(1, 'url', 'urlAfterRedirects'));
      expect(backButtonService['segmentsArray'].length).toEqual(2);
    });

    it('bigCompetition.subtab - should pop array', () => {
      backButtonService['segmentsArray'] = <any>[{}, {}];
      routingState.getCurrentSegment.and.returnValue('bigCompetition');
      routingState.getRouteSegment.and.returnValue('bigCompetition.subtab');
      router.events.next(new NavigationEnd(1, 'url', 'urlAfterRedirects'));
      expect(backButtonService['segmentsArray'].length).toEqual(2);
    });
  });

  describe('#redirectToPreviousPage', () => {
    it('redirect if we have gameBaseUrl or cbUrl', () => {
      storageService.getCookie.and.returnValue('gameBaseUrl');
      backButtonService.redirectToPreviousPage();
      expect(storageService.getCookie).toHaveBeenCalledWith('gameBaseUrl');
      expect(pubSubService.publish).toHaveBeenCalledWith('REDIRECT');
    });

    it('should navigate to previous bet-filter page', () => {
      // eslint-disable-next-line max-len
      backButtonService['segmentsArray'] = [{ segmentName: 'connectMain', url: '/connect' }, { segmentName: 'betFilter', url: '/betFilter' }];
      windowRefService.nativeWindow.location.pathname = '/bet-filter/results';
      backButtonService.redirectToPreviousPage();
      expect(backButtonService['previousPage']).toEqual('/bet-filter');
    });

    it('should navigate to product redirect url', () => {
      backButtonService['getProductRedirectUrl'] = () => 'url';
      backButtonService.redirectToPreviousPage();
      expect(windowRefService.nativeWindow.document.body.classList.remove).toHaveBeenCalledWith('league-standings-opened');
      expect(windowRefService.nativeWindow.location.href).toBe('url');
    });
  });

  describe('getProductRedirectUrl', () => {
    it('should not return url (not mobile portal page)', () => {
      routingState.getCurrentUrl.and.returnValue('/');
      expect(backButtonService['getProductRedirectUrl']()).toEqual('');
    });

    it('should not return url (segments with mobile portal)', () => {
      routingState.getCurrentUrl.and.returnValue('/mobileportal');
      backButtonService['segmentsArray'] = [{ url: '/mobileportal' }] as any;
      expect(backButtonService['getProductRedirectUrl']()).toEqual('');
    });

    it('should not return url (no product data)', () => {
      routingState.getCurrentUrl.and.returnValue('/mobileportal');
      backButtonService['segmentsArray'] = [];
      storageService.getCookie.and.returnValue(null);
      expect(backButtonService['getProductRedirectUrl']()).toEqual('');
    });

    it('should not return url (no product url)', () => {
      routingState.getCurrentUrl.and.returnValue('/mobileportal');
      backButtonService['segmentsArray'] = [];
      storageService.getCookie.and.returnValue({});
      expect(backButtonService['getProductRedirectUrl']()).toEqual('');
    });

    it('should not return url (product url same as current)', () => {
      routingState.getCurrentUrl.and.returnValue('/mobileportal');
      backButtonService['segmentsArray'] = [];
      storageService.getCookie.and.returnValue({ url: 'https://site1.com' });
      windowRefService.nativeWindow.location.href = 'https://site1.com';
      expect(backButtonService['getProductRedirectUrl']()).toEqual('');
    });

    it('should return url', () => {
      routingState.getCurrentUrl.and.returnValue('/mobileportal');
      backButtonService['segmentsArray'] = [];
      storageService.getCookie.and.returnValue({ url: 'https://site1.com' });
      windowRefService.nativeWindow.location.href = 'https://site2.com';
      expect(backButtonService['getProductRedirectUrl']()).toEqual('https://site1.com');
    });
  });
});
