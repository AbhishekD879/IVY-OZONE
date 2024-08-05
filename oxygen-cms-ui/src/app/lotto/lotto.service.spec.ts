import { of } from 'rxjs';
import { LOTTO_VALUES } from './lotto.mock';
import { LottoService } from './lotto.service';
describe('LottoService', () => {
  let service,
  globalLoaderService,
  apiClientService
  let lotto = LOTTO_VALUES;
  beforeEach(() => {
    globalLoaderService = {
      showLoader: jasmine.createSpy('showLoader'),
      hideLoader: jasmine.createSpy('hideLoader')
  };
  apiClientService = {
    lottosService : jasmine.createSpy('lottosService').and.returnValue ({
      saveLotto: jasmine.createSpy('saveLotto').and.returnValue(of({body: lotto})),
      getLottery: jasmine.createSpy('getLottery').and.returnValue(of({body: lotto}))
    })
  };
  service = new LottoService (
    globalLoaderService,
    apiClientService
  );
});
    it('should call wrappedObservable and call saveLotto', () => {
      spyOn(service, 'wrappedObservable');
      service.createLotto('1');
      service.getData = {id:'1'};
      expect(apiClientService.lottosService().saveLotto).toHaveBeenCalledWith('1');
      expect(service.wrappedObservable).toHaveBeenCalledWith(service.getData);    
  });
    it('should call wrappedObservable and call getLottery', () => {
    spyOn(service, 'wrappedObservable');
    service.getLottery('1');
    service.getData = {id:'1'};
    expect(apiClientService.lottosService().getLottery).toHaveBeenCalledWith('1');
    expect(service.wrappedObservable).toHaveBeenCalledWith(service.getData);    
  });
  it('should call hideloader', () => {
    service.handleRequestError('error');
    expect(globalLoaderService.hideLoader).toHaveBeenCalled();
  });
});
