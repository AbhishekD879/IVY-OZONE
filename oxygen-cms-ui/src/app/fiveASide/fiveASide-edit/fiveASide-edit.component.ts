import {Component, OnInit, ViewChild} from '@angular/core';
import {ActivatedRoute, Params, Router} from '@angular/router';
import {FormControl, FormGroup, Validators} from '@angular/forms';
import {HttpResponse} from '@angular/common/http';
import {DialogService} from '@app/shared/dialog/dialog.service';
import {GlobalLoaderService} from '@app/shared/globalLoader/loader.service';
import {Breadcrumb} from '@app/client/private/models/breadcrumb.model';
import {FiveASideFormation} from '@app/client/private/models/fiveASideFormation.model';
import {MARKETS} from '@app/core/constants/banach-markets.constant';
import {FORMATIONS} from '@app/core/constants/formation.constant';
import {FiveASideApiService} from '@app/fiveASide/services/fiveASide.api.service';

@Component({
  templateUrl: './fiveASide-edit.component.html',
  styleUrls: ['./fiveASide-edit.component.scss'],
  providers: [
    DialogService
  ]
})
export class FiveASideEditComponent implements OnInit {
  public marketTemplateNames: string[] = MARKETS.map((market) => market.title);  // array of free constant template names for dropdown markets list
  public formations: string[] = FORMATIONS.slice(); // array of free constant names for dropdown formations list
  public isLoading: boolean = false;
  public fiveASideFormation: FiveASideFormation;
  public form: FormGroup;
  public breadcrumbsData: Breadcrumb[];

  @ViewChild('actionButtons') actionButtons;

  constructor(
    private router: Router,
    private activatedRoute: ActivatedRoute,
    private apiClientService: FiveASideApiService,
    private dialogService: DialogService,
    private globalLoaderService: GlobalLoaderService,
  ) {
    this.isValidModel = this.isValidModel.bind(this);
  }

  ngOnInit(): void {
    this.form = new FormGroup({
      title: new FormControl('', [Validators.required]),
      actualFormation: new FormControl('', [Validators.required]),
      position1: new FormControl(''),
      stat1: new FormControl(null, [Validators.required]),
      position2: new FormControl(''),
      stat2: new FormControl(null, [Validators.required]),
      position3: new FormControl(''),
      stat3: new FormControl(null, [Validators.required]),
      position4: new FormControl(''),
      stat4: new FormControl(null, [Validators.required]),
      position5: new FormControl(''),
      stat5: new FormControl(null, [Validators.required])
    });
    this.loadInitData();
  }

  loadInitData(isLoading: boolean = true): void {
    this.globalLoaderService.showLoader();
    this.isLoading = isLoading;

    this.activatedRoute.params.subscribe((params: Params) => {
      this.apiClientService
        .getSingleFormation(params['id'])
        .map((formation: HttpResponse<FiveASideFormation>) => {
          return formation.body;
        }).subscribe((formation: FiveASideFormation) => {
          this.fiveASideFormation = formation as FiveASideFormation;
          this.setBreadcrumbsData();
          this.globalLoaderService.hideLoader();
          this.isLoading = false;
        }, () => {
          this.globalLoaderService.hideLoader();
          this.isLoading = false;
        });
    });
  }

  private setBreadcrumbsData(): void {
    this.breadcrumbsData = [];
    this.breadcrumbsData.push({
      label: `5 A Side`,
      url: `/byb/5aSide`
    });
    this.breadcrumbsData.push({
      label: this.fiveASideFormation.title,
      url: `/byb/5aSide/${this.fiveASideFormation.id}`
    });
  }

  save(): void {
    this.globalLoaderService.showLoader();
    this.fiveASideFormation.stat1 = this.findStat(this.fiveASideFormation.stat1.title);
    this.fiveASideFormation.stat2 = this.findStat(this.fiveASideFormation.stat2.title);
    this.fiveASideFormation.stat3 = this.findStat(this.fiveASideFormation.stat3.title);
    this.fiveASideFormation.stat4 = this.findStat(this.fiveASideFormation.stat4.title);
    this.fiveASideFormation.stat5 = this.findStat(this.fiveASideFormation.stat5.title);
    this.apiClientService.putFormationChanges(this.fiveASideFormation)
      .map((data: HttpResponse<FiveASideFormation>) => {
        return data.body;
      })
      .subscribe((data: FiveASideFormation) => {
        this.fiveASideFormation = data;
        this.actionButtons.extendCollection(this.fiveASideFormation);
        this.dialogService.showNotificationDialog({
          title: '5 A Side Formation',
          message: '5 A Side Formation is Saved.'
        });
        this.globalLoaderService.hideLoader();
      }, error => {
        console.error(error.message);
        this.globalLoaderService.hideLoader();
      });
  }

  revert(): void {
    this.loadInitData();
  }

  remove(): void {
    this.globalLoaderService.showLoader();
    this.apiClientService.deleteFormation(this.fiveASideFormation.id)
      .subscribe(() => {
        this.globalLoaderService.hideLoader();
        this.router.navigate(['/byb/5aSide/']);
      }, error => {
        console.error(error.message);
        this.globalLoaderService.hideLoader();
      });
  }

  public actionsHandler(event): void {
    switch (event) {
      case 'remove':
        this.remove();
        break;
      case 'save':
        this.save();
        break;
      case 'revert':
        this.revert();
        break;
      default:
        console.error('Unhandled Action');
        break;
    }
  }

  isValidModel(fiveASideFormation: FiveASideFormation): boolean {
    return fiveASideFormation && fiveASideFormation.title !== '';
  }

  findStat(statname) {
    return MARKETS.find((market) => market.title === statname);
  }
}
