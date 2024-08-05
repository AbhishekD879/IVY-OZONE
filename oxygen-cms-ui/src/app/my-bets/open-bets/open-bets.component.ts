import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder, FormArray } from '@angular/forms';
import { BrandService } from '@root/app/client/private/services/brand.service';
import { GlobalLoaderService } from '../../shared/globalLoader/loader.service';
import { ApiClientService } from '@root/app/client/private/services/http';

@Component({
  selector: 'app-open-bets',
  templateUrl: './open-bets.component.html',
  styleUrls: ['./open-bets.component.scss']
})
export class OpenBetsComponent implements OnInit {
  modulesAmount: any;
  myBets: FormGroup;
  hideAction: boolean = true;

  constructor(
    private fb: FormBuilder,
    private brandService: BrandService,
    private globalLoaderService: GlobalLoaderService,
    private apiClientService: ApiClientService,

  ) {
    this.createForm()
  }

  ngOnInit(): void {
    this.loadInItData();
  }
  loadInItData() {
    this.globalLoaderService.showLoader();
    this.hideAction = false;
    this.apiClientService.MyBetsService().getmyBetsData(this.brandService.brand, 'open-bets').map(res => res.body).subscribe((res) => {
      this.hideAction = true;
      this.patchData(res);
      this.globalLoaderService.hideLoader();
    }, () => {
      this.hideAction = true;
      this.globalLoaderService.hideLoader();
    }
    )
  }
  addTimingImg() {
    const arr = this.myBets.get('brandedImageList') as FormArray;
    arr.push(this.createImgTimeForm());
  }
  createImgTimeForm() {
    return this.fb.group({
      imgLink: [''],
      fromDate: [''],
      toDate: ['']
    })
  }
  patchData(data) {
    if (data.brandedImageList?.length) {
      this.myBets.addControl('brandedImageList', this.fb.array([]))
      this.myBets.patchValue(data)
    }
    else {
      this.myBets.patchValue(data)
    }
    this.myBets.patchValue({brand:this.brandService.brand})
    this.myBets.patchValue({type:'open-bets'})


  }
  createForm() {
    this.myBets = this.fb.group({
      addDescText: [''],
      type: ['open-bets'],
      defaultImgLink: [''],
      noBetText: [''],
      id: [''],
      createdBy: [''],
      updatedBy: [''],
      updatedAt: [''],
      brand: [this.brandService.brand],
      createdAt: [''],
      updatedByUserName: [''],
      createdByUserName: [''],
    })
  }
  get myBetsControl() {
    return this.myBets.controls;
  }
  get myBetsValue() {
    return this.myBets.value;
  }
  actionsHandler(type: string) {
    switch (type) {
      case 'revert':
        this.loadInItData();
        break;
      case 'save':
        this.saveMyBets();
        break;
    }
  }
  saveMyBets() {
    this.globalLoaderService.showLoader();
    this.hideAction = false;
    const payload = this.myBets.value;
    if (payload.id) {
      this.apiClientService.MyBetsService().putmyBetsData(this.brandService.brand, payload.id, payload, 'open-bets').map(res => res.body).subscribe((res) => {
        this.patchData(res);
        console.log(this.myBets.value)
        this.hideAction = true;
        this.globalLoaderService.hideLoader();
      }, () => {
        this.hideAction = true;
        this.globalLoaderService.hideLoader();
      }
      );
    }
    else {
      this.apiClientService.MyBetsService().postmyBetsData(this.brandService.brand, payload, 'open-bets').subscribe((res) => {
        this.patchData(res);
        this.hideAction = true;
        console.log(this.myBets.value)
        this.globalLoaderService.hideLoader();
      }, () => {
        this.hideAction = true;
        this.globalLoaderService.hideLoader();
      }
      );
    }
  }

}
