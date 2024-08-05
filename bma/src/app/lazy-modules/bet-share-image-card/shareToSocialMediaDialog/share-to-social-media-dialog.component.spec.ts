import { of } from "rxjs";
import { ShareToSocialMediaDialogComponent } from "./share-to-social-media-dialog.component";
import { AbstractDialogComponent } from "@app/shared/components/oxygenDialogs/abstract-dialog";
import * as mockData from "./share-to-share-data.mock";
import { fakeAsync, tick } from "@angular/core/testing";
import environment from '@environment/oxygenEnvConfig';

describe('ShareToSocialMediaDialogComponent', () => {
  let component: ShareToSocialMediaDialogComponent;
  let sessionStorageService,
    device, cmsService, betShareImageCardService,
    windowRef, nativeBridgeService,
    pubSubService, betShareGTAService;

  beforeEach(() => {
    device = { isAndriod: true, isWrapper: true };

    windowRef = {
      document: {
        body: {
          classList: {
            add: jasmine.createSpy('add'),
            remove: jasmine.createSpy('remove')
          }
        }
      },
      nativeWindow: {
        navigator: {
          share: jasmine.createSpy('share').and.returnValue(Promise.resolve('success')),
          canShare: jasmine.createSpy('canShare').and.returnValue(true)
        }
      }
    };


    sessionStorageService = {
      set: jasmine.createSpy('set'),
      get: jasmine.createSpy('get').and.returnValue({
        cashedOutBetControl: mockData.USER_PREF_FLAGS, wonBetControl: mockData.USER_PREF_FLAGS,
        lostBetControl: mockData.USER_PREF_FLAGS, openBetControl: mockData.USER_PREF_FLAGS
      })
    };

    cmsService = {
      fetchBetShareConfigDetails: jasmine.createSpy('fetchBetShareConfigDetails').and.returnValue(of(mockData.CMS_DATA))
    };

    betShareImageCardService = {
      prepImgObject: jasmine.createSpy('prepImgObject').and.returnValue(mockData.imgObject),
      shareImageDataMapper: jasmine.createSpy('shareImageDataMapper').and.returnValue(mockData.BUILD_BET_SHARE_IMG_DATA),
      regularBetsDataFormation: jasmine.createSpy('regularBetsDataFormation').and.returnValue(mockData.REGULAR_BET_DATA),
      jackPotPoolDataFormation: jasmine.createSpy('jackPotPoolDataFormation').and.returnValue(mockData.POOLS_DATA),
      totePoolBetDataFormation: jasmine.createSpy('totePoolBetDataFormation').and.returnValue(mockData.POOLS_DATA),
      totePotPoolBetDataFormation: jasmine.createSpy('totePotPoolBetDataFormation').and.returnValue(mockData.POOLS_DATA),
      lottoDataFormation: jasmine.createSpy('lottoDataFormation').and.returnValue(mockData.LOTTO_BET_DATA),
      transfromToCurrency: jasmine.createSpy('transfromToCurrency ').and.returnValue('$123')
    };

    nativeBridgeService = {
      shareContentOnSocialMediaGroups: jasmine.createSpy('shareContentOnSocialMediaGroups').and.returnValue(true)
    };

    pubSubService = {
      subscribe: jasmine.createSpy().and.returnValue({ detail: { appName: 'test' } }),
      API: {
        BET_SHARING_COMPLETED: 'BET_SHARING_COMPLETED'
      }
    };

    betShareGTAService = {
      setGtmData: jasmine.createSpy('setGtmData')
    };

    component = new ShareToSocialMediaDialogComponent(device, windowRef, sessionStorageService,
      cmsService, betShareImageCardService,
      nativeBridgeService, pubSubService, betShareGTAService);
    component.flags = mockData.USER_PREF_FLAGS;
    component.settledBetsCheck = true;
    component.cmsData = mockData.CMS_DATA as any;
    environment.brand = 'bma';
    component.betDataToShare = {
      popUpTitle: 'heyy',
      flags: {},
      description: {},
      shareData: 'test'
    }
  });

  it(`should be instance of 'AbstractDialogComponent'`, () => {
    expect(AbstractDialogComponent).isPrototypeOf(component);
  });

  it('ngOnInit should call super.ngOnInit', () => {
    const canvas = document.createElement('canvas');
    canvas.id = "betDataCanvas";
    const body = document.getElementsByTagName("body")[0];
    body.appendChild(canvas);
    spyOn(component,'initializeFonts');
    pubSubService.subscribe.and.callFake((a, b, cb) => cb( {detail: { appName: 'test' }}));
    const parentNgOnInit = spyOn(ShareToSocialMediaDialogComponent.prototype['__proto__'], 'ngOnInit');
    component.params = { data: { ...mockData.REGULAR_SHARE_FOOTBALL_CATEGORY , betData: { location : 'cashOutSection' }}};
    component.ngOnInit();
    component['prepareGTMObject'](false, 'cashed');
    expect(pubSubService.subscribe).toHaveBeenCalledWith('betSharing', 'BET_SHARING_COMPLETED', jasmine.any(Function));
    expect(parentNgOnInit).toHaveBeenCalled();
  });
  
  it('ngOnInit should call initialise fonts', () => {
    const twoDRendering = { 
      beginPath: () => {},
      moveTo: (m1, m2) => {},
      lineTo: (l1, l2) => {},
      closePath: () => {},
      drawImage: (...d1) => {},
      font: "15px Gotham Narrow",
      fillStyle: "#fff",
      fillText: (...f1) => {},
      measureText: (m1) => { return {width: 500}},
     }
    const canvas = {
      getContext: (id) => { return twoDRendering },
      width: 540,
      height: 600,
      toBlob: jasmine.createSpy().and.callFake((callback) => {
        const mockFileReader = {
        result:'',
        onloadend:()=> {
            console.log('onloadend');
        }
      };
      const mBlob = { size: 1024, type: "application/pdf" };
        callback({ size: 1024, type: "application/pdf" });
        component.callBlob(mBlob, mockFileReader);
    })
    }
    component.initializeFonts(canvas);
    expect(component.isCoral).toBeDefined();
  });

  it('ngOnInit should call initialise fonts with lads', () => {
    component.isCoral = false;
    const twoDRendering = { 
      beginPath: () => {},
      moveTo: (m1, m2) => {},
      lineTo: (l1, l2) => {},
      closePath: () => {},
      drawImage: (...d1) => {},
      font: "15px Gotham Narrow",
      fillStyle: "#fff",
      fillText: (...f1) => {},
      measureText: (m1) => { return {width: 500}},
     }
    const canvas = {
      getContext: (id) => { return twoDRendering },
      width: 540,
      height: 600,
      toBlob: jasmine.createSpy().and.callFake((callback) => {
        const mockFileReader = {
        result:'',
        onloadend:()=> {
            console.log('onloadend');
        }
      };
      const mBlob = { size: 1024, type: "application/pdf" };
        callback({ size: 1024, type: "application/pdf" });
        component.callBlob(mBlob, mockFileReader);
    })
    }
    component.initializeFonts(canvas);
    expect(component.isCoral).toBeDefined();
  });
  
  it('should open dialog overlay on share click', () => {
    const params = { data: { sportType: 'regularBets', betData: mockData.REGULAR_BET_DATA1, currencySymbol: '$', bets: { eventSource: mockData.EVENT_SOURCE } } };
    const openSpy = spyOn(ShareToSocialMediaDialogComponent.prototype['__proto__'], 'open');
    AbstractDialogComponent.prototype.setParams(params);
    component.open();
    expect(component).toBeTruthy();
  });

  it('should open sharepopup with settled and won status', () => {
    const params = { data: { sportType: 'regularBets', betData: { settled: 'Y', status: 'won' }, currencySymbol: '$' } };
    const openSpy = spyOn(ShareToSocialMediaDialogComponent.prototype['__proto__'], 'open');
    AbstractDialogComponent.prototype.setParams(params);
    component.open();
    expect(component).toBeTruthy();
  });

  it('should open sharepopup with settled and lost status', () => {
    const params = { data: { sportType: 'regularBets', betData: { settled: 'Y', status: 'lost' }, currencySymbol: '$' } };
    const openSpy = spyOn(ShareToSocialMediaDialogComponent.prototype['__proto__'], 'open');
    AbstractDialogComponent.prototype.setParams(params);  
    component.open();
    expect(component).toBeTruthy();
  });

  it('should open sharepopup with settled and cashed status', () => {
    const params = { data: { sportType: 'regularBets', betData: { settled: 'Y', status: 'cashed out' }, currencySymbol: '$' } };
    const openSpy = spyOn(ShareToSocialMediaDialogComponent.prototype['__proto__'], 'open');
    AbstractDialogComponent.prototype.setParams(params);
    component.open();
    expect(component).toBeTruthy();
  });

  it('should open sharepopup with settled and open status', () => {
    const params = { data: { sportType: 'regularBets', betData: { settled: 'Y', status: 'open' }, currencySymbol: '$' } };
    const openSpy = spyOn(ShareToSocialMediaDialogComponent.prototype['__proto__'], 'open');
    AbstractDialogComponent.prototype.setParams(params);
    component.open();
    expect(component).toBeTruthy();
  });

  it('should open dialog overlay with lotto bets settled', () => {
    const params = { data: { sportType: 'lotto', betData: { bet: { settled: 'N' }, status: 'open' }, currencySymbol: '$' } };
    const openSpy = spyOn(ShareToSocialMediaDialogComponent.prototype['__proto__'], 'open');
    AbstractDialogComponent.prototype.setParams(params);
    component.open();
    expect(component.settledBetsCheck).toBe(false);
  });

  it('should open dialog overlay with lotto bets open status', () => {
    const params = { data: { sportType: 'lotto', betData: { betData: { bet: { status: 'open' } }, settled: 'Y' }, currencySymbol: '$' } };
    const openSpy = spyOn(ShareToSocialMediaDialogComponent.prototype['__proto__'], 'open');
    AbstractDialogComponent.prototype.setParams(params);
    component.open();
    expect(component.settledBetsCheck).toBeTruthy();
    expect(component.betStatusControlData).toBeTruthy();
  });

  it('should open dialog overlay with totePotPoolBet bet', () => {
    const params = { data: { sportType: 'totePotPoolBet', betData: { settled: 'Y', status: 'won' }, currencySymbol: '$' } };
    const openSpy = spyOn(ShareToSocialMediaDialogComponent.prototype['__proto__'], 'open');
    AbstractDialogComponent.prototype.setParams(params);
    component.open();
    expect(component).toBeTruthy();
  });

  it('should open dialog overlay with totePoolBet bet', () => {
    const params = { data: { sportType: 'totePoolBet', betData: { settled: 'Y', status: 'won' }, currencySymbol: '$' } };
    const openSpy = spyOn(ShareToSocialMediaDialogComponent.prototype['__proto__'], 'open');
    AbstractDialogComponent.prototype.setParams(params);
    component.open();
    expect(component).toBeTruthy();
  });

  it('should open dialog overlay with jackPotPool bet', () => {
    const params = { data: { sportType: 'jackPotPool', betData: { settled: 'Y', status: 'open' }, currencySymbol: '$' } };
    const openSpy = spyOn(ShareToSocialMediaDialogComponent.prototype['__proto__'], 'open');
    AbstractDialogComponent.prototype.setParams(params);
    component.open();
    expect(component).toBeTruthy();
  });

  it('should call checked flags for odds check with cashedOutBetControl', () => {
    component.betStatusControlData = 'cashedOutBetControl';
    component.checked(true, 'odds');
    expect(component).toBeTruthy();
  });

  it('should call checked flags for odds check with wonBetControl', () => {
    component.betStatusControlData = 'wonBetControl';
    component.checked(true, 'odds');
    expect(component).toBeTruthy();
  });

  it('should call checked flags for odds check with lostBetControl', () => {
    component.betStatusControlData = 'lostBetControl';
    component.checked(true, 'odds');
    expect(component).toBeTruthy();
  });

  it('should call checked flags for odds check with openBetControl', () => {
    sessionStorageService.get.and.returnValue(null);
    component.betStatusControlData = 'openBetControl';
    component.checked(true, 'odds');
    expect(component).toBeTruthy();
  });

  it('share on ios device and call share with SGL forecast', async() => {

    device.isAndroid = false;
    component.shareData = mockData.SHARE_DATA;
    component.shareData.betType = 'SGL';
    component.shareData.sortType = 'reverseforecast';
    // const canvas = document.createElement('canvas');
    // // const canvas = document.getElementById('betId') as HTMLCanvasElement;
    // canvas.id = "12345";
    // const body = document.getElementsByTagName("body")[0];
    // body.appendChild(canvas);
    const twoDRendering = { 
      beginPath: () => {},
      moveTo: (m1, m2) => {},
      lineTo: (l1, l2) => {},
      closePath: () => {},
      drawImage: (...d1) => {},
      font: "15px Gotham Narrow",
      fillStyle: "#fff",
      fillText: (...f1) => {},
      measureText: (m1) => { return {width: 500}},
     }
    const canvas = {
      getContext: (id) => { return twoDRendering },
      width: 540,
      height: 600,
      toBlob: jasmine.createSpy().and.callFake((callback) => {
        const mockFileReader = {
        result:'',
        onloadend:()=> {
            console.log('onloadend');
        }
      };
      const mBlob = { size: 1024, type: "application/pdf" };
        callback({ size: 1024, type: "application/pdf" });
        component.callBlob(mBlob, mockFileReader);
    })
    }

    const params = { data: { ...mockData.REGULAR_BET_CATEGORY_ID } };
    spyOn(component, 'prepareImg').and.callThrough();
    const closeDialogSpy = spyOn(ShareToSocialMediaDialogComponent.prototype['__proto__'], 'closeDialog');
    AbstractDialogComponent.prototype.setParams(params);
    await component.share(canvas);

    expect(closeDialogSpy).toHaveBeenCalled();
    expect(component).toBeTruthy();
  });

  it('should get eventData as false for isOpen', async() => {
    device.isAndroid = false;
    component.shareData = mockData.SHARE_DATA;
    component.shareData.betType = 'SGL';
    component.shareData.sortType = 'reverseforecast';
    const twoDRendering = { 
      beginPath: () => {},
      moveTo: (m1, m2) => {},
      lineTo: (l1, l2) => {},
      closePath: () => {},
      drawImage: (...d1) => {},
      font: "15px Gotham Narrow",
      fillStyle: "#fff",
      fillText: (...f1) => {},
      measureText: (m1) => { return {width: 500}},
     }
    const canvas = {
      getContext: (id) => { return twoDRendering },
      width: 540,
      height: 600,
      toBlob: jasmine.createSpy().and.callFake((callback) => {
        const mockFileReader = {
        result:'',
        onloadend:()=> {
            console.log('onloadend');
        }
      };
      const mBlob = { size: 1024, type: "application/pdf" };
        callback({ size: 1024, type: "application/pdf" });
        component.callBlob(mBlob, mockFileReader);
    })
    }
    const params = { data: { betData: 
      {
        bet: 
          {
            settled: "N"
          },
          id: '123',
          status: 'cashed out'
      }
    } };
    spyOn(component, 'prepareImg').and.callThrough();
    const closeDialogSpy = spyOn(ShareToSocialMediaDialogComponent.prototype['__proto__'], 'closeDialog');
    AbstractDialogComponent.prototype.setParams(params);
    await component.share(canvas);
    expect(component).toBeTruthy();
  })

  it('should get eventData as false for status won', async() => {
    device.isAndroid = false;
    component.shareData = mockData.SHARE_DATA;
    component.shareData.betType = 'SGL';
    component.shareData.sortType = 'reverseforecast';
    component.settledBetsCheck = false;
    const twoDRendering = { 
      beginPath: () => {},
      moveTo: (m1, m2) => {},
      lineTo: (l1, l2) => {},
      closePath: () => {},
      drawImage: (...d1) => {},
      font: "15px Gotham Narrow",
      fillStyle: "#fff",
      fillText: (...f1) => {},
      measureText: (m1) => { return {width: 500}},
     }
    const canvas = {
      getContext: (id) => { return twoDRendering },
      width: 540,
      height: 600,
      toBlob: jasmine.createSpy().and.callFake((callback) => {
        const mockFileReader = {
        result:'',
        onloadend:()=> {
            console.log('onloadend');
        }
      };
      const mBlob = { size: 1024, type: "application/pdf" };
        callback({ size: 1024, type: "application/pdf" });
        component.callBlob(mBlob, mockFileReader);
    })
    }
    const params = { data: { betData: 
      {
        bet: 
          {
            settled: "Y"
          },
          id: '123'
      }
    } };
    spyOn(component, 'prepareImg').and.callThrough();
    const closeDialogSpy = spyOn(ShareToSocialMediaDialogComponent.prototype['__proto__'], 'closeDialog');
    AbstractDialogComponent.prototype.setParams(params);
    await component.share(canvas);
    expect(component).toBeTruthy();
  })

  it('should get eventData as false for sortType', async() => {
    device.isAndroid = false;
    component.shareData = mockData.SHARE_DATA;
    component.shareData.betType = 'SGL';
    component.shareData.sortType = 'reverseforecast';
    const twoDRendering = { 
      beginPath: () => {},
      moveTo: (m1, m2) => {},
      lineTo: (l1, l2) => {},
      closePath: () => {},
      drawImage: (...d1) => {},
      font: "15px Gotham Narrow",
      fillStyle: "#fff",
      fillText: (...f1) => {},
      measureText: (m1) => { return {width: 500}},
     }
    const canvas = {
      getContext: (id) => {
        return twoDRendering;
      },
      width: 540,
      height: 600,
      toBlob: jasmine.createSpy().and.callFake((callback) => {
        const mockFileReader = {
        result:'',
        onloadend:()=> {
            console.log('onloadend');
        }
      };
      const mBlob = { size: 1024, type: "application/pdf" };
        callback({ size: 1024, type: "application/pdf" });
        component.callBlob(mBlob, mockFileReader);
    })
    };
    const params = { data: { betData: 
      {
        bet: 
          {
            settled: "N"
          },
          id: '123',
          eventSource: {
            sortType: 'test',
            totalStatus: "cashed out"
          }
      }
    } };
    spyOn(component, 'prepareImg').and.callThrough();
    const closeDialogSpy = spyOn(ShareToSocialMediaDialogComponent.prototype['__proto__'], 'closeDialog');
    AbstractDialogComponent.prototype.setParams(params);
    await component.share(canvas);
    expect(component).toBeTruthy();
  })

  it('should get eventData as false for msg1', async() => {
    device.isAndroid = false;
    environment.brand = 'ladbrokes';
    component.shareData = mockData.SHARE_DATA;
    component.shareData.betType = 'SGL';
    component.shareData.sortType = 'reverseforecast';
    const twoDRendering = { 
      beginPath: () => {},
      moveTo: (m1, m2) => {},
      lineTo: (l1, l2) => {},
      closePath: () => {},
      drawImage: (...d1) => {},
      font: "15px Gotham Narrow",
      fillStyle: "#fff",
      fillText: (...f1) => {},
      measureText: (m1) => { return {width: 600}},
     }
    const canvas = {
      getContext: (id) => {
        return twoDRendering;
      },
      width: 540,
      height: 600,
      toBlob: jasmine.createSpy().and.callFake((callback) => {
        const mockFileReader = {
        result:'',
        onloadend:()=> {
            console.log('onloadend');
        }
      };
      const mBlob = { size: 1024, type: "application/pdf" };
        callback({ size: 1024, type: "application/pdf" });
        component.callBlob(mBlob, mockFileReader);
    })
    };
    const params = { data: { betData: 
      {
        bet: 
          {
            settled: "N"
          },
          id: '123',
          eventSource: {
            sortType: 'test',
            totalStatus: "cashed"
          },
          isSettled: "N"
      }
    } };
    spyOn(component, 'prepareImg').and.callThrough();
    const closeDialogSpy = spyOn(ShareToSocialMediaDialogComponent.prototype['__proto__'], 'closeDialog');
    AbstractDialogComponent.prototype.setParams(params);
    await component.share(canvas);
    expect(component).toBeTruthy();
  })

  it('should get string returned when text width is less than max width', async() => {
    device.isAndroid = false;
    component.shareData = mockData.SHARE_DATA;
    component.shareData.betType = 'lotto';
    component.shareData.sortType = 'reverseforecast';
    const twoDRendering = { 
      beginPath: () => {},
      moveTo: (m1, m2) => {},
      lineTo: (l1, l2) => {},
      closePath: () => {},
      drawImage: (...d1) => {},
      font: "15px Gotham Narrow",
      fillStyle: "#fff",
      fillText: (...f1) => {},
      measureText: (m1) => { return {width: 10}},
     }
    const canvas = {
      getContext: (id) => {
        return twoDRendering;
      },
      width: 540,
      height: 600,
      toBlob: jasmine.createSpy().and.callFake((callback) => {
        const mockFileReader = {
        result:'',
        onloadend:()=> {
            console.log('onloadend');
        }
      };
      const mBlob = { size: 1024, type: "application/pdf" };
        callback({ size: 1024, type: "application/pdf" });
        component.callBlob(mBlob, mockFileReader);
    })
    };
    const params = { data: { betData: 
      {
        bet: 
          {
            settled: "N"
          },
          id: '123',
          eventSource: {
            sortType: 'test',
            totalStatus: "cashed out"
          }
      }
    } };
    spyOn(component, 'prepareImg').and.callThrough();
    const closeDialogSpy = spyOn(ShareToSocialMediaDialogComponent.prototype['__proto__'], 'closeDialog');
    AbstractDialogComponent.prototype.setParams(params);
    await component.share(canvas);
    expect(component).toBeTruthy();
  })

  it('should get betType when there is no sorType and betType in list', async() => {
    device.isAndroid = false;
    component.shareData = mockData.SHARE_DATA;
    component.shareData.betType = 'lotto1';
    component.shareData.sortType = null;
    const twoDRendering = { 
      beginPath: () => {},
      moveTo: (m1, m2) => {},
      lineTo: (l1, l2) => {},
      closePath: () => {},
      drawImage: (...d1) => {},
      font: "15px Gotham Narrow",
      fillStyle: "#fff",
      fillText: (...f1) => {},
      measureText: (m1) => { return {width: 10}},
     }
    const canvas = {
      getContext: (id) => {
        return twoDRendering;
      },
      width: 540,
      height: 600,
      toBlob: jasmine.createSpy().and.callFake((callback) => {
        const mockFileReader = {
        result:'',
        onloadend:()=> {
            console.log('onloadend');
        }
      };
      const mBlob = { size: 1024, type: "application/pdf" };
        callback({ size: 1024, type: "application/pdf" });
        component.callBlob(mBlob, mockFileReader);
    })
    };
    const params = { data: { betData: 
      {
        bet: 
          {
            settled: "N"
          },
          id: '123',
          eventSource: {
            totalStatus: "cashed out",
            leg:[{eventEntity:{categoryId:'1'}}]
          }
      }
    } };
    spyOn(component, 'prepareImg').and.callThrough();
    const closeDialogSpy = spyOn(ShareToSocialMediaDialogComponent.prototype['__proto__'], 'closeDialog');
    AbstractDialogComponent.prototype.setParams(params);
    await component.share(canvas);
    expect(component).toBeTruthy();
  })

  it('share on ios device and call share with fiveaside', () => {

    device.isAndroid = false;
    component.shareData = mockData.SHARE_DATA;
    component.shareData.betType = 'SGL';
    const twoDRendering = { 
      beginPath: () => {},
      moveTo: (m1, m2) => {},
      lineTo: (l1, l2) => {},
      closePath: () => {},
      drawImage: (...d1) => {},
      font: "15px Gotham Narrow",
      fillStyle: "#fff",
      fillText: (...f1) => {},
      measureText: (m1) => { return {width: 500}},
     }
    const canvas = {
      getContext: (id) => {
        return twoDRendering;
      },
      width: 540,
      height: 600,
      toBlob: jasmine.createSpy().and.callFake((callback) => {
        const mockFileReader = {
        result:'',
        onloadend:()=> {
            console.log('onloadend');
        }
      };
      const mBlob = { size: 1024, type: "application/pdf" };
        callback({ size: 1024, type: "application/pdf" });
        component.callBlob(mBlob, mockFileReader);
    })
    };
    const params = { data: { ...mockData.REGULAR_SHARE_5ASIDE_CATEGORY } };
    spyOn(component, 'prepareImg').and.callThrough();
    const closeDialogSpy = spyOn(ShareToSocialMediaDialogComponent.prototype['__proto__'], 'closeDialog');
    AbstractDialogComponent.prototype.setParams(params);
    component.share(canvas);

    expect(closeDialogSpy).toHaveBeenCalled();
    expect(betShareImageCardService.shareImageDataMapper).toHaveBeenCalled();
  });

  it('share on ios device and call share with football', () => {

    device.isAndroid = false;
    component.shareData = mockData.SHARE_DATA;
    component.shareData.betType = 'SGL';
    const twoDRendering = { 
      beginPath: () => {},
      moveTo: (m1, m2) => {},
      lineTo: (l1, l2) => {},
      closePath: () => {},
      drawImage: (...d1) => {},
      font: "15px Gotham Narrow",
      fillStyle: "#fff",
      fillText: (...f1) => {},
      measureText: (m1) => { return {width: 500}},
     }

    const canvas = {
      getContext: (id) => {
        return twoDRendering;
      },
      width: 540,
      height: 600,

      toBlob: jasmine.createSpy().and.callFake((callback) => {
          const mockFileReader = {
          result:'',
          onloadend:()=> {
              console.log('onloadend');
          }
        };
        const mBlob = { size: 1024, type: "application/pdf" };
          callback({ size: 1024, type: "application/pdf" });
          component.callBlob(mBlob, mockFileReader);
      })
      
    };

    const params = { data: { ...mockData.REGULAR_SHARE_FOOTBALL_CATEGORY } };
    component.params = params;
    spyOn(component, 'prepareImg').and.callThrough();
    const closeDialogSpy = spyOn(ShareToSocialMediaDialogComponent.prototype['__proto__'], 'closeDialog');
    AbstractDialogComponent.prototype.setParams(params);

    component.share(canvas);

    expect(closeDialogSpy).toHaveBeenCalled();
    expect(betShareImageCardService.shareImageDataMapper).toHaveBeenCalled();
  });

  it('share on ios device and call share with multiple sports', () => {

    device.isAndroid = false;
    component.shareData = mockData.SHARE_DATA;
    component.shareData.betType = 'SGL';
    const twoDRendering = { 
      beginPath: () => {},
      moveTo: (m1, m2) => {},
      lineTo: (l1, l2) => {},
      closePath: () => {},
      drawImage: (...d1) => {},
      font: "15px Gotham Narrow",
      fillStyle: "#fff",
      fillText: (...f1) => {},
      measureText: (m1) => { return {width: 500}},
     }

    const canvas = {
      getContext: (id) => {
        return twoDRendering;
      },
      width: 540,
      height: 600,

      toBlob: jasmine.createSpy().and.callFake((callback) => {
          const mockFileReader = {
          result:'',
          onloadend:()=> {
              console.log('onloadend');
          }
        };
        const mBlob = { size: 1024, type: "application/pdf" };
          callback({ size: 1024, type: "application/pdf" });
          component.callBlob(mBlob, mockFileReader);
      })
      
    };

    const params = { data: { ...mockData.REGULAR_SHARE_FOOTBALL_CATEGORY } };
    params.data.betData.eventSource.leg.push({
      backupEventEntity: { id: '123' },
      part: [{ outcome: [{ eventCategory:{id: '3',name:'Football'}}]}],
      cashoutId: '12345'
    });
    component.params = params;
    spyOn(component, 'prepareImg').and.callThrough();
    const closeDialogSpy = spyOn(ShareToSocialMediaDialogComponent.prototype['__proto__'], 'closeDialog');
    AbstractDialogComponent.prototype.setParams(params);

    component.share(canvas);

    expect(closeDialogSpy).toHaveBeenCalled();
    expect(betShareImageCardService.shareImageDataMapper).toHaveBeenCalled();
  });

  it('share on ios device and call share with SGL forecast cashed status', () => {

    device.isAndroid = false;
    component.shareData = mockData.SHARE_DATA;
    component.shareData.sortType = '';
    component.shareData.betType = 'SGL';
    component.settledBetsCheck = false;
    const twoDRendering = { 
      beginPath: () => {},
      moveTo: (m1, m2) => {},
      lineTo: (l1, l2) => {},
      closePath: () => {},
      drawImage: (...d1) => {},
      font: "15px Gotham Narrow",
      fillStyle: "#fff",
      fillText: (...f1) => {},
      measureText: (m1) => { return {width: 500}},
     }
    const canvas = {
      getContext: (id) => {
        return twoDRendering;
      },
      width: 540,
      height: 600,
      toBlob: jasmine.createSpy().and.callFake((callback) => {
        const mockFileReader = {
        result:'',
        onloadend:()=> {
            console.log('onloadend');
        }
      };
      const mBlob = { size: 1024, type: "application/pdf" };
        callback({ size: 1024, type: "application/pdf" });
        component.callBlob(mBlob, mockFileReader);
    })
    };
    const params = { data: { ...mockData.POOLS_DATA } };
    params.data.betData.status = 'cashed out';
    params.data.betData.settled = 'Y';
    spyOn(component, 'prepareImg').and.callThrough();
    const closeDialogSpy = spyOn(ShareToSocialMediaDialogComponent.prototype['__proto__'], 'closeDialog');
    AbstractDialogComponent.prototype.setParams(params);
    component.share(canvas);

    expect(closeDialogSpy).toHaveBeenCalled();
  });

  it('share on ios device and call share with SGL forecast settledBetsCheck open status', () => {
    device.isAndroid = false;
    component.shareData = mockData.SHARE_DATA;
    component.shareData.sortType = '';
    component.shareData.betType = 'SGL';
    component.settledBetsCheck = false;
    const twoDRendering = { 
      beginPath: () => {},
      moveTo: (m1, m2) => {},
      lineTo: (l1, l2) => {},
      closePath: () => {},
      drawImage: (...d1) => {},
      font: "15px Gotham Narrow",
      fillStyle: "#fff",
      fillText: (...f1) => {},
      measureText: (m1) => { return {width: 500}},
     }
    const canvas = {
      getContext: (id) => { return twoDRendering },
      width: 540,
      height: 600,
      toBlob: jasmine.createSpy().and.callFake((callback) => {
        const mockFileReader = {
        result:'',
        onloadend:()=> {
            console.log('onloadend');
        }
      };
      const mBlob = { size: 1024, type: "application/pdf" };
        callback({ size: 1024, type: "application/pdf" });
        component.callBlob(mBlob, mockFileReader);
    })
    }
    const params = { data: { ...mockData.POOLS_DATA } };
    params.data.betData.status = 'open';
    params.data.betData.settled = 'N';
    spyOn(component, 'prepareImg').and.callThrough();
    const closeDialogSpy = spyOn(ShareToSocialMediaDialogComponent.prototype['__proto__'], 'closeDialog');
    AbstractDialogComponent.prototype.setParams(params);
    component.share(canvas);

    expect(closeDialogSpy).toHaveBeenCalled();
  });


  it('call sendEditedImage', async() => {
    spyOn(component, 'setSportBasedImageUrl');
    component.cmsData = mockData.CMS_DATA.genericSharingLink as any;
    device.isAndroid = true;
    device.isWrapper = true;
    const twoDRendering = { 
      beginPath: () => {},
      moveTo: (m1, m2) => {},
      lineTo: (l1, l2) => {},
      closePath: () => {},
      drawImage: (...d1) => {},
      font: "15px Gotham Narrow",
      fillStyle: "#fff",
      fillText: (...f1) => {},
      measureText: (m1) => { return {width: 500}},
     }
    const canvas = {
      getContext: (id) => { return twoDRendering },
      width: 540,
      height: 600,
      toBlob: jasmine.createSpy().and.callFake((callback) => {
        const mockFileReader = {
        result:'',
        onloadend:()=> {
            console.log('onloadend');
        }
      };
      const mBlob = { size: 1024, type: "application/pdf" };
        callback({ size: 1024, type: "application/pdf" });
        component.callBlob(mBlob, mockFileReader);
    })
    }
    const data = { betId: '12345' };
    component.sendEditedImage(data, null, canvas);
    await delay(3000).then(() => {
      console.log("delayyy");
    });
    expect(component).toBeTruthy();
    async function delay(milliseconds: number) {
      return new Promise((resolve) => setTimeout(resolve, milliseconds));
    }
  });

  it('should call sendEditedImage andriod canshare error', () => {
    spyOn(component, 'setSportBasedImageUrl');
    device.isWrapper = false;
    device.isAndroid = true;
    const twoDRendering = { 
      beginPath: () => {},
      moveTo: (m1, m2) => {},
      lineTo: (l1, l2) => {},
      closePath: () => {},
      drawImage: (...d1) => {},
      font: "15px Gotham Narrow",
      fillStyle: "#fff",
      fillText: (...f1) => {},
      measureText: (m1) => { return {width: 500}},
     }
    const canvas = {
      getContext: (id) => { return twoDRendering },
      width: 540,
      height: 600,
      toBlob: jasmine.createSpy().and.callFake((callback) => {
        const mockFileReader = {
        result:'',
        onloadend:()=> {
            console.log('onloadend');
        }
      };
      const mBlob = { size: 1024, type: "application/pdf" };
        callback({ size: 1024, type: "application/pdf" });
        component.callBlob(mBlob, mockFileReader);
    })
    }
    windowRef.nativeWindow.navigator.canShare.and.returnValue(false);
    const data = { betId: '12345' };
    component.sendEditedImage(data, null, canvas);
    expect(component).toBeTruthy();
  });

  it('call sendEditedImage throw error', async() => {
    spyOn(component, 'setSportBasedImageUrl');
    component.cmsData = mockData.CMS_DATA.genericSharingLink as any;
    const mockFileReader = {
      result:'',
      onloadend: jasmine.createSpy().and.callFake((callback) => {
        callback();
      }),
    readAsDataURL: (blob) => {

      }
    };
    device.isAndroid = true;
    device.isWrapper = true;
    const twoDRendering = { 
      beginPath: () => {},
      moveTo: (m1, m2) => {},
      lineTo: (l1, l2) => {},
      closePath: () => {},
      drawImage: (...d1) => {},
      font: "15px Gotham Narrow",
      fillStyle: "#fff",
      fillText: (...f1) => {},
      measureText: (m1) => { return {width: 500}},
     }
    const canvas = {
      getContext: (id) => { return twoDRendering },
      width: 540,
      height: 600,
      toBlob: jasmine.createSpy().and.callFake((callback) => {
        const mockFileReader = {
        result:'',
        onloadend: jasmine.createSpy().and.callFake((callback) => {
          callback();
        }),
      readAsDataURL: (blob) => {

        }
      };
      const mBlob = { size: 1024, type: "application/pdf" };
        callback(new Blob());
        component.callBlob(new Blob(), mockFileReader);
    })
    }
    const data = { betId: '12345' };
    component.sendEditedImage(data, mockFileReader, canvas);
    await delay(3000).then(() => {
      console.log("delayyy");
    });
    expect(component).toBeTruthy();
    expect(
      nativeBridgeService.shareContentOnSocialMediaGroups
    ).toHaveBeenCalledTimes(1);
    async function delay(milliseconds: number) {
      return new Promise((resolve) => setTimeout(resolve, milliseconds));
    }
  });

  it('should call sendEditedImage on exception', () => {  
    device.isAndroid = true;
    device.isWrapper = true;
    // const canvas = document.createElement('canvas');
    // canvas.id = "12345";
    // const body = document.getElementsByTagName("body")[0];
    // body.appendChild(canvas);
    const twoDRendering = { 
      beginPath: () => {},
      moveTo: (m1, m2) => {},
      lineTo: (l1, l2) => {},
      closePath: () => {},
      drawImage: (...d1) => {},
      font: "15px Gotham Narrow",
      fillStyle: "#fff",
      fillText: (...f1) => {},
      measureText: (m1) => { return {width: 500}},
     }
    const canvas = {
      getContext: (id) => { return twoDRendering },
      width: 540,
      height: 600,
      toBlob: jasmine.createSpy().and.callFake((callback) => {
        const mockFileReader = {
        result:'',
        onloadend:()=> {
            console.log('onloadend');
        }
      };
      const mBlob = { size: 1024, type: "application/pdf" };
        callback({ size: 1024, type: "application/pdf" });
        component.callBlob(mBlob, mockFileReader);
    })
    }
    const data = { betId: '12345' };
    
    nativeBridgeService.shareContentOnSocialMediaGroups = jasmine.createSpy('shareContentOnSocialMediaGroups').and.throwError('err');
    component.sendEditedImage(data, null, canvas);
    expect(
      nativeBridgeService.shareContentOnSocialMediaGroups
    ).toHaveBeenCalledTimes(0);
  })

  it('call sendEditedImage without wrapper', () => {
    const reader = new window.FileReader();
    spyOn(component, 'setSportBasedImageUrl');
    device.isWrapper = false;
    const twoDRendering = { 
      beginPath: () => {},
      moveTo: (m1, m2) => {},
      lineTo: (l1, l2) => {},
      closePath: () => {},
      drawImage: (...d1) => {},
      font: "15px Gotham Narrow",
      fillStyle: "#fff",
      fillText: (...f1) => {},
      measureText: (m1) => { return {width: 500}},
     }
    const canvas = {
      getContext: (id) => { return twoDRendering },
      width: 540,
      height: 600,
      toBlob: jasmine.createSpy().and.callFake((callback) => {
        const mockFileReader = {
        result:'',
        onloadend:()=> {
            console.log('onloadend');
        }
      };
      const mBlob = { size: 1024, type: "application/pdf" };
        callback({ size: 1024, type: "application/pdf" });
        component.callBlob(mBlob, mockFileReader);
    })
    }
    const data = { betId: '12345' };
    component.sendEditedImage(data, null, canvas);
    expect(component).toBeTruthy();
  });

  it('should call sendEditedImage catch block on error', () => {  
    device.isAndroid = true;
    device.isWrapper = true;
    const data = { betId: '12345' };
    
    nativeBridgeService.shareContentOnSocialMediaGroups = jasmine.createSpy('shareContentOnSocialMediaGroups').and.throwError('err');
    component.sendEditedImage(data);
    expect(
      nativeBridgeService.shareContentOnSocialMediaGroups
    ).toHaveBeenCalledTimes(0);
  })

  it('should call prepareImg catch block on error', () => {  
    device.isAndroid = true;
    device.isWrapper = true;
    const data = { betId: '12345' };
    
    nativeBridgeService.shareContentOnSocialMediaGroups = jasmine.createSpy('shareContentOnSocialMediaGroups').and.throwError('err');
    component.prepareImg(data);
    expect(
      nativeBridgeService.shareContentOnSocialMediaGroups
    ).toHaveBeenCalledTimes(0);
  })

  it('sendEditedImage andriod without wrapperand andriod true', () => {
    const reader = new window.FileReader();
    spyOn(component, 'setSportBasedImageUrl');
    device.isWrapper = false;
    device.isAndroid = true;
    const twoDRendering = { 
      beginPath: () => {},
      moveTo: (m1, m2) => {},
      lineTo: (l1, l2) => {},
      closePath: () => {},
      drawImage: (...d1) => {},
      font: "15px Gotham Narrow",
      fillStyle: "#fff",
      fillText: (...f1) => {},
      measureText: (m1) => { return {width: 500}},
     }
    const canvas = {
      getContext: (id) => { return twoDRendering },
      width: 540,
      height: 600,
      toBlob: jasmine.createSpy().and.callFake((callback) => {
        const mockFileReader = {
        result:'',
        onloadend:()=> {
            console.log('onloadend');
        }
      };
      const mBlob = { size: 1024, type: "application/pdf" };
        callback({ size: 1024, type: "application/pdf" });
        component.callBlob(mBlob, mockFileReader);
    })
    }
    const data = { betId: '12345' };
    component.sendEditedImage(data, null, canvas);
    expect(component).toBeTruthy();
  });


  it('should call sendEditedImage andriod canshare error failed to share', () => {
    const reader = new window.FileReader();
    spyOn(component, 'setSportBasedImageUrl');
    device.isWrapper = false;
    device.isAndroid = true;
    const twoDRendering = { 
      beginPath: () => {},
      moveTo: (m1, m2) => {},
      lineTo: (l1, l2) => {},
      closePath: () => {},
      drawImage: (...d1) => {},
      font: "15px Gotham Narrow",
      fillStyle: "#fff",
      fillText: (...f1) => {},
      measureText: (m1) => { return {width: 500}},
     }
    const canvas = {
      getContext: (id) => { return twoDRendering },
      width: 540,
      height: 600,
      toBlob: jasmine.createSpy().and.callFake((callback) => {
        const mockFileReader = {
        result:'',
        onloadend:()=> {
            console.log('onloadend');
        }
      };
      const mBlob = { size: 1024, type: "application/pdf" };
        callback({ size: 1024, type: "application/pdf" });
        component.callBlob(mBlob, mockFileReader);
    })
    }
    windowRef.nativeWindow.navigator.share.and.returnValue(Promise.reject('failed to share...'));
    const data = { betId: '12345' };
    component.sendEditedImage(data, null, canvas);
    expect(component).toBeTruthy();
  });

  it('should call share bet with generic sharing url', () => {
    const reader = new window.FileReader();
    spyOn(component, 'setSportBasedImageUrl');
    device.isWrapper = false;
    device.isAndroid = true;
    const twoDRendering = { 
      beginPath: () => {},
      moveTo: (m1, m2) => {},
      lineTo: (l1, l2) => {},
      closePath: () => {},
      drawImage: (...d1) => {},
      font: "15px Gotham Narrow",
      fillStyle: "#fff",
      fillText: (...f1) => {},
      measureText: (m1) => { return {width: 500}},
     }
    const canvas = {
      getContext: (id) => { return twoDRendering },
      width: 540,
      height: 600,
      toBlob: jasmine.createSpy().and.callFake((callback) => {
        const mockFileReader = {
        result:'',
        onloadend:()=> {
            console.log('onloadend');
        }
      };
      const mBlob = { size: 1024, type: "application/pdf" };
        callback({ size: 1024, type: "application/pdf" });
        component.callBlob(mBlob, mockFileReader);
    })
    }
    const data = { betId: '12345' };
    component.sendEditedImage(data, null, canvas);
    expect(component).toBeTruthy();
  });

  it('should call sendEditedImage and can share false', () => {
    const reader = new window.FileReader();
    spyOn(component, 'setSportBasedImageUrl');
    device.isWrapper = false;
    device.isAndroid = true;
    const twoDRendering = { 
      beginPath: () => {},
      moveTo: (m1, m2) => {},
      lineTo: (l1, l2) => {},
      closePath: () => {},
      drawImage: (...d1) => {},
      font: "15px Gotham Narrow",
      fillStyle: "#fff",
      fillText: (...f1) => {},
      measureText: (m1) => { return {width: 500}},
     }
    const canvas = {
      getContext: (id) => { return twoDRendering },
      width: 540,
      height: 600,
      toBlob: jasmine.createSpy().and.callFake((callback) => {
        const mockFileReader = {
        result:'',
        onloadend:()=> {
            console.log('onloadend');
        }
      };
      const mBlob = { size: 1024, type: "application/pdf" };
        callback({ size: 1024, type: "application/pdf" });
        component.callBlob(mBlob, mockFileReader);
    })
    }
    windowRef.nativeWindow.navigator.canShare.and.returnValue(false);
    const data = { betId: '12345' };
    component.sendEditedImage(data, null, canvas);
    expect(component).toBeTruthy();
  });


  it('should call sendEditedImage andriod share error', () => {
    const reader = new window.FileReader();
    spyOn(component, 'setSportBasedImageUrl');
    device.isWrapper = false;
    device.isAndroid = true;
    const twoDRendering = { 
      beginPath: () => {},
      moveTo: (m1, m2) => {},
      lineTo: (l1, l2) => {},
      closePath: () => {},
      drawImage: (...d1) => {},
      font: "15px Gotham Narrow",
      fillStyle: "#fff",
      fillText: (...f1) => {},
      measureText: (m1) => { return {width: 500}},
     }
    const canvas = {
      getContext: (id) => { return twoDRendering },
      width: 540,
      height: 600,
      toBlob: jasmine.createSpy().and.callFake((callback) => {
        const mockFileReader = {
        result:'',
        onloadend:()=> {
            console.log('onloadend');
        }
      };
      const mBlob = { size: 1024, type: "application/pdf" };
        callback({ size: 1024, type: "application/pdf" });
        component.callBlob(mBlob, mockFileReader);
    })
    }
    windowRef.nativeWindow.navigator.share.and.returnValue(Promise.reject(''));
    const data = { betId: '12345' };
    component.sendEditedImage(data, null, canvas);
    expect(component).toBeTruthy();
  });

  describe('prepare image objects', () => {

    beforeEach(() => {
      const begambleImg = new Image();
      begambleImg.crossOrigin="anonymous";
      begambleImg.src = "https://scmedia.itsfogo.com/$-$/9ec4377d22a7465e952b051023d79fa2.jpg";
      component.beGambleAwareLogoUrlObj = begambleImg;
      const brandLogoImg = new Image();
      brandLogoImg.crossOrigin="anonymous";
      brandLogoImg.src = "https://scmedia.itsfogo.com/$-$/7f10c18c8ae340a9b08219809b3ccd21.svg";
      component.brandLogo = brandLogoImg;
      const extensionUrlImg = new Image();
      extensionUrlImg.crossOrigin="anonymous";
      extensionUrlImg.src = "https://scmedia.itsfogo.com/$-$/5539b5e8d1cc4b6595ea27657d46ce3f.jpg";
      component.brandLogo = extensionUrlImg;

    })

    it('prepare build your bet image object for share',fakeAsync( () => {
      spyOn(component, 'sendEditedImage');
      device.isAndroid = false;
      const data = mockData.BUILD_BET_SHARE_IMG_DATA;
      const twoDRendering = { 
        beginPath: () => {},
        moveTo: (m1, m2) => {},
        lineTo: (l1, l2) => {},
        closePath: () => {},
        drawImage: (...d1) => {},
        font: "15px Gotham Narrow",
        fillStyle: "#fff",
        fillText: (...f1) => {},
        measureText: (m1) => { return {width: 500}},
       }
      const canvas = {
        getContext: (id) => { return twoDRendering },
        width: 540,
        height: 600,
        toBlob: jasmine.createSpy().and.callFake((callback) => {
          const mockFileReader = {
          result:'',
          onloadend:()=> {
              console.log('onloadend');
          }
        };
        const mBlob = { size: 1024, type: "application/pdf" };
          callback({ size: 1024, type: "application/pdf" });
          component.callBlob(mBlob, mockFileReader);
      })
      }
      component.prepareImg(data, canvas);
      tick();
      expect(component).toBeTruthy();
    }));

    it('prepareImg totepool to be true',fakeAsync( () => {
      const imgObject = new Image();
      imgObject.crossOrigin="anonymous";
      imgObject.src ="https://scmedia.itsfogo.com/$-$/5539b5e8d1cc4b6595ea27657d46ce3f.jpg";
      spyOn(component, 'sendEditedImage');
      device.isAndroid = false;
      const data: any = [{selectionName: "football"}];
      data.betType = "Totepool";
      data.betId = "12345"; 
      data.imageObj = imgObject;
      data.msg1 = "checkout my bet!";
      environment.brand = 'ladbrokes';
      const twoDRendering = { 
        beginPath: () => {},
        moveTo: (m1, m2) => {},
        lineTo: (l1, l2) => {},
        closePath: () => {},
        drawImage: (...d1) => {},
        font: "15px Gotham Narrow",
        fillStyle: "#fff",
        fillText: (...f1) => {},
        measureText: (m1) => { return {width: 500}},
       }
      const canvas = {
        getContext: (id) => { return twoDRendering },
        width: 540,
        height: 600,
        toBlob: jasmine.createSpy().and.callFake((callback) => {
          const mockFileReader = {
          result:'',
          onloadend:()=> {
              console.log('onloadend');
          }
        };
        const mBlob = { size: 1024, type: "application/pdf" };
          callback({ size: 1024, type: "application/pdf" });
          component.callBlob(mBlob, mockFileReader);
      })
      }
      component.prepareImg(data, canvas);
      tick();
      expect(component).toBeTruthy();
    }));

    it('prepareImg selectionName to be true',fakeAsync( () => {
      const imgObject = new Image();
      imgObject.crossOrigin="anonymous";
      imgObject.src ="https://scmedia.itsfogo.com/$-$/5539b5e8d1cc4b6595ea27657d46ce3f.jpg";
      spyOn(component, 'sendEditedImage');
      device.isAndroid = false;
      const data: any = [{selectionName: "football", line1: ["line1", "line2"]}];
      data.betId = "12345"; 
      data.imageObj = imgObject;
      data.msg1 = "checkout my bet!"
      const twoDRendering = { 
        beginPath: () => {},
        moveTo: (m1, m2) => {},
        lineTo: (l1, l2) => {},
        closePath: () => {},
        drawImage: (...d1) => {},
        font: "15px Gotham Narrow",
        fillStyle: "#fff",
        fillText: (...f1) => {},
        measureText: (m1) => { return {width: 500}},
       }
      const canvas = {
        getContext: (id) => { return twoDRendering },
        width: 540,
        height: 600,
        toBlob: jasmine.createSpy().and.callFake((callback) => {
          const mockFileReader = {
          result:'',
          onloadend:()=> {
              console.log('onloadend');
          }
        };
        const mBlob = { size: 1024, type: "application/pdf" };
          callback({ size: 1024, type: "application/pdf" });
          component.callBlob(mBlob, mockFileReader);
      })
      }
      component.prepareImg(data, canvas);
      tick();
      expect(component).toBeTruthy();
    }));

    it('prepareImg lines to be counted',fakeAsync( () => {
      const imgObject = new Image();
      imgObject.crossOrigin="anonymous";
      imgObject.src ="https://scmedia.itsfogo.com/$-$/5539b5e8d1cc4b6595ea27657d46ce3f.jpg";
      spyOn(component, 'sendEditedImage');
      device.isAndroid = false;
      const data: any = [{selectionName: "football", line1: ["line1", "line2 is the long text to test the ellipsis in bet sharing for open bets, settled bets"], line2: ["line1", "line2"], line3: ["line1", "line2"]}];
      data.betId = "12345"; 
      data.imageObj = imgObject;
      data.msg1 = "checkout my bet!"
      const twoDRendering = { 
        beginPath: () => {},
        moveTo: (m1, m2) => {},
        lineTo: (l1, l2) => {},
        closePath: () => {},
        drawImage: (...d1) => {},
        font: "15px Gotham Narrow",
        fillStyle: "#fff",
        fillText: (...f1) => {},
        measureText: (m1) => { return {width: 500}},
       }
      const canvas = {
        getContext: (id) => { return twoDRendering },
        width: 540,
        height: 600,
        toBlob: jasmine.createSpy().and.callFake((callback) => {
          const mockFileReader = {
          result:'',
          onloadend:()=> {
              console.log('onloadend');
          }
        };
        const mBlob = { size: 1024, type: "application/pdf" };
          callback({ size: 1024, type: "application/pdf" });
          component.callBlob(mBlob, mockFileReader);
      })
      }
      component.prepareImg(data, canvas);
      tick();
      expect(component).toBeTruthy();
    }));

    it('prepareImg lines to be counted for msg2 pools coral',fakeAsync( () => {
      const imgObject = new Image();
      imgObject.crossOrigin="anonymous";
      imgObject.src ="https://scmedia.itsfogo.com/$-$/5539b5e8d1cc4b6595ea27657d46ce3f.jpg";
      spyOn(component, 'sendEditedImage');
      device.isAndroid = false;
      const data: any = [{selectionName: "football", line1: ["line1", "line2"], line2: ["line1", "line2"], line3: ["line1", "line2"], selectionHeaderName: 'Open Bets', 
        selectionOutcomes: ["outcome1", "outcome2"], marketName: "Bet Builder"}];
      data.betId = "12345";
      data.imageObj = imgObject;
      data.msg1 = "checkout my bet! I won a wonderful bet!!!";
      data.msg2 = "Its an open bet.";
      data.betType = "tote pool";
      data.stake = "2";
      const twoDRendering = { 
        beginPath: () => {},
        moveTo: (m1, m2) => {},
        lineTo: (l1, l2) => {},
        closePath: () => {},
        drawImage: (...d1) => {},
        font: "15px Gotham Narrow",
        fillStyle: "#fff",
        fillText: (...f1) => {},
        measureText: (m1) => { return {width: 500}},
       }
      const canvas = {
        getContext: (id) => { return twoDRendering },
        width: 540,
        height: 600,
        toBlob: jasmine.createSpy().and.callFake((callback) => {
          const mockFileReader = {
          result:'',
          onloadend:()=> {
              console.log('onloadend');
          }
        };
        const mBlob = { size: 1024, type: "application/pdf" };
          callback({ size: 1024, type: "application/pdf" });
          component.callBlob(mBlob, mockFileReader);
      })
      }
      component.isCoral = true;
      component.prepareImg(data, canvas);
      tick();
      expect(component).toBeTruthy();
    }));

    it('prepareImg lines to be counted for msg2 pools lads',fakeAsync( () => {
      const imgObject = new Image();
      imgObject.crossOrigin="anonymous";
      imgObject.src ="https://scmedia.itsfogo.com/$-$/5539b5e8d1cc4b6595ea27657d46ce3f.jpg";
      spyOn(component, 'sendEditedImage');
      device.isAndroid = false;
      const data: any = [{selectionName: "football", line1: ["line1", "line2"], line2: ["line1", "line2"], line3: ["line1", "line2"], selectionHeaderName: 'Open Bets', 
        selectionOutcomes: ["outcome1", "outcome2"], marketName: "Bet Builder"}];
      data.betId = "12345";
      data.imageObj = imgObject;
      data.msg1 = "checkout my bet! I won a wonderful bet!!!";
      data.msg2 = "Its an open bet.";
      data.betType = "tote pool";
      data.stake = "2";
      const twoDRendering = { 
        beginPath: () => {},
        moveTo: (m1, m2) => {},
        lineTo: (l1, l2) => {},
        closePath: () => {},
        drawImage: (...d1) => {},
        font: "15px Gotham Narrow",
        fillStyle: "#fff",
        fillText: (...f1) => {},
        measureText: (m1) => { return {width: 600}},
       }
      const canvas = {
        getContext: (id) => { return twoDRendering },
        width: 540,
        height: 600,
        toBlob: jasmine.createSpy().and.callFake((callback) => {
          const mockFileReader = {
          result:'',
          onloadend:()=> {
              console.log('onloadend');
          }
        };
        const mBlob = { size: 1024, type: "application/pdf" };
          callback({ size: 1024, type: "application/pdf" });
          component.callBlob(mBlob, mockFileReader);
      })
      }
      component.isCoral = false;
      component.prepareImg(data, canvas);
      tick();
      expect(component).toBeTruthy();
    }));

    it('prepareImg lines to be counted for msg2 for build bet',fakeAsync( () => {
      environment.brand = 'ladbrokes';
      const imgObject = new Image();
      imgObject.crossOrigin="anonymous";
      imgObject.src ="https://scmedia.itsfogo.com/$-$/5539b5e8d1cc4b6595ea27657d46ce3f.jpg";
      spyOn(component, 'sendEditedImage');
      device.isAndroid = false;
      const data: any = [{selectionName: ["football"], line1: ["line1", "line2"], line2: ["line1", "line2"], line3: ["line1", "line2"], selectionHeaderName: 'Open Bets', 
        selectionOutcomes: ["outcome1", "outcome2"], marketName: "Bet Builder"}];
      data.betId = "12345"; 
      data.imageObj = imgObject;
      data.msg1 = "checkout my bet! I won a wonderful bet!!!";
      data.msg2 = "Its an open bet.";
      data.betType = "Bet Builder";
      data.returns = "2.33";
      data.isSettled = true;
      const twoDRendering = { 
        beginPath: () => {},
        moveTo: (m1, m2) => {},
        lineTo: (l1, l2) => {},
        closePath: () => {},
        drawImage: (...d1) => {},
        font: "15px Gotham Narrow",
        fillStyle: "#fff",
        fillText: (...f1) => {},
        measureText: (m1) => { return {width: 500}},
       }
      const canvas = {
        getContext: (id) => { return twoDRendering },
        width: 540,
        height: 600,
        toBlob: jasmine.createSpy().and.callFake((callback) => {
          const mockFileReader = {
          result:'',
          onloadend:()=> {
              console.log('onloadend');
          }
        };
        const mBlob = { size: 1024, type: "application/pdf" };
          callback({ size: 1024, type: "application/pdf" });
          component.callBlob(mBlob, mockFileReader);
      })
      }
      component.prepareImg(data, canvas);
      tick();
      expect(component).toBeTruthy();
    }));
  })



  it('prepareGTMObject with totepootpoolbet', () => {
    component.params = { data: { sportType: "totePotPoolBet" , betData: { location: 'openbets' }}};
    component.params.data.sportType = 'totePotPoolBet';
    component['prepareGTMObject'](false, 'cashed');
    component.settledBetsCheck = false;
    expect(betShareGTAService.setGtmData).toHaveBeenCalled();
  });

  it('prepareGTMObject with no appname', () => {
    component.params.data.sportType = 'totePotPoolBet';
    component['prepareGTMObject'](false, null);
    component.settledBetsCheck = false;
    expect(betShareGTAService.setGtmData).toHaveBeenCalled();
  });


  it('closeThisDialog', () => {
    const closeDialogSpy = spyOn(ShareToSocialMediaDialogComponent.prototype['__proto__'], 'closeDialog');
    spyOn(component as any, 'prepareGTMObject');
    component.close(true);
    expect(closeDialogSpy).toHaveBeenCalled();
    expect(windowRef.document.body.classList.remove).toHaveBeenCalledWith('bet-share-modal-open');
  });


  it('should call statusText', () => {
    component.statusText('open');
    expect(component).toBeTruthy();
  });

  it('should call statusText', () => {
    const status = "won";
    component.statusText(status);
    expect(component).toBeTruthy();
  });

  it('should call isShareDisabled', () => {
    const flags = {
      oddsFlag:true,
      stakeFlag: true,
      returnsFlag: true,
      selectionNameFlag: true,
      eventNameFlag: true,
      dateFlag: true
    };
    component.betDataToShare = {
      shareData: {
        returns: true
      }
    };
    component.userPrefernceNames = [{returns: "66"}];
    component['isShareDisabled'](flags);
    expect(component.isShareAllowed).toBeTrue();
  })

  
  it('should call prepareGTMObject', () => {
    component.flags = {
      returnsFlag: true,
    };
    component.betDataToShare = {
      shareData: {
        returns: true
      }
    };
    component.params = { data: { sportType: "tote pool" , betData: { location: 'openbets' }}};
    component.userPrefernceNames = [{returns: "66"}];
    component.settledBetsCheck = false;
    component['prepareGTMObject'](true, "whatsapp");
    expect(betShareGTAService.setGtmData).toHaveBeenCalledWith('open bets', 'tote pool', '66');
  })

  it('should call tranformWithCurrency', () => {
    component['currencySymbol'] = '$';
    const data = component.tranformWithCurrency('$11');
    expect(data).toBe('$11');
  });

  it('should call tranformWithCurrency', () => {
    component['currencySymbol'] = '$';
    const data = component.tranformWithCurrency('11');
    expect(data).toBeTruthy('$11');
  });

  describe('prepare image objects for lotto bet', () => {

    beforeEach(() => {
      const begambleImg = new Image();
      begambleImg.crossOrigin="anonymous";
      begambleImg.src = "https://scmedia.itsfogo.com/$-$/9ec4377d22a7465e952b051023d79fa2.jpg";
      component.beGambleAwareLogoUrlObj = begambleImg;
      const brandLogoImg = new Image();
      brandLogoImg.crossOrigin="anonymous";
      brandLogoImg.src = "https://scmedia.itsfogo.com/$-$/7f10c18c8ae340a9b08219809b3ccd21.svg";
      component.brandLogo = brandLogoImg;
      const extensionUrlImg = new Image();
      extensionUrlImg.crossOrigin="anonymous";
      extensionUrlImg.src = "https://scmedia.itsfogo.com/$-$/5539b5e8d1cc4b6595ea27657d46ce3f.jpg";
      component.brandLogo = extensionUrlImg;
    })

  it('prepare lotto image object for coral share ',fakeAsync( () => {
    spyOn(component, 'sendEditedImage');
    device.isAndroid = false;
    const data = mockData.LOTTO_BET_SHARE_IMG_DATA;
    // const lottocanvas = document.createElement('canvas');
    // lottocanvas.id = "67910";
    // const body = document.getElementsByTagName("body")[0];
    // body.appendChild(lottocanvas);
    const twoDRendering = { 
      beginPath: () => {},
      moveTo: (m1, m2) => {},
      lineTo: (l1, l2) => {},
      closePath: () => {},
      drawImage: (...d1) => {},
      font: "15px Gotham Narrow",
      fillStyle: "#fff",
      fillText: (...f1) => {},
      measureText: (m1) => { return {width: 500}},
     }
    const canvas = {
      getContext: (id) => { return twoDRendering },
      width: 540,
      height: 600,
      toBlob: jasmine.createSpy().and.callFake((callback) => {
        const mockFileReader = {
        result:'',
        onloadend:()=> {
            console.log('onloadend');
        }
      };
      const mBlob = { size: 1024, type: "application/pdf" };
        callback({ size: 1024, type: "application/pdf" });
        component.callBlob(mBlob, mockFileReader);
    })
    }
    component.prepareImg(data, canvas);
    tick();
    expect(component).toBeTruthy();
  }));

  it('prepare lotto image object for lads share ',fakeAsync( () => {
    spyOn(component, 'sendEditedImage');
    device.isAndroid = false;
    const data = mockData.LOTTO_BET_SHARE_IMG_DATA;
    const twoDRendering = { 
      beginPath: () => {},
      moveTo: (m1, m2) => {},
      lineTo: (l1, l2) => {},
      closePath: () => {},
      drawImage: (...d1) => {},
      font: "15px Gotham Narrow",
      fillStyle: "#fff",
      fillText: (...f1) => {},
      measureText: (m1) => { return {width: 500}},
     }
    const canvas = {
      getContext: (id) => { return twoDRendering },
      width: 540,
      height: 600,
      toBlob: jasmine.createSpy().and.callFake((callback) => {
        const mockFileReader = {
        result:'',
        onloadend:()=> {
            console.log('onloadend');
        }
      };
      const mBlob = { size: 1024, type: "application/pdf" };
        callback({ size: 1024, type: "application/pdf" });
        component.callBlob(mBlob, mockFileReader);
    })
    }
    component.isCoral = false;
    component.prepareImg(data, canvas);
    tick();
    expect(component).toBeTruthy();
  }));
});

it('prepareImg url height to be added if no height or undefined',fakeAsync( () => {
  spyOn(component, 'sendEditedImage');
  device.isAndroid = false;
  const data: any = [{selectionName: ["football"], line1: ["line1", "line2"], line2: ["line1", "line2"], line3: ["line1", "line2"], 	selectionHeaderName: 'Open Bets', 
    selectionOutcomes: ["outcome1", "outcome2"], marketName: "Bet Builder"}];
  data.betId = "12345"; 
  data.msg1 = "checkout my bet! I won a wonderful bet!!!";
  data.msg2 = "Its an open bet.";
  data.betType = "Bet Builder";
  data.returns = "2.33";
  data.isSettled = true;
  data.imageObj = { height: 0, width: 500 };
  const twoDRendering = { 
    beginPath: () => {},
    moveTo: (m1, m2) => {},
    lineTo: (l1, l2) => {},
    closePath: () => {},
    drawImage: (...d1) => {},
    font: "15px Gotham Narrow",
    fillStyle: "#fff",
    fillText: (...f1) => {},
    measureText: (m1) => { return {width: 500}},
   }
  const canvas = {
    getContext: (id) => { return twoDRendering },
    width: 540,
    height: 600,
    toBlob: jasmine.createSpy().and.callFake((callback) => {
      const mockFileReader = {
      result:'',
      onloadend:()=> {
          console.log('onloadend');
      }
    };
    const mBlob = { size: 1024, type: "application/pdf" };
      callback({ size: 1024, type: "application/pdf" });
      component.callBlob(mBlob, mockFileReader);
  })
  }
  component.prepareImg(data, canvas);
  tick();
  expect(component).toBeTruthy();
}));
});
