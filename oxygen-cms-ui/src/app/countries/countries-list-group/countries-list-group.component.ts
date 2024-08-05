import { Component, OnInit, Input } from '@angular/core';
import { CountryCode } from '../../client/private/models/country.model';

@Component({
  selector: 'countries-list-group',
  templateUrl: './countries-list-group.component.html',
  styleUrls: ['./countries-list-group.component.scss']
})
export class CountriesListGroupComponent implements OnInit {
  @Input() countries: CountryCode[] = [];
  @Input() title: string;

  public searchField: string = '';

  constructor() { }

  ngOnInit() {
  }

  public get data(): CountryCode[] {
    if (this.searchField.length === 0) {
      return this.countries;
    }
    return this.countries.filter((country) => {
      return country.label.toLowerCase().indexOf(this.searchField.toLowerCase()) !== -1;
    });
  }

}
