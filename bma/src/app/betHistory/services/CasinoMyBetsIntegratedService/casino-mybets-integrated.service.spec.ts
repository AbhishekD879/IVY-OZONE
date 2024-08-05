import { CasinoMyBetsIntegratedService } from './casino-mybets-integrated.service';

describe('test CasinoMyBetsIntegratedService', () => {
  let service: CasinoMyBetsIntegratedService;
  let renderer,
      windowRef,
      gtmService,
      storageService,
      ezNavVanillaService;

     beforeEach(() => {
      renderer = windowRef = gtmService = storageService = ezNavVanillaService = {} as any;
      windowRef = {
        document: {
            getElementsByClassName: jasmine.createSpy('querySelector').and.returnValue({
                parentNode: {}
            } as any)
        },
        nativeWindow: {
          top: {
            location: {
              replace: jasmine.createSpy('replace')
            }
          }
        }
      };
      renderer = {
        renderer: {
            addClass: jasmine.createSpy('addClass')
        }
      };
      storageService = {
        set: jasmine.createSpy('storageService.set'),
        get: jasmine.createSpy('storageService.get')
      };
      gtmService = {
        push: jasmine.createSpy('push')
      };
      ezNavVanillaService = {
        isMyBetsInCasino: true
      };
      service = new CasinoMyBetsIntegratedService(renderer, windowRef, gtmService, storageService, ezNavVanillaService);
      });

    describe('#bmaInit', () => {  
      beforeEach(() => {
        windowRef.document = {
              getElementsByClassName: jasmine.createSpy('querySelector').and.returnValue(
                  ['elem1', 'elem2'])
          };
      });
      it('bma init with isMyBetsInCasino as true and isFirstTimeLoading as true', () => {
        service['ezNavVanillaService'].isMyBetsInCasino = true;
        service.bmaInit();
        expect(renderer.renderer.addClass).toHaveBeenCalled();
      });

      it('bma init with isMyBetsInCasino as false and isFirstTimeLoading as false', () => {
        service['ezNavVanillaService'].isMyBetsInCasino = false;
        service.bmaInit();
        expect(renderer.renderer.addClass).not.toHaveBeenCalled();
      });
    });

    describe('#getOpenBetTabActiveStatus', () => {  
      it('getOpenBetTabActiveStatus with isFirstTimeLoading as true', () => {
        service['ezNavVanillaService'].isFirstTimeLoading = true;
        expect(service.getOpenBetTabActiveStatus()).toBe(true);
      });

      it('getOpenBetTabActiveStatus with isFirstTimeLoading as false', () => {
        service['ezNavVanillaService'].isFirstTimeLoading = false;
        expect(service.getOpenBetTabActiveStatus()).toBe(false);
      });
    });

    describe('#handleStorageData', () => {  
      it('handleStorageData with userKey and checkboxValue as true', () => {
        const event = {checkboxValue: true, btnClicked: 'yes lets go'};
        service['ezNavVanillaService'].userKey = 'setDate-testAccount';
        service['ezNavVanillaService'].confirmationPopupData = {'setDate-testAccount': ''};
        service.handleStorageData(event);
        expect(service['ezNavVanillaService'].confirmationPopupData[service['ezNavVanillaService'].userKey]).toBe('yes lets go');
      });
      it('handleStorageData with userKey and checkboxValue as false', () => {
        const event = {checkboxValue: false, btnClicked: 'yes lets go'};
        const btnClicked = 'yes lets go';
        service['ezNavVanillaService'].userKey = 'setDate-testAccount';
        service['ezNavVanillaService'].confirmationPopupData = {'setDate-testAccount': ''};
        service.handleStorageData(event);
        expect(service['ezNavVanillaService'].confirmationPopupData[service['ezNavVanillaService'].userKey]).toBe(undefined);
      });
    });

    describe('#confirmationPopUpClick', () => {  
      it('confirmationPopUpClick with output as userAction and btnClicked as yes lets go', () => {
        const event = {
          output: 'userAction',
          value: {
            checkboxValue: true, 
            btnClicked: 'yes lets go'
          }
        };
        spyOn(service, 'handleStorageData');
        expect(service.confirmationPopUpClick(event)).toBe(true);
      });

      it('confirmationPopUpClick with output as userAction and btnClicked as no thanks', () => {
        const event = {
          output: 'userAction',
          value: {
            checkboxValue: true, 
            btnClicked: 'no thanks'
          }
        };
        spyOn(service, 'handleStorageData');
        expect(service.confirmationPopUpClick(event)).toBe(false);
      });

      it('confirmationPopUpClick with output as null and btnClicked as no thanks', () => {
        const event = {
          output: null,
          value: {
            checkboxValue: true, 
            btnClicked: 'no thanks'
          }
        };
        const handleStorageDataSpy = spyOn(service, 'handleStorageData');
        spyOn(service, 'setGtmData');
        service.confirmationPopUpClick(event);
        expect(handleStorageDataSpy).not.toHaveBeenCalled();
      });

      it('confirmationPopUpClick with output as userAction and btnClicked as yes lets go with someUrl argument', () => {
        const event = {
          output: 'userAction',
          value: {
            checkboxValue: true, 
            btnClicked: 'yes lets go'
          }
        };
        const handleStorageDataSpy = spyOn(service, 'handleStorageData');
        spyOn(service, 'setGtmData');
        service.confirmationPopUpClick(event, 'someUrl');
        expect(handleStorageDataSpy).toHaveBeenCalled();
      });

      it('confirmationPopUpClick with output as userAction and btnClicked undefined', () => {
        const event = {
          output: 'userAction',
          value: {
            checkboxValue: true, 
            btnClicked: undefined
          }
        };
        const handleStorageDataSpy = spyOn(service, 'handleStorageData');
        service.confirmationPopUpClick(event);
        expect(handleStorageDataSpy).not.toHaveBeenCalled();
      });
    });

    describe('#setGtmData', () => {  
      it('setGtmData with gtmEventLabel as test event label', () => {
        service.setGtmData('test event label');
        expect(service['gtmService'].push).toHaveBeenCalled();
      });
    });

    describe('#goToSportsCTABtnClick', () => {  
      it('goToSportsCTABtnClick with no argument and popup data yes lets go', () => {
        service['ezNavVanillaService'].userKey = 'setDate-testAccount';
        service['ezNavVanillaService'].confirmationPopupData = {'setDate-testAccount': 'yes lets go'};
        spyOn(service, 'setGtmData');
        expect(service.goToSportsCTABtnClick('test event label')).toBe(false);
      });

      it('goToSportsCTABtnClick with no argument and popup data no thanks', () => {
        service['ezNavVanillaService'].userKey = 'setDate-testAccount';
        service['ezNavVanillaService'].confirmationPopupData = {'setDate-testAccount': 'no thanks'};
        spyOn(service, 'setGtmData');
        expect(service.goToSportsCTABtnClick('test event label')).toBe(false);
      });

      it('goToSportsCTABtnClick with no argument and popup data empty', () => {
        service['ezNavVanillaService'].userKey = 'setDate-testAccount';
        service['ezNavVanillaService'].confirmationPopupData = {'setDate-testAccount': ''};
        spyOn(service, 'setGtmData');
        expect(service.goToSportsCTABtnClick('test event label')).toBe(true);
      });

      it('goToSportsCTABtnClick with someUrl as argument and popup data no thanks', () => {
        service['ezNavVanillaService'].userKey = 'setDate-testAccount';
        service['ezNavVanillaService'].confirmationPopupData = {'setDate-testAccount': 'no thanks'};
        spyOn(service, 'setGtmData');
        expect(service.goToSportsCTABtnClick('test event label', 'someUrl')).toBe(false);
      });
    });

    describe('#isMyBetsInCasino', ()=> {
      it('isMyBetsInCasino', () => {
        expect(service.isMyBetsInCasino).toEqual(true);
      });
    });
});
