import { LottoNumberSelectorComponent } from '@app/lotto/components/lottoNumberSelectorDialog/lotto-number-selector-dialog.component';
import { EMPTY, of } from 'rxjs';
import environment from '@environment/oxygenEnvConfig';

describe('LottoNumberSelectorComponent', () => {
  let component: LottoNumberSelectorComponent;
  let deviceService: any;
  let segmentDataUpdateService: any;
  let filterService: any;
  let windowRef;
  let storage;
  let locale;

  beforeEach(() => {
    deviceService = {};
    windowRef = {};

    segmentDataUpdateService = { changes: of({ numbersSelected: 12, numbersData: 33 }) };

    filterService = { getComplexTranslation: jasmine.createSpy('getComplexTranslation') };
    storage = {
      get: jasmine.createSpy('get'),
      set: jasmine.createSpy('set'),
      remove: jasmine.createSpy('remove')
    };

    locale = {
      getString: jasmine.createSpy('getString').and.returnValue('bma')
    };

    component = new LottoNumberSelectorComponent(
      deviceService,
      segmentDataUpdateService,
      filterService,
      windowRef,
      storage,
      locale
    );
    component.dialog = {
      close: jasmine.createSpy('close'),
      onKeyDownHandler: jasmine.createSpy('onKeyDownHandler'),
      changeDetectorRef: { detectChanges: jasmine.createSpy('detectChanges') },
      doneSelected: jasmine.createSpy('doneSelected')
    };
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  describe('ngOnInit', () => {
    let params = {};
    environment.brand = 'ladbrokes';
    beforeEach(() => {
      params = {};
    });

    describe('should not set params', () => {
      it('when changes observable is not resolved', () => {
        segmentDataUpdateService.changes = EMPTY;
      });
      it('when params are not defined observable is not resolved', () => {
        params = null;
      });
      it('when params are not defined observable is not resolved', () => {
        segmentDataUpdateService.changes = of(null);
      });

      afterEach(() => {
        component.params = params;
        component.ngOnInit();
        expect(component.params).toEqual(params);
        expect(component.dialog.changeDetectorRef.detectChanges).not.toHaveBeenCalled();
      });
    });

    describe('check if line already exists', ()=>{
      beforeEach(() => {
        component.params = {
          'lineSummary': [{
            "numbersData": [
              {
                "value": 3,
                "selected": true,
                "disabled": false
              },
              {
                "value": 23,
                "selected": true,
                "disabled": false
              },
              {
                "value": 42,
                "selected": true,
                "disabled": false
              }
            ],
            "isBonusBall": false,
            "isFavourite": false
          }],
          'doneSelected':()=>{}
        };
        component.ngOnInit();
      });
      it('Selected Number Exists to be false', () => {  
        component.params = null;
        component.checkSelectedNumbersExists();
        expect(component.selectedNumbersExists).toBe(false);
      });
    
      it('Selected Number Exists to be true', () => {
        component.params.numbersData = component.params.lineSummary[0].numbersData;
        component.checkSelectedNumbersExists();
        expect(component.selectedNumbersExists).toBe(true);
      });

      it('Selected Number Exists to be true', () => {
        component.params.numbersData = component.params.lineSummary[0].numbersData;
        component.params.lineSummary = null;
        component.checkSelectedNumbersExists();
        expect(component.selectedNumbersExists).toBe(false);
      });
    });
    it('should set params', () => {
      component.params = params;
      component.ngOnInit();

      expect(component.params.numbersSelected).toEqual(12);
      expect(component.params.numbersData).toEqual(33);
      expect(component.dialog.changeDetectorRef.detectChanges).toHaveBeenCalled();
    });
  });

  it('getDipTranlationsl', () => {
    component.getDipTranlations('12');

    expect(filterService.getComplexTranslation).toHaveBeenCalledWith('lotto.lucky', '%num', '12');
  });

  it('isSelected', () => {
    component.params = { numbersData: [{ selected: true }] } as any;

    expect(component.isSelected).toBeTruthy();
  }); 
  
  it('isSelected', () => {
    component.isSelected = false;
    expect(component.isSelected).toBeFalsy();
  }); 
});
