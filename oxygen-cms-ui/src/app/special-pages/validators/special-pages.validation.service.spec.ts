import { SpecialPagesValidationService } from '@app/special-pages/validators/special-pages.validation.service';
import { OBJECTITEMS_MOCK } from '@app/special-pages/constants/euro-dashboard';


describe('SpecialPagesValidationService', () => {
    let service: SpecialPagesValidationService;

    beforeEach(() => {
        service = new SpecialPagesValidationService();
    });

    it('tests if SpecialPagesValidationService Service Created', () => {
        expect(service).toBeTruthy();
    });

    describe('isUnique', () => {
        it('returns true when parameters passed are unique', () => {
            service['isUnique']('4', OBJECTITEMS_MOCK, 'tierName');
            expect(service.isUnique('4', OBJECTITEMS_MOCK, 'tierName')).toBeTrue();
        });
        it('returns false when parameters passed are not unique', () => {
            service['isUnique']('3', OBJECTITEMS_MOCK, 'tierName');
            expect(service.isUnique('3', OBJECTITEMS_MOCK, 'tierName')).toBeFalse();
        });
    });
    describe('checkIfInteger', () => {
        it('returns true when integer is passed', () => {
            service['checkIfInteger']('4');
            expect(service.checkIfInteger('4')).toBeTrue();
        });
        it('returns false when integer value is not passed', () => {
            service['checkIfInteger']('5t');
            expect(service.checkIfInteger('5t')).toBeFalse();
        });
    });

});

