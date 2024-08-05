import { TestBed } from '@angular/core/testing';

import { MybadgesApiService } from './mybadges.api.service';

describe('Mybadges.ApiService', () => {
  let service: MybadgesApiService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(MybadgesApiService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
