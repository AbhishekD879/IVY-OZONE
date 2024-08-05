import { MY_ENTRIES_LIST } from '@app/fiveASideShowDown/mockdata/entryinfo.mock';
import {
  FiveASideEntryListComponent
} from '@app/fiveASideShowDown/components/fiveASideEntry/fiveASideEntryList/fiveaside-entry-list.component';

describe('FiveASideEntryListComponent', () => {

  let component: FiveASideEntryListComponent;
  let fiveASideEntryInfoService, coreToolsService;

  beforeEach((() => {
    fiveASideEntryInfoService = {
      entriesCreation: jasmine.createSpy('entriesCreation').and.returnValue(MY_ENTRIES_LIST),
      isOpened: jasmine.createSpy('isOpened').and.returnValue(MY_ENTRIES_LIST)
    };
      coreToolsService = {
        uuid: jasmine.createSpy().and.returnValue('122344543')
      },
      component = new FiveASideEntryListComponent(fiveASideEntryInfoService, coreToolsService);
  }));

  describe('ngOnInit', () => {
    it('ngOnInit', () => {
      component.myEntriesList = MY_ENTRIES_LIST as any;
      component.eventStatus = 'preplay';
      spyOn(component as any, 'rankBasedOnOdds');
      component.ngOnInit();
      expect(fiveASideEntryInfoService.entriesCreation).toHaveBeenCalled();
    });
    it('ngOnInit', () => {
      component.myEntriesList = MY_ENTRIES_LIST as any;
      component.eventStatus = 'live';
      spyOn(component as any, 'rankBasedOnOdds');
      component.ngOnInit();
      expect(fiveASideEntryInfoService.entriesCreation).not.toHaveBeenCalled();
    });
    it('ngOnInit', () => {
      component.myEntriesList = MY_ENTRIES_LIST as any;
      component.eventStatus = 'post';
      spyOn(component as any, 'rankBasedOnOdds');
      component.ngOnInit();
      expect(fiveASideEntryInfoService.entriesCreation).not.toHaveBeenCalled();
    });
  });
  describe('rankBasedOnOdds', () => {
    beforeEach(() => {
      MY_ENTRIES_LIST[0].rank = 0;
      MY_ENTRIES_LIST[1].rank = 0;
      MY_ENTRIES_LIST[2].rank = 0;
      MY_ENTRIES_LIST[0].oddsDecimal = 0;
      MY_ENTRIES_LIST[1].oddsDecimal = 0;
      MY_ENTRIES_LIST[2].oddsDecimal = 0;
    });
    it('rankBasedOnOdds having odds same for all', () => {
      MY_ENTRIES_LIST[0].oddsDecimal = 0.25;
      MY_ENTRIES_LIST[1].oddsDecimal = 0.25;
      MY_ENTRIES_LIST[2].oddsDecimal = 0.25;
      component.entries = MY_ENTRIES_LIST as any;
      component['rankBasedOnOdds']();
      expect(component.entries[0].rank).toBe(1);
      expect(component.entries[1].rank).toBe(1);
      expect(component.entries[2].rank).toBe(1);
    });
    it('rankBasedOnOdds having odds two same', () => {
      MY_ENTRIES_LIST[0].oddsDecimal = 0.35;
      MY_ENTRIES_LIST[1].oddsDecimal = 0.25;
      MY_ENTRIES_LIST[2].oddsDecimal = 0.25;
      component.entries = MY_ENTRIES_LIST as any;
      component['rankBasedOnOdds']();
      expect(component.entries[0].rank).toBe(1);
      expect(component.entries[1].rank).toBe(2);
      expect(component.entries[2].rank).toBe(2);
    });
    it('rankBasedOnOdds having odds two same', () => {
      MY_ENTRIES_LIST[0].oddsDecimal = 0.35;
      MY_ENTRIES_LIST[1].oddsDecimal = 0.35;
      MY_ENTRIES_LIST[2].oddsDecimal = 0.25;
      component.entries = MY_ENTRIES_LIST as any;
      component['rankBasedOnOdds']();
      expect(component.entries[0].rank).toBe(1);
      expect(component.entries[1].rank).toBe(1);
      expect(component.entries[2].rank).toBe(3);
    });
    it('rankBasedOnOdds having odds different', () => {
      MY_ENTRIES_LIST[0].oddsDecimal = 0.35;
      MY_ENTRIES_LIST[1].oddsDecimal = 0.25;
      MY_ENTRIES_LIST[2].oddsDecimal = 0.15;
      component.entries = MY_ENTRIES_LIST as any;
      component['rankBasedOnOdds']();
      expect(component.entries[0].rank).toBe(1);
      expect(component.entries[1].rank).toBe(2);
      expect(component.entries[2].rank).toBe(3);
    });
    it('rankBasedOnOdds having odds different', () => {
      MY_ENTRIES_LIST[0].oddsDecimal = 0.35;
      MY_ENTRIES_LIST[1].oddsDecimal = 0.25;
      MY_ENTRIES_LIST[2].oddsDecimal = 0.15;
      component.entries = MY_ENTRIES_LIST as any;
      component.entries.push({'oddsDecimal':'0.15'} as any);
      component['rankBasedOnOdds']();
      expect(component.entries[0].rank).toBe(1);
      expect(component.entries[1].rank).toBe(2);
      expect(component.entries[2].rank).toBe(3);
      expect(component.entries[3].rank).toBe(3);
    });
  });
});
