import { of } from 'rxjs';

import { OddsCardSpecialsComponent } from '@shared/components/oddsCard/oddsCardSpecials/odds-card-specials.component';
import { oddsCardConstant } from '@app/shared/constants/odds-card-constant';

describe('OddsCardSpecialsComponent', () => {
  let component: OddsCardSpecialsComponent;

  let eventServiceStub;
  let templateServiceStub;
  let timeServiceStub;
  let smartBoostsServiceStub;
  let filtersStub;
  let routingHelperStub;
  let routerStub;
  let marketTypeServiceStub;
  let sportsConfigHelperService, seoDataService,gtmService;

  const nameStub = 'TestName';
  const wasPriceStub = '12/11';
  const parsedNameStub = { name: nameStub, wasPrice: wasPriceStub };

  beforeEach(() => {
    filtersStub = {};
    routingHelperStub = {};
    routerStub = seoDataService = {};
    marketTypeServiceStub = {};
    eventServiceStub = {
      isLiveStreamAvailable: jasmine.createSpy()
    };
    templateServiceStub = {
      getTemplate: jasmine.createSpy().and.returnValue(''),
      isMultiplesEvent: jasmine.createSpy(),
      isListTemplate: (selectedMarket: string)=>{
        return oddsCardConstant.LIST_TEMPLATES.indexOf(selectedMarket) !== -1;
       }
    };
    timeServiceStub = {
      getLocalHourMin: jasmine.createSpy(),
      getEventTime: jasmine.createSpy(),
    };
    smartBoostsServiceStub = {
      isSmartBoosts: jasmine.createSpy().and.returnValue(true),
      parseName: jasmine.createSpy().and.returnValue(parsedNameStub),
    };
    sportsConfigHelperService = {
      getSportPathByCategoryId: jasmine.createSpy('getSportPathByCategoryId').and.returnValue(of(''))
    };

    component = new OddsCardSpecialsComponent(
      eventServiceStub,
      marketTypeServiceStub,
      templateServiceStub,
      routerStub,
      timeServiceStub,
      filtersStub,
      routingHelperStub,
      smartBoostsServiceStub,
      sportsConfigHelperService,
      seoDataService,
      gtmService
    );
  });

  it('should create component instance', () => {
    expect(component).toBeTruthy();
  });

  describe('ngOnInit', () => {
    beforeEach(() => {
      component.event = { markets: [], startTime: '' } as any;
    });

    it(`should set 'isSmartBoosts' property`, () => {
      component.ngOnInit();

      expect(component.isSmartBoosts).toBeTruthy();
    });

    it(`should form Name And Score`, () => {
      spyOn(component, 'formNameAndWasPrice');

      component.ngOnInit();

      expect(component.formNameAndWasPrice).toHaveBeenCalled();
    });
  });

  describe('formNameAndWasPrice', () => {
    function callFormNameAndScore(isSmartBoosts) {
      component.isSmartBoosts = isSmartBoosts;
      component.formNameAndWasPrice();
    }

    it(`should set parsed 'outcomeName' if market is SmartBoosts`, () => {
      callFormNameAndScore(true);
      expect(component.oddsName).toEqual(nameStub);
    });

    it(`should set score if market is SmartBoosts`, () => {
      callFormNameAndScore(true);
      expect(component.wasPrice).toEqual(wasPriceStub);
    });

    it(`should Not set score if market is Not SmartBoosts`, () => {
      callFormNameAndScore(false);
      expect(component.wasPrice).toBeUndefined();
    });

    it(`should Not set parsed 'outcomeName' if market is Not SmartBoosts`, () => {
      callFormNameAndScore(false);
      expect(component.oddsName).not.toEqual(nameStub);
    });
  });

  it(`should properly get oddsName`, () => {
    component.eventName = 'test-event-name';
    component.outcomeName = 'test-outcome-name';
    component.outcomes = [{ id: 1 }, { id: 2 }] as any;
    let result = component.oddsName;
    expect(result).toEqual('test-event-name');
    component.outcomes = [];
    result = component.oddsName;
    expect(result).toEqual('test-outcome-name');
    component.outcomes = [{ id: 1 }] as any;
    result = component.oddsName;
    expect(result).toEqual('test-outcome-name');
  });

});

