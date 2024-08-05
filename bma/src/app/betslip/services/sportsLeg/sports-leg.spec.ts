import { IBetSelection } from '@betslip/services/betSelection/bet-selection.model';
import { SportsLeg } from '@betslip/services/sportsLeg/sports-leg';

describe('#SportsLeg', () => {
  let sportsLeg;

  const betSelection = {
    outcomeId: '858258950',
    handicap: 'handicap',
    winPlace: 'WIN',
    price: {
      priceNum: 7,
      priceDen: 5
    },
    docId: '1'
  } as Partial<IBetSelection> as IBetSelection;

  beforeEach(() => {
    const sportsLegPriceService = jasmine.createSpyObj('sportsLegPriceService', {
      parse: jasmine.createSpy('parse'),
      construct: jasmine.createSpy('construct')
    });
    const betSelectionsService = jasmine.createSpyObj('betSelectionsService', ['some'] );
    const selection: IBetSelection = betSelection;
    const docId = 1;
    const partsType = jasmine.createSpyObj('legPartService', {
      construct: jasmine.createSpy('construct').and.returnValue({})
    });

    sportsLeg = new SportsLeg(sportsLegPriceService, betSelectionsService, selection, docId, partsType);
  });

  it('should init values', () => {
    expect(sportsLeg.winPlace).toBe(betSelection.winPlace);
    expect(sportsLeg.combi).toBe(betSelection.combi);
    expect(sportsLeg.price).toBeDefined();
    expect(sportsLeg.selection).toBe(betSelection);
    expect(sportsLeg.docId).toBe(Number(betSelection.docId));
    expect(sportsLeg.sportsLegPriceService.construct).toHaveBeenCalled();
  });

  it('should return priceParams', () => {
    const res = sportsLeg.newPrice({ doc: 'doc' });

    expect(res.doc).toBe('doc');
  });

  it('should call sportsLeg.sportsLegPriceService.construct()', () => {
    sportsLeg.newPrice({ });
    expect(sportsLeg.sportsLegPriceService.construct).toHaveBeenCalled();
  });

  describe('doc method testing', () => {
    const docMethodResult = { },
      part = { outcome: { details: { isGpAvailable: true } } },
      parts = [part];

    beforeEach(() => {
      spyOn(sportsLeg, 'renderPart').and.returnValue({ legPart: 'legPart' });
      spyOn(sportsLeg, 'setPlaces');
      sportsLeg.parts = parts;
      const spy = sportsLeg.price = jasmine.createSpyObj('price', ['doc']);
      spy.doc.and.returnValue(docMethodResult);
    });

    it('should call renderPart(), setPlaces(), price.doc()', () => {
      sportsLeg.doc(true);

      expect(sportsLeg.renderPart).toHaveBeenCalledWith(part);
      expect(sportsLeg.setPlaces).toHaveBeenCalledWith(sportsLeg.selection, 'legPart');
      expect(sportsLeg.price.doc).toHaveBeenCalledWith(true, true);
    });

    it('should return correct result', () => {
      const res = sportsLeg.doc(true);
      const expectedRes = '{"documentId":1,"sportsLeg":{"legPart":["legPart"],"winPlaceRef":{"id":"WIN"}}}';

      expect(JSON.stringify(res)).toBe(expectedRes);
    });

    it('should handle combi ref', () => {
      sportsLeg.combi = 'SCORECAST';
      const res = sportsLeg.doc(true);
      expect(res.sportsLeg.outcomeCombiRef).toEqual({ id: 'SCORECAST' });
    });
  });

  it('should call doc()', () => {
    const part = jasmine.createSpyObj('part', ['doc']);

    part.doc = jasmine.createSpy('doc');

    sportsLeg.renderPart(part);

    expect(part.doc).toHaveBeenCalled();
  });

  describe('setPlaces', () => {
    it('should set places', () => {
      const part: any[] = [{}];
      sportsLeg.setPlaces({ combi: 'combi' }, part);
      expect(part[0].places).toBe('*');
    });

    it('should not set places', () => {
      const part: any[] = [{}];
      sportsLeg.setPlaces({ combi: 'SCORECAST' }, part);
      expect(part[0].places).toBeUndefined();
    });
  });

  it('normalizeCombiName', () => {
    sportsLeg.combi = 'FORECAST';
    sportsLeg.normalizeCombiName();
    expect(sportsLeg.combi).toBe('FORECAST');

    sportsLeg.combi = 'FORECAST_COM';
    sportsLeg.normalizeCombiName();
    expect(sportsLeg.combi).toBe('FORECAST');
  });
});
