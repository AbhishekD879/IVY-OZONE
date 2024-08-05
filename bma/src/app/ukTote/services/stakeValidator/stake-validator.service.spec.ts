import { StakeValidatorService } from '@uktote/services/stakeValidator/stake-validator.service';

describe('StakeValidatorService', () => {
  let stakeValidatorService: StakeValidatorService;

  let options;
  let expectedResult;

  beforeEach(() => {
    options = {
      stake: 11,
      totalStake: 10,
      pool: {
        minStakePerLine: 3,
        maxStakePerLine: 3,
        stakeIncrementFactor: 3,
        minTotalStake: 3,
        maxTotalStake: 3
      }
    };
    expectedResult = {
      maxStakePerLine: true,
      maxTotalStake: true,
      minStakePerLine: false,
      minTotalStake: false,
      stakeIncrementFactor: true
    };
    stakeValidatorService = new StakeValidatorService();
  });

  it('Tests if StakeValidatorService Service Created', () => {
    expect(stakeValidatorService).toBeTruthy();
  });

  it('#getValidationState', () => {
    const actualResult = stakeValidatorService.getValidationState(options);

    expect(actualResult).toEqual(expectedResult);
  });

  it('#getValidationState when min value is valid', () => {
    options.pool.minTotalStake = 11;
    const actualResult = stakeValidatorService.getValidationState(options);

    expect(actualResult.minTotalStake).toEqual(true);
  });

  it('#getValidationState when maxTotalStake value is valid', () => {
    options.totalStake = 10;
    options.pool.maxTotalStake = 9;
    const actualResult = stakeValidatorService.getValidationState(options);

    expect(actualResult.maxTotalStake).toEqual(true);
  });

  it('#getValidationState when maxTotalStake value is not valid', () => {
    options.totalStake = 9;
    options.pool.maxTotalStake = 10;
    const actualResult = stakeValidatorService.getValidationState(options);

    expect(actualResult.maxTotalStake).toEqual(false);
  });

  it('#getValidationState when minStakePerLine value is valid', () => {
    options.stake = 9;
    options.pool.minStakePerLine = 10;
    const actualResult = stakeValidatorService.getValidationState(options);

    expect(actualResult.minStakePerLine).toEqual(true);
  });

  it('#getValidationState when minStakePerLine value is not valid', () => {
    options.stake = 10;
    options.pool.minStakePerLine = 9;
    const actualResult = stakeValidatorService.getValidationState(options);

    expect(actualResult.minStakePerLine).toEqual(false);
  });

  it('#getValidationState when maxStakePerLine value is valid', () => {
    options.stake = 10;
    options.pool.maxStakePerLine = 9;
    const actualResult = stakeValidatorService.getValidationState(options);

    expect(actualResult.maxStakePerLine).toEqual(true);
  });

  it('#getValidationState when maxStakePerLine value is not valid', () => {
    options.stake = 9;
    options.pool.maxStakePerLine = 10;
    const actualResult = stakeValidatorService.getValidationState(options);

    expect(actualResult.maxStakePerLine).toEqual(false);
  });

  it('#getValidationState when stakeIncrementFactor value is valid', () => {
    options.stake = 9;
    options.pool.stakeIncrementFactor = 10;
    const actualResult = stakeValidatorService.getValidationState(options);

    expect(actualResult.stakeIncrementFactor).toEqual(true);
  });

  it('#getValidationState when stakeIncrementFactor value is not valid', () => {
    options.stake = null;
    const actualResult = stakeValidatorService.getValidationState(options);

    expect(actualResult.stakeIncrementFactor).toEqual(false);
  });

  it('#getValidationState when minTotalStake value is valid', () => {
    options.totalStake = 9;
    options.pool.minTotalStake = 10;
    const actualResult = stakeValidatorService.getValidationState(options);

    expect(actualResult.minTotalStake).toEqual(true);
  });

  it('#getValidationState when minTotalStake value is not valid', () => {
    options.totalStake = 10;
    options.pool.minTotalStake = 9;
    const actualResult = stakeValidatorService.getValidationState(options);

    expect(actualResult.minTotalStake).toEqual(false);
  });

  it('#isIncrementValid not a number was passed', () => {
    const value = undefined;
    const factor = 10;
    const result = stakeValidatorService['isIncrementValid'](value, factor);
    expect(result).toBeFalsy();
  });
});
