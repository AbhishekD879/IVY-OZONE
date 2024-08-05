import { CSPSegmentConstants } from "@app/app.constants";
import { of } from "rxjs";
import { CmsUniversalSegmentedComponent } from "./cms-universal-segmented.component";

describe('CmsUniversalSegmentedComponent', () => {
  let component: CmsUniversalSegmentedComponent;

  let mockData$ = {
    exclusionSegments: '',
    inclusionSegments: '',
    activeSegment: ''
  };
  
  let segmentObj = {
    exclusionList: [],
    inclusionList: [],
    universalSegment: true
  };

  let apiClientService;

  beforeEach(() => {
    apiClientService = {
      segmentMethods: jasmine.createSpy('segmentMethods').and.returnValue({
        getSegments: jasmine.createSpy('getSegments').and.returnValue(of({ body: [{ 'name': 'Universal' },{'name': 'Cricket'},{'name': 'FootBall'}] })),
      })
    };

    component = new CmsUniversalSegmentedComponent(
      apiClientService
    );
    component.segmentsData = {...mockData$};
    component.segmentsList = ['Universal','Cricket', 'Foot Ball']
  });

  it('#OnInit check if form valid/invalid', () => {
    let flag = component.isValid();
    component.isFormValid.emit = jasmine.createSpy();
    component.ngOnInit();
    expect(apiClientService.segmentMethods().getSegments).toHaveBeenCalled();
    expect(component.segmentsList.length).toBe(2);
    expect(component.segmentsFilteredList.length).toBe(2);
    expect(component.isFormValid.emit).toHaveBeenCalledWith(flag);
  });

  it('should set universal Data ', () => {
    let mock = component.segmentsData;
    mock.activeSegment = CSPSegmentConstants.UNIVERSAL;
    component.segmentsDataObj = segmentObj;
    expect(component.segmentsData).toEqual(mock);
  });

  it('should set segmented Data', () => {
    let segmentObj = {
      exclusionList: [],
      inclusionList: ['Cricket', 'American-Football'],
      universalSegment: false
    };
    let mock = component.segmentsData;
    mock.activeSegment = CSPSegmentConstants.SEGMENTED;
    mock.inclusionSegments = 'Cricket,American-Football';
    component.segmentsDataObj = segmentObj;
    expect(component.segmentsData).toEqual(mock);
  });

  it('selecting universal should set segmented data to empty', () => {
    let event = { value: CSPSegmentConstants.UNIVERSAL };
    component.segmentsData = mockData$;
    component.segmentsData.activeSegment = CSPSegmentConstants.UNIVERSAL;;
    component.segmentsData.inclusionSegments = 'Cricket, Hockey';
    component.segmentHandler(event.value);
    expect(component.segmentsData.inclusionSegments).toBe('');
  });

  it('selecting segmented should set exclusionsegments data to empty', () => {
    let event = { value: 'SEGMENTED' };
    component.segmentsData = component.segmentsData;
    component.segmentsData.activeSegment = 'SEGMENTED';
    component.segmentsData.exclusionSegments = 'Cricket, Hockey';
    component.segmentHandler(event.value);
    expect(component.segmentsData.exclusionSegments).toBe('');
  });

  it('should check if activesegment is empty', () => {
    component.segmentsData.activeSegment = '';
    expect(component.isValid()).toBe(false);
  });

  it('should return modified segment data', () => {
    let mock = component.segmentsData;
    mock.exclusionSegments = 'Cricket, Foot Ball, Hockey';
    mock.activeSegment = CSPSegmentConstants.UNIVERSAL;
    let expectedData = {
      universalSegment: false,
      inclusionList: [],
      exclusionList: ['Cricket', 'Foot Ball', 'Hockey']
    }
    component.modifySegmentData = jasmine.createSpy('modifySegmentData').and.returnValue(expectedData);
    expect(component.modifySegmentData(mock)).toEqual(expectedData);
  });

  it('should modify data for exclusion using formatSegmentValue', () => {
    let mock = component.segmentsData;
    mock.exclusionSegments = 'Cricket, Foot Ball, Hockey';
    mock.activeSegment = CSPSegmentConstants.UNIVERSAL;
    let expectedData = {
      universalSegment: true,
      inclusionList: [],
      exclusionList: ['Cricket', 'Foot Ball', 'Hockey']
    }
    expect(component.modifySegmentData(mock)).toEqual(expectedData);
  });

  it('should modify data for inclusion using formatSegmentValue', () => {
    let mock = component.segmentsData;
    mock.inclusionSegments = 'Cricket, Foot Ball, Hockey';
    mock.activeSegment = CSPSegmentConstants.SEGMENTED;
    let expectedData = {
      universalSegment: false,
      inclusionList: ['Cricket', 'Foot Ball', 'Hockey'],
      exclusionList: []
    }
    expect(component.modifySegmentData(mock)).toEqual(expectedData);
  });

  it('should emit value, data for isFormValid, segmentdata', () => {
    let event = {
      target: {
        name: 'exclusion',
        value: 'Cricket'
      }
    }
    component.isFormValid.emit = jasmine.createSpy();
    component.segmentsModifiedData.emit = jasmine.createSpy();
    component.validateAndFilterSegments(event);
    expect(component.modifySegmentData).toBeDefined();
    let data = component.modifySegmentData(component.segmentsData);
    expect(component.isFormValid.emit).toHaveBeenCalledWith(component.isValid());
    expect(component.segmentsModifiedData.emit).toHaveBeenCalledWith(data);
  });

  it('checks if the string has empty spaces', () => {
    const segmentValue = '';
    expect(component.formatSegmentValue(segmentValue)).toEqual([]);
  });

  it('checks if the string has empty comma', () => {
    const segmentValue = ',,';
    expect(component.formatSegmentValue(segmentValue)).toEqual([]);
  });

  it('checks if the string has value and empty comma', () => {
    const segmentValue = 'cricket, hockey ,';
    expect(component.formatSegmentValue(segmentValue)).toEqual(['cricket', 'hockey']);
  });

  it('should filter the segment data based on search string', () => {
    let event = { target : { name: 'exclusion', value: 'Cricket,Foo' }};
    component['validateAndFilterSegments'](event);
    expect(component.segmentsFilteredList).toEqual(['Foot Ball']);
  });

  it('on exclusive segment selection the data should get updated properly', () => {
    component.universal = {
      nativeElement : {
        value: ''
      }
    } as any;
    let event = { option: { value: 'FootBall' }};
    component.segmentSearch = 'Foo';
    component.segmentsData.exclusionSegments = 'Cricket,Foo';
    component['exclusionSegmentSelected'](event);
    expect(component.segmentsData.exclusionSegments).toEqual('Cricket,FootBall');
  });

  it('on inclusive segment selection the data should get updated properly', () => {
    component.inclsuion = {
      nativeElement : {
        value: ''
      }
    } as any;
    let event = { option: { value: 'FootBall' }};
    component.segmentSearch = 'Foo';
    component.segmentsData.inclusionSegments = 'Cricket,Foo';
    component['inclusionSegmentSelected'](event);
    expect(component.segmentsData.inclusionSegments).toEqual('Cricket,FootBall');
  });

  it('validate the segment string', () => {
    let event = { target: { name: 'inclusion', value: 'Foot-Ball' }};
    component['validateAndFilterSegments'](event);
    expect(component.isInclusionInvalid).toBeFalse();
  });

  it('should not allow user to enter special characters in a segment string', () => {
    let event = { target: { name: 'exclusion', value: 'FootBall$' }};
    component['validateAndFilterSegments'](event);
    expect(component.isExclusionInvalid).toBeTrue();
  });

  it("should not allow empty segments to enter", () => {
    let selectedSegments = 'FootBall,Cricket,,';
    component['validateAndEmitData'](true,selectedSegments);
    expect(component.isSegmentValid).toBeFalse();
  })

  it("should not allow empty commas to enter", () => {
    let selectedSegments = ',,';
    component['validateAndEmitData'](false,selectedSegments);
    expect(component.isSegmentValid).toBeTrue();
  })
});