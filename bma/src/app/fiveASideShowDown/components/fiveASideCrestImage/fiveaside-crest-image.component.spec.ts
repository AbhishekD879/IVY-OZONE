import { FiveasideCrestImageComponent } from '@app/fiveASideShowDown/components/fiveASideCrestImage/fiveaside-crest-image.component';

describe('FiveasideCrestImageComponent', () => {
  let component: FiveasideCrestImageComponent;
  let leaderboardService;

  beforeEach(() => {
    leaderboardService = {
      checkHexColor: jasmine.createSpy('checkHexColor').and.returnValue('#0000')
    };
    component = new FiveasideCrestImageComponent(leaderboardService as any);
  });
  it('should create', () => {
    expect(component).toBeTruthy();
  });
  it('should assign background color in ngOnInit', () => {
    component.team = { primaryColour: '#1234', secondaryColour: '#1234'};
    component.ngOnInit();
    expect(component.backgroundColor).not.toBeNull();
  });
});
