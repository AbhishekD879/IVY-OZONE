// eslint-disable-next-line
import { CompetitionsOutrightsTabComponent } from '@lazy-modules/competitionsSportTab/components/competitionsPage/competitionsPageTabs/competitions-outrights-tab.component';

describe('#CompetitionsOutrightsTabComponent', () => {
  let component: CompetitionsOutrightsTabComponent;
  let routingHelper;

  const event = { id: 21312 } as any;

  beforeEach(() => {
    routingHelper = {
      formEdpUrl: jasmine.createSpy('formEdpUrl')
    };
    component = new CompetitionsOutrightsTabComponent(routingHelper);
  });

  it('@trackById - should track event ', () => {
    component.trackById(event);
    expect(component.trackById(event)).toBe(21312);
  });

  it('@eventURL - should go to EDP', () => {
    component.eventURL(event);
    expect(routingHelper.formEdpUrl).toHaveBeenCalledWith(event);
  });
});
