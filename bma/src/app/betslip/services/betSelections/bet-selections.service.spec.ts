import { BetSelectionsService } from '@betslip/services/betSelections/bet-selections.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { IBetSelection } from '@betslip/services/betSelection/bet-selection.model';

describe('BetSelectionsService', () => {
  let betSelectionService: BetSelectionsService;
  let pubSubService: PubSubService;

  const betSelection: IBetSelection = {
    id: 32432
  } as IBetSelection;

  beforeEach(() => {
    pubSubService = jasmine.createSpyObj({
      publishSync: jasmine.createSpy(),
      API: jasmine.createSpy()
    });

    betSelectionService = new BetSelectionsService(pubSubService);
    betSelectionService.selectionsData = [{
      id: 'SCORECAST|123|345',
      params: {
        id: 'SCORECAST|123|345'
      }
    }];
  });

  it('constructor', () => {
    expect(betSelectionService).toBeTruthy();
    expect(betSelectionService.selectionsData).toBeTruthy();
  });

  it('addSelection', () => {
    spyOn(betSelectionService.selectionsData, 'push');
    betSelectionService.addSelection(betSelection);

    expect(betSelectionService.selectionsData.push).toHaveBeenCalledWith(betSelection);
    expect(pubSubService.publishSync).toHaveBeenCalledWith(
      pubSubService.API.BETSLIP_SELECTIONS_UPDATE,
      jasmine.any(Object));
  });

  it('removeSelection', () => {
    spyOn(betSelectionService.selectionsData, 'splice');
    betSelectionService.removeSelection(betSelection);

    expect(betSelectionService.selectionsData.splice).toHaveBeenCalled();
    expect(pubSubService.publishSync).toHaveBeenCalledWith(
      pubSubService.API.BETSLIP_SELECTIONS_UPDATE,
      jasmine.any(Object));
  });

  it('removeMultiSelection', () => {
    spyOn(betSelectionService.selectionsData, 'splice');
    betSelectionService.removeMultiSelection(<any>[betSelection]);

    expect(betSelectionService.selectionsData.splice).toHaveBeenCalled();
    expect(pubSubService.publishSync).toHaveBeenCalledWith(
      pubSubService.API.BETSLIP_SELECTIONS_UPDATE,
      jasmine.any(Object));
  });

  it('removeSelectionById', () => {
    spyOn(betSelectionService, 'removeSelection');
    betSelectionService.removeSelectionById(123);

    expect(betSelectionService.removeSelection).toHaveBeenCalled();
  });

  describe('getOutcome', () => {
    it('should getOutcome', () => {
      betSelectionService.selectionsData = [
        {
          outcomes: [
            {
              id: '10'
            }
          ]
        }
      ];

      expect(betSelectionService.getOutcome('10')).toEqual(betSelectionService.selectionsData[0].outcomes[0]);
    });

    it('should getOutcome (null)', () => {
      betSelectionService.selectionsData = [
        {
          outcomes: [
            {
              id: '20'
            }
          ]
        }
      ];

      expect(betSelectionService.getOutcome('10')).toEqual(null);
    });
  });

  it('flush', () => {
    betSelectionService.flush();

    expect(betSelectionService.selectionsData.length).toEqual(0);
    expect(pubSubService.publishSync).toHaveBeenCalledWith(
      pubSubService.API.BETSLIP_SELECTIONS_UPDATE,
      jasmine.any(Object));
  });

  it('count', () => {
    const result = betSelectionService.count();

    expect(result).toEqual(betSelectionService.selectionsData.length);
  });

  it('mapParsed', () => {
    betSelectionService.findById = jasmine.createSpy('findById');

    betSelectionService.mapParsed({
      outcomes: [{ id: '1' }]
    } as any);
    betSelectionService.mapParsed({
      combi: 'FORECAST',
      outcomes: [{ id: '1' }, { id: '2' }],
      legParts: [{ places: '1' }, { places: '2' }]
    } as any);
    betSelectionService.mapParsed({
      combi: 'FORECAST',
      outcomes: [{ id: '1' }, { id: '2' }],
      legParts: [{ places: '*' }, { places: '*'} ]
    } as any);

    expect(betSelectionService.findById).toHaveBeenCalledWith('SGL|1');
    expect(betSelectionService.findById).toHaveBeenCalledWith('FORECAST|1|2');
    expect(betSelectionService.findById).toHaveBeenCalledWith('FORECAST_COM|1|2');
  });

  describe('findById', () => {
    it('should find if scorecast bet is already in betslip', () => {
      expect(betSelectionService.findById('SCORECAST|123|345')).toEqual({
        id: 'SCORECAST|123|345',
        params: { id: 'SCORECAST|123|345' }
      } as IBetSelection);
    });

    it('should find if SGL bet is already in betslip', () => {
      betSelectionService.selectionsData = [{
        id: '123',
        params: {
          id: '123'
        }
      }];
      expect(betSelectionService.findById('123')).toEqual({
        id: '123',
        params: { id: '123' }
      } as IBetSelection);
    });

    it('should set bet if betFound is undefined', () => {
      betSelectionService.selectionsData = [{
        id: '123',
        params: {
          id: '123'
        }
      }];
      expect(betSelectionService.findById('431')).toBeUndefined();
    });

    it('should set bet if there is no selectionsData', () => {
      betSelectionService.selectionsData = [];
      expect(betSelectionService.findById('431')).toBeUndefined();
    });

    it('should findById if there is no selectionsData (SCORECAST)', () => {
      betSelectionService.selectionsData = [];
      expect(betSelectionService.findById('SCORECAST|431|5')).toBeUndefined();
    });

    it('should findById (!betFound)', () => {
      betSelectionService.data = [{
        params: {
          id: '15'
        }
      }];
      expect(betSelectionService.findById('15')).toEqual(betSelectionService.data[0]);
    });
  });
});
