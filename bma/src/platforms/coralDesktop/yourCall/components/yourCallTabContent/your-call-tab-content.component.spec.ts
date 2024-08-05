import { DesktopYourCallTabContentComponent
} from '@coralDesktop/yourCall/components/yourCallTabContent/your-call-tab-content.component';

describe('DesktopYourCallTabContentComponent', () => {

  let component: DesktopYourCallTabContentComponent;
  let yourCallService, yourCallMarketsService, yourCallDashboardService;

  beforeEach(() => {
    yourCallService = {};
    yourCallMarketsService = {};
    yourCallDashboardService = {};

    component = new DesktopYourCallTabContentComponent();
  });

  it('should set text to LowerCase', () => {
    expect(component.getTitle('TEXT To LoWerCase')).toBe('text to lowercase');
    expect(component.getTitle(undefined)).toBe('');
  });
});
