import { UkTotesBetRecognitionService } from './uk-totes-bet-recognition.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { CoreToolsService } from '@core/services/coreTools/core-tools.service';
import * as uktote from '@localeModule/translations/en-US/uktote.lang';

describe('UkTotesBetRecognitionService', () => {
  let service: UkTotesBetRecognitionService;
  const coreToolsService = new CoreToolsService();

  beforeEach(() => {
    const localeService = new LocaleService(coreToolsService);
    localeService.setLangData(uktote);
    service = new UkTotesBetRecognitionService(localeService);
  });

  describe('recognizeBet', () => {
    describe('should properly parse', () => {
      let totePoolType;

      describe('bet for Exacta pool type', () => {
        it('for UK Tote', () => { totePoolType = 'UEXA'; });
        it('for Int Tote', () => { totePoolType = 'EX'; });
        afterEach(() => {
          expect(service.recognizeBet({ x: 1, y: 2 }, totePoolType)).toEqual('1 exacta bet'.toUpperCase());
          expect(service.recognizeBet({ any: [1, 2] }, totePoolType)).toEqual('1 reverse exacta bet'.toUpperCase());
          expect(service.recognizeBet({ any: [1, 2, 3] }, totePoolType)).toEqual('6 combination exacta bets'.toUpperCase());
          expect(service.recognizeBet({}, totePoolType)).toEqual('');
        });
      });

      describe('bet for Trifecta pooltype', () => {
        it('for UK Tote', () => { totePoolType = 'UTRI'; });
        it('fot Int Tote', () => { totePoolType = 'TR'; });
        afterEach(() => {
          expect(service.recognizeBet({ x: 1, y: 2, z: 3 }, totePoolType)).toEqual('1 trifecta bet'.toUpperCase());
          expect(service.recognizeBet({ any: [1, 2, 3] }, totePoolType)).toEqual('6 combination trifecta bets'.toUpperCase());
          expect(service.recognizeBet({}, totePoolType)).toEqual('');
        });
      });

      describe('bet for Win pooltype', () => {
        it('for UK Tote', () => { totePoolType = 'UWIN'; });
        it('fot Int Tote', () => { totePoolType = 'WN'; });
        afterEach(() => {
          expect(service.recognizeBet({ any: [1, 2, 3, 4] }, totePoolType)).toEqual('4 Win Selections');
          expect(service.recognizeBet({ any: [1] }, totePoolType)).toEqual('1 Win Selection');
          expect(service.recognizeBet({ any: [] }, totePoolType)).toEqual('');
          expect(service.recognizeBet({}, totePoolType)).toEqual('');
        });
      });

      describe('bet for Place pooltype', () => {
        it('for UK Tote', () => { totePoolType = 'UPLC'; });
        it('fot Int Tote', () => { totePoolType = 'PL'; });
        afterEach(() => {
          expect(service.recognizeBet({ any: [1, 2, 3, 4] }, totePoolType)).toEqual('4 Place Selections');
          expect(service.recognizeBet({ any: [1] }, totePoolType)).toEqual('1 Place Selection');
          expect(service.recognizeBet({ any: [] }, totePoolType)).toEqual('');
          expect(service.recognizeBet({}, totePoolType)).toEqual('');
        });
      });

      it('bet for unknown pool type', () => {
        expect(service.recognizeBet({ x: 1, y: 2 }, 'ANY')).toEqual('');
      });

      it('pool type was not passed', () => {
        expect(service.recognizeBet({ x: 1, y: 2 } )).toEqual('');
      });
    });
  });
});
