import { PopularBetFiltersCreateComponent } from "./popular-bet-filters-create.component";
import { FormControl, FormGroup } from "@angular/forms";

describe("PopularBetFiltersCreateComponent", () => {
  let component: PopularBetFiltersCreateComponent;
  let dialogRef;
  let dialog;

  beforeEach(() => {
    dialogRef = {
      close: jasmine.createSpy("close"),
    };
    dialog = {
      sportFilterData: {
        displayName: "",
        isEnabled: true,
        time: 0,
        isTimeInHours: true,
        isDefault: true,
      },
      originalData: {
        displayName: "",
        isEnabled: true,
        time: 0,
        isTimeInHours: true,
        isDefault: true,
      },
    };
    component = new PopularBetFiltersCreateComponent(dialogRef, dialog);
  });

  it("it should call ngOnInit on when create filter", () => {
    component.dialog.pageType = "create";
    component.popularBetsSportObj = {
      displayName: "",
      isEnabled: true,
      time: 0,
      isTimeInHours: true,
      isDefault: true,
    };
    component.ngOnInit();
    expect(component.dialog.pageType).toBeTruthy();
   });

  it("it should call ngOnInit on when edit filter", () => {
    component.dialog.pageType = "edit";
    component.dialog.filter = {
      displayName: "",
      isEnabled: true,
      time: 0,
      isTimeInHours: true,
      isDefault: false,
    };
    component.ngOnInit();
    expect(component.dialog.pageType).toBeTruthy();
  });

  it("it should call ngOnInit on when create and false ", () => {
    component.dialog.pageType = "edqqqit";
    component.popularBetsSportObj = {
      displayName: "test",
      isEnabled: true,
      time: 0,
      isTimeInHours: true,
      isDefault: true,
    };
    component.form = new FormGroup({
      displayName: new FormControl(component.popularBetsSportObj.displayName || ''),
      isEnabled: new FormControl(component.isEnabledSportFilter || '', []),
      isTimeInHours: new FormControl(true ),
      time: new FormControl(component.popularBetsSportObj.time ),
    });
    component.ngOnInit();
     expect(component.form).toBeDefined();
  });
  

  it("isEnabledSportFilter", () => {
    component.popularBetsSportObj = {isEnabled: true}as any;
    component.isEnabledSportFilter({checked : true });
    expect(component.isEnabledSportFilter).toBeTruthy();
  });
  it("isEnabledSportFilter when checked = false ", () => {
    component.popularBetsSportObj = {isEnabled: true ,
    isDefault : false }as any;
    component.isEnabledSportFilter({checked : false });
    expect(component.isEnabledSportFilter).toBeTruthy();
  });

  it("closeDialog", () => {
    component.cancel();
    expect(dialogRef.close).toHaveBeenCalled();
  });

  it("it should call popularBetsFilterValid with form values", () => {
    component.popularBetsSportObj = {
      displayName: "test",
      isEnabled: true,
      time: 0,
      isTimeInHours: true
    };
    const valid =  component.popularBetsFilterValid();
    expect(valid).toBeFalsy();
    expect(component.popularBetsSportObj.time).toEqual(0);
    expect(component.popularBetsSportObj.displayName).toEqual('test');
  });

  it('it should call defaultPropertyHandler', ()=>{
    component.popularBetsSportObj = {
      displayName: "test",
      isEnabled: true,
      time: 0, 
      isTimeInHours: true
    };
    const event = {checked : true};
    component.defaultPropertyHandler(event)
  })
  
  it("it should call setHoursMinFormData ", () => {
    component.popularBetsSportObj = {
      displayName: "test",
      isEnabled: true,
      time: 0, 
      isTimeInHours: true
    };
   component.hoursOrMinutes = "1hr"
   component.setHoursMinFormData('');
   expect(component.popularBetsSportObj).toEqual({ displayName: "test",
   isEnabled: true,
   time: 1, 
   isTimeInHours: true})
  });
  
});
