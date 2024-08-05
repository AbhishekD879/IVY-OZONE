// eslint-disable-next-line
import { OutrightsSportTabComponent } from '@sb/components/outrightsSportTab/outrights-sport-tab.component';

describe('#OutrightsSportTabComponent', () => {
  let component: OutrightsSportTabComponent;
  let sportTabsService, pubSubService, routingHelper, slpSpinnerStateService;

  const event = { id: 21312 } as any;

  beforeEach(() => {
    slpSpinnerStateService = {
      handleSpinnerState: jasmine.createSpy('handleSpinnerState')
    };
    sportTabsService = {};
    pubSubService = {};
    routingHelper = {
      formEdpUrl: jasmine.createSpy('formEdpUrl')
    };
    component = new OutrightsSportTabComponent(sportTabsService, pubSubService, routingHelper, slpSpinnerStateService);
  });

  it('@eventURL - should go to EDP', () => {
    component.eventURL(event);
    expect(routingHelper.formEdpUrl).toHaveBeenCalledWith(event);
  });
});
