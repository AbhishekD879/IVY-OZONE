
import { LuckyDipOddsButtonComponent } from "@lazy-modules/luckyDip/components/luckyDip-odds-button/luckyDip-odds-button.component";

describe('LuckyDipOddsButtonComponent', () => {
    let component: LuckyDipOddsButtonComponent,
        componentFactoryResolver,
        dialogService, windowRefService,
        pubSubService,userService;

    beforeEach(() => {
        pubSubService = {
            API: {
                SESSION_LOGIN: ''
            },
            subscribe: jasmine.createSpy().and.callFake((a, b, cb) => cb && cb()),
        },
            componentFactoryResolver = {
                resolveComponentFactory: jasmine.createSpy('componentFactoryResolver.resolveComponentFactory')
            } as any;
        dialogService = {
            API: {
                splashModal: 'splashModal',
                animationModal: 'animationModal'
            },
            openDialog: jasmine.createSpy('openDialog'),
            closeDialog: jasmine.createSpy('closeDialog')
        };
        windowRefService = {
            document: {
    
              getElementById: jasmine.createSpy().and.returnValue({}),
              body: {
                classList: {
                  add: jasmine.createSpy('add'),
                  remove: jasmine.createSpy('remove')
                }
              },
    
            },
    
          }
        component = new LuckyDipOddsButtonComponent(
            userService,windowRefService, pubSubService,
            componentFactoryResolver, dialogService,
        );
    });

    describe('onLuckyDipButtonClick', () => {

        it('should open popup', () => {
            const event = {
                stopPropagation: jasmine.createSpy('stopPropagation')
            };

            const spyOpenPopUp = spyOn(component, 'openPopUp');
            component.onLuckyDipButtonClick(event as any);

            expect(spyOpenPopUp).toHaveBeenCalled();
        });
    });

    describe('openPopUp', () => {
        
        it('should open dialog', () => {
            component.odds = '125/1';
            
           component.openAnimationPopUp=jasmine.createSpy('openAnimationPopUp');
           component.odds='4';
            component['dialogService'].openDialog = jasmine.createSpy('openDialog').and.callFake((message, componentFactory, c,callback) => {

                if (message === 'splashModal') {
                    callback;
                    callback.data.callConfirm('val');
                    expect(callback.data.odds).toEqual('4');
                }
            })
            component.openPopUp();

            expect(componentFactoryResolver.resolveComponentFactory).toHaveBeenCalledWith(jasmine.any(Function));
        });
    });

    describe('openAnimationPopUp', () => {

        const val = {}

        it(' should  call openDialog ', () => {
            component['dialogService'].openDialog = jasmine.createSpy('openDialog').and.callFake((message, componentFactory, c,callback) => {

                if (message === 'animationModal') {
                    callback;
                    callback.data.openBetReceipt();
                }
            })
            component.openAnimationPopUp(val);

            // expect(dialogService.openDialog).toHaveBeenCalledWith('animationModal',undefined,false,data)
            expect(dialogService.openDialog).toHaveBeenCalled();
            expect(component.openBetReceipt).toBeTruthy();
        })
    })
});
