import { SportsLegService } from './sports-leg.service';

describe('#SportsLegService', () => {
  let sportsLegService;
  beforeEach(() => {

    const sportsLegPriceService = jasmine.createSpyObj('sportsLegPriceService', {
      parse: jasmine.createSpy('parse')
    });

    const betSelectionsService = jasmine.createSpyObj('betSelectionsService', ['some'] );

    sportsLegService = new SportsLegService(sportsLegPriceService, betSelectionsService);
  });

  it('should return SportsLeg object', () => {
    const selection = {};
    const res = sportsLegService.construct(selection, 10, {});

    expect(res).toBeDefined();
    expect(typeof res).toBe('object');
  });

  it('should return parced object', () => {
    const root = {
      sportsLeg: {
        winPlaceRef: {
          id: 'WIN'
        },
        legPart: [
          {
            outcomeRef: {
              id: '861252286'
            }
          }
        ],
        price: {
          priceNum: '13',
          priceDen: '10',
          priceTypeRef: {
            id: 'LP'
          }
        }
      },
      documentId: '1'
    };

    const res = sportsLegService.parse(root);

    expect(sportsLegService.sportsLegPriceService.parse).toHaveBeenCalled();
    expect(res).toBeDefined();
  });

  it('should parse outcome combi ref', () => {
    const res = sportsLegService.parse({
      sportsLeg: {
        winPlaceRef: {},
        outcomeCombiRef: { id: 'FORECAST' },
        legPart: []
      }
    });
    expect(res.combi).toBe('FORECAST');
  });
});
