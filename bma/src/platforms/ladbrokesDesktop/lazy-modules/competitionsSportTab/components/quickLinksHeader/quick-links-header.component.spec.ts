import { QuickLinksHeaderComponent } from './quick-links-header.component';
import QuickLinks from '../../constants/quickLinks';

describe('LadbrokesQuickLinksHeaderComponent', () => {
  let component: QuickLinksHeaderComponent;

  beforeEach(() => {
    component = new QuickLinksHeaderComponent();
  });

  it('constructor', () => {
    expect(component).toBeTruthy();
  });

  it('quickLinks', () => {
    expect(component.quickLinks).toBe(QuickLinks);
  });

  it('should trackQuickLink', () => {
    expect(component.trackQuickLink(1, QuickLinks[0])).toBe(QuickLinks[0].id);
  });
});
