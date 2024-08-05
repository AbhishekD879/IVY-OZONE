import { LegService } from '@betslip/services/leg/leg.service';
import { BetSelectionsService } from '@betslip/services/betSelections/bet-selections.service';
import { JsonElement } from '@betslip/services/json-element';
import { IDocRef } from '@app/bpp/services/bppProviders/bpp-providers.model';
import { IBetSelection } from '@betslip/services/betSelection/bet-selection.model';
import { Leg } from '@betslip/services/leg/leg';

describe('LegService', () => {
  let legService: LegService;
  let betSelectionService: BetSelectionsService;

  const _doc: IDocRef = jasmine.createSpyObj({
    documentId: jasmine.createSpy()
  });

  const betSelection: IBetSelection = jasmine.createSpyObj({
    id: jasmine.createSpy()
  });

  beforeEach(() => {
    betSelectionService = jasmine.createSpyObj({
      mapParsed: jasmine.createSpy()
    });

    legService = new LegService(betSelectionService);
  });

  it('constructor', () => {
    expect(legService).toBeTruthy();
  });

  it('construct: should return  Leg instance', () => {
    const result = legService.construct(betSelection, 1);
    expect(result).toEqual(jasmine.any(Leg));
  });

  it('parseAndConstruct: should parse data and construct legs', () => {
    spyOn(legService, 'parse');
    spyOn(legService, 'construct');

    legService.parseAndConstruct(_doc);
    expect(legService.parse).toHaveBeenCalledWith(_doc);
    expect(legService.construct).toHaveBeenCalled();
    expect(betSelectionService.mapParsed).toHaveBeenCalled();
  });

  it('parse: should create parsed object', () => {
    const result = legService.parse(_doc);

    expect(result).toEqual({ abstract: 'leg', _doc });
  });

  it('doc: should use json format ', () => {
    spyOn(JsonElement, 'element');
    legService.doc();

    expect(JsonElement.element).toHaveBeenCalledWith('leg', { abstract: 'leg' });
  });
});
