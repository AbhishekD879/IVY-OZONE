import { BetpackEmptyPageComponent } from "./betpack-empty-page.component";
import {
  fakeAsync
} from "@angular/core/testing";

describe("BetpackInfopageComponent", () => {
  let component, betReceiptService,storageService, gtmService;

  beforeEach(() => {
    betReceiptService= jasmine.createSpy("betReceiptService");
    storageService = {
      set: jasmine.createSpy("storageService.set"),
      get: jasmine.createSpy("storageService.get"),
    };
    gtmService = {
      push: jasmine.createSpy("push"),
    };
    getComponentInstance();
  });
  const getComponentInstance = () => {
    component = new BetpackEmptyPageComponent(betReceiptService,storageService, gtmService);
  };
  describe("onInit", () => {
    it("sendGtmData isReview false", fakeAsync(() => {
      component.isReview=false;
      component.ngOnInit();
      expect(gtmService.push).toHaveBeenCalledWith('trackEvent', { event: 'trackEvent', eventAction: 'bet bundles', eventCategory: 'bet bundles marketplace', eventLabel: 'bet bundles is empty' });
    }));
    it("sendGtmData isReview true", fakeAsync(() => {
      component.isReview=true;
      component.ngOnInit();
      expect(gtmService.push).toHaveBeenCalledWith('trackEvent', { event: 'trackEvent', eventAction: 'my bet bundles', eventCategory: 'bet bundles marketplace', eventLabel: 'bet bundles is empty' });
    }));
  });
});
