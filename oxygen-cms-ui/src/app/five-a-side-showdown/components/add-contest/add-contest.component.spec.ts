import { ADD_CONTEST_DEFAULT } from "@app/five-a-side-showdown/components/add-contest/add-contest.mock";
import { AddContestComponent } from "@app/five-a-side-showdown/components/add-contest/add-contest.component";

describe("AddContestComponent", () => {
  let component: AddContestComponent;
  let modalData;
  let dialogRef;
  let brandService;
  let globalLoaderService;
  let apiClientService;
  let errorService;

  beforeEach(() => {
    dialogRef = {
      close: jasmine.createSpy("close"),
    };
    brandService = {
      brand: "bma",
    };
    component = new AddContestComponent(modalData, dialogRef, brandService, globalLoaderService, apiClientService, errorService);
  });

  it("should create", () => {
    expect(component).toBeTruthy();
  });

  it("ngOnInit should initialize data", () => {
    component.ngOnInit();
    expect(component.contest.brand).toEqual(ADD_CONTEST_DEFAULT.brand);
  });

  it("check if close handler is called for modal close", () => {
    component["closeDialog"]();
    expect(dialogRef.close).toHaveBeenCalled();
  });

  it("Adding a contest", () => {
    component["addContest"]();
    expect(component.contest).toBeUndefined();
  });

  it("should return date in ISO Format for date Object", () => {
    const HANDLESTARTDATE: string = "2021-01-13T11:59:43.603Z";
    component.contest = ADD_CONTEST_DEFAULT;
    component.handleStartDate(HANDLESTARTDATE);
    expect(component.contest.startDate.length).not.toEqual(0);
  });

  it('#test for block special chars ', () => {
    const event = {
      target: {
        value: '@@@@test123%%%&****((())_'
      }
    } as any;
    component.blockSpecialChars(event);
    expect(event.target.value).toEqual('test123');
  });
});
