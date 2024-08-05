import { FiveasideBetHeaderComponent
} from '@lazy-modules/fiveASideShowDown/components/fiveASideBetHeader/fiveaside-bet-header.component';

describe('FiveasideBetHeaderComponent', () => {
  let component: FiveasideBetHeaderComponent;
  let router,
  rulesEntryService;

  beforeEach(() => {
    router = {
      navigateByUrl: jasmine.createSpy('navigateByUrl').and.returnValue(Promise.resolve('success'))
    };
    rulesEntryService = {
      trackGTMEvent: jasmine.createSpy('trackGTMEvent')
    };
    component = new FiveasideBetHeaderComponent(router, rulesEntryService);
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
  xit('#onWidgetClick should trigger and navigate', () => {
    component.bet = {
      event: ['123456'],
      id: '2379097305',
      source: 'f',
      contestId: '60eb075772149d6475386619',
      leg: [{ part: [{ outcome: [{}] }] }]
    };
    component.onWidgetClick();
    expect(router.navigateByUrl).toHaveBeenCalled();
  });
});
