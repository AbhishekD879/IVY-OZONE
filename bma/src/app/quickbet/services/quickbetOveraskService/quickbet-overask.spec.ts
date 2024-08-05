import { QuickbetOveraskService } from './quickbet-overask.service';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';

let pubSubService;
let storageService;
let service;

const quickBetDataMock =  {
  bet: [{
    leg: [
      {
        sportsLeg: {
          legPart: [
            {
              outcomeRef: {
                eventDesc: '',
                id: '100',
                marketDesc: '',
                outcomeDesc: '',
              }
            }
          ],
          winPlaceRef: { id: '' }
        }
      }
    ],
    stake: { stakePerLine: '50' },
  }],
  betslip: {}
};

describe('QuickbetOveraskService', () => {

  beforeEach(() => {
    storageService = jasmine.createSpyObj({
      set: jasmine.createSpy(),
      get: jasmine.createSpy()
    });

    pubSubService = {
      API: pubSubApi,
      publish: jasmine.createSpy('publish')
    };


    service = new QuickbetOveraskService(pubSubService, storageService);
  });

  it('Should call callbacks and set selection into storage ', () => {
    const selectionData = {
      freebet: '',
      selectionType: '',
      isLP: '',
      price: '',
      typeName: '',
      eventIsLive: '',
      hasGP: '',
      isEachWayAvailable: '',
    };
    service.execute(quickBetDataMock, selectionData);
    expect(pubSubService.publish).toHaveBeenCalledWith('show-slide-out-betslip', true);
    expect(pubSubService.publish).toHaveBeenCalledWith('EXECUTE_OVERASK', jasmine.any(Object));
    expect(storageService.set).toHaveBeenCalled();
    expect(storageService.set).toHaveBeenCalledWith('betSelections', jasmine.any(Object));
  });

  it('Should return selection for storage', () => {
    const selectionData = {
      freebet: {
        freebetTokenId: 1
      },
      selectionType: '',
      isLP: '',
      price: '',
      typeName: '',
      eventIsLive: '',
      hasGP: '',
      isEachWayAvailable: '',
      stake: null
    };
    const storageData = {
      outcomesIds: [ '100' ],
      userStake: '',
      userEachWay: false,
      userFreeBet: 1,
      goToBetslip: false,
      id: 'SGL|100',
      price: {
        priceType: 'SP'
      },
      type: 'SGL',
      typeName: '',
      eventIsLive: '',
      hasBPG: '',
      hasEachWay: '',
      isSuspended: false
    };
    const result = service.getSelectionForStorage(quickBetDataMock, selectionData);
    expect(result).toEqual(storageData);

    selectionData.stake = '50.00';
    storageData.userStake = '50';
    expect(service.getSelectionForStorage(quickBetDataMock, selectionData)).toEqual(storageData);

    selectionData.isLP = 'true';
    selectionData.price = { priceType: 'LP' } as any;
    storageData.price.priceType = 'LP';

    expect(service.getSelectionForStorage(quickBetDataMock, selectionData)).toEqual(storageData);
  });

  it('Should return selection for storage x2', () => {
    const selectionData = {
      selectionType: 'scorecast',
      isLP: '',
      price: '',
      typeName: '',
      eventIsLive: '',
      hasGP: '',
      isEachWayAvailable: '',
      stake: '50.00'
    };
    const result = service.getSelectionForStorage(quickBetDataMock, selectionData);
    expect(result).toEqual({
      outcomesIds: ['100'],
      userStake: '50',
      userEachWay: false,
      userFreeBet: '',
      goToBetslip: false,
      id: 'SCORECAST|100',
      price: { priceType: 'SP' },
      type: 'SCORECAST',
      typeName: '',
      eventIsLive: '',
      hasBPG: '',
      hasEachWay: '',
      isSuspended: false
    });
  });

  it('Should return array of outcome Ids', () => {
    expect(service.getOutcomeIds(quickBetDataMock.bet[0].leg[0].sportsLeg.legPart)).toEqual(['100']);
  });
});
