import { StreamBetTemplatesComponent } from './stream-bet-templates.component';
import { IMarket } from '@core/models/market.model';

describe('StreamBetTemplatesComponent', () => {
  let component: StreamBetTemplatesComponent;
  let streamBetService;
  const market = {
    cashoutAvail: '',
    correctPriceTypeCode: '',
    dispSortName: '',
    eachWayFactorNum: '',
    eachWayFactorDen: '',
    eachWayPlaces: '',
    id: '',
    isLpAvailable: true,
    isMarketBetInRun: true,
    isSpAvailable: true,
    liveServChannels: '',
    isEachWayAvailable: false,
    liveServChildrenChannels: '',
    marketsNames: '',
    marketStatusCode: '',
    name: '',
    nextScore: 0,
    outcomes: [],
    periods: [],
    priceTypeCodes: '',
    terms: '',
    templateMarketId: 0,
    templateMarketName: '',
    viewType: 'inplay',
    label: 'label',
    isTopFinish: true,
    isToFinish: false,
    insuranceMarkets: false,
    isOther: true,
    isWO: false
  } as IMarket;

  beforeEach(() => {
    streamBetService = {
        getMarketTemplate: jasmine.createSpy().and.returnValue('horse-racing-template')
    };
    component = new StreamBetTemplatesComponent(streamBetService);    
  });

  it('StreamBetTemplatesComponent: should create component instance', () => {
    expect(component).toBeTruthy();
  });

  it('StreamBetTemplatesComponent: getMarketTemplate', () => {    
    const eventEntity = {
        categoryId: '21',
        siteChannels: 'M, S, ',
        liveStreamAvailable: true,
        markets: [ market ]
    } as any;
    expect(component.getMarketTemplate(market, eventEntity)).toEqual('horse-racing-template');
  });

  it('StreamBetTemplatesComponent: handleSelectionClick', () => {
    component.selectionClickEmit.emit = jasmine.createSpy();
    component.handleSelectionClick(market);
    expect(component.selectionClickEmit.emit).toHaveBeenCalled();
  });
});
