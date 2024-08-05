package com.entain.oxygen.util;

import com.entain.oxygen.entity.HorseInfo;
import com.entain.oxygen.exceptions.InvalidHorseIdException;
import com.entain.oxygen.exceptions.PreferenceDtoException;
import com.entain.oxygen.exceptions.ValidationsException;
import com.entain.oxygen.model.PreferenceDto;
import com.entain.oxygen.model.UserStableDto;
import java.util.Arrays;
import java.util.List;
import java.util.regex.Pattern;
import java.util.stream.Collectors;
import lombok.experimental.UtilityClass;
import org.owasp.html.HtmlPolicyBuilder;
import org.owasp.html.PolicyFactory;
import org.springframework.http.HttpStatus;
import org.springframework.util.StringUtils;
import reactor.core.publisher.Mono;

@UtilityClass
public class Validations {

  private static final List<String> BRAND;
  private static final List<String> ODDS;
  private static final int NOTE_LENGTH = 180;
  public static final String INVALID_HORSE_MESSAGE = "Invalid horse id";
  public static final String INVALID_BRAND_MESSAGE = "Invalid brand";
  private static final Pattern HORSE_ID_PATTERN = Pattern.compile("^\\d+$");

  static {
    BRAND = Arrays.stream(Brand.values()).map(Brand::value).collect(Collectors.toList());
    ODDS = Arrays.stream(Preference.values()).map(Preference::value).collect(Collectors.toList());
  }

  public static void validateBrandAndOdds(PreferenceDto dto) throws PreferenceDtoException {
    validateBrand(dto.getBrand());
    validateOdds(dto.getOddPreference());
  }

  public static void validateBrand(String brand) throws PreferenceDtoException {
    String errMsg = "brand is invalid., refer valid brands->";
    if (!(StringUtils.hasLength(brand) && BRAND.contains(brand))) {
      throw new PreferenceDtoException(errMsg + BRAND);
    }
  }

  public static void validateOdds(String oddsPreference) throws PreferenceDtoException {
    String errMsg = "odds preference is invalid., refer valid preferences->";
    if (!(StringUtils.hasLength(oddsPreference) && (ODDS.contains(oddsPreference)))) {
      throw new PreferenceDtoException(errMsg + ODDS);
    }
  }

  public Mono<String> validateHorseId(String horseId) {
    if (!isHorseIdValid(horseId))
      return Mono.error(
          new ValidationsException(INVALID_HORSE_MESSAGE, HttpStatus.BAD_REQUEST.value()));

    return Mono.just(horseId);
  }

  public boolean isHorseIdValid(String horseId) {
    return HORSE_ID_PATTERN.matcher(horseId).matches();
  }

  public Mono<UserStableDto> validateAndSanitize(UserStableDto dto) {

    checkIfValidHorseIdAndBrand(dto);

    PolicyFactory policy = new HtmlPolicyBuilder().toFactory();

    try {
      dto.getMyStable().stream()
          .forEach(
              (HorseInfo horseInfo) -> {
                if (horseInfo.getNote().length() <= NOTE_LENGTH) {
                  horseInfo.setNote(policy.sanitize(horseInfo.getNote()));
                } else {
                  throw new InvalidHorseIdException(
                      "Notes length can't be greater than " + NOTE_LENGTH + " chars");
                }
              });
    } catch (RuntimeException ex) {
      return Mono.error(new ValidationsException(ex.getMessage(), HttpStatus.BAD_REQUEST.value()));
    }

    return Mono.just(dto);
  }

  public static Mono<UserStableDto> checkIfValidHorseIdAndBrand(UserStableDto dto) {
    try {
      validateBrand(dto.getBrand());
      dto.getMyStable().stream()
          .forEach(
              (HorseInfo horseInfo) -> {
                if (!isHorseIdValid(horseInfo.getHorseId()))
                  throw new InvalidHorseIdException("Invalid horseId");
              });
    } catch (InvalidHorseIdException ex) {
      return Mono.error(
          new ValidationsException(INVALID_HORSE_MESSAGE, HttpStatus.BAD_REQUEST.value()));
    } catch (PreferenceDtoException e) {
      return Mono.error(
          new ValidationsException(INVALID_BRAND_MESSAGE, HttpStatus.BAD_REQUEST.value()));
    }
    return Mono.just(dto);
  }
}
