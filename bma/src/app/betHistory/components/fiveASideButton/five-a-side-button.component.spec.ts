import { FiveASideComponent } from '@app/betHistory/components/fiveASideButton/five-a-side-button.component';

describe('FiveASideComponent', () => {
  let component: FiveASideComponent;
  let routerStub;
  let routingHelperStub;
  let gtmServiceMock;
  let pubSubService;

  beforeEach(() => {
    routerStub = {
      navigateByUrl: jasmine.createSpy('navigateByUrl').and
      .returnValue('/event/football/england/premier-league/liverpool-vs-newcastle/2345671/5-a-side/pitch')
    };
    routingHelperStub = {
        formFiveASideUrl: jasmine.createSpy('formFiveASideUrl').and
        .returnValue('/football/england/premier-league/liverpool-vs-newcastle/2345671')
    };
    gtmServiceMock = {
        push: jasmine.createSpy('push')
      };
    pubSubService = {
      publish: jasmine.createSpy('publish')
    };

    component = new FiveASideComponent(routerStub, routingHelperStub,
        gtmServiceMock, pubSubService );
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  describe('#navigateToFiveASide', () => {
    it('should navigate To Five A Side pitch view ', () => {
      component.leg = {
        part: [{
          outcome: [{
            eventCategory: {
              name: 'Football'
            },
            eventClass: {
              name: 'England'
            },
            eventType: {
              name: 'Premier League'
            },
            event: {
              name: 'liverpool vs newcastle',
              id: '2345671'
            }
          }],
        }],
      } as any;
      const gtmData = {
        eventCategory: '5-A-Side',
        eventAction: 'click',
        eventLabel: 'Go to 5-a-side'
      };
      const url = routingHelperStub.formFiveASideUrl('Football', 'England', 'Premier League', 'liverpool vs newcastle', '2345671');
      const result = routerStub.navigateByUrl('`/event/football/england/premier-league/liverpool-vs-newcastle/2345671/5-a-side/pitch`');
      component.navigateToFiveASide();
      expect(url)
        .toBe('/football/england/premier-league/liverpool-vs-newcastle/2345671');
      expect(result).toBe('/event/football/england/premier-league/liverpool-vs-newcastle/2345671/5-a-side/pitch');
      expect(gtmServiceMock.push).toHaveBeenCalledWith('trackEvent', gtmData);
      expect(pubSubService.publish).toHaveBeenCalledWith('SHOW_FIVE_A_SIDE', true);
    });
  });
 });
