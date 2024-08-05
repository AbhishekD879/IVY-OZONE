package com.ladbrokescoral.cashout.config;

import static com.ladbrokescoral.cashout.model.Code.CASHOUT_BET_NO_CASHOUT;
import static com.ladbrokescoral.cashout.model.Code.OPEN_BET_CASHOUT_SERVICE_FAILED_REQUEST_ERROR;
import static com.ladbrokescoral.cashout.model.Code.OPEN_BET_CASHOUT_SERVICE_FAILED_RESPONSE_ERROR;

import com.ladbrokescoral.cashout.api.client.entity.response.CashoutOffer;
import com.ladbrokescoral.cashout.model.response.CashoutData;
import com.ladbrokescoral.cashout.model.response.CashoutData.CashoutDataBuilder;
import com.ladbrokescoral.cashout.model.response.ErrorCashout;
import com.ladbrokescoral.cashout.model.response.UpdateDto;
import java.util.Objects;
import java.util.function.Function;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class ConverterConfig {

  private static final String BET_DO_NOT_HAVE_CASHOUT =
      "Cashout unavailable: This bet does not have cashout available";

  @Bean
  public Function<CashoutOffer, CashoutData> cashoutOfferToCashoutData() {
    return cashoutOffer -> {
      // cashoutOfferReqRef field is equal to OpenBet bet id, the cashout offer was calculated for
      String betId = cashoutOffer.getCashoutOfferReqRef();
      CashoutDataBuilder cashoutDataBuilder = CashoutData.builder().betId(betId);

      // if response contains message field that response is unsuccessful and do not contain
      // cashoutValue
      String errorReason = cashoutOffer.getMessage();

      if (OPEN_BET_CASHOUT_SERVICE_FAILED_RESPONSE_ERROR
          .toString()
          .equals(cashoutOffer.getStatus())) {
        cashoutDataBuilder.cashoutStatus(OPEN_BET_CASHOUT_SERVICE_FAILED_RESPONSE_ERROR.toString());
      } else if (BET_DO_NOT_HAVE_CASHOUT.equals(errorReason)) {
        cashoutDataBuilder.cashoutStatus(CASHOUT_BET_NO_CASHOUT.toString());
      } else if (Objects.nonNull(errorReason)) {
        cashoutDataBuilder.cashoutStatus(OPEN_BET_CASHOUT_SERVICE_FAILED_REQUEST_ERROR.toString());
      } else if (Objects.isNull(cashoutOffer.getCashoutValue())) {
        cashoutDataBuilder.cashoutStatus(OPEN_BET_CASHOUT_SERVICE_FAILED_RESPONSE_ERROR.toString());
      } else {
        cashoutDataBuilder.cashoutValue(cashoutOffer.getCashoutValue().toString());
      }
      return cashoutDataBuilder.build();
    };
  }

  @Bean
  public Function<CashoutData, UpdateDto> cashoutDataToBetUpdate() {
    return cashoutData -> {
      String cashoutValue = cashoutData.getCashoutValue();
      String cashoutStatus = cashoutData.getCashoutStatus();
      if (Objects.nonNull(cashoutValue)
          || CASHOUT_BET_NO_CASHOUT.toString().equals(cashoutStatus)) {
        return UpdateDto.builder().cashoutData(cashoutData).build();
      } else {
        return UpdateDto.builder().error(new ErrorCashout(cashoutStatus)).build();
      }
    };
  }

  @Bean
  public Function<CashoutOffer, UpdateDto> cashoutOfferToBetUpdate(
      Function<CashoutOffer, CashoutData> cashoutOfferToCashoutData,
      Function<CashoutData, UpdateDto> cashoutDataToBetUpdate) {
    return cashoutOfferToCashoutData.andThen(cashoutDataToBetUpdate);
  }
}
