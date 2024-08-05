import { commandApi } from '@core/services/communication/command/command-api.constant';
import { BannerClickService } from '@core/services/aemBanners/banner-click.service';

describe('BannerClickService', () => {
  let service: BannerClickService;
  let mouseEvent;
  let offer;
  let router;
  let windowRefService;
  let command;

  beforeEach(() => {
    router = { navigateByUrl: jasmine.createSpy('navigateByUrl') };

    windowRefService = {
      nativeWindow: jasmine.createSpyObj('nativeWindow', ['open'])
    };

    command = {
      executeAsync: jasmine.createSpy().and.returnValue(Promise.resolve({})),
      API: commandApi
    };

    offer = {
      link : 'some/link',
      target: '_blank'
    };

    mouseEvent = jasmine.createSpyObj('mouseEvent', ['preventDefault']);

    service = new BannerClickService(
      router,
      windowRefService,
      command
    );
  });

  it('should open external link in same window', () => {
    offer.link = 'http://external.com';
    offer.target = '_self';
    service.handleBannerClick(mouseEvent, offer, false);
    expect(windowRefService.nativeWindow.open).toHaveBeenCalledWith('http://external.com', '_self');
  });

  it('should open link in app with router', () => {
    offer.link = 'another/internal/url';
    offer.target = '_self';
    service.handleBannerClick(mouseEvent, offer, false);
    expect(router.navigateByUrl).toHaveBeenCalledWith('another/internal/url');
  });

  it('should open adding to betslip', () => {
    offer.link = 'betslip/add/893075493';
    offer.target = '_self';
    service.handleBannerClick(mouseEvent, offer, false);
    expect(command.executeAsync).toHaveBeenCalledWith(command.API.ADD_TO_BETSLIP_BY_OUTCOME_IDS, ['893075493', true, true, false]);
  });

  it('should open adding to betslip only with 1 id with wrong ids separator', () => {
    offer.link = 'betslip/add/123456789-893075493';
    offer.target = '_self';
    service.handleBannerClick(mouseEvent, offer, false);
    expect(command.executeAsync).toHaveBeenCalledWith(command.API.ADD_TO_BETSLIP_BY_OUTCOME_IDS, ['123456789', true, true, false]);
  });

  it('should open adding to betslip with 2 ids', () => {
    offer.link = 'betslip/add/123,456';
    offer.target = '_self';
    service.handleBannerClick(mouseEvent, offer, false);
    expect(command.executeAsync).toHaveBeenCalledWith(command.API.ADD_TO_BETSLIP_BY_OUTCOME_IDS, ['123,456', true, true, false]);
  });

  it('should not open adding to betslip', () => {
    offer.link = 'betslip/add/noid';
    offer.target = '_self';
    service.handleBannerClick(mouseEvent, offer, false);
    expect(command.executeAsync).not.toHaveBeenCalledWith(command.API.ADD_TO_BETSLIP_BY_OUTCOME_IDS, ['noid', true, true, false]);
    expect(router.navigateByUrl).toHaveBeenCalledWith('betslip/add/noid');
  });

  it('should not open adding to betslip - link is empty', () => {
    offer.link = '';
    offer.target = '_self';
    service.handleBannerClick(mouseEvent, offer, false);
    expect(command.executeAsync).not.toHaveBeenCalled();
    expect(router.navigateByUrl).not.toHaveBeenCalled();
  });
});
