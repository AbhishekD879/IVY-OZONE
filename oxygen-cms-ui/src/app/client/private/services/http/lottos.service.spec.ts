import { of } from "rxjs";
import { LottosService } from "./lottos.service";
describe ('LottosService', () => {
    let service: LottosService;
    let http,domain,brand;
    beforeEach(() => {
        service = new LottosService(http, domain, brand);
    });
    it('should be created', () => {
        expect(service).toBeTruthy();
    });
    describe('getLottery',()=>{
        let id = '1'
        it('should send request to get lotto',()=>{
          let sendRequestSpy = spyOn(service as any, 'sendRequest').and.returnValue(of({}));
          service.getLottery(id);
          expect(sendRequestSpy).toHaveBeenCalled();
        });
    });
    describe('saveLotto', () => {
        let lotto = {id: '1'} as any;
        it('should save lotto', () => {
          let sendRequestSpy = spyOn(service as any, 'sendRequest').and.returnValue(of({}));
          service.saveLotto(lotto);
          expect(sendRequestSpy).toHaveBeenCalled();
        })
    })
    describe('updateLottoDetails', () => {
        let lotto = {id: '1'} as any;
        it('should updateLottoDetails lotto', () => {
            let sendRequestSpy = spyOn(service as any, 'sendRequest').and.returnValue(of({}));
            service.updateLottoDetails(lotto);
            expect(sendRequestSpy).toHaveBeenCalled();
          })
    })
    describe('remove', () => {
        let lotto = {id: '1'} as any;
        it('should remove lotto', () => {
            let sendRequestSpy = spyOn(service as any, 'sendRequest').and.returnValue(of({}));
            service.remove(lotto);
            expect(sendRequestSpy).toHaveBeenCalled();
          })
    })
    describe('findAllByBrand', () => {
        it('should findAllByBrand lotto', () => {
            let sendRequestSpy = spyOn(service as any, 'sendRequest').and.returnValue(of({}));
            service.findAllByBrand();
            expect(sendRequestSpy).toHaveBeenCalled();
          })
    })
    describe('putAllByBrand', () => {
        let lotto = {id: '1'} as any;
        it('should putAllByBrand lotto', () => {
            let sendRequestSpy = spyOn(service as any, 'sendRequest').and.returnValue(of({}));
            service.putAllByBrand(lotto);
            expect(sendRequestSpy).toHaveBeenCalled();
          })
    })
    describe('reorder', () => {
        let lotto = {id: '1'} as any;
        it('should reorder lotto', () => {
            let sendRequestSpy = spyOn(service as any, 'sendRequest').and.returnValue(of({}));
            service.reorder(lotto);
            expect(sendRequestSpy).toHaveBeenCalled();
          })
    })
    describe('uploadSvg', () => {
        let lotto = {id: '1'} as any;
        let file = FormData as any
        it('should uploadSvg lotto', () => {
            let sendRequestSpy = spyOn(service as any, 'sendRequest').and.returnValue(of({}));
            service.uploadSvg(lotto, file);
            expect(sendRequestSpy).toHaveBeenCalled();
          })
    })
})