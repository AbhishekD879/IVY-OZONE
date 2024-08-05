import { TestBed } from '@angular/core/testing';

import { SeasonsApiService } from './seasons.api.service';

describe('Seasons.ApiService', () => {
  let service: SeasonsApiService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(SeasonsApiService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
