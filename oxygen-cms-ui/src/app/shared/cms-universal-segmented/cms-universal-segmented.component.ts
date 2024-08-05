import { Component, Input, Output, EventEmitter, OnInit, ViewEncapsulation, OnChanges, SimpleChanges, ViewChild, ElementRef } from '@angular/core';
import { ISegment, ISegmentConfig, ISegmentModel } from '@app/client/private/models/segment.model';
import { CSPSegmentConstants } from '@app/app.constants';
import { ApiClientService } from '@app/client/private/services/http';
import { HttpResponse } from '@angular/common/http';
import { Subject } from 'rxjs';
import { debounceTime, distinctUntilChanged } from 'rxjs/operators';

@Component({
  selector: 'cms-universal-segmented',
  templateUrl: './cms-universal-segmented.component.html',
  styleUrls: ['./cms-universal-segmented.component.scss'],
  encapsulation: ViewEncapsulation.None
})
export class CmsUniversalSegmentedComponent implements OnInit, OnChanges {
  public constants = CSPSegmentConstants;
  segmentsList: string[];
  segmentsFilteredList: string[];
  segmentSearch: string;
  segmentsData: ISegmentConfig = {
    exclusionSegments: '',
    inclusionSegments: '',
    activeSegment: ''
  }
  onSegmentChange = new Subject<any>();
  isInclusionInvalid = false;
  isExclusionInvalid = false;
  isSegmentValid = true;
  @Input() set segmentsDataObj(data: ISegmentModel) {
    this.segmentsData = {
      exclusionSegments: data.exclusionList.join(),
      inclusionSegments: data.inclusionList.join(),
      activeSegment: data.universalSegment ? this.constants.UNIVERSAL : this.constants.SEGMENTED
    };
    this.isFormValid.emit(this.isValid());
  };
  @Input() isRevert: boolean;
  @Output() segmentsModifiedData: EventEmitter<ISegmentModel> = new EventEmitter<ISegmentModel>();
  @Output() isFormValid: EventEmitter<boolean> = new EventEmitter();
  @ViewChild('inclusion') inclsuion: ElementRef<HTMLInputElement>;
  @ViewChild('universal') universal: ElementRef<HTMLInputElement>;

  constructor(private apiClientService: ApiClientService) {
    this.onSegmentChange.pipe(
      debounceTime(400), distinctUntilChanged())
      .subscribe(value => {
        this.validateAndFilterSegments(value);
      })
   }

   ngOnChanges(changes: SimpleChanges): void {
    // To clear validations on reverting the changes.
    if(changes['isRevert'] && changes['isRevert'].currentValue) {
      this.isExclusionInvalid = false;
      this.isInclusionInvalid = false;
      this.isSegmentValid = true;
    }
   }

  ngOnInit() {
    // Gets the segments list for autocomplete and filters Universal.
    this.apiClientService.segmentMethods().getSegments().subscribe((data: HttpResponse<ISegment[]>) => {
      this.segmentsList = data.body.map(function(segment: ISegment) {
        return segment.name;
      });
      const universalIndex = this.segmentsList.findIndex((segment) => segment === CSPSegmentConstants.UNIVERSAL_TITLE);
      this.segmentsList.splice(universalIndex,1);
      this.segmentsFilteredList = this.segmentsList;
      this.filterSegments(this.segmentsData, true);
    });
    this.isFormValid.emit(this.isValid());
  }

  /**
   * Handling radio change logic and emitting flag value to check form status
   * */
  segmentHandler(event: string): void {
    if (event) {
      if (event === CSPSegmentConstants.UNIVERSAL) {
        this.segmentsData.inclusionSegments = '';
      } else if (event === CSPSegmentConstants.SEGMENTED) {
        this.segmentsData.exclusionSegments = '';
      }
      this.segmentsFilteredList = this.segmentsList;
      this.validateAndEmitData(true, event);
    }
    if (this.segmentsData.inclusionSegments === '' && this.segmentsData.exclusionSegments === '') {
      this.isExclusionInvalid = false;
      this.isInclusionInvalid = false;
    }
  }

  /**
   * verifying the input data based upon user selection.
   * Return false if inclusion segment is selected and no input fields entered.
   * */
  isValid(): boolean {
    if (this.segmentsData.activeSegment === '' || this.isInclusionInvalid || this.isExclusionInvalid || !this.isSegmentValid) {
      return false;
    }
    return !(this.segmentsData.activeSegment === CSPSegmentConstants.SEGMENTED && this.segmentsData.inclusionSegments === '');
  }

  /**
   * Handling the input change and emitting the changes to parent and checking validation.
   */
  validateAndFilterSegments(event: { target : { name: string, value: string }}): void {
    const regex = /^[a-zA-Z0-9_,-]*$/;
    if(!regex.test(event.target.value)){
      if(event.target.name === 'exclusion') {
        this.isExclusionInvalid = true;
      } else if(event.target.name === 'inclusion') {
        this.isInclusionInvalid = true;
      }
    }
    else {
      this.isExclusionInvalid = false;
      this.isInclusionInvalid = false;
    }
    if(event && event.target.name === 'exclusion') {
      this.segmentsData.exclusionSegments = event.target.value;
    } else if (event && event.target.name === 'inclusion') {
      this.segmentsData.inclusionSegments = event.target.value;
    }
    if(event) {
      this.segmentsFilteredList = this.segmentsList;
      const selectedSegments = event.target.value.split(',');
      this.segmentSearch = selectedSegments[selectedSegments.length - 1];
      this.isSegmentValid = true;
      if (event.target.value && event.target.value?.split(',').includes("")) {
        this.isSegmentValid = false;
      }
      this.segmentsFilteredList = this.filter(this.segmentSearch);
      if(event.target.value.includes(',')){
        const segmentsArray = event.target.value?.split(',');
        let segmentString = event.target.value;
        if(segmentsArray.findIndex((seg) => seg === this.segmentSearch) >= 0) {
          segmentString = segmentsArray.filter((seg) => seg !== this.segmentSearch).join(',');
        }
        this.validateAndEmitData(false, segmentString);
      } else {
        this.validateAndEmitData(false, event.target.value);
      }
    }
  }

  /**
   * On exclusion segments selected, this will create object and emits data.
   * @param event
   */
  exclusionSegmentSelected(event: { option : { value: string }}): void {
    this.segmentsData.exclusionSegments = this.formatAndValidateSegments(this.segmentsData.exclusionSegments, event);
    this.segmentsFilteredList = this.segmentsList;
    this.validateAndEmitData(true, this.segmentsData.exclusionSegments);
    this.universal.nativeElement.value = this.segmentsData.exclusionSegments;
  }

  /**
   * On inclusion segments selected, this will create object and emits data.
   * @param event
   */
  inclusionSegmentSelected(event: { option : { value: string }}): void {
    this.segmentsData.inclusionSegments = this.formatAndValidateSegments(this.segmentsData.inclusionSegments, event);
    this.segmentsFilteredList = this.segmentsList;
    this.validateAndEmitData(true, this.segmentsData.inclusionSegments);
    this.inclsuion.nativeElement.value = this.segmentsData.inclusionSegments;
  }

  /**
   * return object by converting the segments comma separated to array.
   * @param segment value
   * @returns
   */
  modifySegmentData(segment: ISegmentConfig): ISegmentModel {
    let segmentsObj: ISegmentModel = {
      exclusionList: !segment.exclusionSegments ? [] : this.formatSegmentValue(segment.exclusionSegments.trim()),
      inclusionList: !segment.inclusionSegments ? [] : this.formatSegmentValue(segment.inclusionSegments.trim()),
      universalSegment: segment.activeSegment === CSPSegmentConstants.UNIVERSAL
    }
    return segmentsObj;
  }

  /**
   * checks if the string has empty spaces or empty comma appended at the last index and
   * removes empty spaces after splitting
   * @param segment value
   * @returns
   */
   formatSegmentValue(segment: string): string[] {
    let index = segment.length - 1;
    if (index >= 0) {
      while (segment[index] === ',' || segment[index] === ' ') {
        segment = segment.substr(0, index);
        index = segment.length - 1;
      }
      return segment.length > 0 ? segment.split(',').map(res => res.trim()) : [];
    } else {
      return [];
    }
  }

  /**
   * checks if inclusion segments field is empty
   * @returns true or false
   */
  isInclusionEmpty(): boolean {
    return !this.segmentsData.inclusionSegments && this.segmentsData.activeSegment === this.constants.SEGMENTED;
  }

  /**
   * Get the segments based on search.
   * @param segmentSearch
   * @returns filtered segments list
   */
  private filter(segmentSearch: string): string[] {
    let filter = segmentSearch.toLowerCase();
    return this.segmentsList.filter(segment => segment.toLowerCase().startsWith(filter));
  }

  /**
   * To validate, create an object of type ISegmentModel
   * and emits the created object.
   */
  private validateAndEmitData(isNotFromInput: boolean, selectedSegments?: string): void {
    if(isNotFromInput) {
      this.isSegmentValid = true;
      if (selectedSegments && selectedSegments?.split(",").includes("")) {
        this.isSegmentValid = false;
      }
    }
    this.filterSegments(this.segmentsData, isNotFromInput);
    this.isFormValid.emit(this.isValid());
    let data = this.modifySegmentData(this.segmentsData);
    this.segmentsModifiedData.emit(data);
  }

  /**
   * To remove/Filter out the selected segments.
   * @param segmentData
   */
  private filterSegments(segmentData: ISegmentConfig, isNotFromInput?: boolean): void {
    if(segmentData.exclusionSegments || segmentData.inclusionSegments) {
      let segments = [];

      if (segmentData.exclusionSegments) {
        segments = segmentData.exclusionSegments.split(',');
      } else if (segmentData.inclusionSegments) {
        segments = segmentData.inclusionSegments.split(',');
      }

      if(isNotFromInput) {
        this.segmentsFilteredList = this.segmentsFilteredList.filter(function(segment: string){
          return !segments.find((seg) => seg === segment);
        });
      } else {
        const lastIndex = segments.length - 1;
        this.segmentsFilteredList = this.segmentsFilteredList.filter(function(segment: string){
          return !segments.find((seg,index) => seg === segment && index !== lastIndex);
        });
      }
    } else {
      this.segmentsFilteredList = this.segmentsList;
    }
  }

  private formatAndValidateSegments(segments: string, event: { option : { value: string }}): string {
    // This is to make sure that the search input is removed from the segments value
    let selectedSegments = segments.split(',');
    let length = selectedSegments.length;
    if (this.segmentSearch === selectedSegments[length-1]) {
      selectedSegments.splice(length-1,1);
      segments = selectedSegments.join(',');
    }
    const segmentSeparated = segments !== '' ? ( segments.endsWith(',') ? '': ',' ) : ''
    segments = segments + segmentSeparated + event.option.value;
    return segments;
  }
}
