import { ChangeDetectorRef, Component, OnInit, ViewChild } from "@angular/core";
import {
  AbstractControl,
  FormControl,
  FormGroup,
  ValidationErrors,
  ValidatorFn,
  Validators,
} from "@angular/forms";
import { ActivatedRoute, Router, Params } from "@angular/router";
import { HttpResponse } from "@angular/common/http";
import { MatSelect } from "@angular/material/select";
import { MatOption } from "@angular/material/core";
import * as _ from "lodash";
import { SportsNextEventCarousel } from "@app/client/private/models/sportsNextEventCarousel.model";
import { Breadcrumb } from "@app/client/private/models/breadcrumb.model";
import { SportsModulesBreadcrumbsService } from "@app/sports-modules/sports-modules-breadcrumbs.service";
import { ApiClientService } from "@app/client/private/services/http";
import { BrandService } from "@app/client/private/services/brand.service";
import { GlobalLoaderService } from "@app/shared/globalLoader/loader.service";
import { SportsModule } from "@app/client/private/models/homepage.model";
import { SportCategory } from "@app/client/private/models/sportcategory.model";
import { SportsModulesService } from "@app/sports-modules/sports-modules.service";
import { DialogService } from "@app/shared/dialog/dialog.service";
import { MatSnackBar } from "@angular/material/snack-bar";
import { AppConstants } from "@root/app/app.constants";
@Component({
  selector: "app-next-event-carousel-form",
  templateUrl: "./next-event-carousel-form.component.html",
  styleUrls: ["./next-event-carousel-form.component.scss"],
})
export class NextEventCarouselFormComponent implements OnInit {
  @ViewChild("actionButtons") actionButtons;
  @ViewChild("select") select: MatSelect;
  public nextEventCarousel: SportsNextEventCarousel = {
    id: null,
    title: null,
    classIds: "",
    typeIds: [],
    limit: null,
    buttonText: "",
    redirectionUrl: "",
    mobileImageId: "",
    desktopImageId: "",
    disabled: true,
    brand: this.brandService.brand,
    sortOrder: null,
    sportId: 0,
    pageId: null,
    pageType: null,
    createdBy: null,
    createdAt: null,
    updatedBy: null,
    updatedAt: null,
    updatedByUserName: null,
    createdByUserName: null,
    universalSegment: true,
  };

  public breadcrumbsData: Breadcrumb[];
  public form: FormGroup;
  public nextEventId: string;
  public sportConfigId: string;
  public routeParams: Params;
  public moduleId: string;
  public module: SportsModule;
  public pageTitle: string = "Next Event Carousel";
  public isRevert = false;
  typeIdsData = [];
  public allSelected = false;
  public nextEventCarouselList: SportsNextEventCarousel[] = [];
  constructor(
    private activatedRoute: ActivatedRoute,
    private router: Router,
    private sportsModulesBreadcrumbsService: SportsModulesBreadcrumbsService,
    private apiClientService: ApiClientService,
    private globalLoaderService: GlobalLoaderService,
    private brandService: BrandService,
    private sportsModulesService: SportsModulesService,
    private dialogService: DialogService,
    private snackBar: MatSnackBar,
    private changeDetect: ChangeDetectorRef
  ) {
    this.validationHandler = this.validationHandler.bind(this);
  }

  public ngOnInit(): void {
    this.activatedRoute.params.subscribe((params: Params) => {
      this.routeParams = params;
      this.sportConfigId = params["id"];
      this.nextEventId = params["nextEventId"];
      this.moduleId = params["moduleId"];
      this.pageTitle = this.nextEventId
        ? "Next Event Carousel: "
        : "New Next Event Carousel: ";
      this.loadInitialData(params);
    });
  }

  private setupForm(): void {
    this.form = new FormGroup({
      title: new FormControl(this.nextEventCarousel.title, [
        Validators.required,
        this.titleUniqueValidator(),
      ]),
      classIds: new FormControl(this.nextEventCarousel.classIds, [
        Validators.required,
        Validators.pattern(/^\d+(,\d+)*$/),
      ]),
      typeIds: new FormControl(this.nextEventCarousel.typeIds, [
        Validators.required,
      ]),
      disabled: new FormControl(this.nextEventCarousel.disabled, []),
      limit: new FormControl(this.nextEventCarousel.limit, [
        Validators.pattern(/^(\d*)$/),
        Validators.min(1),
      ]),
      buttonText: new FormControl(this.nextEventCarousel.buttonText, [
        Validators.required,
      ]),
      redirectionUrl: new FormControl(this.nextEventCarousel.redirectionUrl, [
        Validators.required,
      ]),
      mobileImageId: new FormControl(this.nextEventCarousel.mobileImageId, [
        Validators.required,
      ]),
      desktopImageId: new FormControl(this.nextEventCarousel.desktopImageId, [
        Validators.required,
      ]),
    });
  }
  get formControls() {
    return this.form?.controls;
  }
  setFormValuesToObject() {
    this.nextEventCarousel.title = this.form.get("title").value;
    this.nextEventCarousel.classIds = this.form.get("classIds").value;
    this.nextEventCarousel.typeIds = this.form.get("typeIds").value;
    this.nextEventCarousel.disabled = this.form.get("disabled").value;
    this.nextEventCarousel.limit = this.form.get("limit").value;
    this.nextEventCarousel.buttonText = this.form.get("buttonText").value;
    this.nextEventCarousel.redirectionUrl = this.form.get("redirectionUrl").value;
    this.nextEventCarousel.mobileImageId = this.form.get("mobileImageId").value;
    this.nextEventCarousel.desktopImageId =
      this.form.get("desktopImageId").value;
  }

  public save(): void {
    if (!this.form.valid) {
      return;
    }

    if (this.nextEventId) {
      this.updateRequest();
    } else {
      this.createRequest();
    }
  }

  private loadInitialData(params: Params): void {
    this.form = null;
    this.globalLoaderService.showLoader();
    if (this.nextEventId) {
      // edit
      this.apiClientService
        .sportsNextEventCarousel()
        .findById(this.nextEventId)
        .map((response: HttpResponse<SportsNextEventCarousel>) => response.body)
        .subscribe(
          (nextEventCarousel: any) => {
            this.nextEventCarousel = nextEventCarousel;
            this.nextEventCarousel.typeIds = nextEventCarousel.typeIds
              ?.split(",")
              .map(function (item) {
                return parseInt(item);
              });
            // this.loadCarousels();
            this.setupForm();
            this.loadTypeIds();
            this.getBreadcrumbs(params);
            this.globalLoaderService.hideLoader();
          },
          (err) => {
            this.globalLoaderService.hideLoader();
          }
        );
    } else {
      // create; module data is needed to set carousel sportId
      this.sportsModulesService
        .getSingleModuleData(this.moduleId, this.sportConfigId)
        .subscribe(
          (moduleData: [SportsModule, SportCategory]) => {
            this.module = moduleData[0];
            this.nextEventCarousel.sportId = this.module.sportId;
            this.getBreadcrumbs(params);
            // this.loadCarousels();
            this.setupForm();
            this.globalLoaderService.hideLoader();
          },
          (err) => {
            this.globalLoaderService.hideLoader();
          }
        );
    }
  }

  loadCarousels() {
    this.apiClientService
      .sportsNextEventCarousel()
      .findAllByBrand(this.brandService.brand)
      .map((response: HttpResponse<SportsNextEventCarousel[]>) => response.body)
      .subscribe((carousels: SportsNextEventCarousel[]) => {
        this.nextEventCarouselList = carousels;
        this.form.controls['title'].updateValueAndValidity();
      });
  }

  private createRequest(): void {
    if (!this.form.valid) {
      return;
    }
    this.globalLoaderService.showLoader();
    this.nextEventCarousel.pageId = this.module.pageId;
    this.nextEventCarousel.pageType = "sport";
    this.setFormValuesToObject();
    let nextEventFormData: any = { ...this.nextEventCarousel };
    nextEventFormData.typeIds = nextEventFormData.typeIds.toString();
    this.apiClientService
      .sportsNextEventCarousel()
      .save(nextEventFormData)
      .map((response: HttpResponse<SportsNextEventCarousel>) => response.body)
      .subscribe(
        (carousel: SportsNextEventCarousel) => {
          this.globalLoaderService.hideLoader();
          this.changeDetect.detectChanges();
          this.snackBar.open(`Record has been saved`, "Ok!", {
            duration: AppConstants.HIDE_DURATION,
          });
          this.router.navigate([this.getUrlToGoEdit(carousel.id)]);
        },
        (error) => {
          this.globalLoaderService.hideLoader();
        }
      );
  }

  private updateRequest(): void {
    if (!this.form.valid) {
      return;
    }
    this.globalLoaderService.showLoader();
    this.setFormValuesToObject();
    let nextEventFormData: any = { ...this.nextEventCarousel };
    nextEventFormData.typeIds = nextEventFormData.typeIds.toString();
    this.apiClientService
      .sportsNextEventCarousel()
      .update(nextEventFormData)
      .map((response: HttpResponse<SportsNextEventCarousel>) => response.body)
      .subscribe(
        (carousel: any) => {
          this.nextEventCarousel = carousel;
          this.nextEventCarousel.typeIds = carousel.typeIds.split(",")
          .map(function (item) {
            return parseInt(item);
          });
          this.updateForm();
          // this.loadCarousels();
          this.actionButtons.extendCollection(this.nextEventCarousel);
          this.globalLoaderService.hideLoader();
          this.changeDetect.detectChanges();
          this.snackBar.open(`Record has been updated.`, "Ok!", {
            duration: AppConstants.HIDE_DURATION,
          });
        },
        (error) => {
          this.globalLoaderService.hideLoader();
        }
      );
  }

  updateForm() {
    this.form.patchValue(this.nextEventCarousel);
  }
  private remove(): void {
    this.globalLoaderService.showLoader();
    this.apiClientService
      .sportsNextEventCarousel()
      .delete(this.nextEventCarousel.id)
      .subscribe(
        (response) => {
          this.globalLoaderService.hideLoader();
          this.changeDetect.detectChanges();
          this.snackBar.open(`Record has been deleted`, "Ok!", {
            duration: AppConstants.HIDE_DURATION,
          });
          this.router.navigate([this.getUrlToGoBack]);
        },
        (error) => {
          this.globalLoaderService.hideLoader();
        }
      );
  }

  private revert(): void {
    this.loadInitialData(this.routeParams);
    this.isRevert = true;
  }

  loadTypeIds() {
    this.nextEventCarousel.classIds = this.form.get("classIds").value.trim();
    if (!this.nextEventCarousel.classIds || !this.form.get("classIds").valid) {
      this.typeIdsData = [];
      this.nextEventCarousel.typeIds = [];
      return;
    } else {
      let classIds = this.form.get("classIds").value.trim();
      classIds = classIds.split(",");
      classIds = classIds && classIds.length > 0 && _.uniq(classIds);
      this.form.controls.classIds.setValue(classIds.join(","));
      this.nextEventCarousel.classIds = classIds.join(",");
    }
    this.globalLoaderService.showLoader();
    this.apiClientService
      .sportsNextEventCarousel()
      .getTypeIds(this.nextEventCarousel.classIds)
      .map((response: HttpResponse<SportsNextEventCarousel[]>) => response.body)
      .subscribe((typeIdsData: any[]) => {
        this.typeIdsData = _.uniqWith(typeIdsData, (a, b) => {
          return _.isEqual(a, b);
        });
        const intersectList = _.intersection(
          _.map(this.typeIdsData, "typeId"),
          this.nextEventCarousel.typeIds
        );
        this.nextEventCarousel.typeIds = intersectList;
        this.allSelected = this.typeIdsData.length === intersectList.length;
        this.globalLoaderService.hideLoader();
        this.changeDetect.detectChanges();
        if (this.typeIdsData.length === 0) {
          this.dialogService.showNotificationDialog({
            title: "Next Event Carousel",
            message: "No matching Type ID's for this class ID's",
          });
        }
      });
  }
  public validationHandler(): boolean {
    this.setFormValuesToObject();
    return this.form.valid;
  }

  public toggleActiveStatus(): void {
    this.nextEventCarousel.disabled = !this.nextEventCarousel.disabled;
    this.form.controls.disabled.setValue(this.nextEventCarousel.disabled);
  }

  public actionsHandler(event): void {
    switch (event) {
      case "remove":
        this.remove();
        break;
      case "save":
        this.save();
        break;
      case "revert":
        this.revert();
        break;
      default:
        console.error("Unhandled Action");
        break;
    }
  }
  private getBreadcrumbs(params: Params): void {
    const title: string = this.nextEventId
      ? this.nextEventCarousel.title
      : "Create";

    this.sportsModulesBreadcrumbsService
      .getBreadcrubs(params, {
        customBreadcrumbs: [
          {
            label: title,
          },
        ],
      })
      .subscribe((breadcrumbsData: Breadcrumb[]) => {
        this.breadcrumbsData = breadcrumbsData;
      });
  }

  private get getUrlToGoBack(): string {
    if (this.sportConfigId) {
      return `sports-pages/sport-categories/${this.sportConfigId}/sports-module/next-event-carousel/${this.moduleId}`;
    }
  }
  private getUrlToGoEdit(carouselId: string): string {
    if (this.sportConfigId) {
      return `sports-pages/sport-categories/${this.sportConfigId}/sports-module/next-event-carousel/${this.moduleId}
      /carousel/edit/${carouselId}`;
    }
  }

  toggleAllSelection(): void {
    if (this.allSelected) {
      this.select.options.forEach((item: MatOption) => item.select());
    } else {
      this.select.options.forEach((item: MatOption) => item.deselect());
    }
  }
  optionClick(): void {
    this.allSelected = !this.select.options.some(
      (option) => option.selected === false
    );
  }

  titleUniqueValidator(): ValidatorFn {
    return (control: AbstractControl): ValidationErrors | null => {
      const val = control.value;
      let matchedData = [];
      matchedData = this.nextEventCarouselList.filter(
        (data) =>
          val &&
          data.title.toLowerCase() === val.toLowerCase() &&
          data.id !== this.nextEventId
      );
      return matchedData.length > 0 ? { notUnique: true } : null;
    };
  }
}
