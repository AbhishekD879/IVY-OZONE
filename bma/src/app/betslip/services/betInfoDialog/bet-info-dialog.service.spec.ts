import { fakeAsync, tick } from '@angular/core/testing';

import { BetInfoDialogService } from './bet-info-dialog.service';
import { LocaleService } from '@core/services/locale/locale.service';
import environment from '@environment/oxygenEnvConfig';

describe('BetInfoDialogService', () => {

  let service: BetInfoDialogService;
  let localeService: any = LocaleService;
  let infoDialogService;
  let cmsService
  let buttons;
  let env;
  const betsdata = [{multiplier:'2', num_win:'4'}, {multiplier:'2', num_win:'5'}, {multiplier:'2', num_win:'6'},{multiplier:'2', num_win:'1'}];
  

  beforeEach(() => {
    env = <any>environment;

    localeService = {
      getString: jasmine.createSpy('getString').and.callFake(value => value)
    } as any;

    cmsService = {
      systemConfiguration: { LuckyBonus: { BetSlipPopUpHeader: 'betslip header', BetSlipPopUpMessage: 'popup message',
       BetReceiptPopUpHeader: 'bet receipt header', BetReceiptPopUpMessage: 'bet receipt popup message',
       SettledBetPopUpHeader: 'settled bets header', SettledBetPopUpMessage: 'settled popup messge' } }
    };
    infoDialogService = {
      openInfoDialog: jasmine.createSpy('openInfoDialog').and.callFake((title, txt, cssClass, id, onClose, btns) => {
        buttons = btns;
      }),
      closePopUp: jasmine.createSpy('closePopUp')
    };

    service = new BetInfoDialogService(
      localeService,
      infoDialogService,
      cmsService
    );
  });


  
  it('should return true when enable bet pack is false', () => {
    cmsService = { systemConfiguration: { LuckyBonus: { lucky: false } } };
  })

  it('should check if it is sport category is racing', () => {
    const horseRacingCategory = env.CATEGORIES_DATA.racing.horseracing;
    const greyhoundCategory = env.CATEGORIES_DATA.racing.greyhound;
    const footballCategory = env.CATEGORIES_DATA.footballId;

    expect(service.isRacing(horseRacingCategory.id)).toBeTruthy();
    expect(service.isRacing(greyhoundCategory.id)).toBeTruthy();
    expect(service.isRacing(footballCategory.id)).toBeFalsy();
  });

  it('should show multiples pop-up', fakeAsync(() => {
    service.multiple('ACC4', 4);
    expect(infoDialogService.openInfoDialog).toHaveBeenCalled();
  }));

  it('should show multiples pop-up with lucky', fakeAsync(() => {
    service.multiple('ACC4', 4, betsdata, true, 'betslip', 'Lucky 15');
    expect(infoDialogService.openInfoDialog).toHaveBeenCalled();
    const data = [{multiplier:'1', num_win:'4'}, {multiplier:'1', num_win:'5'}, {multiplier:'1', num_win:'6'}];
    service.multiple('L15', 4, data, true, 'betslip', 'Lucky 15');
    expect(infoDialogService.openInfoDialog).toHaveBeenCalled();
    service.multiple('L31', 4, data, true, 'betslip', 'Lucky 31');
    expect(infoDialogService.openInfoDialog).toHaveBeenCalled();
    service.multiple('L63', 4, betsdata, undefined, 'betslip', 'Lucky 63');
    expect(infoDialogService.openInfoDialog).toHaveBeenCalled();
  }));

  it('should close multiples pop-up on button click', fakeAsync(() => {
    service.multiple('ACC4', 4);
    tick();
    expect(infoDialogService.openInfoDialog).toHaveBeenCalled();
    buttons[0].handler();
  }));

  describe('getMultiplesInfo', () => {
    it('should return info for accumulator bet', () => {
      service['getMultiplesInfo']('ACC4', 4);
      expect(localeService.getString).toHaveBeenCalledWith('bs.AC_common_dialog_info');
    });

    it('should return info for single bet about', () => {
      service['getMultiplesInfo']('SS3', 4);
      expect(localeService.getString).toHaveBeenCalledWith('bs.SS_common_dialog_info');
    });

    it('should return info for double bet about', () => {
      service['getMultiplesInfo']('DS3', 4);
      expect(localeService.getString).toHaveBeenCalledWith('bs.DS_common_dialog_info');
    });

    it('should return info for main bets', () => {
      service['getMultiplesInfo']('DBL', 4);
      expect(localeService.getString).toHaveBeenCalledWith(`bs.DBL_dialog_info`);
    });
    it('should return number of bets', () => {
      localeService.getString.and.returnValue('KEY_NOT_FOUND');
      service['getMultiplesInfo']('TST', 4);
      expect(localeService.getString).toHaveBeenCalledWith('bs.betsNumber', [4]);
    });
  });

  describe('getLuckyPopupText', () => {
    it('should return betslip popup message', () => {
      const response = service['getLuckyPopupText']('L15', betsdata, 'betslip', cmsService.systemConfiguration.LuckyBonus);
      expect(response).toEqual('popup message');
    })

    it('should return bet receipt popup message', () => {
      const response = service['getLuckyPopupText']('L31', betsdata, 'bet receipt', cmsService.systemConfiguration.LuckyBonus);
      expect(response).toEqual('bet receipt popup message');
    })

    it('should return settled bets popup message', () => {
      const response = service['getLuckyPopupText']('L63', betsdata, 'settled bets', cmsService.systemConfiguration.LuckyBonus);
      expect(response).toEqual('settled popup messge');
    })
  });

  describe('getDialogTitle', () => {
    it('should return betslip popup header', () => {
      const response = service['getDialogTitle']('L15', cmsService.systemConfiguration.LuckyBonus, 'betslip', betsdata, true, true);
      expect(response).toEqual('betslip header');
    })

    it('should return bet receipt popup header', () => {
      const response = service['getDialogTitle']('L31', cmsService.systemConfiguration.LuckyBonus, 'bet receipt', betsdata, true, true);
      expect(response).toEqual('bet receipt header');
    })

    it('should return settled bets popup header', () => {
      const response = service['getDialogTitle']('L63', cmsService.systemConfiguration.LuckyBonus, 'settled bets', betsdata, true, true);
      expect(response).toEqual('settled bets header');
    })
  });

  describe('checkProps', () => {
    it('should return betslip popup header', () => {
      const response = service['checkProps'](cmsService.systemConfiguration.LuckyBonus, 'betslip');
      expect(response).toBeTrue();
    })

    it('should return bet receipt popup header', () => {
      const response = service['checkProps'](cmsService.systemConfiguration.LuckyBonus, 'bet receipt');
      expect(response).toBeTrue();
    })

    it('should return settled bets popup header', () => {
      const response = service['checkProps'](cmsService.systemConfiguration.LuckyBonus, 'settled bets');
      expect(response).toBeTrue();
    })
    
    it('should return betslip popup header to fasle', () => {
      cmsService = {
        systemConfiguration: { LuckyBonus: { BetSlipPopUpHeader: '', BetSlipPopUpMessage: '',
         BetReceiptPopUpHeader: '', BetReceiptPopUpMessage: '',
         SettledBetPopUpHeader: '', SettledBetPopUpMessage: '' } }
      };
      const response = service['checkProps'](cmsService.systemConfiguration.LuckyBonus, 'betslip');
      expect(response).toBeFalse();
    })

    it('should return bet receipt popup header to fasle', () => {
      cmsService = {
        systemConfiguration: { LuckyBonus: { BetSlipPopUpHeader: '', BetSlipPopUpMessage: '',
         BetReceiptPopUpHeader: '', BetReceiptPopUpMessage: '',
         SettledBetPopUpHeader: '', SettledBetPopUpMessage: '' } }
      };
      const response = service['checkProps'](cmsService.systemConfiguration.LuckyBonus, 'bet receipt');
      expect(response).toBeFalse();
    })

    it('should return settled bets popup header to fasle', () => {
      cmsService = {
        systemConfiguration: { LuckyBonus: { BetSlipPopUpHeader: '', BetSlipPopUpMessage: '',
         BetReceiptPopUpHeader: '', BetReceiptPopUpMessage: '',
         SettledBetPopUpHeader: '', SettledBetPopUpMessage: '' } }
      };
      const response = service['checkProps'](cmsService.systemConfiguration.LuckyBonus, 'settled bets');
      expect(response).toBeFalse();
    })

    it('should return betslip popup header to fasle', () => {   
      const response = service['checkProps'](undefined, 'betslip');
      expect(response).toBeFalse();
    })

    it('should return bet receipt popup header to fasle', () => { 
      const response = service['checkProps'](undefined, 'bet receipt');
      expect(response).toBeFalse();
    })

    it('should return settled bets popup header to fasle', () => {
      const response = service['checkProps'](undefined, 'settled bets');
      expect(response).toBeFalse();
    })
  });

  describe('checkProps', () => {
    it('should call getLinks() and return links', () => {
      const link = [{caption: 'bs.more', cssClass: 'link-more', hyperlink: 'https://help.ladbrokes.com'}]
      const response = service['getLinks'](true, 'https://help.ladbrokes.com');
      expect(response).toEqual(link);
    })
  });
});
