import { fakeAsync, tick } from '@angular/core/testing';
import { Subject } from 'rxjs';
import { BybSelectedSelectionsService } from './byb-selected-selections';
import environment from '@environment/oxygenEnvConfig';

describe('SelectedSelections', () => {
    let component;
    let gtmService;
    let marketService;
    let pubsub;
    let callbackHandler;

    beforeEach(() => {
        // component = new BybSelectedSelectionsService(gtmService, marketService);
        callbackHandler = (ctrlName: string, eventName: string, callback) => {
            callback();
        };
        gtmService = {
            push: jasmine.createSpy('push')
          };
          pubsub = {
            subscribe: jasmine.createSpy('subscribe').and.callFake(callbackHandler),
            API: {
                QB_QUICKSTAKE_PRESSED_DIGIT_KEYBOARD: 'QB_QUICKSTAKE_PRESSED_DIGIT_KEYBOARD',
                DIGIT_KEYBOARD_KEY_PRESSED: 'DIGIT_KEYBOARD_KEY_PRESSED,'
            }
          };
    });

    //isActiveGroup
    describe('betPlacementSucess', () => {
        it('should call betPlacementSucess', fakeAsync(() => {
            component = new BybSelectedSelectionsService(gtmService, marketService,pubsub);
            let retVal = null;
            component.betPlacementSubject$ = new Subject();
            component.betPlacementSubject$.subscribe(val => {
                retVal = val;
            });
            component.betPlacementSucess();
            tick();
            expect(retVal).toBe(true);
        }));
    });

    //callGTM
    describe('callGTM', () => {
        it('should call callGTM', () => {
            component = new BybSelectedSelectionsService(gtmService, marketService,pubsub);
            component.eventEntity = {
                categoryId: '16',
                typeId: '25230',
                id: 1,
                eventIsLive: true
            };
            const eventsArr = ['toggle', 'expand-collapse', 'add-selection', 'open-close',
                'remove-selection', 'add-bet', 'show-stats', 'edit-bet'];
            eventsArr.forEach(key => {
                component.callGTM(key, {
                    selectionName: 's',
                    openClose: 'oc',
                    deselect: 'ds',
                    selectionsCnt: 'sc',
                    odds: 'os',
                    eventLabel: 'el',
                    action: true
                });
            });
        });

        it('should call callGTM with remaining data', () => {
            component = new BybSelectedSelectionsService(gtmService, marketService,pubsub);
            component.eventEntity = {
                categoryId: '16',
                typeId: '25230',
                id: 1,
                eventIsLive: false
            };
            const eventsArr = ['toggle', 'expand-collapse', 'add-selection', 'open-close',
                'remove-selection', 'add-bet', 'show-stats', 'edit-bet'];
            eventsArr.forEach(key => {
                component.callGTM(key, {
                    selectionName: 's',
                    openClose: 'oc',
                    selectionsCnt: 'sc',
                    odds: 'os',
                    eventLabel: 'el'
                });
            });
        });
    });


    //placeBet
    describe('placeBet', () => {
        it('should call placeBet', () => {
            component = new BybSelectedSelectionsService(gtmService, marketService,pubsub);
            const receipt = {receipt: '1', totalStake: '2', betId: '3'};
            const bet = {price: '4'};
            const eventEntity = {
                categoryId: '16',
                typeId: '25230',
                id: 1,
                eventIsLive: false
            };
            const selection = {selections: [1,2], freeBet: '1', currencyName: 'GBP'};
            component.stakeFromQb = 2;
            component.digitKeyBoardStatus = true;
            component.placeBet(receipt, bet, eventEntity, selection);
        });

       it('should call placeBet', () => {
            component = new BybSelectedSelectionsService(gtmService, marketService,pubsub);
            const receipt = {receipt: '1', totalStake: '2', betId: '3'};
            const bet = {price: '4'};
            const eventEntity = {
                categoryId: '16',
                typeId: '25230',
                id: 1,
                eventIsLive: false
            };
            const selection = {selections: [1,2], freeBet: '1', currencyName: 'GBP'};
            component.stakeFromQb = 1;
            component.digitKeyBoardStatus = false;
            component.placeBet(receipt, bet, eventEntity, selection);
        });

        it('should call placeBet with No selections', () => {
            component = new BybSelectedSelectionsService(gtmService, marketService,pubsub);
            const receipt = {receipt: '1', totalStake: '2', betId: '3'};
            const bet = {price: '4'};
            const eventEntity = {
                categoryId: '16',
                typeId: '25230',
                id: 1,
                eventIsLive: true
            };
            const selection = { freebetValue : '1', currencyName: 'GBP'};
            component.placeBet(receipt, bet, eventEntity, selection);
        });

        it('should call constructor', () => {
            environment.brand= 'lads';
            component = new BybSelectedSelectionsService(gtmService, marketService,pubsub);
            expect(component.byb).toBe('bet builder');
        });

        it('should call constructor with bma 1', () => {
            environment.brand= 'bma';
            component = new BybSelectedSelectionsService(gtmService, marketService,pubsub);
            expect(component.byb).toBe('build your bet');
        });

        it('should call constructor with bma 2', () => {
            const pubsub:any={
                API:{
                    QB_QUICKSTAKE_PRESSED_DIGIT_KEYBOARD: 'QB_QUICKSTAKE_PRESSED_DIGIT_KEYBOARD',
                    DIGIT_KEYBOARD_KEY_PRESSED: 'DIGIT_KEYBOARD_KEY_PRESSED',
                    LUCKY_DIP_KEYPAD_PRESSED:"LUCKY_DIP_KEYPAD_PRESSED"
                },
                subscribe:jasmine.createSpy('pubsub.subscribe')
                  .and.callFake((filename: string, eventName: string, callback: Function) => {
                if(eventName === 'LUCKY_DIP_KEYPAD_PRESSED'){
                    callback(true)
                }
                else callback()
            })} 
            environment.brand= 'bma';
            component = new BybSelectedSelectionsService(gtmService, marketService,pubsub);
            component.digitKeyBoardStatus = false;
         
            expect(component.byb).toBe('build your bet');
        });
        it('should call constructor with bma 3', fakeAsync(() => {
            const pubsub:any={
                API:{
                    QB_QUICKSTAKE_PRESSED_DIGIT_KEYBOARD: 'QB_QUICKSTAKE_PRESSED_DIGIT_KEYBOARD',
                    DIGIT_KEYBOARD_KEY_PRESSED: 'DIGIT_KEYBOARD_KEY_PRESSED',
                    LUCKY_DIP_KEYPAD_PRESSED:"LUCKY_DIP_KEYPAD_PRESSED"
                },
                subscribe:jasmine.createSpy('pubsub.subscribe')
                  .and.callFake((filename: string, eventName: string, callback: Function) => {
                if(eventName === 'LUCKY_DIP_KEYPAD_PRESSED'){
                    callback(false)
                }
                else callback()
            })} 
            environment.brand= 'bma';
            component = new BybSelectedSelectionsService(gtmService, marketService,pubsub);
            component.isBetPlaceClicked = true;
            component.digitKeyBoardStatus = true;
            
            expect(component.byb).toBe('build your bet');
        }));

    });

    describe('digitKeyBoardStatusInit', () => {
        it('digitKeyBoardStatusInit' , () => {
            environment.brand = 'bma';
            component = new BybSelectedSelectionsService(gtmService, marketService,pubsub);
            component.isBetPlaceClicked = true;
            component.digitKeyBoardStatus = true;
            component.digitKeyBoardStatusInit(false);
        })
        it('digitKeyBoardStatusInit' , () => {
            environment.brand = 'bma';
            component = new BybSelectedSelectionsService(gtmService, marketService,pubsub);
            component.isBetPlaceClicked = false;
            component.digitKeyBoardStatus = false;
            component.digitKeyBoardStatusInit(true);
        })
    })
});