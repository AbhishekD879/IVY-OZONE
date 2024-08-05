import { commandApi } from '../communication/command/command-api.constant';
import { pubSubApi } from '../communication/pubsub/pubsub-api.constant';
import { DigitalSportBetsService } from './digital-sport-bets.service';
describe('DigitalSportsBetsService', () => {

  let service: DigitalSportBetsService;

  let command;
  let storage;
  let user;
  let pubsub;

  beforeEach(() => {
    user = {
      oddsFormat: 'mockString',
    };
    storage = {
      get: jasmine.createSpy().and.returnValue(true)
    };
    command = {
      executeAsync: jasmine.createSpy().and.returnValue(Promise.resolve(null)),
      API: commandApi
    };
    pubsub = {
      subscribe: jasmine.createSpy(),
      API: pubSubApi
    };

    service = new DigitalSportBetsService(
      user,
      storage,
      command,
      pubsub
    );
  });


  it('should call iframe \'postMessage\' with correct params', () => {
    const iframe = document.createElement('iframe');
    iframe.src = 'about:blank';
    document.body.appendChild(iframe);
    iframe.contentWindow.postMessage = jasmine.createSpy();
    service.sendOddsToDS('token', iframe);
    expect(iframe.contentWindow.postMessage).toHaveBeenCalledWith('ds:odds:mockString', '*' as any);
    service.sendOddsToDS(undefined, iframe);
    expect(iframe.contentWindow.postMessage).toHaveBeenCalledTimes(1);
  });

  it('should subscribe to \'digitalSportBetsFactory\' channel', () => {
    const callback = () => {};
    service.getDSBetslipCounter(callback);
    expect(command.executeAsync).toHaveBeenCalledWith(command.API.DS_READY, undefined, 0);
    expect(pubsub.subscribe).toHaveBeenCalledWith('digitalSportBetsFactory', pubsub.API.DS_BETSLIP_COUNTER_UPDATE, callback);
  });
});
