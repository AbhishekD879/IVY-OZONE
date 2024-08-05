import { QuickbetReceiptLdComponent } from './quickbet-receipt-ld.component';

import { BehaviorSubject, of } from 'rxjs';

describe('QuickbetReceiptLdComponent', () => {

  let component: QuickbetReceiptLdComponent,
    userService,
    storageService,
    nativeBridge,
    windowRefService,
    pubSub,
    ldCmsService

  beforeEach(() => {

    storageService = {
      set: jasmine.createSpy('storageService.set'),
      get: jasmine.createSpy('storageService.get')
    };
    userService = {
      set: jasmine.createSpy(),
      username: 'username',
      winAlertsToggled: false,
      currencySymbol: '$'
    };
    ldCmsService = {
      isLuckyDipReceipt: new BehaviorSubject({} as any)
    }
    windowRefService = {
      nativeWindow: {
        NativeBridge: {
          pushNotificationsEnabled: true,

        },
        location: {
          pathname: 'testPath'
        }
      }
    } as any;
    nativeBridge = {
      isWrapper: true
    }
    component = new QuickbetReceiptLdComponent(

      userService,
      windowRefService,
      storageService,
      nativeBridge,
      ldCmsService,pubSub
    );
  });

  it('should create instance', () => {
    expect(component).toBeDefined();

  });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });

  describe('ngOnInit', () => {
    it('it should assign receiptData', () => {
      const data = {
        legParts: [{
          outcomeDesc: 2,
        }

        ],
        betTags: {
          betTag: [{ tagName: 'LDIP' }],
        },
        price: {
          priceNum: 5,
          priceDen: 2
        },
        stake: {
          amount: 100
        },
        receipt: {
          id: 'id1'
        },
        payout: {
          potential: ''
        }
      } as any;
      ldCmsService.isLuckyDipReceipt = of(data);
      component.ngOnInit();
      expect(component.receiptData).toEqual(data);
    })

    it('recept data should be validated', () => {
      component.receiptData = {
        price: {
          priceNum: " ",
          priceDen: " ",
          priceTypeRef: {
            id: " "
          }
        },
        receipt: {
          id: " "
        },
        date: null,
        stake: {
          stakePerLine: " ",
          amount: " "
        },
        payout: {
          potential: " "
        },
        bet: {
          id: '',
          isConfirmed: '',
          cashoutValue: ''
        },
        legParts: [
          {
            eventDesc: " ",
            marketDesc: " ",
            outcomeId: " ",
            outcomeDesc: " "
          }
        ]
      } as any;
      component.outcomeDescriptionText = 'abc';

      const data = {
        betTags: {
          betTag: [{ tagName: 'LDIP' }],
        },
        price: {
          priceNum: 5,
          priceDen: 2
        },
        stake: {
          amount: 100
        },
        receipt: {
          id: 'id1'
        },
        payout: {
          potential: ''
        },
        legParts: [
          {
            eventDesc: " ",
            marketDesc: " ",
            outcomeId: " ",
            outcomeDesc: " "
          }
        ]
      } as any;
      ldCmsService.isLuckyDipReceipt = of(data);

      component.ngOnInit();
      expect(component.receiptData).toBeDefined();
    })
    it('recept data should be validated', () => {
      component.receiptData = {
        price: {
          priceNum: " ",
          priceDen: " ",
          priceTypeRef: {
            id: " "
          }
        },
        receipt: {
          id: " "
        },
        date: null,
        stake: {
          stakePerLine: " ",
          amount: " "
        },
        payout: {
          potential: " "
        },
        bet: {
          id: '',
          isConfirmed: '',
          cashoutValue: ''
        },
        legParts: [
          {
            eventDesc: " ",
            marketDesc: " ",
            outcomeId: " ",
            outcomeDesc: " "
          }
        ]
      } as any;
      component.outcomeDescriptionText = 'abc';

      const data = {
        betTags: {
          betTag: [{ tagName: '' }],
        },
        price: {
          priceNum: 5,
          priceDen: 2
        },
        stake: {
          amount: 100
        },
        receipt: {
          id: 'id1'
        },
        payout: {
          potential: ''
        },
        legParts: [
          {
            eventDesc: " ",
            marketDesc: " ",
            outcomeId: " ",
            outcomeDesc: " "
          }
        ]
      } as any;
      ldCmsService.isLuckyDipReceipt = of(data);

      component.ngOnInit();
      expect(component.receiptData).toBeDefined();
    })
  })


  describe('toggleWinAlerts', () => {
    it('should call toggleWinAlerts ', () => {
      component.receiptData = {
        receipt: {
          id: 'id1',
        }
      }

      component.winAlertsReceiptId = undefined;

      component.toggleWinAlerts(true);
      expect(userService.winAlertsToggled).toBeFalsy()
    })

    it('should call toggleWinAlerts ', () => {
      component.receiptData = {
        receipt: {
          id: 'id1',
        }
      }

      component.toggleWinAlerts(false);
      expect(userService.winAlertsToggled).toBeFalsy()
    })

  })

  describe('winAlertsTooltipLD', () => {
    it('should call winAlertsTooltipLD ', () => {

      const data = {
        'receiptViewsCounter-username': 'ru1'
      }
      storageService.get = jasmine.createSpy('get').and.returnValue({ data });
      component.winAlertsTooltipLD();
      expect(userService.winAlertsToggled).toBeFalsy()
    })

    it('winAlertsTooltipLD should return true ', () => {
      expect(component.winAlertsTooltipLD()).toBeTruthy();
      expect(userService.winAlertsToggled).toBeFalsy()
    })
  })

  describe('isNativeBridge', () => {
    it('should return true', () => {

      expect(component.isNativeBridge()).toBeTruthy();
      component.ngOnDestroy()

    })
  })
});
