import { TestBed } from '@angular/core/testing';

import { MyBetsService } from './my-bets.service';

describe('MyBetsService', () => {
  let service: MyBetsService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(MyBetsService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
