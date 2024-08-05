import { AfterViewInit, Component, EventEmitter, Input, Output } from '@angular/core';
import { DomSanitizer } from '@angular/platform-browser';
import { SortableTableService } from '@app/client/private/services/sortable.table.service';
import { StyleService } from '@app/client/private/services/style.service';
import { CSPSegmentConstants } from '@app/app.constants';
import { CMSDataTableComponent } from './cms.data.table.component';
import { MatSnackBar } from '@angular/material/snack-bar';
import { BigCompetitionAPIService } from '@app/sports-pages/big-competition/service/big-competition.api.service';
import { DatePipe } from '@angular/common';

@Component({
    selector: 'cms-segment-data-table',
    templateUrl: './cms.segement-data.table.component.html',
    styleUrls: ['./cms.data.table.component.scss'],
    providers: [
        SortableTableService, BigCompetitionAPIService,DatePipe
    ]
})
export class CMSSegmentDataTableComponent extends CMSDataTableComponent implements AfterViewInit {
    @Input() selectedSegment?: string;
    @Input() customTableData: Array<any> = [];
    @Input() reorder: boolean = false;
    @Input() pageId?: number = null;
    @Input() pageType?: string = null;
    /**
     * sportcaterogy flag to enable the checkbox on selecting "Show in Sports Ribbon"
     */
    @Input() sportsCategoryFlag: boolean;
    @Input() surfaceBetsFlag: boolean;
    
    /**
     * emit the value on selecting the checkbox
     * @type {EventEmitter<any>}
     */
    @Output() showOnSportsFlagChange = new EventEmitter();

    @Output() removeExpiredData = new EventEmitter();
    showOnSportsRibbonColumName = CSPSegmentConstants.SHOW_IN_SPORTS_RIBBON_COLUMN;
    enabled:string = 'Enabled';
    highlightsTab: string = 'Highlights Tab';
    edp: string = 'EDP';
    displayInDesktop: string = 'Display in Desktop';

    @Input() multyRemove: boolean;
    @Input() removebybdata: boolean;
    constructor(
        protected sortableTableService: SortableTableService,
        protected sanitizer: DomSanitizer,
        private addRemoveStyleService: StyleService,
        protected snackBar: MatSnackBar,
        protected bigCompetion: BigCompetitionAPIService,
        protected datePipe:DatePipe
    ) {
        super(sortableTableService, sanitizer, snackBar, bigCompetion, datePipe);
    }

    ngAfterViewInit() {
        this.addRemoveStyleService.addStyle('tooltip-wrap', '.mat-tooltip { word-break: break-all; }');
        if (this.reorder) {
            this.addReorderingToTable();
        }
    }

    /**
     * sorting of table
     */
    addReorderingToTable(): void {
        const self = this;
        this.sortableTableService.addSorting({
            dataToReorder: self.customTableData,
            mainSelector: `.custom-table.${self.tableUniqueClass} tbody`,
            handlerSelector: '.drag-handler',
            onReorderEnd(data, indexOfDraggedElement) {
                const newOrder = {
                    order: self.customTableData.map(element => element.id),
                    segmentName: self.selectedSegment,
                    id: self.customTableData[indexOfDraggedElement].id,
                    pageType: self.pageType,
                    pageId: self.pageId
                };
                self.onElementsOrder.emit(newOrder);
            }
        });
    }

    //on enable/disable sports ribbon checkbox emit that data to other compoennt to save in the DB
    selectingShowOnSportsRibbon(sportsRibbonFlag,rowIndex){
        this.showOnSportsFlagChange.emit({sportsRibbonFlag,rowIndex});
    }

    //to enable/disable active surface bets checkboxes
    selectingShowOnSurfaceBets(flag, rowIndex, name) {
     this.showOnSportsFlagChange.emit({flag, rowIndex, name});
    }
    removebybData(data: any) {
        this.removeExpiredData.emit(data);
    }
   
    ngOnDestroy() {
        this.addRemoveStyleService.removeStyle('tooltip-wrap');
    }
}
