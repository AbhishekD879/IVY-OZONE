import { CasinoMyBetsFiveASideComponent } from "./casino-mybets-five-a-side-button.component";


describe('CasinoMyBetsFiveASideComponent', () => {
  let component: CasinoMyBetsFiveASideComponent;
  let routerStub;
  let routingHelperStub;
  let gtmServiceMock;
  let pubSubService;
  let casinoMyBetsIntegratedService;

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
    casinoMyBetsIntegratedService = {
      goToSportsCTABtnClick: jasmine.createSpy('goToSportsCTABtnClick'),
      confirmationPopUpClick: jasmine.createSpy('confirmationPopUpClick')
    };

    component = new CasinoMyBetsFiveASideComponent(routerStub, routingHelperStub,
        gtmServiceMock, pubSubService, casinoMyBetsIntegratedService);
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

    it('should navigate To Five A Side pitch view, isMyBetsInCasino is true and showLeavingCasinoDialog is false', () => {
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
      component.isMyBetsInCasino = true;
      component.showLeavingCasinoDialog = false;
      component.navigateToFiveASide();
      expect(component['casinoMyBetsIntegratedService'].goToSportsCTABtnClick).toHaveBeenCalled();  
    });
  });

  describe('#confirmationDialogClick', () => {
    it('confirmationDialogClick, with generateUrl and event data', () => {
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
      const event = {
        output: 'userAction',
        value: {
          checkboxValue: true, 
          btnClicked: 'no thanks'
        }
      };
      component.confirmationDialogClick(event);
      expect(component['casinoMyBetsIntegratedService'].confirmationPopUpClick).toHaveBeenCalled();  
    });
  });
 });
