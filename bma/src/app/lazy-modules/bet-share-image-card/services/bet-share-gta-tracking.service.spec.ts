import { BetShareGTAService } from "./bet-share-gta-tracking.service";

describe('BetShareGTAService', () => {

    let gtmService;
    let service: BetShareGTAService;

    beforeEach(() => {
        gtmService={
            push: jasmine.createSpy('push')
          };
        service = new BetShareGTAService(gtmService)
    })

      it("Should  send gtm data  when more than 5 is false", () => {
        service.setGtmData('', '', '');
        expect(gtmService.push).toHaveBeenCalled();
      })
    });