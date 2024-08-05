// import { ILeg } from '../models/bet.model';
import { LottoBuildBetDocService } from './lotto-build-bet-doc.service';
import { lottoMock } from './lotto-build-bet.mock';
describe('LottoBuildBetDocService', () => {
  let service: LottoBuildBetDocService,

    deviceService,
    clientUserAgentService,
    timeSyncService,
    betslipStakeService;

  beforeEach(() => {
    deviceService = {
      channel: {
        channelRef: ''
      }
    };
    clientUserAgentService = {
      getId: jasmine.createSpy('getId').and.returnValue('')
    };
    timeSyncService = {ip: ''};
    betslipStakeService = {
      getTotalStake: jasmine.createSpy('getTotalStake').and.returnValue(0.10)
    };

    service = new LottoBuildBetDocService(deviceService, clientUserAgentService, timeSyncService, betslipStakeService);
  });

  describe('constructPlaceBetObj', () => {
   
    it('should form the bet placement payload', () => {
     const payload =  service.constructPlaceBetObj(lottoMock.input, 'GBP') as any;
     expect(payload).toEqual(lottoMock.output);
    });
  });
});
