package com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.placebet;

import com.coral.oxygen.middleware.ms.quickbet.Messages;
import com.entain.oxygen.bettingapi.model.bet.api.response.Bet;
import com.entain.oxygen.bettingapi.model.bet.api.response.BetError;
import com.entain.oxygen.bettingapi.model.bet.api.response.BetsResponse;
import com.entain.oxygen.bettingapi.model.bet.api.response.ErrorBody;
import java.util.ArrayList;
import java.util.List;
import java.util.Objects;
import java.util.Optional;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.NoArgsConstructor;

/** Created by azayats on 31.10.17. */
public class RegularPlaceBetResponse {
  private static final String UNAUTH_ACCESS_MESSAGE = "Token expired or user does not exist";
  private Data data;

  public RegularPlaceBetResponse() {}

  public RegularPlaceBetResponse(Data data) {
    this.data = data;
  }

  public Data getData() {
    return data;
  }

  public void setData(Data data) {
    this.data = data;
  }

  public static RegularPlaceBetResponse errorResponse(BetsResponse body) {
    BetError betError = body.getBetError().get(0);
    Optional<PriceDto> priceDto =
        Optional.ofNullable(betError.getPrice())
            .filter(ps -> !ps.isEmpty()) //
            .map(ps -> ps.get(0)) //
            .map(p -> new PriceDto(p.getPriceNum(), p.getPriceDen(), p.getPriceTypeRef().getId()));
    Bet bet = body.getBet().get(0);
    Optional<StakeDto> stakeDto =
        Optional.ofNullable(bet.getStake()) //
            .filter(
                stake ->
                    Objects.nonNull(stake.getMaxAllowed())
                        || Objects.nonNull(stake.getMinAllowed())) //
            .map(
                stake ->
                    new StakeDto() //
                        .withMaxAllowed(stake.getMaxAllowed()) //
                        .withMinAllowed(stake.getMinAllowed()));
    return errorResponse(
        betError.getCode(),
        betError.getErrorDesc(),
        betError.getSubErrorCode(),
        betError.getHandicap(),
        priceDto.orElse(null),
        stakeDto.orElse(null));
  }

  public static RegularPlaceBetResponse errorResponse(String code, String description) {
    return RegularPlaceBetResponse.errorResponse(code, description, null, null, null, null);
  }

  public static RegularPlaceBetResponse errorResponse(
      String code, String description, String subErrorCode) {
    return RegularPlaceBetResponse.errorResponse(code, description, subErrorCode, null, null, null);
  }

  public static RegularPlaceBetResponse errorResponse(
      String code,
      String description,
      String subErrorCode,
      Double handicap,
      PriceDto price,
      StakeDto stake) {
    RegularPlaceBetResponse.Error error = new RegularPlaceBetResponse.Error();
    error.setCode(code);
    error.setDescription(description);
    error.setSubErrorCode(subErrorCode);
    error.setHandicap(handicap);
    error.setPrice(price);
    error.setStake(stake);
    Data data = new Data();
    data.setError(error);
    return new RegularPlaceBetResponse(data);
  }

  public static RegularPlaceBetResponse errorResponse(RegularPlaceBetResponse.Error error) {
    Data data = new Data();
    data.setError(error);
    return new RegularPlaceBetResponse(data);
  }

  public static RegularPlaceBetResponse errorResponse(ErrorBody errorBody) {
    return RegularPlaceBetResponse.errorResponse(errorBody.getStatus(), errorBody.getError());
  }

  public static RegularPlaceBetResponse unauthorizedAccessError() {
    return RegularPlaceBetResponse.errorResponse(
        Messages.UNAUTHORIZED_ACCESS.code(), UNAUTH_ACCESS_MESSAGE);
  }

  public static RegularPlaceBetResponse priceChangeError(
      Integer priceNum, Integer priceDen, String message) {
    return RegularPlaceBetResponse.errorResponse(
        "CHANGE_ERROR",
        message,
        "PRICE_CHANGED",
        null,
        new PriceDto(String.valueOf(priceNum), String.valueOf(priceDen), "BANACH"),
        null);
  }

  public static class Data {
    private List<ReceiptResponseDto> receipt;
    private Error error;

    public List<ReceiptResponseDto> getReceipt() {
      if (receipt == null) {
        receipt = new ArrayList<>();
      }
      return receipt;
    }

    public void setReceipt(List<ReceiptResponseDto> receipt) {
      this.receipt = receipt;
    }

    public Error getError() {
      return error;
    }

    public void setError(Error error) {
      this.error = error;
    }

    @Override
    public boolean equals(Object o) {
      if (this == o) return true;
      if (o == null || getClass() != o.getClass()) return false;
      Data data = (Data) o;
      return Objects.equals(receipt, data.receipt) && Objects.equals(error, data.error);
    }

    @Override
    public int hashCode() {
      return Objects.hash(receipt, error);
    }

    @Override
    public String toString() {
      return "Data{" + "receipt=" + receipt + ", error=" + error + '}';
    }
  }

  @lombok.Data
  @Builder
  @NoArgsConstructor
  @AllArgsConstructor
  public static class Error {
    private String code;
    private String description;
    private String subErrorCode;
    private Double handicap;
    private PriceDto price;
    private StakeDto stake;
    private String maxStake;

    public Error(String code, String subErrorCode, String description) {
      this.code = code;
      this.subErrorCode = subErrorCode;
      this.description = description;
    }

    public Error(String code, String description) {
      this.code = code;
      this.description = description;
    }
  }

  @Override
  public boolean equals(Object o) {
    if (this == o) return true;
    if (o == null || getClass() != o.getClass()) return false;
    RegularPlaceBetResponse that = (RegularPlaceBetResponse) o;
    return Objects.equals(data, that.data);
  }

  @Override
  public int hashCode() {

    return Objects.hash(data);
  }

  @Override
  public String toString() {
    return "RegularPlaceBetResponse{" + "data=" + data + '}';
  }
}
