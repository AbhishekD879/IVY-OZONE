import { LegFactoryService } from '@betslip/services/legFactory/leg-factory.service';
import { ComplexLegService } from '@betslip/services/complexLeg/complex-leg.service';
import { ScorecastSportsLegService } from '@betslip/services/scorecastSportsLeg/scorecast-sports-leg.service';
import { ForecastSportsLegService } from '@betslip/services/forecastSportsLeg/forecast-sports-leg.service';
import { SportsLegService } from '@betslip/services/sportsLeg/sports-leg.service';
import { HandicapSportsLegService } from '@betslip/services/handicapSportsLeg/handicap-sports-leg.service';
import { ILeg } from '@app/bpp/services/bppProviders/bpp-providers.model';

describe('LegFactoryService', () => {
  let legFactoryService: LegFactoryService;
  let complexLegService: ComplexLegService;
  let sportsLegService: SportsLegService;
  let forecastSportsLegService: ForecastSportsLegService;
  let scorecastSportsLegService: ScorecastSportsLegService;
  let handicapSportsLegService: HandicapSportsLegService;

  const betSelections: any[] = [
    {
      isFCTC: true
    }, {
      eachWayOn: jasmine.createSpy('eachWayOn'),
      hasEachWay: true
    }, {
      hasEachWay: false
    }
  ];

  const docs = [jasmine.createSpyObj({
    documentId: jasmine.createSpy()
  }) as ILeg];

  beforeEach(() => {
    complexLegService = jasmine.createSpyObj({
      add: jasmine.createSpy(),
      getTricastForecastLegs: jasmine.createSpy('getTricastForecastLegs')
    });

    sportsLegService = jasmine.createSpyObj({
      construct: jasmine.createSpy(),
      parseAndConstruct: jasmine.createSpy()
    });

    forecastSportsLegService = jasmine.createSpyObj({
      construct: jasmine.createSpy(),
      parseAndConstruct: jasmine.createSpy()
    });

    scorecastSportsLegService = jasmine.createSpyObj({
      construct: jasmine.createSpy(),
      parseAndConstruct: jasmine.createSpy()
    });

    handicapSportsLegService = jasmine.createSpyObj({
      construct: jasmine.createSpy(),
      parseAndConstruct: jasmine.createSpy()
    });

    legFactoryService = new LegFactoryService(complexLegService, sportsLegService, forecastSportsLegService,
      scorecastSportsLegService, handicapSportsLegService);
  });

  it('constructor', () => {
    expect(legFactoryService).toBeTruthy();
  });

  it('constructLegs', () => {
    legFactoryService.constructLegs(betSelections);
    expect(complexLegService.getTricastForecastLegs).toHaveBeenCalledTimes(1);
  });

  it('constructLegs with Lotto Data', () => {
    betSelections[0].isLotto = true;
    legFactoryService.constructLegs(betSelections);
    expect(complexLegService.getTricastForecastLegs).not.toHaveBeenCalled();
  });

  it('parseLegs: should parse strategy', () => {
    legFactoryService.parseLegs(docs);
    expect(sportsLegService.parseAndConstruct).toHaveBeenCalledTimes(1);
  });

  it('constructStrategy', () => {
    expect(
      legFactoryService['constructStrategy']({ type: 'SGL' } as any, 0)
    ).toEqual(jasmine.any(Function));
    expect(
      legFactoryService['constructStrategy']({ type: 'DBL' } as any, 0)
    ).toEqual({});
  });

  it('selectHandicapRangeType', () => {
    expect(legFactoryService['selectHandicapRangeType']({} as any)).toBeFalsy();
    expect(
      legFactoryService['selectHandicapRangeType']({
        handicap: { type: 'AH' }
      } as any)
    ).toBe('ASIAN_FULLTIME');
  });

  it('parseHandicapRangeType', () => {
    expect(legFactoryService['parseHandicapRangeType']({} as any)).toBe('');
    expect(
      legFactoryService['parseHandicapRangeType']({
        sportsLeg: {
          legPart: [{
            range: {
              rangeTypeRef: { id: 'RANGE' }
            }
          }]
        }
      } as any)
    ).toBe('RANGE');
  });

  it('parseCombiType', () => {
    expect(legFactoryService['parseCombiType']({} as any)).toBe('');
    expect(
      legFactoryService['parseCombiType']({
        sportsLeg: {
          outcomeCombiRef: { id: 'SCORECAST' }
        }
      } as any)
    ).toBe('SCORECAST');
  });
});
