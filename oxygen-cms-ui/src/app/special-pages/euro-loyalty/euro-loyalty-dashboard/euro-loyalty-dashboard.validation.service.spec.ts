import { EuroLoyaltyValidationService } from '@app/special-pages/euro-loyalty/euro-loyalty-dashboard/euro-loyalty-dashboard.validation.service';
import { PROP_MOCK } from '@app/special-pages/constants/euro-dashboard';

describe('EuroLoyaltyValidationService', () => {
    let service: EuroLoyaltyValidationService;
    let specialPagesValidationService;

    beforeEach(() => {
        specialPagesValidationService =  {
            checkIfInteger: jasmine.createSpy('checkIfInteger').and.returnValue(true)
        };
        service = new EuroLoyaltyValidationService(specialPagesValidationService);
    });

    it('tests if EuroLoyaltyValidationService Service Created', () => {
        expect(service).toBeTruthy();
    });

    describe('isValidConfigProperty', () => {
        it('returns true when config is valid', () => {
            const propValue = Object.assign({}, PROP_MOCK);
            spyOn(service, 'isNewPropertyNameValid').and.returnValue(true);
            spyOn(service, 'isTierNumberValid').and.returnValue(true);
            spyOn(service, 'isFreeBetLocationValid').and.returnValue(true);
            spyOn(service, 'isOfferIdValid').and.returnValue(true);
            expect(service.isValidConfigProperty(propValue, true)).toBeTrue();
        });
        it('returns false when config is not valid', () => {
            const propValue = Object.assign({}, PROP_MOCK);
            propValue.offerIdSeq = '';
            service['isValidConfigProperty'](propValue, false);
            expect(service.isValidConfigProperty(propValue, false)).toBeFalse();
        });
    });
    describe('isNewPropertyNameValid', () => {
        it('returns true it has all tierInfo and tierName is unique', () => {
            const propValue = Object.assign({}, PROP_MOCK);
            service['isNewPropertyNameValid'](propValue, true);
            expect(service.isNewPropertyNameValid(propValue, true)).toBeTrue();
        });
        it('returns false it does not have all tierInfo and tierName is not unique', () => {
            const propValue = Object.assign({}, PROP_MOCK);
            propValue.offerIdSeq = '';
            service['isNewPropertyNameValid'](propValue, false);
            expect(service.isNewPropertyNameValid(propValue, false)).toBeFalse();
        });
    });
    describe('isTierNumberValid', () => {
        it('returns true when tierNumber is an integer', () => {
            service['isTierNumberValid'](4);
            expect(specialPagesValidationService.checkIfInteger).toHaveBeenCalledWith(4);
            expect(service.isTierNumberValid(4)).toBeTrue();
        });
        it('returns false when tierNumber is not an integer', () => {
            specialPagesValidationService.checkIfInteger = jasmine.createSpy('checkIfInteger').and.returnValue(false);
            service['isTierNumberValid'](0.5);
            expect(specialPagesValidationService.checkIfInteger).toHaveBeenCalledWith(0.5);
            expect(service.isTierNumberValid(0.5)).toBeFalse();
        });
    });
    describe('isFreeBetLocationValid', () => {
        it('returns true when freeBetLocation has integer values', () => {
            service['isFreeBetLocationValid']('4');
            expect(specialPagesValidationService.checkIfInteger).toHaveBeenCalledWith('4');
            expect(service.isFreeBetLocationValid('4')).toBeTrue();
        });
        it('returns false when freeBetLocation does not have integer values', () => {
            specialPagesValidationService.checkIfInteger = jasmine.createSpy('checkIfInteger').and.returnValue(false);
            service['isFreeBetLocationValid']('h');
            expect(specialPagesValidationService.checkIfInteger).toHaveBeenCalledWith('h');
            expect(service.isFreeBetLocationValid('h')).toBeFalse();
        });
    });
    describe('isOfferIdValid', () => {
        it('returns true when offerId has integer values and is one less than freeBetPositionSequence', () => {
            const propValue = Object.assign({}, PROP_MOCK);
            spyOn(service, 'checkLocationAndSequenceCount').and.returnValue(true);
            service['isOfferIdValid'](propValue);
            expect(specialPagesValidationService.checkIfInteger).toHaveBeenCalledWith(propValue.offerIdSeq);
            expect(service['checkLocationAndSequenceCount'](propValue)).toBeTrue();
            expect(service.isOfferIdValid(propValue)).toBeTrue();
        });
        it('returns false when offerId does not have integer values and is not one less than freeBetPositionSequence', () => {
            const propValue = Object.assign({}, PROP_MOCK);
            propValue.freeBetPositionSequence = [12134, 23455];
            specialPagesValidationService.checkIfInteger = jasmine.createSpy('checkIfInteger').and.returnValue(false);
            service['isOfferIdValid'](propValue);
            expect(specialPagesValidationService.checkIfInteger).toHaveBeenCalledWith(propValue.offerIdSeq);
            expect(service.isOfferIdValid(propValue)).toBeFalse();
        });
    });
    describe('checkLocationAndSequenceCount', () => {
        it('returns false if count of freebet position sequence is not one greater than count of freebet locations', () => {
            const propValue = Object.assign({}, PROP_MOCK);
            propValue.freeBetPositionSequence = [12134, 23455];
            expect(service['checkLocationAndSequenceCount'](propValue)).toBeFalse();
        });
    });
});
