import { FirstBetGAService } from "./first-bet-ga.service";

describe('setGtmData', () => {

    let gtmService;
    let service: FirstBetGAService;

    beforeEach(() => {
        gtmService={
            push: jasmine.createSpy('push')
          };
        service = new FirstBetGAService(gtmService)
    })

      it("Should  send gtm data  when more than 5 is false", () => {
        service.setGtmData('', '', '', '', '');
        expect(gtmService.push).toHaveBeenCalled();
      })
    });