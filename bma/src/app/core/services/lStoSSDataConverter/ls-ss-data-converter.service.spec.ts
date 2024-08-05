import { LStoSSDataStructureConverterService } from './ls-ss-data-converter.service';
import { ILiveServeUpdMock } from './ls-ss-data-converter.service.mock';

describe('LStoSSDataStructureConverterService', () => {
  let service: LStoSSDataStructureConverterService;
  let fracToDecService;

  beforeEach(() => {
    fracToDecService = {
      getDecimal: jasmine.createSpy().and.returnValue(1.11)
    };

    service = new LStoSSDataStructureConverterService(fracToDecService);
  });

  describe('convertData', () => {
    let update;

    beforeEach(() => {
      update = {
        payload: JSON.parse(JSON.stringify(ILiveServeUpdMock.lsOutcome)),
        subject_type: 'sSELCN',
        subject_number: ILiveServeUpdMock.lsOutcome.subject_number
      };
    });

    it('should convert update message with subject in payload property', () => {});
    it('should convert update message with subject outside payload property', () => {
      delete update.payload.subject;
      update.subject = ILiveServeUpdMock.lsOutcome.subject;
    });
    it('should convert update message with subject both in and outside payload property', () => {
      update.subject = 'sNOT_INCLUDED';
    });
    afterEach(() => {
      expect(service.convertData(update)).toEqual(<any>{
        id: '446334653',
        displayOrder: '0',
        liveServChannels: 'sTEST0446334653',
        name: 'test',
        marketId: '116106848',
        outcomeMeaningMinorCode: 'H',
        outcomeStatusCode: 'A',
        prices: [{ priceNum: 1, priceDen: 9, priceType: 'LP', priceDec: 1.11 }],
        outcomeMeaningScores: '1,1,'
      });
    });
  });

  it('it should return string with id\'s', () => {
    const result = '255, 35,1367, 619,1333, 400,',
      allIds = service['mapToCollectionIds'](<any>ILiveServeUpdMock.lsMarket);

    expect(allIds).toEqual(result);
  });

  it('it should return string with collection id\'s', () => {
    const result = ',1367, 619,1333, 400',
      collectionIds = service['fromCollectionToString'](<any>ILiveServeUpdMock.lsMarket.collections);

    expect(<any>collectionIds).toEqual(<any>result);
  });

  it('it should convert new LS selection to SS format', () => {
    const type = 'sSELCN';

    const res = service['convert'](
      type,
      <any>ILiveServeUpdMock.lsOutcome,
      ILiveServeUpdMock.lsOutcome.subject_number,
    );
    expect(<any>res).toEqual(<any>ILiveServeUpdMock.resultOutcome);
  });

  it('it should convert new LS market to SS format', () => {
    const type = 'sEVMKT';
    const res = service['convert'](
      type,
      <any>ILiveServeUpdMock.lsMarket,
      ILiveServeUpdMock.lsMarket.subject_number
    );
    expect(<any>res).toEqual(<any>ILiveServeUpdMock.resultMarket);
  });
});
