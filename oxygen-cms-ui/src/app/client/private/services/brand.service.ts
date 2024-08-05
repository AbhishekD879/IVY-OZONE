import { Injectable } from '@angular/core';
import { Brand } from '../models/brand.model';

@Injectable()
export class BrandService {
  private DEFAULT_BRAND: string = 'bma';
  private _brand: string;
  private brands: Brand[];

  constructor() {
    this._brand = localStorage.getItem('brand') || this.DEFAULT_BRAND;
  }

  public get defaultBrand() {
    return this.DEFAULT_BRAND;
  }

  public get brand() {
    return this._brand ? this._brand : this.defaultBrand;
  }

  public set brand(brand: string) {
    localStorage.setItem('brand', brand);
    window.location.reload();
  }

  public get brandsList(): Brand[] {
    return this.brands;
  }

  public set brandsList(b: Brand[]) {
    this.brands = b;
  }

  /**
   * Check if ImageManager ON for brand
   * TODO: Remove after full migration both brands (coral/ladbrokes) to Image Manager
  */
  isIMActive(): boolean {
    const config = {
      bma: true,
      ladbrokes: true
    };

    return !!config[this.brand.toLowerCase()];
  }
}
