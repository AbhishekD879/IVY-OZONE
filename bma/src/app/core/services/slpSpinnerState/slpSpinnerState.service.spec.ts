
import { SlpSpinnerStateService } from './slpSpinnerState.service';

describe('#SlpSpinnerStateService', () => {
  let service: SlpSpinnerStateService;

  beforeEach(() => {
    service = new SlpSpinnerStateService();
  });

  describe('#createSpinnerStream', () => {
    it('should create stream', () => {
      expect(service.slpSpinnerStateObservable$).toBeUndefined();
      service.createSpinnerStream();

      expect(service.slpSpinnerStateObservable$).toBeDefined();
    });
  });

  describe('#handleSpinnerState', () => {
    it('should handle state', () => {
      service.createSpinnerStream();
      service.handleSpinnerState();

      expect(service['spinnersCounter']).toEqual(2);
    });

    it('should handle state when no slpSpinnerStateObservable$', () => {
      service.handleSpinnerState();

      expect(service['spinnersCounter']).toEqual(1);
    });

    it('should handle state when slpSpinnerStateObservable$ is closed', () => {
      service.createSpinnerStream();
      expect(service['spinnersCounter']).toEqual(1);
      service.handleSpinnerState();
      expect(service['spinnersCounter']).toEqual(2);
      service.clearSpinnerState();
      expect(service['spinnersCounter']).toEqual(1);
      service.handleSpinnerState();
      expect(service['spinnersCounter']).toEqual(1);
    });
  });

  describe('#clearSpinnerState', () => {
    it('should clear state spinnersCounter', () => {
      service['spinnersCounter'] = 3;
      service.clearSpinnerState();

      expect(service['spinnersCounter']).toEqual(1);
    });

    it('should clear state for slpSpinnerStateObservable$', () => {
      service.createSpinnerStream();
      expect(service.slpSpinnerStateObservable$.closed).toEqual(false);
      expect(service.slpSpinnerStateObservable$.isStopped).toEqual(false);

      service['spinnersCounter'] = 3;
      service.clearSpinnerState();

      expect(service['spinnersCounter']).toEqual(1);
      expect(service.slpSpinnerStateObservable$.closed).toEqual(true);
      expect(service.slpSpinnerStateObservable$.isStopped).toEqual(true);
    });
  });
});
