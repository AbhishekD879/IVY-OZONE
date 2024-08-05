import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { CdkTableModule } from '@angular/cdk/table';
import { MatAutocompleteModule } from '@angular/material/autocomplete';
import { MatButtonModule } from '@angular/material/button';
import { MatButtonToggleModule } from '@angular/material/button-toggle';
import { MatCardModule } from '@angular/material/card';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { MatChipsModule } from '@angular/material/chips';
import { MatNativeDateModule, MatRippleModule } from '@angular/material/core';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatDialogModule } from '@angular/material/dialog';
import { MatExpansionModule } from '@angular/material/expansion';
import { MatGridListModule } from '@angular/material/grid-list';
import { MatIconModule } from '@angular/material/icon';
import { MatInputModule } from '@angular/material/input';
import { MatListModule } from '@angular/material/list';
import { MatMenuModule } from '@angular/material/menu';
import { MatPaginatorModule } from '@angular/material/paginator';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatRadioModule } from '@angular/material/radio';
import { MatSelectModule } from '@angular/material/select';
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatSlideToggleModule } from '@angular/material/slide-toggle';
import { MatSliderModule } from '@angular/material/slider';
import { MatSnackBarModule } from '@angular/material/snack-bar';
import { MatSortModule } from '@angular/material/sort';
import { MatStepperModule } from '@angular/material/stepper';
import { MatTableModule } from '@angular/material/table';
import { MatTabsModule } from '@angular/material/tabs';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatTooltipModule } from '@angular/material/tooltip';
import { InputTrimModule } from 'ng2-trim-directive';

import { CamelCaseToSpacePipe } from '../client/private/pipes/camelCaseToSpace';
import { ArrayNoNullPipe } from './cmsDataTable/array-no-null.pipe';
import { ByteToKbPipe } from '@app/client/private/pipes/byteToKb.pipe';
import { ConfirmDialogComponent } from './dialog/confirm-dialog/confirm-dialog.component';
import { PromptDialogComponent } from './dialog/prompt-dialog/prompt-dialog.component';
import { NotificationDialogComponent } from './dialog/notification-dialog/notification-dialog.component';
import { TinymceComponent } from './tinymce/tinymce.component';
import { DateAndTimeComponent } from './formElements/dateAndTime/date.time.component';
import { CMSDataTableComponent } from './cmsDataTable/cms.data.table.component';
import { CMSSegmentDataTableComponent } from './cmsDataTable/cms.segement-data.table.component';
import { CMSDataTablePaginationComponent } from './cmsDataTable/cms.data.table.pagination.component';
import { HeaderActivityBadgeComponent } from './design/acitvityBadge/activity.badge.component';
import { DownloadCvsComponent } from './download-cvs/download-cvs.component';
import { DateRangeComponent } from './formElements/dateRange/date.range.component';
import { BannersAutocompleteComponent } from './banners-autocomplete/banners-autocomplete.component';
import { CmsSimpleSelectListComponent } from './cms-simple-select-list/cms-simple-select-list.component';
import { CmsUploadComponent } from './cms-upload/cms-upload.component';
import { ActionButtonsComponent } from './action-buttons/action-buttons.component';
import { BreadcrumbsComponent } from './breadcrumbs/breadcrumbs.component';
import { CmsAlertComponent } from './cms-alert/cms-alert.component';
import { CreateUpdatedAtByComponent } from './create-updated-at-by/create-updated-at-by.component';
import { ActiveInactiveExpiredComponent } from './active-inactive-expired/active-inactive-expired.component';
import { VipLevelsInputComponent } from './formElements/vipLevelsInput/vip-levels-input.component';
import { NumberListInputComponent } from './formElements/numberList/number-list-input.component';
import { NumberOnlyDirective } from '@app/shared/formElements/numberOnly/numberOnly.directive';
import { CustomerVariantsSelectComponent } from './formElements/customer-variants-select/customer-variants-select.component';
import { DialogService } from './dialog/dialog.service';
import { CmsUploadDropdownComponent } from '@app/shared/cms-upload-dropdown/cms-upload-dropdown.component';
import { SvgListComponent } from '@app/shared/svgList/svg-list.component';
import { FracToDecService } from '@app/shared/services/fracToDec/frac-to-dec.service';
import {TimelineDataTableComponent} from '@app/shared/timelineDataTable/timeline.data.table.component';
import {TimelineActionButtonsComponent} from '@app/shared/timelineActionButtons/timeline-action-buttons.component';
import { SvgIconSelectInputComponent } from './svg-icon-select-input/svg-icon-select-input.component';
import { DeleteDialogComponent } from './dialog/delete-dialog/delete-dialog.component';
import {SseService} from '@app/shared/sse/sse.service';
import {InlineMultiselectComponent} from '@app/shared/inlineMultiselect/inline-multiselect.component';
import { CmsSegmentDropdownComponent } from './cms-segment-dropdown/cms-segment-dropdown.component';
import { TwoDigitDecimaNumberDirective } from '@app/shared/formElements/twodigitdecimalnumber/twodigitdecimalnumber.directive';
import { CmsUniversalSegmentedComponent } from './cms-universal-segmented/cms-universal-segmented.component';
import { PreventWhiteSpacesDirective } from '@app/shared/formElements/prevent-white-spaces/prevent-white-spaces.directive';
import { CommonSvgInputSelectComponent } from './common-svg-input-select/common-svg-input-select.component';
import { TimeRangeComponent } from './formElements/timeRange/time.range.component';

@NgModule({
  imports: [
    CommonModule,
    CdkTableModule,
    FormsModule,
    MatAutocompleteModule,
    MatButtonModule,
    MatButtonToggleModule,
    MatCardModule,
    MatCheckboxModule,
    MatChipsModule,
    MatStepperModule,
    MatDatepickerModule,
    MatDialogModule,
    MatExpansionModule,
    MatGridListModule,
    MatIconModule,
    MatInputModule,
    MatListModule,
    MatMenuModule,
    MatNativeDateModule,
    MatPaginatorModule,
    MatProgressBarModule,
    MatProgressSpinnerModule,
    MatRadioModule,
    MatRippleModule,
    MatSelectModule,
    MatSidenavModule,
    MatSliderModule,
    MatSlideToggleModule,
    MatSnackBarModule,
    MatSortModule,
    MatTableModule,
    MatTabsModule,
    MatToolbarModule,
    MatTooltipModule,
    RouterModule,
    ReactiveFormsModule,
    InputTrimModule
  ],
  declarations: [
    CamelCaseToSpacePipe,
    ArrayNoNullPipe,
    ByteToKbPipe,
    ConfirmDialogComponent,
    PromptDialogComponent,
    NotificationDialogComponent,
    TinymceComponent,
    DateAndTimeComponent,
    DateRangeComponent,
    TimeRangeComponent,
    CMSDataTableComponent,
    CMSSegmentDataTableComponent,
    CMSDataTablePaginationComponent,
    TimelineDataTableComponent,
    TimelineActionButtonsComponent,
    CamelCaseToSpacePipe,
    CmsUploadComponent,
    CmsUploadDropdownComponent,
    SvgListComponent,
    HeaderActivityBadgeComponent,
    DownloadCvsComponent,
    BannersAutocompleteComponent,
    CmsSimpleSelectListComponent,
    ActionButtonsComponent,
    BreadcrumbsComponent,
    CmsAlertComponent,
    CreateUpdatedAtByComponent,
    ActiveInactiveExpiredComponent,
    VipLevelsInputComponent,
    NumberListInputComponent,
    NumberOnlyDirective,
    CustomerVariantsSelectComponent,
    SvgIconSelectInputComponent,
    DeleteDialogComponent,
    InlineMultiselectComponent,
    CmsSegmentDropdownComponent,
    TwoDigitDecimaNumberDirective,
    PreventWhiteSpacesDirective,
    CmsUniversalSegmentedComponent,
    CommonSvgInputSelectComponent
  ],
  entryComponents: [
    ConfirmDialogComponent,
    PromptDialogComponent,
    NotificationDialogComponent,
    DeleteDialogComponent
  ],
  exports: [
    CamelCaseToSpacePipe,
    ArrayNoNullPipe,
    ByteToKbPipe,
    CommonModule,
    FormsModule,
    ReactiveFormsModule,
    CdkTableModule,
    MatAutocompleteModule,
    MatButtonModule,
    MatButtonToggleModule,
    MatCardModule,
    MatCheckboxModule,
    MatChipsModule,
    MatStepperModule,
    MatDatepickerModule,
    MatDialogModule,
    MatExpansionModule,
    MatGridListModule,
    MatIconModule,
    MatInputModule,
    MatListModule,
    MatMenuModule,
    MatNativeDateModule,
    MatPaginatorModule,
    MatProgressBarModule,
    MatProgressSpinnerModule,
    MatRadioModule,
    MatRippleModule,
    MatSelectModule,
    MatSidenavModule,
    MatSliderModule,
    MatSlideToggleModule,
    MatSnackBarModule,
    MatSortModule,
    MatTableModule,
    MatTabsModule,
    MatToolbarModule,
    MatTooltipModule,
    TinymceComponent,
    DateAndTimeComponent,
    DateRangeComponent,
    TimeRangeComponent,
    CMSDataTableComponent,
    CMSSegmentDataTableComponent,
    CMSDataTablePaginationComponent,
    TimelineDataTableComponent,
    TimelineActionButtonsComponent,
    CmsUploadComponent,
    CmsUploadDropdownComponent,
    SvgListComponent,
    HeaderActivityBadgeComponent,
    DownloadCvsComponent,
    BannersAutocompleteComponent,
    CmsSimpleSelectListComponent,
    ActionButtonsComponent,
    BreadcrumbsComponent,
    CmsAlertComponent,
    InputTrimModule,
    CreateUpdatedAtByComponent,
    ActiveInactiveExpiredComponent,
    VipLevelsInputComponent,
    NumberListInputComponent,
    NumberOnlyDirective,
    CustomerVariantsSelectComponent,
    SvgIconSelectInputComponent,
    InlineMultiselectComponent,
    CmsSegmentDropdownComponent,
    TwoDigitDecimaNumberDirective,
    PreventWhiteSpacesDirective,
    CmsUniversalSegmentedComponent,
    CommonSvgInputSelectComponent
  ],
  providers: [
    DialogService,
    FracToDecService,
    ByteToKbPipe,
    SseService
  ]
})
export class SharedModule {
}
