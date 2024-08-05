// import { of,  Observable } from 'rxjs';
// import { LottoBetService } from './lotto-bet.service';
// import { ILottoDraw } from '@app/lotto/models/lotto.model';
// import { tick, fakeAsync } from '@angular/core/testing';

// describe('LottoBetService', () => {
//   let service: LottoBetService;

//   let deviceService;
//   let lottoReceiptService;
//   let coreToolsService;
//   let bppService;
//   let router;
//   let clientUserAgentService;
//   let timeSyncService;
//   beforeEach(() => {
//     deviceService = {
//       channel: {
//         channelRef: {}
//       }
//     };

//     lottoReceiptService = {
//       setReceipt: jasmine.createSpy()
//     };

//     coreToolsService = {
//       getCurrencySymbolFromISO: () => '$'
//     };

//     bppService = {
//       send: jasmine.createSpy().and.returnValue(of(null))
//     };

//     router = {
//       navigate: jasmine.createSpy()
//     };

//     clientUserAgentService = {
//       getId: jasmine.createSpy()
//     };
//     timeSyncService = {
//       ip: '192.168.3.1'
//     };
//     spyOn(window as any, 'setTimeout').and.callFake((arg1: Function) => arg1());

//     service = new LottoBetService(
//       deviceService,
//       lottoReceiptService,
//       coreToolsService,
//       bppService,
//       router,
//       clientUserAgentService,
//       timeSyncService
//     );
//   });

//   it('constructor', () => {
//     expect(service).toBeTruthy();
//   });

//   it('placeBet', fakeAsync(() => {
//     const data = { id: 1 };

//     service['setReceipt'] = jasmine.createSpy('sendRequest').and.returnValue(of([]));
//     // service['sendRequest'] = jasmine.createSpy('sendRequest').and.returnValue(of([]));

//     service.placeBet(data).subscribe();

//     tick();
//     expect(service['setReceipt']).toHaveBeenCalledWith(data);
//     // expect(service['sendRequest']).toHaveBeenCalled();
//   }));

//   it('openReceipt', () => {
//     service.openReceipt();
//     expect(router.navigate).toHaveBeenCalledWith(['/lotto', 'lottery-receipt']);
//   });

//   it('setReceipt', () => {
//     const result = service['setReceipt']({
//       name: 'no name',
//       draws: '',
//       selections: '1|2|3',
//       odds: '',
//       amount: 2,
//       currency: 'USD'
//     });

//     expect(lottoReceiptService.setReceipt).toHaveBeenCalled();
//     expect(result).toEqual(jasmine.any(Observable));
//   });

//   it('sendRequest', () => {
//     service['constructPlaceBetObj'] = jasmine.createSpy();

//     const data = { id: 1 };
//     const result = service['sendRequest'](data);

//     expect(result).toEqual(jasmine.any(Observable));
//     expect(service['constructPlaceBetObj']).toHaveBeenCalledWith(data);
//     expect(bppService.send).toHaveBeenCalled();
//   });

//   it('constructPlaceBetObj', () => {
//     const data = {
//       draws: '',
//       amount: 10,
//       currency: 'USD',
//       selections: '',
//       selectionName: ''
//     };

//     service['constructBetslip'] = jasmine.createSpy();
//     service['constructLeg'] = jasmine.createSpy();
//     service['constructBet'] = jasmine.createSpy();

//     expect(service['constructPlaceBetObj'](data)).toEqual(jasmine.any(Object));
//     expect(service['constructBetslip']).toHaveBeenCalled();
//     expect(service['constructLeg']).toHaveBeenCalled();
//     expect(service['constructBet']).toHaveBeenCalled();
//   });

//   it('constructBet', () => {
//     expect(service['constructBet'](1, 'a', 2, 'USD')).toEqual(jasmine.any(Array));
//   });

//   it('constructLeg', () => {
//     expect(service['constructLeg']('1', [])).toEqual(jasmine.any(Array));
//   });

//   it('should return array of legs', () => {
//     const draws = [
//       {
//         id: '1',
//         sort: 'a',
//         drawDescriptionId: '1'
//       }
//     ] as ILottoDraw[];
//     const actualResult = service['constructLeg']('1', draws);
//     const expectedResult = [{
//       documentId: 1,
//       lotteryLeg: {
//         picks: '1',
//         gameRef: {
//           id: '1'
//         },
//         sortRef: {
//           id: 'a'
//         },
//         drawRef: {
//           id: '1'
//         },
//         subscription: {
//           number: '1',
//           free: '0'
//         }
//       }
//     }] as any;

//     expect(actualResult).toEqual(expectedResult);
//   });

//   it('createBetRef', () => {
//     const result = service['createBetRef'](2);
//     expect(result).toEqual(jasmine.any(Array));
//     expect(result.length).toBe(2);
//   });

//   it('constructBetslip', () => {
//     service['createBetRef'] = jasmine.createSpy();
//     expect(service['constructBetslip'](1, 2, 'USD')).toEqual(jasmine.any(Object));
//     expect(service['createBetRef']).toHaveBeenCalledWith(2);
//   });
// });
