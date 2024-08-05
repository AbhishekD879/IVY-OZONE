import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { FormControl } from '@angular/forms';
import { Observable } from 'rxjs/Observable';
import { startWith } from 'rxjs/operators/startWith';
import { map } from 'rxjs/operators/map';
import { ApiClientService } from '../../client/private/services/http/index';
import { HttpResponse } from '@angular/common/http';

@Component({
  selector: 'banners-autocomplete',
  templateUrl: './banners-autocomplete.component.html',
  styleUrls: ['./banners-autocomplete.component.scss']
})
export class BannersAutocompleteComponent implements OnInit {

  @Input() type: string = 'mobile';

  @Input() selected: string = '';

  @Input() setSelected: boolean = true;

  @Output() onBannerSelected = new EventEmitter();

  public banners: any[] = [];
  public selectedBanner: any = {};
  public myControl: FormControl = new FormControl();
  public filteredOptions: Observable<any>;

  constructor(
    public apiClientService: ApiClientService
  ) {
  }

  loadAllOptions() {
    this.filteredOptions = new Observable(observer => {
      observer.next(this.banners);
      observer.complete();
    });
  }

  ngOnInit() {
    this.apiClientService[`betReceipt${this.type}Banner`]()
        .findAllByBrand().map((response: HttpResponse<any[]>) => {
          return response.body;
        }).subscribe((banners: any[]) => {
          this.banners = banners;
          this.selectedBanner = this.banners.find((banner) => banner.id === this.selected); // TODO: Refactor after backend fix

          if (this.setSelected) {
            this.myControl.setValue(this.selectedBanner);
          }

          this.filteredOptions = this.myControl.valueChanges
              .pipe(
                startWith(''),
                map((value: any) => typeof value === 'string' ? value : value.name),
                map(name => name ? this.filter(name) : this.banners.slice())
          );

          this.myControl.valueChanges.subscribe((value) => {
            if (value.name) {
              this.onBannerSelected.emit(value.id);
              this.loadAllOptions();
            }
          });
        });
  }

  filter(name: string): any[] {
    return this.banners.filter(option =>
      option.name.toLowerCase().indexOf(name.toLowerCase()) === 0);
  }

  displayFn(user?: any): string | undefined {
    return user ? user.name : undefined;
  }

}
