import { of as observableOf } from 'rxjs';
import { fakeAsync, tick } from '@angular/core/testing';
import {
  AccaInsuranceSubtitleComponent
} from '@ladbrokesMobile/betslip/components/accaInsuranceSubtitle/acca-insurance-subtitle.component';
import { Bet } from '@betslip/services/bet/bet';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';

describe('AccaInsuranceSubtitleComponent', () => {
  let cmsService;
  let localeService;
  let domSanitizer;
  let accaService;
  let pubSubService;
  let cmsStaticBlock;
  let component: AccaInsuranceSubtitleComponent;

  beforeEach(() => {
    cmsStaticBlock = {
      title_brand: '',
      uri: '/',
      title: 'title',
      lang: '',
      enabled: false,
      htmlMarkup: 'htmlMarkup'
    };
    cmsService = {
      getStaticBlock: jasmine.createSpy('getStaticBlock').and.returnValue(observableOf(cmsStaticBlock)),
      parseContent: jasmine.createSpy('parseContent').and.returnValue('parsed content')
    };
    accaService = {
      accaInsurancePopup: jasmine.createSpy('accaInsurancePopup'),
      getAccaOfferMaxBonus: jasmine.createSpy('getAccaOfferMaxBonus').and.returnValue('25'),
      isAccaInsuranceEligible: jasmine.createSpy('isAccaInsuranceEligible'),
      isAccaInsuranceSuggested: jasmine.createSpy('isAccaInsuranceSuggested')
    };
    localeService = {
      getString: jasmine.createSpy('getString').and.returnValue('message')
    };
    pubSubService = {
      subscribe: jasmine.createSpy('subscribe'),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      API: pubSubApi
  };
    domSanitizer = {
      bypassSecurityTrustHtml: jasmine.createSpy('bypassSecurityTrustHtml').and.returnValue('htmlMarkup'),
      sanitize: jasmine.createSpy('sanitize').and.returnValue(''),
    };

    component = new AccaInsuranceSubtitleComponent(
      cmsService,
      domSanitizer,
      accaService,
      localeService,
      pubSubService
    );
    component.bet = {
      betOffer: {
        offerType: 'eligible',
        offer: {
          freebetTriggerMaxBonus: '25'
        }
      }
    } as Bet;
  });

  describe('ngOnInit', () => {
    it('should get static block content for acca insurance', fakeAsync(() => {
      const successHandler = jasmine.createSpy('successHandler');
      accaService.isAccaInsuranceEligible.and.returnValue(true);
      component.ngOnInit();

      expect(accaService.isAccaInsuranceEligible).toHaveBeenCalledWith(component.bet);
      expect(cmsService.getStaticBlock).toHaveBeenCalledWith('acca-insurance-content');

      cmsService.getStaticBlock('acca-insurance-content').subscribe(successHandler);
      tick();
      expect(successHandler).toHaveBeenCalledWith(cmsStaticBlock);
      expect(accaService.getAccaOfferMaxBonus).toHaveBeenCalledWith(component.bet);
      expect(domSanitizer.bypassSecurityTrustHtml).toHaveBeenCalledWith('htmlMarkup');
      expect(domSanitizer.sanitize).toHaveBeenCalledWith(1, 'htmlMarkup');
      expect(cmsService.parseContent).toHaveBeenCalledWith('', ['25']);
      expect(component.staticBlockContent).toEqual('parsed content');
    }));

    it('should subscribe to open betslip pubsub event', () => {
      accaService.isAccaInsuranceEligible.and.returnValue(true);
      component.ngOnInit();

      expect(pubSubService.subscribe)
        .toHaveBeenCalledWith('AccaInsuranceSubtitleComponent', 'show-slide-out-betslip-true', jasmine.any(Function));
      expect(localeService.getString).toHaveBeenCalledWith('bs.accaInsuranceQualifyMsg');
    });

    it('should not get static block content for acca insurance', () => {
      component.bet.betOffer.offerType = 'suggested';
      accaService.isAccaInsuranceEligible.and.returnValue(false);
      component.ngOnInit();

      expect(cmsService.getStaticBlock).not.toHaveBeenCalledWith('acca-insurance-content');
      expect(accaService.getAccaOfferMaxBonus).not.toHaveBeenCalledWith(component.bet);
    });

    it('should check if acca insurance is enabled in cms and offer is eligible for user', () => {
      accaService.isAccaInsuranceEligible.and.returnValue(true);
      component.ngOnInit();
      expect(component.isAccaInsurance).toBeTruthy();
    });

    it('should check if acca insurance is enabled in cms and offer is eligible for user(negative case)', () => {
      accaService.isAccaInsuranceEligible.and.returnValue(false);
      component.bet.betOffer.offerType = 'suggested';
      component.ngOnInit();

      expect(component.isAccaInsurance).toBeFalsy();
    });
  });

  it('ngOnDestroy: should unsubscribe from pubsub event', () => {
    component.ngOnDestroy();

    expect(pubSubService.unsubscribe)
      .toHaveBeenCalledWith('AccaInsuranceSubtitleComponent');
  });

  describe('passMessageConfig', () => {
    it('should emit message config to show overlay message in betslip(eligible offer)', () => {
      accaService.isAccaInsuranceEligible.and.returnValue(true);
      component.ngOnInit();
      component.passMessageConfigFn.emit = jasmine.createSpy('emit');
      component.passMessageConfig();

      expect(localeService.getString).toHaveBeenCalledWith('bs.accaInsuranceQualifyMsg');
      expect(component.passMessageConfigFn.emit).toHaveBeenCalledWith({ message: 'message', type: 'ACCA' });
    });

    it('should emit message config to show overlay message in betslip(suggested offer)', () => {
      accaService.isAccaInsuranceEligible.and.returnValue(false);
      accaService.isAccaInsuranceSuggested.and.returnValue(true);
      component.passMessageConfigFn.emit = jasmine.createSpy('emit');
      component.bet.betOffer.offerType = 'suggested';
      component.ngOnInit();
      component.passMessageConfig();

      expect(localeService.getString).toHaveBeenCalledWith('bs.accaInsuranceAddOneMoreMsg');
      expect(component.passMessageConfigFn.emit).toHaveBeenCalledWith({ message: 'message', type: 'ACCA' });
    });

    it('should not emit message config to show overlay message in betslip when no offer were found)', () => {
      accaService.isAccaInsuranceEligible.and.returnValue(false);
      accaService.isAccaInsuranceSuggested.and.returnValue(false);
      component.passMessageConfigFn.emit = jasmine.createSpy('emit');
      component.bet.betOffer = {};
      component.ngOnInit();
      component.passMessageConfig();

      expect(localeService.getString).not.toHaveBeenCalled();
      expect(component.passMessageConfigFn.emit).not.toHaveBeenCalledWith({ message: 'message', type: 'ACCA' });
    });
  });

  it('should open acca insurance info dialog', () => {
    component.openAccaInsuranceInfoDialog();

    expect(accaService.accaInsurancePopup).toHaveBeenCalled();
  });
});
