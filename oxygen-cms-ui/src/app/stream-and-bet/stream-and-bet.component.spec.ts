import { StreamAndBetComponent } from './stream-and-bet.component';
import { of } from 'rxjs';

describe('StreamAndBetComponent', () => {
  let component: StreamAndBetComponent;
  let dialogService, dialog, globalLoaderService, streamAndBetAPIService;
  beforeEach(() => {
    dialogService = {};
    dialog = {};
    globalLoaderService = {
      showLoader: jasmine.createSpy('showLoader'),
      hideLoader: jasmine.createSpy('hideLoader')
    };
    streamAndBetAPIService = {
      getStreamAndBetData: jasmine.createSpy('getStreamAndBetData').and.returnValue(of({body: []})),
      postNewStreamAndBet: jasmine.createSpy('postNewStreamAndBet').and.returnValue(of({body: []})),
      getSiteServeCategories: jasmine.createSpy('getSiteServeCategories').and.returnValue(of({body: []}))
    };
    component = new StreamAndBetComponent(
      dialogService,
      dialog,
      globalLoaderService,
      streamAndBetAPIService
    );
    component.ngOnInit();
  });

  it('should create', () => {
    expect(streamAndBetAPIService.getStreamAndBetData).toHaveBeenCalled();
    expect(streamAndBetAPIService.postNewStreamAndBet).toHaveBeenCalled();
    expect(streamAndBetAPIService.getSiteServeCategories).toHaveBeenCalled();
  });
});
