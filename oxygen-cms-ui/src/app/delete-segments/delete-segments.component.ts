import { HttpResponse } from '@angular/common/http';
import { Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { __spreadArrays } from 'tslib';

import { ISegment } from '../client/private/models/segment.model';
import { ApiClientService } from '../client/private/services/http';
import { DialogService } from '../shared/dialog/dialog.service';
import { GlobalLoaderService } from '../shared/globalLoader/loader.service';
import { CSPSegmentConstants } from '../app.constants';
import { MatAutocompleteTrigger } from '@angular/material/autocomplete';

@Component({
  selector: 'delete-segments',
  templateUrl: './delete-segments.component.html',
  styleUrls: ['./delete-segments.component.scss']
})
export class DeleteSegmentsComponent implements OnInit {
    segmentsList: string[] = [];
    segmentsListModel: ISegment[];
    isPanelOpen: boolean = false;
    totalSegments: Array<{name: string, selected: boolean}> = [];
    filteredSegments: Array<{name: string, selected: boolean}> = [];
    public selectedSegments: string[] = [];

    @ViewChild ('segmentInput') segmentInput: ElementRef<HTMLInputElement>;

    constructor(private globalLoaderService: GlobalLoaderService,
        private apiClientService: ApiClientService,
        private dialogService: DialogService) {
    }

    ngOnInit() {
        this.getSegments();
    }

    /**
     * Removes all the selected segments
     */
    onClear(): void {
        this.selectedSegments = [];
        this.filteredSegments.forEach((seg) => seg.selected = false);
    }

    /**
     * Selects the segment from dropdown
     * @param value segment
     */
    toggleSelection(value: string): void {
        const isDuplicate = this.selectedSegments.find((seg) => seg === value);
        const index = this.filteredSegments.findIndex((seg) => seg.name === value);
        if (!isDuplicate) {
            this.selectedSegments.push(value);
            this.filteredSegments[index].selected = true;
        } else {
            const idx = this.selectedSegments.findIndex((seg) => seg === value);
            this.selectedSegments.splice(idx,1);
            this.filteredSegments[index].selected = false;
        }
        this.segmentInput.nativeElement.blur();
    }

    /**
     * Removes a single segment or multiple segments.
     * @param index 
     * index is optional and is to remove single segment from drop down.
     */
    delete(value?: {name: string, selected: boolean}): void {
        this.dialogService.showConfirmDialog({
            title: 'Delete Segments',
            message: 'Are you sure you want to delete selected segment(s) permanently from CMS?',
            yesCallback: () => {
                this.globalLoaderService.showLoader();
                let segmentsIds: string = '';
                if(value) {
                    // will remove single segment
                    segmentsIds = this.segmentsListModel.find((seg) => seg.name === value.name).id;
                } else {
                    // to remove multiple segments based on ids.
                    const segments: string[] = [];
                    this.selectedSegments.forEach((segment) => {
                        segments.push(this.segmentsListModel.find((seg) => seg.name === segment).id);
                    });
                    segmentsIds = segments.join(',');
                }
                this.apiClientService.segmentMethods().deleteSegments(segmentsIds).subscribe(()=> {
                    this.onClear();
                    this.globalLoaderService.hideLoader();
                    this.getSegments();
                }, error => {
                    this.globalLoaderService.hideLoader();
                });
            }
        });
    }

    /**
     * To remove selected segment from the mat chip on click of x
     * @param index 
     */
    removeItem(index: number): void {
        const segmentName = this.selectedSegments[index];
        this.selectedSegments.splice(index,1);
        this.filter('');
        const idx = this.filteredSegments.findIndex((seg) => seg.name === segmentName);
        this.filteredSegments[idx].selected = false;
        this.filter(this.segmentInput.nativeElement.value);
    }

    /**
     * To filter the autocomplete segments based on the user input.
     * @param value 
     */
    onChange(value: string): void {
        this.filter(value);
    }

    /**
     * This will toggle the autocomplete on chevron icon click
     * @param trigger 
     */
    toggleAutocomplete(trigger: MatAutocompleteTrigger): void {
        if (this.isPanelOpen) {
            trigger.openPanel();
        } else {
            trigger.closePanel();
        }
    }

    /**
     * Action to perform on autocomplete open
     */
    onAutocompleteOpen(): void {
        this.isPanelOpen = false;
    }

    /**
     * Action to perform on autocomplete close
     */
    onAutocompleteClose(): void {
        this.isPanelOpen = true;
        this.segmentInput.nativeElement.value = '';
        this.filter('');
        this.segmentInput.nativeElement.blur();
    }

    /**
     * filters the segments list
     * @param value 
     */
    private filter(value: string): void {
      const filterValue = value.toLowerCase();
      this.filteredSegments = this.totalSegments.filter(segment => segment.name.toLowerCase().includes(filterValue));
    }

    /**
     * Gets the list of total segments from the selected brand.
     */
    private getSegments(): void {
        this.globalLoaderService.showLoader();
        this.apiClientService.segmentMethods().getSegments().subscribe((segments: HttpResponse<ISegment[]>) => {
            this.segmentsListModel = segments.body.slice();
            this.segmentsListModel.splice(0,1);
            this.segmentsList = segments.body.map(function(segment: ISegment) {
                return segment.name;
            });
            const universalIndex = this.segmentsList.findIndex((segment) => segment === CSPSegmentConstants.UNIVERSAL_TITLE);
            this.segmentsList.splice(universalIndex,1);
            this.filteredSegments = [];
            this.segmentsList.forEach((segment) => {
                const filterSegment = {
                    name: segment,
                    selected: false
                };
                this.filteredSegments.push(filterSegment);
            });
            this.totalSegments = this.filteredSegments.slice();
            this.globalLoaderService.hideLoader();
        },
        (error) => {
            console.error(error);
            this.globalLoaderService.hideLoader();
        });
    }
}
