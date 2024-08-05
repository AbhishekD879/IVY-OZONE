import { IUserDataModel } from '@core/services/user/user-data.model';
import * as _ from 'underscore';

describe('IUserDataModel', () => {
  let service, storageService;

  beforeEach(() => {
    storageService = {
      get: jasmine.createSpy(),
      set: jasmine.createSpy()
    };
    service = new IUserDataModel(storageService);
  });

  it('constructor', () => {
    expect(service).toBeTruthy();
  });

  it('sportBalance', () => {
    expect(service.bppToken).toBeNull();
  });

  it('maxStakeScale', () => {
    expect(service.maxStakeScale).toBeNull();
  });

  it('sessionToken', () => {
    expect(service.sessionToken).toBeNull();
  });

  it('username', () => {
    expect(service.username).toBeNull();
  });

  it('sportBalance', () => {
    expect(service.sportBalance).toBeNull();
  });

  it('sportBalanceWithSymbol', () => {
    expect(service.sportBalanceWithSymbol).toBeNull();
  });

  it('pendingWithdrawals', () => {
    expect(service.pendingWithdrawals).toBeNull();
  });

  it('advertiser', () => {
    expect(service.pendingWithdrawals).toBeNull();
  });

  it('accountBusinessPhase', () => {
    expect(service.accountBusinessPhase).toBeNull();
  });

  it('ageVerificationStatus', () => {
    expect(service.ageVerificationStatus).toBeNull();
  });

  it('cardNumber', () => {
    expect(service.cardNumber).toEqual('');
  });

  it('countryCode', () => {
    expect(service.countryCode).toBeNull();
  });

  it('currency', () => {
    expect(service.countryCode).toBeNull();
  });

  it('currencySymbol', () => {
    expect(service.currencySymbol).toEqual('£');
  });

  it('email', () => {
    expect(service.email).toBeNull();
  });

  it('firstname', () => {
    expect(service.firstname).toBeNull();
  });

  it('firstNews', () => {
    expect(service.firstNews).toBeNull();
  });

  it('lastname', () => {
    expect(service.lastname).toBeNull();
  });

  it('loginPending', () => {
    expect(service.loginPending).toBeFalsy();
  });

  it('logoutPending', () => {
    expect(service.logoutPending).toBeFalsy();
  });

  it('LCCP', () => {
    expect(service.LCCP).toBeUndefined();
  });

  it('isManualLogout', () => {
    expect(service.isManualLogout).toBeUndefined();
  });

  it('oddsFormat', () => {
    expect(service.oddsFormat).toEqual('frac');
  });

  it('previouslyLogged', () => {
    expect(service.previouslyLogged).toBeFalsy();
  });

  it('quickDepositTriggered', () => {
    expect(service.quickDepositTriggered).toBeFalsy();
  });

  it('previousLoginTime', () => {
    expect(service.previousLoginTime).toBeNull();
  });

  it('playerCode', () => {
    expect(service.playerCode).toBeNull();
  });

  it('playerDepositLimits', () => {
    expect(service.playerDepositLimits).toBeNull();
  });

  it('postCode', () => {
    expect(service.postCode).toBeNull();
  });

  it('profileId', () => {
    expect(service.profileId).toBeNull();
  });

  it('signupDate', () => {
    expect(service.signupDate).toEqual('');
  });

  it('sessionLimit', () => {
    expect(service.sessionLimit).toEqual(0);
  });

  it('tcVersion', () => {
    expect(service.tcVersion).toBeNull();
  });

  it('vipLevel', () => {
    expect(service.vipLevel).toBeNull();
  });

  it('vipInfo', () => {
    expect(service.vipInfo).toBeNull();
  });

  it('firstLogin', () => {
    expect(service.firstLogin).toBeFalsy();
  });

  it('isTemporaryCard', () => {
    expect(service.isTemporaryCard).toBeFalsy();
  });

  it('passwordResetLogin', () => {
    expect(service.passwordResetLogin).toBeFalsy();
  });

  it('isRedirecting', () => {
    expect(service.isRedirecting).toBeFalsy();
  });

  it('showBalance', () => {
    expect(service.showBalance).toBeTruthy();
  });

  it('showLogoutPopup', () => {
    expect(service.showLogoutPopup).toBeTruthy();
  });

  it('status', () => {
    expect(service.status).toBeFalsy();
  });

  it('quickBetNotification', () => {
    expect(service.quickBetNotification).toBeTruthy();
  });

  it('timeline', () => {
    expect(service.timeline).toBeTruthy();
  });

  it('contactPreferences', () => {
    expect(service.contactPreferences).toBeNull();
  });

  it('payPalBA', () => {
    expect(service.payPalBA).toEqual('');
  });

  it('payPalDepositFraudNetScriptsLoaded', () => {
    expect(service.payPalDepositFraudNetScriptsLoaded).toBeFalsy();
  });

  it('isSignUpPending', () => {
    expect(service.isSignUpPending).toBeFalsy();
  });

  it('logInMessage', () => {
    expect(service.logInMessage).toEqual([]);
  });

  it('accountClosed', () => {
    expect(service.accountClosed).toBeFalsy();
  });

  it('isRouletteJourney', () => {
    expect(service.isRouletteJourney()).toBeFalsy();
  });

  it('winAlertsToggled', () => {
    expect(service.winAlertsToggled).toBeFalsy();
  });

  describe('isInShopUser:', () => {
    it('true', () => {
      service.data.accountBusinessPhase = 'in-shop';
      expect(service.isInShopUser()).toBeTruthy();
    });
    it('false', () => {
      expect(service.isInShopUser()).toBeFalsy();
    });
  });

  describe('isMultiChannelUser:', () => {
    it('true', () => {
      service.data.accountBusinessPhase = 'multi-channel';
      expect(service.isMultiChannelUser()).toBeTruthy();
    });
    it('false', () => {
      expect(service.isMultiChannelUser()).toBeFalsy();
    });
  });

  describe('isRetailUser:', () => {
    it('isMultiChannelUser: true', () => {
      service.data.accountBusinessPhase = 'multi-channel';
      expect(service.isRetailUser()).toBeTruthy();
    });
    it('isInShopUser: true', () => {
      service.data.accountBusinessPhase = 'in-shop';
      expect(service.isRetailUser()).toBeTruthy();
    });
    it('false', () => {
      expect(service.isRetailUser()).toBeFalsy();
    });
  });

  it('should reset all data to their default values except - oddsFormat, quickBetNotification, timeline, logoutPending', () => {
    service.data.username = 'wft';
    service.data.oddsFormat = 'ffs';
    service.data.quickBetNotification = 'ffs';
    service.data.timeline = 'ffs';
    service.data.logoutPending = 'ffs';
    const expectedData = _.clone(service.data);
    expectedData.username = null;

    spyOn(service, 'set').and.callThrough();
    service.resetData();

    expect(service.set).toHaveBeenCalled();
    expect(service.data).toEqual(expectedData);
  });

});
