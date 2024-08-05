import { Component, EventEmitter, Input, OnChanges, OnInit, Output, SimpleChanges } from '@angular/core';
import { ApiClientService } from '@app/client/private/services/http';
import { ISegment } from '@app/client/private/models/segment.model';
import { HttpResponse } from '@angular/common/http';
import { CSPSegmentConstants } from '@app/app.constants';
import { GlobalLoaderService } from '@app/shared/globalLoader/loader.service';

@Component({
  selector: 'cms-segment-dropdown',
  templateUrl: './cms-segment-dropdown.component.html',
  styleUrls: ['./cms-segment-dropdown.component.scss']
})
export class CmsSegmentDropdownComponent implements OnInit, OnChanges {
  /**
   * pre-selected segment
   * @type {string}
   */
  @Input() activeSegment?: string = CSPSegmentConstants.UNIVERSAL_TITLE;

  /**
  * Emits selected segment of type string
  */
  @Output() selectedSegment = new EventEmitter();

  /**
   * disable dropdown
   */
   @Input() disabled?: string;

  /**
  * active segment of type string
  */
  activeSegment$: string;
  selectedValue: string;
  segmentsList: string[];
  segmentsFilteredList: string[];

  
  constructor(private apiClientService: ApiClientService,
    private globalLoaderService: GlobalLoaderService) { }
  
  ngOnInit(): void {
    this.apiClientService.segmentMethods().getSegments().subscribe((data: HttpResponse<ISegment[]>) => {
      this.segmentsList = this.segmentsFilteredList = data.body.map(function(segment: ISegment) {
        return segment.name;
      });
      this.selectedValue = this.segmentsList.find((segment: string) => segment === this.activeSegment);
    });
  }

  ngOnChanges(changes: SimpleChanges) {
    if(changes.activeSegment && changes.activeSegment.currentValue && !changes.activeSegment.firstChange) {
      this.selectedValue = this.segmentsList.find((segment: string) => segment === changes.activeSegment.currentValue);
      if(!this.selectedValue) this.getSegmentsList(); 
    }
  }

  /**
   * handle onchange of segment dropdown
   */
  segmentChange(): void {
    this.activeSegment$ = this.segmentsList.find((segment: string) => segment === this.selectedValue);
    this.segmentsFilteredList = this.segmentsList;
    this.selectedSegment.emit(this.activeSegment$);
  }
  
  /**
   * Search for the segments based on the segment search
   * @param segmentSearch 
   */
  onSearch(segmentSearch: string) {
    this.segmentsFilteredList = this.segmentsList;
    this.segmentsFilteredList = this.filter(segmentSearch);
    if(!segmentSearch && this.activeSegment !== CSPSegmentConstants.UNIVERSAL_TITLE) {
      this.selectedSegment.emit(CSPSegmentConstants.UNIVERSAL_TITLE);
    }
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

  getSegmentsList() {
    this.globalLoaderService.showLoader();
    this.apiClientService.segmentMethods().getSegments().subscribe((data: HttpResponse<ISegment[]>) => {
      this.segmentsList = this.segmentsFilteredList = data.body.map(function(segment: ISegment) {
        return segment.name;
      });
      this.selectedValue = this.segmentsList.find((segment: string) => segment === this.activeSegment);
      this.globalLoaderService.hideLoader();
    });
  }
}